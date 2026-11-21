"""Composición de los intentos del simulacro (cambio de OpenSpec `simulacro-rotatorio`).

Si el banco del simulacro tiene exactamente `examen.preguntas` preguntas, cada intento las contiene todas, ordenadas por id
(comportamiento histórico). Si tiene más, cada intento extrae `examen.preguntas` respetando:

1. las cuotas por dominio (pesos de `dominios`) y por tipo (`examen.distribucion`), siempre;
2. el máximo de objetivos distintos dentro de cada dominio (óptimo exacto, por flujo de coste mínimo);
3. entre esas soluciones, el mínimo de preguntas de `evitar` (el intento anterior del usuario);
4. el resto, al azar.

Lo usan la consola, `scripts/validar_preguntas.py` y `scripts/quiz.py --simulacro`.
"""
import json
import random
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from .manifiesto import TIPOS, Manifiesto

def _restos_mayores(total: int, pesos: dict, desempate, capacidad: dict | None = None) -> dict:
    """Reparte `total` unidades en proporción a `pesos` (método de restos mayores, con aritmética exacta).
    Desempata los restos iguales con `desempate(clave)` (menor primero) y no supera `capacidad` si se da."""
    suma = sum(Fraction(str(v)) for v in pesos.values())
    ideal = {k: total * Fraction(str(v)) / suma for k, v in pesos.items()}
    asignado = {k: int(ideal[k]) for k in pesos}
    if capacidad:
        asignado = {k: min(n, capacidad[k]) for k, n in asignado.items()}
    resto = total - sum(asignado.values())
    orden = sorted(pesos, key=lambda k: (-(ideal[k] - int(ideal[k])), desempate(k)))
    while resto > 0:
        avance = False
        for k in orden:
            if resto and (not capacidad or asignado[k] < capacidad[k]):
                asignado[k] += 1
                resto -= 1
                avance = True
        if not avance:
            raise ValueError("no se puede repartir: capacidad insuficiente")
    return asignado


def cuotas_dominio(m: Manifiesto) -> dict[int, int]:
    """Preguntas de cada dominio por intento (restos mayores sobre los pesos; desempate: mayor peso, menor id)."""
    return _restos_mayores(m.examen_preguntas, {d: v["peso"] for d, v in m.dominios.items()},
                           lambda d: (-m.dominios[d]["peso"], d))


def cuotas_tipo(m: Manifiesto) -> dict[str, int]:
    """Preguntas de cada tipo por intento según `examen.distribucion` (vacío si no se declara)."""
    dist = {t: v for t, v in m.examen_distribucion.items() if v > 0}
    return _restos_mayores(m.examen_preguntas, dist, TIPOS.index) if dist else {}


def cuotas(m: Manifiesto) -> dict[tuple[int, str | None], int]:
    """(dominio, tipo) -> preguntas por intento. Tipo None si el manifiesto no declara `examen.distribucion`.

    Matriz determinista: los tipos se reparten de menor a mayor cuota global entre los dominios (restos mayores sobre
    cuota_dominio × cuota_tipo / N, sin superar lo que le queda a cada dominio; desempate: mayor cuota de dominio, menor
    id) y el tipo mayoritario completa cada dominio."""
    qd = cuotas_dominio(m)
    qt = cuotas_tipo(m)
    if not qt:
        return {(d, None): n for d, n in qd.items() if n}
    tipos = sorted(qt, key=lambda t: (qt[t], TIPOS.index(t)))
    queda = dict(qd)
    resultado = {}
    for t in tipos[:-1]:
        reparto = _restos_mayores(qt[t], {d: qd[d] for d in qd if qd[d]}, lambda d: (-qd[d], d),
                                  {d: queda[d] for d in qd if qd[d]}) if qt[t] else {}
        for d, n in reparto.items():
            resultado[(d, t)] = n
            queda[d] -= n
    for d, n in queda.items():
        resultado[(d, tipos[-1])] = n
    return {k: n for k, n in sorted(resultado.items()) if n}


def rotatorio(m: Manifiesto, banco: list[dict]) -> bool:
    """True si el banco tiene más preguntas que el examen (cada intento es una extracción)."""
    return bool(m.examen_preguntas) and len(banco) > m.examen_preguntas


