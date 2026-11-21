"""Composición de los intentos del simulacro (cambio de OpenSpec `simulacro-rotatorio`).

Si el banco del simulacro tiene exactamente `examen.preguntas` preguntas, cada intento las contiene todas, ordenadas por id
(comportamiento histórico). Si tiene más, cada intento extrae `examen.preguntas` respetando:

1. las cuotas por dominio (pesos de `dominios`) y por tipo (`examen.distribucion`), siempre;
2. sin repetir objetivo dentro de un dominio, salvo que el banco lo haga inevitable;
3. preferencia por las preguntas que no estaban en `evitar` (el intento anterior del usuario);
4. el resto, al azar.

Lo usan la consola, `scripts/validar_preguntas.py` y `scripts/quiz.py --simulacro`.
"""
import random
from collections import Counter, defaultdict
from fractions import Fraction

from .manifiesto import TIPOS, Manifiesto

REINTENTOS = 20  # selecciones voraces por dominio; se queda la mejor


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


def repeticiones_inevitables(m: Manifiesto, banco: list[dict]) -> dict[int, int]:
    """Por dominio, cuántas veces un intento tiene que repetir objetivo como mínimo."""
    distintos = defaultdict(set)
    for p in banco:
        distintos[p.get("dominio")].add(_objetivo(p))
    return {d: max(0, n - len(distintos[d])) for d, n in cuotas_dominio(m).items()}


def comprobar_banco(m: Manifiesto, banco: list[dict]) -> tuple[list[str], list[str]]:
    """(errores, líneas de resumen) de un banco del simulacro. Sin errores ni resumen si el banco no es rotatorio."""
    if not m.tiene_simulacro or not rotatorio(m, banco):
        return [], []
    q = cuotas(m)
    con_tipo = bool(cuotas_tipo(m))
    hay = Counter(_celda(p, con_tipo) for p in banco)
    errores = []
    for (d, t), n in q.items():
        if hay[(d, t)] < n:
            de_tipo = f"de tipo {t} " if t else ""
            errores.append(f"el simulacro necesita {n} preguntas {de_tipo}del dominio {d} por intento y el banco tiene {hay[(d, t)]}")
    partes = []
    for d, n in cuotas_dominio(m).items():
        detalle = " + ".join(f"{q[(d, t)]} {t}" for (dd, t) in q if dd == d and t)
        partes.append(f"D{d} {n}" + (f" ({detalle})" if detalle else ""))
    resumen = [f"cada intento: {m.examen_preguntas} de {len(banco)} preguntas: " + ", ".join(partes)]
    rep = {d: n for d, n in repeticiones_inevitables(m, banco).items() if n}
    resumen.append("objetivos repetidos inevitables por intento: " + (", ".join(f"D{d} {n}" for d, n in rep.items()) or "ninguno"))
    dificultad = Counter(p.get("dificultad") or "sin indicar" for p in banco)
    resumen.append("dificultad del banco: " + ", ".join(f"{k} {v}" for k, v in sorted(dificultad.items())))
    return errores, resumen


def _elegir_dominio(celdas: list[tuple[list[dict], int]], rnd: random.Random, evitar) -> tuple[tuple[int, int], list[dict]]:
    """Una selección voraz de un dominio: ((objetivos repetidos, preguntas de evitar), preguntas)."""
    usados: Counter = Counter()
    elegidas: list[dict] = []
    for candidatos, n in sorted(celdas, key=lambda c: len(c[0]) - c[1]):  # primero la celda con menos holgura
        libres = list(candidatos)
        for _ in range(n):
            p = min(libres, key=lambda x: (_objetivo(x) in usados, x["id"] in evitar, rnd.random()))
            libres.remove(p)
            usados[_objetivo(p)] += 1
            elegidas.append(p)
    return (len(elegidas) - len(usados), sum(p["id"] in evitar for p in elegidas)), elegidas


def extraer(m: Manifiesto, banco: list[dict], rnd: random.Random, evitar=frozenset()) -> list[str]:
    """Ids de un intento, en el orden de presentación. ValueError si el banco no permite formar el examen."""
    n = m.examen_preguntas
    if not n or len(banco) < n:
        raise ValueError(f"El simulacro necesita {n} preguntas y hay {len(banco)}.")
    if not rotatorio(m, banco):
        return sorted(p["id"] for p in banco)
    errores, _ = comprobar_banco(m, banco)
    if errores:
        raise ValueError(f"El banco del simulacro no permite formar el examen: {errores[0]}.")
    evitar = set(evitar)
    q = cuotas(m)
    con_tipo = bool(cuotas_tipo(m))
    por_celda = defaultdict(list)
    for p in banco:
        por_celda[_celda(p, con_tipo)].append(p)
    minimo = repeticiones_inevitables(m, banco)
    ids: list[str] = []
    for d in sorted({d for d, _ in q}):
        celdas = [(por_celda[(d, t)], k) for (dd, t), k in q.items() if dd == d]
        mejor = None
        for _ in range(REINTENTOS):
            puntos, elegidas = _elegir_dominio(celdas, rnd, evitar)
            if mejor is None or puntos < mejor[0]:
                mejor = (puntos, elegidas)
            if puntos == (minimo[d], 0):
                break
        ids += [p["id"] for p in mejor[1]]
    rnd.shuffle(ids)
    return ids
