"""Repaso de conocimientos, repetir falladas, explicación tras cada respuesta y modo estudio del simulacro."""
import re

import pytest
from conftest import con_repaso, crear_usuario, entrar, escribir, post, pregunta_repaso

from app.models import Intento


@pytest.fixture
def app_repaso(curso, tmp_path):
    from app.config import Settings
    from app.main import create_app

    con_repaso(curso)
    base = curso / "cursos" / "aif-c01" / "modulos"
    escribir(curso, [pregunta_repaso("R3-001"), pregunta_repaso("R3-002", enunciado="¿Qué técnica añade ejemplos al prompt?")],
             fichero="repaso.yaml")
    escribir(curso, [pregunta_repaso("R0-001", dominio=0, tarea="CP", objetivo="CP.2",
                                     enunciado="¿Quién protege los datos del cliente en la nube?")], "00-base-aws", fichero="repaso.yaml")
    (base / "00-base-aws" / "README.md").write_text("# Base de AWS\n\nTexto.\n", encoding="utf8")
    (base / "03-modelos-fundacionales" / "README.md").write_text(
        "# Modelos fundacionales\n\n## Mapa de cobertura\n\n| Objetivo | Sección |\n|---|---|\n| 3.1.1 | [Selección de modelos](#selección-de-modelos) |\n\n"
        "## Selección de modelos\n\nTexto.\n", encoding="utf8")
    s = Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/repaso.db", courses_dir=curso / "cursos",
                 schemas_dir=curso / "schemas", login_max_intentos=3)
    return create_app(s)


def iniciar(c, **datos):
    r = post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", **datos)
    assert r.status_code == 303, r.text
    return int(re.search(r"/c/aif-c01/tests/(\d+)", r.headers["location"]).group(1))


def ids(app, iid):
    with app.state.sesiones() as db:
        return list(db.get(Intento, iid).preguntas)


def responder(c, iid, n, **datos):
    return post(c, f"/c/aif-c01/tests/{iid}/responder", f"/c/aif-c01/tests/{iid}/p/{n}", n=n, **datos)


def test_pagina_de_tests_como_ruta_de_estudio(app_repaso):
    crear_usuario(app_repaso)
    html = entrar(app_repaso).get("/c/aif-c01/tests").text
    for texto in ("1. Repaso de conocimientos", "2. Preguntas de examen", "3. Repetir falladas", "4. Simulacro", "Modo estudio"):
        assert texto in html
    assert "Todos los módulos (3)" in html


def test_repaso_por_modulo_y_de_todos(app_repaso):
    crear_usuario(app_repaso)
    c = entrar(app_repaso)
    assert ids(app_repaso, iniciar(c, modo="repaso", filtro="00-base-aws", n="10")) == ["R0-001"]
    assert sorted(ids(app_repaso, iniciar(c, modo="repaso", filtro="", n="10"))) == ["R0-001", "R3-001", "R3-002"]
    assert post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", modo="repaso", filtro="06-simulacro").status_code == 400


def test_los_tests_de_examen_no_incluyen_repaso(app_repaso):
    crear_usuario(app_repaso)
    c = entrar(app_repaso)
    for datos in ({"modo": "mixto"}, {"modo": "dominio", "filtro": "3"}, {"modo": "modulo", "filtro": "03-modelos-fundacionales"}):
        assert not any(p.startswith("R") for p in ids(app_repaso, iniciar(c, n="20", **datos)))


def test_explicacion_plegable_con_enlace_a_la_teoria(app_repaso):
    crear_usuario(app_repaso)
    c = entrar(app_repaso)
    iid = iniciar(c, modo="repaso", filtro="03-modelos-fundacionales", n="1")
    responder(c, iid, 1, r="b")
    html = c.get(f"/c/aif-c01/tests/{iid}/p/1").text
    assert "Repaso de conocimientos" in html and '<details class="explicacion">' in html and "Ver explicación" in html
    assert "/c/aif-c01/modulo/03-modelos-fundacionales/teoria#selecci%C3%B3n-de-modelos" in html
    assert "Por qué no son correctas las demás opciones" in html


def test_respuesta_incorrecta_abre_la_explicacion(app_repaso):
    crear_usuario(app_repaso)
    c = entrar(app_repaso)
    iid = iniciar(c, modo="repaso", filtro="00-base-aws", n="1")
    responder(c, iid, 1, r="a")
    html = c.get(f"/c/aif-c01/tests/{iid}/p/1").text
    assert '<details class="explicacion" open>' in html and "Conocimientos previos" in html


def test_repetir_falladas(app_repaso):
    crear_usuario(app_repaso)
    c = entrar(app_repaso)
    iid = iniciar(c, modo="repaso", filtro="03-modelos-fundacionales", n="2")
    for n, pid in enumerate(ids(app_repaso, iid), 1):
        responder(c, iid, n, r="a" if pid == "R3-001" else "b")  # falla R3-001, acierta R3-002
    assert "Falladas (1)" in c.get("/c/aif-c01/tests").text
    otra = iniciar(c, modo="falladas", n="10")
    assert ids(app_repaso, otra) == ["R3-001"]
    responder(c, otra, 1, r="b")
    assert "Falladas (0)" in c.get("/c/aif-c01/tests").text
    r = post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", modo="falladas", n="10")
    assert r.headers["location"] == "/c/aif-c01/tests"


def test_simulacro_en_modo_estudio_muestra_la_explicacion(app_repaso):
    crear_usuario(app_repaso)
    c = entrar(app_repaso)
    iid = iniciar(c, modo="simulacro", estudio="1")
    r = responder(c, iid, 1, r="b")
    assert r.headers["location"].endswith("/p/1")  # se queda en la pregunta para ver la explicación
    html = c.get(f"/c/aif-c01/tests/{iid}/p/1").text
    assert "Modo estudio" in html and "RAG incorpora" in html and "Respuesta registrada" not in html


def test_las_falladas_del_simulacro_no_se_repiten(app_repaso):
    crear_usuario(app_repaso)
    c = entrar(app_repaso)
    iid = iniciar(c, modo="simulacro")
    responder(c, iid, 1, r="a")
    assert "Falladas (0)" in c.get("/c/aif-c01/tests").text


def test_estadisticas_nombran_los_conocimientos_previos(app_repaso):
    crear_usuario(app_repaso)
    c = entrar(app_repaso)
    iid = iniciar(c, modo="repaso", filtro="00-base-aws", n="1")
    responder(c, iid, 1, r="b")
    assert "Conocimientos previos" in c.get("/c/aif-c01/estadisticas").text