def _celda(p: dict, con_tipo: bool) -> tuple:
    return (p.get("dominio"), p.get("tipo") if con_tipo else None)


def _objetivo(p: dict) -> str:
    return p.get("objetivo") or p["id"]  # sin objetivo declarado, la pregunta no restringe a ninguna otra


def _celdas_por_dominio(m: Manifiesto, banco: list[dict]) -> dict[int, list[tuple[list[dict], int]]]:
    """dominio -> [(preguntas de la celda dominio × tipo, cuota de la celda)], con las preguntas en el orden del banco."""
    con_tipo = bool(cuotas_tipo(m))
    por_celda = defaultdict(list)
    for p in banco:
        por_celda[_celda(p, con_tipo)].append(p)
    resultado = defaultdict(list)
    for (d, t), n in cuotas(m).items():
        resultado[d].append((por_celda[(d, t)], n))
    return dict(resultado)


class _Flujo:
    """Flujo de coste mínimo por caminos más cortos sucesivos (Bellman-Ford). Basta para unas decenas de nodos."""

    def __init__(self, n: int):
        self.aristas: list[list[int]] = []  # [destino, capacidad, coste, índice de la inversa]
        self.salientes: list[list[int]] = [[] for _ in range(n)]

    def arista(self, a: int, b: int, capacidad: int, coste: int) -> int:
        self.salientes[a].append(len(self.aristas))
        self.aristas.append([b, capacidad, coste, len(self.aristas) + 1])
        self.salientes[b].append(len(self.aristas))
        self.aristas.append([a, 0, -coste, len(self.aristas) - 1])
        return len(self.aristas) - 2

    def flujo(self, e: int) -> int:
        """Unidades que circulan por la arista e (la capacidad de su inversa)."""
        return self.aristas[self.aristas[e][3]][1]

    def resolver(self, origen: int, destino: int) -> None:
        n = len(self.salientes)
        while True:
            dist, previa = [None] * n, [None] * n
            dist[origen] = 0
            for _ in range(n):  # Bellman-Ford: hay costes negativos, pero nunca ciclos negativos en el residual
                cambio = False
                for a in range(n):
                    if dist[a] is None:
                        continue
                    for e in self.salientes[a]:
                        b, cap, coste, _ = self.aristas[e]
                        if cap > 0 and (dist[b] is None or dist[a] + coste < dist[b]):
                            dist[b], previa[b], cambio = dist[a] + coste, e, True
                if not cambio:
                    break
            if dist[destino] is None:
                return
            camino, b = [], destino
            while b != origen:
                e = previa[b]
                camino.append(e)
                b = self.aristas[self.aristas[e][3]][0]
            delta = min(self.aristas[e][1] for e in camino)
            for e in camino:
                self.aristas[e][1] -= delta
                self.aristas[self.aristas[e][3]][1] += delta


def _optimo_dominio(celdas: list[tuple[list[dict], int]], evitar, rnd: random.Random,
                    forzar: str | None = None, excluir: str | None = None) -> tuple[list[dict], int]:
    """Selección exacta de un dominio: (preguntas elegidas, objetivos distintos).

    Flujo de coste mínimo: origen → celda (capacidad = cuota) → pregunta (1; coste 1 si está en `evitar`) → objetivo →
    destino por dos aristas: la primera unidad con coste −GRANDE (objetivo nuevo) y el resto con coste 0 (repetición).
    Con GRANDE mayor que el nº de preguntas, el coste mínimo maximiza primero los objetivos distintos y, entre esas
    soluciones, minimiza las preguntas de `evitar`. Las preguntas y los objetivos se añaden en un orden barajado con `rnd`,
    así que los empates entre soluciones óptimas se resuelven al azar, sin garantía de uniformidad (Bellman-Ford se queda
    con el primer camino más corto que encuentra). Para el análisis del banco, `forzar` incluye una pregunta (coste −ENORME)
    y `excluir` la quita."""
    preguntas = [(c, p) for c, (cands, _) in enumerate(celdas) for p in cands if p["id"] != excluir]
    rnd.shuffle(preguntas)
    objetivos = list(dict.fromkeys(_objetivo(p) for _, p in preguntas))
    n_celdas = len(celdas)
    origen, destino = 0, 1
    nodo_obj = {o: 2 + n_celdas + len(preguntas) + i for i, o in enumerate(objetivos)}
    f = _Flujo(2 + n_celdas + len(preguntas) + len(objetivos))
    grande = len(preguntas) + 1
    enorme = grande * (len(preguntas) + 1)
    for c, (_, cuota) in enumerate(celdas):
        f.arista(origen, 2 + c, cuota, 0)
    elegida = []
    for i, (c, p) in enumerate(preguntas):
        coste = -enorme if p["id"] == forzar else 1 if p["id"] in evitar else 0
        elegida.append(f.arista(2 + c, 2 + n_celdas + i, 1, coste))
        f.arista(2 + n_celdas + i, nodo_obj[_objetivo(p)], 1, 0)
    nuevo = []
    for o in objetivos:
        nuevo.append(f.arista(nodo_obj[o], destino, 1, -grande))
        f.arista(nodo_obj[o], destino, len(preguntas), 0)
    f.resolver(origen, destino)
    return [p for (_, p), e in zip(preguntas, elegida) if f.flujo(e)], sum(f.flujo(e) for e in nuevo)


