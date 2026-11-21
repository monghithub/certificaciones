"""Composición del simulacro (curso/simulacro.py): cuotas, extracción, rotación y compatibilidad."""
import random
from collections import Counter
from dataclasses import replace
from pathlib import Path

import pytest
import yaml
from conftest import banco_simulacro

from curso import simulacro as s
from curso.manifiesto import TIPOS, Manifiesto, cargar_manifiesto

RAIZ = Path(__file__).resolve().parent.parent
AIF = cargar_manifiesto(RAIZ / "cursos" / "aif-c01")
# Banco previsto de AIF-C01 (82): 18/19/22/12/11 por dominio, con 3/4/5/3/3 de respuesta múltiple; 17/14/19/11/8 objetivos.
PREVISTO = {1: (15, 3), 2: (15, 4), 3: (17, 5), 4: (9, 3), 5: (8, 3)}
OBJETIVOS = {1: 17, 2: 14, 3: 19, 4: 11, 5: 8}
SEMILLAS = range(500)


def manifiesto(n=65, pesos=(20, 24, 28, 14, 14), distribucion=None) -> Manifiesto:
    return Manifiesto(slug="x", titulo="X", idioma="es-ES", carpeta=Path("."), simulacro="06-simulacro",
                      dominios={d: {"nombre": f"D{d}", "peso": p} for d, p in enumerate(pesos, 1)},
                      examen_preguntas=n, examen_minutos=90,
                      examen_distribucion={"multiple_choice": 80, "multiple_response": 20} if distribucion is None else distribucion)


def celdas(banco, ids):
    por_id = {p["id"]: p for p in banco}
    return Counter((por_id[i]["dominio"], por_id[i]["tipo"]) for i in ids)


def repetidos(banco, ids):
    por_id = {p["id"]: p for p in banco}
    por_dominio = Counter()
    for d, objs in _objetivos_por_dominio(por_id, ids).items():
        por_dominio[d] = len(objs) - len(set(objs))
    return por_dominio


def _objetivos_por_dominio(por_id, ids):
    out = {}
    for i in ids:
        out.setdefault(por_id[i]["dominio"], []).append(por_id[i]["objetivo"])
    return out


# ---------------------------------------------------------------- cuotas
def test_cuotas_de_aif_c01():
    assert s.cuotas_dominio(AIF) == {1: 13, 2: 16, 3: 18, 4: 9, 5: 9}
    assert s.cuotas_tipo(AIF) == {"multiple_choice": 52, "multiple_response": 13}
    q = s.cuotas(AIF)
    assert [q[(d, "multiple_response")] for d in range(1, 6)] == [2, 3, 4, 2, 2]
    assert [q[(d, "multiple_choice")] for d in range(1, 6)] == [11, 13, 14, 7, 7]


def test_cuotas_sin_distribucion_solo_por_dominio():
    q = s.cuotas(manifiesto(distribucion={}))
    assert q == {(1, None): 13, (2, None): 16, (3, None): 18, (4, None): 9, (5, None): 9}


@pytest.mark.parametrize("semilla", range(200))
def test_cuotas_suman_por_fila_y_columna(semilla):
    rnd = random.Random(semilla)
    n_dom = rnd.randint(1, 6)
    cortes = sorted(rnd.sample(range(1, 100), n_dom - 1))
    pesos = [b - a for a, b in zip([0] + cortes, cortes + [100])]
    tipos = rnd.sample(TIPOS, rnd.randint(1, 4))
    m = manifiesto(n=rnd.randint(1, 120), pesos=pesos, distribucion={t: rnd.randint(1, 60) for t in tipos})
    q, qd, qt = s.cuotas(m), s.cuotas_dominio(m), s.cuotas_tipo(m)
    assert sum(qd.values()) == sum(qt.values()) == sum(q.values()) == m.examen_preguntas
    assert all(n > 0 for n in q.values())
    for d, n in qd.items():
        assert sum(v for (dd, _), v in q.items() if dd == d) == n
    for t, n in qt.items():
        assert sum(v for (_, tt), v in q.items() if tt == t) == n


