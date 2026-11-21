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
    assert s.comprobar_banco(AIF, banco) == ([], [])
    for semilla in range(5):
        assert s.extraer(AIF, list(reversed(banco)), random.Random(semilla)) == [f"S-{k:03d}" for k in range(1, 66)]


def test_banco_real_de_aif_c01():
    """Hoy el banco de AIF-C01 tiene el tamaño del examen: mismas preguntas y orden que antes del cambio."""
    banco = yaml.safe_load((RAIZ / "cursos" / "aif-c01" / "modulos" / "06-simulacro" / "preguntas.yaml").read_text(encoding="utf8"))
    ids = s.extraer(AIF, banco, random.Random())
    if s.rotatorio(AIF, banco):
        assert celdas(banco, ids) == Counter(s.cuotas(AIF))
        assert repetidos(banco, ids) == Counter(s.repeticiones_inevitables(AIF, banco))
    else:
        assert ids == sorted(p["id"] for p in banco)[: AIF.examen_preguntas]


def test_banco_menor_que_el_examen():
    with pytest.raises(ValueError, match="necesita 65 preguntas y hay 10"):
        s.extraer(AIF, banco_simulacro({1: (10, 0)}), random.Random())


def test_banco_que_no_permite_formar_el_examen():
    banco = banco_simulacro({**PREVISTO, 4: (11, 1)})  # 82, pero solo 1 de respuesta múltiple en el Dominio 4 (cuota 2)
    errores, _ = s.comprobar_banco(AIF, banco)
    assert errores == ["el simulacro necesita 2 preguntas de tipo multiple_response del dominio 4 por intento y el banco tiene 1"]
    with pytest.raises(ValueError, match="no permite formar el examen"):
        s.extraer(AIF, banco, random.Random())


def test_resumen_del_banco():
    banco = banco_simulacro(PREVISTO, OBJETIVOS)
    errores, resumen = s.comprobar_banco(AIF, banco)
    assert errores == []
    assert resumen[0].startswith("cada intento: 65 de 82 preguntas: D1 13 (11 multiple_choice + 2 multiple_response)")
    assert resumen[1] == "objetivos repetidos inevitables por intento: D2 2, D5 1"
    assert resumen[2].startswith("dificultad del banco:")


def test_sin_simulacro_no_hay_comprobacion():
    assert s.comprobar_banco(replace(AIF, simulacro=None), banco_simulacro(PREVISTO)) == ([], [])