def repeticiones_inevitables(m: Manifiesto, banco: list[dict]) -> dict[int, int]:
    """Por dominio, cuántas veces un intento tiene que repetir objetivo como mínimo: cuota del dominio menos el máximo de
    objetivos distintos que caben respetando las cuotas por celda (dominio × tipo)."""
    celdas = _celdas_por_dominio(m, banco)
    return {d: n - _optimo_dominio(celdas.get(d, []), (), random.Random(0))[1] for d, n in cuotas_dominio(m).items()}


def factible(m: Manifiesto, banco: list[dict]) -> list[str]:
    """Errores si un banco rotatorio no tiene preguntas suficientes para alguna cuota (dominio, tipo). Solo un recuento:
    es lo que comprueban la consola y `extraer`; el análisis completo está en `comprobar_banco`."""
    if not m.tiene_simulacro or not rotatorio(m, banco):
        return []
    con_tipo = bool(cuotas_tipo(m))
    hay = Counter(_celda(p, con_tipo) for p in banco)
    errores = []
    for (d, t), n in cuotas(m).items():
        if hay[(d, t)] < n:
            de_tipo = f"de tipo {t} " if t else ""
            errores.append(f"el simulacro necesita {n} preguntas {de_tipo}del dominio {d} por intento y el banco tiene {hay[(d, t)]}")
    return errores


def fuera_de_cuota(m: Manifiesto, banco: list[dict]) -> list[tuple[dict, str]]:
    """Preguntas que la extracción ignora porque su dominio o su tipo no tienen cuota, con el motivo."""
    q = cuotas(m)
    con_tipo = bool(cuotas_tipo(m))
    dominios = {d for d, _ in q}
    fuera = []
    for p in banco:
        if _celda(p, con_tipo) in q:
            continue
        if p.get("dominio") not in dominios:
            fuera.append((p, f"su dominio {p.get('dominio')} no tiene cuota en el examen"))
        else:
            fuera.append((p, f"su tipo {p.get('tipo')} no está en examen.distribucion"))
    return fuera


def analizar(m: Manifiesto, banco: list[dict]) -> tuple[list[dict], list[dict]]:
    """(preguntas que no pueden salir nunca, preguntas que salen en todos los intentos) de un banco factible.

    Una pregunta no sale nunca si ninguna selección con el máximo de objetivos distintos de su dominio la incluye (se
    fuerza y el máximo baja); sale siempre si todas la incluyen (se excluye y el máximo baja o las cuotas no se llenan).
    Como `extraer` solo devuelve selecciones con ese máximo, el resultado no depende del intento anterior."""
    nunca, siempre = [], []
    rnd = random.Random(0)
    for _, celdas in sorted(_celdas_por_dominio(m, banco).items()):
        total = sum(n for _, n in celdas)
        _, mejor = _optimo_dominio(celdas, (), rnd)
        for cands, _ in celdas:
            for p in cands:
                elegidas, distintos = _optimo_dominio(celdas, (), rnd, forzar=p["id"])
                if p not in elegidas or distintos < mejor:
                    nunca.append(p)
                    continue
                elegidas, distintos = _optimo_dominio(celdas, (), rnd, excluir=p["id"])
                if len(elegidas) < total or distintos < mejor:
                    siempre.append(p)
    return sorted(nunca, key=lambda p: p["id"]), sorted(siempre, key=lambda p: p["id"])