# ---------------------------------------------------------------- extracción
def test_extraccion_respeta_cuotas_y_objetivos_en_500_semillas():
    banco = banco_simulacro(PREVISTO, OBJETIVOS)
    assert len(banco) == 82
    ids_banco = {p["id"] for p in banco}
    q = s.cuotas(AIF)
    minimo = s.repeticiones_inevitables(AIF, banco)
    assert {d: n for d, n in minimo.items() if n} == {2: 2, 5: 1}
    for semilla in SEMILLAS:
        ids = s.extraer(AIF, banco, random.Random(semilla))
        assert len(ids) == 65 and len(set(ids)) == 65 and set(ids) <= ids_banco
        assert celdas(banco, ids) == Counter(q)
        assert repetidos(banco, ids) == Counter(minimo), semilla


def test_misma_semilla_mismo_intento_y_orden_aleatorio():
    banco = banco_simulacro(PREVISTO, OBJETIVOS)
    a = s.extraer(AIF, banco, random.Random(7))
    assert a == s.extraer(AIF, banco, random.Random(7))
    assert a != sorted(a)
    assert a != s.extraer(AIF, banco, random.Random(8))


@pytest.mark.parametrize("semilla", range(50))
def test_rotacion_incluye_las_no_vistas_en_el_intento_anterior(semilla):
    banco = banco_simulacro(PREVISTO)  # un objetivo distinto por pregunta: la regla de objetivos no interfiere
    rnd = random.Random(semilla)
    primero = s.extraer(AIF, banco, rnd)
    segundo = s.extraer(AIF, banco, rnd, evitar=set(primero))
    no_vistas = {p["id"] for p in banco} - set(primero)
    assert len(no_vistas) == 17 and no_vistas <= set(segundo)
    assert len(set(primero) | set(segundo)) == 82  # dos intentos seguidos recorren el banco entero


def test_rotacion_no_rompe_las_cuotas_ni_los_objetivos():
    banco = banco_simulacro(PREVISTO, OBJETIVOS)
    minimo = Counter(s.repeticiones_inevitables(AIF, banco))
    anterior = s.extraer(AIF, banco, random.Random(1))
    for semilla in range(100):
        ids = s.extraer(AIF, banco, random.Random(semilla), evitar=set(anterior))
        assert celdas(banco, ids) == Counter(s.cuotas(AIF))
        assert repetidos(banco, ids) == minimo


def test_curso_sin_distribucion_solo_respeta_dominios():
    m = manifiesto(distribucion={})
    banco = banco_simulacro(PREVISTO, OBJETIVOS)
    ids = s.extraer(m, banco, random.Random(3))
    por_dominio = Counter(d for (d, _), n in celdas(banco, ids).items() for _ in range(n))
    assert por_dominio == Counter(s.cuotas_dominio(m))


# ---------------------------------------------------------------- compatibilidad y errores
def test_banco_del_tamano_del_examen_se_comporta_como_antes():
    banco = banco_simulacro({1: (12, 1), 2: (14, 2), 3: (13, 5), 4: (8, 1), 5: (5, 4)})  # 65, con un reparto que no cumple las cuotas
    assert not s.rotatorio(AIF, banco)
    assert s.comprobar_banco(AIF, banco) == ([], [], [])
    assert s.factible(AIF, banco) == []
    for semilla in range(5):
        assert s.extraer(AIF, list(reversed(banco)), random.Random(semilla)) == [f"S-{k:03d}" for k in range(1, 66)]


def test_banco_real_de_aif_c01():
    """El banco real, cargado como la consola: cuotas y repeticiones mínimas si es rotatorio; si no, el banco entero."""
    banco = s.cargar_banco(AIF, RAIZ / "schemas")
    assert banco
    ids = s.extraer(AIF, banco, random.Random())
    if s.rotatorio(AIF, banco):
        assert celdas(banco, ids) == Counter(s.cuotas(AIF))
        assert repetidos(banco, ids) == Counter({d: n for d, n in s.repeticiones_inevitables(AIF, banco).items() if n})
    else:
        assert ids == sorted(p["id"] for p in banco)


def test_banco_menor_que_el_examen():
    with pytest.raises(ValueError, match="necesita 65 preguntas y hay 10"):
        s.extraer(AIF, banco_simulacro({1: (10, 0)}), random.Random())


def test_banco_que_no_permite_formar_el_examen():
    banco = banco_simulacro({**PREVISTO, 4: (11, 1)})  # 82, pero solo 1 de respuesta múltiple en el Dominio 4 (cuota 2)
    assert s.factible(AIF, banco) == s.comprobar_banco(AIF, banco)[0] == ["el simulacro necesita 2 preguntas de tipo multiple_response del dominio 4 por intento y el banco tiene 1"]
    with pytest.raises(ValueError, match="no permite formar el examen"):
        s.extraer(AIF, banco, random.Random())


def test_resumen_del_banco():
    banco = banco_simulacro(PREVISTO, OBJETIVOS)
    errores, avisos, resumen = s.comprobar_banco(AIF, banco)
    assert errores == [] and avisos == []
    assert resumen[0].startswith("cada intento: 65 de 82 preguntas: D1 13 (11 multiple_choice + 2 multiple_response)")
    assert resumen[1] == "objetivos repetidos inevitables por intento: D2 2, D5 1"
    assert resumen[2].startswith("preguntas que salen en todos los intentos: ")
    assert resumen[3].startswith("dificultad del banco:")


def test_sin_simulacro_no_hay_comprobacion():
    assert s.comprobar_banco(replace(AIF, simulacro=None), banco_simulacro(PREVISTO)) == ([], [], [])


# ---------------------------------------------------------------- óptimo exacto (revisión independiente)
def _con_objetivos(banco, objetivos):
    for p, o in zip(banco, objetivos):
        p["objetivo"] = o
    return banco


def _seleccion(banco, ids, evitar=()):
    """(objetivos repetidos, preguntas de evitar) de una selección."""
    return sum(repetidos(banco, ids).values()), sum(i in evitar for i in ids)


def test_contraejemplo_la_preferencia_por_no_vistas_no_repite_objetivo():
    # Respuesta múltiple (cuota 2): o5, o4, o1, y solo o4 sin ver. Opción múltiple (cuota 3): o6, o4, o4, o6, o2.
    m = manifiesto(n=5, pesos=(100,), distribucion={"multiple_choice": 60, "multiple_response": 40})
    banco = _con_objetivos(banco_simulacro({1: (5, 3)}), ["o6", "o4", "o4", "o6", "o2", "o5", "o4", "o1"])
    evitar = {p["id"] for p in banco if not (p["tipo"] == "multiple_response" and p["objetivo"] == "o4")}
    assert s.repeticiones_inevitables(m, banco) == {1: 0}
    for semilla in range(200):
        ids = s.extraer(m, banco, random.Random(semilla), evitar)
        assert repetidos(banco, ids) == Counter(), semilla


def test_contraejemplo_repeticiones_inevitables_por_celda():
    # Opción múltiple (cuota 2): A, A. Respuesta múltiple (cuota 1): B, C. Hay 3 objetivos, pero A se repite siempre.
    m = manifiesto(n=3, pesos=(100,), distribucion={"multiple_choice": 67, "multiple_response": 33})
    banco = _con_objetivos(banco_simulacro({1: (2, 2)}), ["A", "A", "B", "C"])
    assert s.cuotas(m) == {(1, "multiple_choice"): 2, (1, "multiple_response"): 1}
    assert s.repeticiones_inevitables(m, banco) == {1: 1}
    assert repetidos(banco, s.extraer(m, banco, random.Random(1))) == Counter({1: 1})
    assert "objetivos repetidos inevitables por intento: D1 1" in s.comprobar_banco(m, banco)[2]


def _maximo_distintos(celdas):
    """Referencia independiente: emparejamiento bipartito máximo (Kuhn) entre huecos de las celdas y objetivos."""
    huecos = [{p["objetivo"] for p in cands} for cands, cuota in celdas for _ in range(cuota)]
    pareja = {}

    def aumentar(h, visto):
        for o in huecos[h]:
            if o not in visto:
                visto.add(o)
                if o not in pareja or aumentar(pareja[o], visto):
                    pareja[o] = h
                    return True
        return False

    return sum(aumentar(h, set()) for h in range(len(huecos)))