def comprobar_banco(m: Manifiesto, banco: list[dict]) -> tuple[list[str], list[tuple[str | None, str]], list[str]]:
    """Análisis completo de un banco del simulacro para el validador: (errores, avisos, líneas de resumen).
    Cada aviso es (id de la pregunta o None, mensaje). Vacío si el banco no es rotatorio."""
    if not m.tiene_simulacro or not rotatorio(m, banco):
        return [], [], []
    errores = factible(m, banco)
    avisos = [(p.get("id"), f"no sale nunca: {motivo}") for p, motivo in fuera_de_cuota(m, banco)]
    q = cuotas(m)
    partes = []
    for d, n in cuotas_dominio(m).items():
        detalle = " + ".join(f"{q[(d, t)]} {t}" for (dd, t) in q if dd == d and t)
        partes.append(f"D{d} {n}" + (f" ({detalle})" if detalle else ""))
    resumen = [f"cada intento: {m.examen_preguntas} de {len(banco)} preguntas: " + ", ".join(partes)]
    if not errores:
        rep = {d: n for d, n in repeticiones_inevitables(m, banco).items() if n}
        resumen.append("objetivos repetidos inevitables por intento: " + (", ".join(f"D{d} {n}" for d, n in rep.items()) or "ninguno"))
        nunca, siempre = analizar(m, banco)
        avisos += [(p["id"], f"no puede salir nunca: con ella, el dominio {p['dominio']} cubriría menos objetivos distintos "
                             f"(tipo {p['tipo']}, objetivo {p.get('objetivo')}); cambia su objetivo o su tipo") for p in nunca]
        resumen.append(f"preguntas que salen en todos los intentos: {len(siempre)}"
                       + (f" ({', '.join(p['id'] for p in siempre)})" if siempre else ""))
    dificultad = Counter(p.get("dificultad") or "sin indicar" for p in banco)
    resumen.append("dificultad del banco: " + ", ".join(f"{k} {v}" for k, v in sorted(dificultad.items())))
    return errores, avisos, resumen


def extraer(m: Manifiesto, banco: list[dict], rnd: random.Random, evitar=frozenset()) -> list[str]:
    """Ids de un intento, en el orden de presentación. ValueError si el banco no permite formar el examen."""
    n = m.examen_preguntas
    if not n or len(banco) < n:
        raise ValueError(f"El simulacro necesita {n} preguntas y hay {len(banco)}.")
    if not rotatorio(m, banco):
        return sorted(p["id"] for p in banco)
    errores = factible(m, banco)
    if errores:
        raise ValueError(f"El banco del simulacro no permite formar el examen: {errores[0]}.")
    evitar = set(evitar)
    ids: list[str] = []
    for _, celdas in sorted(_celdas_por_dominio(m, banco).items()):
        ids += [p["id"] for p in _optimo_dominio(celdas, evitar, rnd)[0]]
    rnd.shuffle(ids)
    return ids


def cargar_banco(m: Manifiesto, esquemas: Path) -> list[dict]:
    """Banco del simulacro como lo carga la consola: solo `modulos/<simulacro>/preguntas.yaml`, preguntas que cumplen
    el esquema, de dominios declarados y sin ids repetidos (gana la primera)."""
    f = m.carpeta / "modulos" / (m.simulacro or "") / "preguntas.yaml"
    if not m.simulacro or not f.is_file():
        return []
    validador = Draft202012Validator(json.loads((Path(esquemas) / "pregunta.schema.json").read_text(encoding="utf8")))
    banco, vistos = [], set()
    for p in yaml.safe_load(f.read_text(encoding="utf8")) or []:
        if (isinstance(p, dict) and not any(validador.iter_errors(p)) and p["dominio"] in m.dominios
                and p["id"] not in vistos):
            vistos.add(p["id"])
            banco.append(p)
    return banco