def _banco_aif_aleatorio(rnd):
    """Banco de 82 con la forma de AIF-C01: todos los objetivos presentes, repartidos al azar entre los tipos."""
    banco = banco_simulacro(PREVISTO)
    k = 0
    for d, (n_mc, n_mr) in sorted(PREVISTO.items()):
        objs = [f"{d}.1.{i}" for i in range(1, OBJETIVOS[d] + 1)]
        objs += [rnd.choice(objs) for _ in range(n_mc + n_mr - len(objs))]
        rnd.shuffle(objs)
        _con_objetivos(banco[k:k + n_mc + n_mr], objs)
        k += n_mc + n_mr
    return banco


@pytest.mark.parametrize("semilla", range(300))
def test_fuzz_bancos_con_la_forma_de_aif_c01(semilla):
    rnd = random.Random(semilla)
    banco = _banco_aif_aleatorio(rnd)
    q = s.cuotas(AIF)
    celdas = {d: [([p for p in banco if (p["dominio"], p["tipo"]) == (dd, t)], n) for (dd, t), n in q.items() if dd == d]
              for d in range(1, 6)}
    minimo = {d: s.cuotas_dominio(AIF)[d] - _maximo_distintos(c) for d, c in celdas.items()}
    assert s.repeticiones_inevitables(AIF, banco) == minimo
    anterior = s.extraer(AIF, banco, rnd)
    for evitar in (set(), set(anterior), set(rnd.sample([p["id"] for p in banco], 65))):
        ids = s.extraer(AIF, banco, rnd, evitar)
        assert Counter((p["dominio"], p["tipo"]) for p in banco if p["id"] in set(ids)) == Counter(q)
        assert repetidos(banco, ids) == Counter({d: n for d, n in minimo.items() if n})


@pytest.mark.parametrize("semilla", range(300))
def test_fuzz_optimo_lexicografico_por_fuerza_bruta(semilla):
    """Bancos pequeños de un dominio: objetivos distintos máximos y, entre esas soluciones, las mínimas de evitar."""
    from itertools import combinations, product

    rnd = random.Random(semilla)
    m = manifiesto(n=5, pesos=(100,), distribucion={"multiple_choice": 60, "multiple_response": 40})
    n_mc, n_mr = rnd.randint(3, 6), rnd.randint(2, 4)
    pool = [f"o{i}" for i in range(rnd.randint(2, 6))]
    banco = _con_objetivos(banco_simulacro({1: (n_mc, n_mr)}), [rnd.choice(pool) for _ in range(n_mc + n_mr)])
    if len(banco) <= 5:
        banco += _con_objetivos(banco_simulacro({1: (1, 0)}), ["extra"])
        banco[-1]["id"] = "S-900"
    evitar = {p["id"] for p in banco if rnd.random() < 0.5}
    mc = [p["id"] for p in banco if p["tipo"] == "multiple_choice"]
    mr = [p["id"] for p in banco if p["tipo"] == "multiple_response"]
    mejor = min(_seleccion(banco, list(a) + list(b), evitar) for a, b in product(combinations(mc, 3), combinations(mr, 2)))
    for k in range(3):
        assert _seleccion(banco, s.extraer(m, banco, random.Random(k), evitar), evitar) == mejor


# ---------------------------------------------------------------- análisis del banco y óptimo frente a fuerza bruta
def test_pregunta_que_no_puede_salir_nunca_y_preguntas_que_salen_siempre():
    # Respuesta múltiple (cuota 2): X, Y, A. Opción múltiple (cuota 3): A, B, C. Para cubrir 5 objetivos distintos,
    # la respuesta múltiple tiene que ser X e Y: la de A no sale nunca y las cinco restantes salen siempre.
    m = manifiesto(n=5, pesos=(100,), distribucion={"multiple_choice": 60, "multiple_response": 40})
    banco = _con_objetivos(banco_simulacro({1: (3, 3)}), ["A", "B", "C", "X", "Y", "A"])
    nunca, siempre = s.analizar(m, banco)
    assert [p["id"] for p in nunca] == ["S-006"]
    assert [p["id"] for p in siempre] == ["S-001", "S-002", "S-003", "S-004", "S-005"]
    errores, avisos, resumen = s.comprobar_banco(m, banco)
    assert errores == []
    assert avisos == [("S-006", "no puede salir nunca: con ella, el dominio 1 cubriría menos objetivos distintos "
                                "(tipo multiple_response, objetivo A); cambia su objetivo o su tipo")]
    assert "preguntas que salen en todos los intentos: 5 (S-001, S-002, S-003, S-004, S-005)" in resumen
    for semilla in range(50):  # coherente con la extracción, también con evitar
        ids = set(s.extraer(m, banco, random.Random(semilla), evitar={"S-004"}))
        assert "S-006" not in ids and {"S-001", "S-002", "S-003", "S-004", "S-005"} <= ids


def test_analisis_coherente_con_la_extraccion_en_bancos_aleatorios():
    for semilla in range(20):
        rnd = random.Random(semilla)
        banco = _banco_aif_aleatorio(rnd)
        nunca, siempre = ({p["id"] for p in x} for x in s.analizar(AIF, banco))
        vistas = Counter()
        for k in range(60):
            evitar = set(rnd.sample([p["id"] for p in banco], 40)) if k % 2 else set()
            vistas.update(s.extraer(AIF, banco, rnd, evitar))
        assert not nunca & set(vistas)
        assert all(vistas[i] == 60 for i in siempre)


def test_preguntas_fuera_de_cuota():
    m = manifiesto(n=5, pesos=(100,), distribucion={"multiple_choice": 100})
    banco = banco_simulacro({1: (6, 1)})  # S-007 es de respuesta múltiple, que no está en examen.distribucion
    banco += _con_objetivos(banco_simulacro({1: (1, 0)}), ["9.1.1"])
    banco[-1].update(id="S-900", dominio=9)  # dominio sin cuota
    errores, avisos, _ = s.comprobar_banco(m, banco)
    assert errores == []
    assert ("S-007", "no sale nunca: su tipo multiple_response no está en examen.distribucion") in avisos
    assert ("S-900", "no sale nunca: su dominio 9 no tiene cuota en el examen") in avisos
    assert not {"S-007", "S-900"} & set(s.extraer(m, banco, random.Random(1)))


def _optimo_fuerza_bruta(banco, evitar):
    """Referencia independiente: (repeticiones, preguntas de evitar) mínimas por dominio, probando todas las
    combinaciones de cada celda (los bancos de AIF-C01 son poco mayores que las cuotas, así que son pocas)."""
    from itertools import combinations, product

    total = [0, 0]
    for d in range(1, 6):
        grupos = [list(combinations([p for p in banco if (p["dominio"], p["tipo"]) == (d, t)], n))
                  for (dd, t), n in s.cuotas(AIF).items() if dd == d]
        mejor = None
        for partes in product(*grupos):
            elegidas = [p for parte in partes for p in parte]
            objs = [p["objetivo"] for p in elegidas]
            puntos = (len(objs) - len(set(objs)), sum(p["id"] in evitar for p in elegidas))
            mejor = puntos if mejor is None or puntos < mejor else mejor
        total[0] += mejor[0]
        total[1] += mejor[1]
    return tuple(total)


@pytest.mark.parametrize("semilla", range(200))
def test_fuzz_evitar_minimo_en_bancos_con_la_forma_de_aif_c01(semilla):
    rnd = random.Random(1000 + semilla)
    banco = _banco_aif_aleatorio(rnd)
    for evitar in (set(s.extraer(AIF, banco, rnd)), set(rnd.sample([p["id"] for p in banco], 50))):
        ids = s.extraer(AIF, banco, rnd, evitar)
        assert _seleccion(banco, ids, evitar) == _optimo_fuerza_bruta(banco, evitar)
