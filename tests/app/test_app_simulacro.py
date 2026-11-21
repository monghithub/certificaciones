"""Simulacro rotatorio en la consola: composición, rotación, reanudar e intentos antiguos."""
from collections import Counter
from datetime import timedelta

import pytest
from conftest import banco_simulacro, crear_usuario, entrar, escribir, post
from test_app_quiz import iniciar, preguntas, responder

from app.models import Intento, ahora

# Examen de 5: 1 pregunta por dominio; 4 de opción múltiple y 1 de respuesta múltiple (en el Dominio 1).
BANCO = {1: (0, 2), 2: (2, 0), 3: (2, 0), 4: (2, 0), 5: (1, 0)}


def envejecer(app, segundos=20):
    """Retrasa el inicio de todos los intentos (fuera de la ventana de doble envío, dentro del minuto de la fixture)."""
    with app.state.sesiones() as db:
        for i in db.query(Intento):
            i.inicio -= timedelta(seconds=segundos)
        db.commit()


def con_banco(curso, por_dominio=BANCO):
    f = curso / "cursos" / "aif-c01" / "curso.yaml"
    f.write_text(f.read_text(encoding="utf8").replace("preguntas: 3", "preguntas: 5"), encoding="utf8")
    banco = banco_simulacro(por_dominio)
    escribir(curso, banco, "06-simulacro")
    return {p["id"]: p for p in banco}


@pytest.fixture
def app_rot(curso, tmp_path):
    from app.config import Settings
    from app.main import create_app

    banco = con_banco(curso)
    s = Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/rot.db", courses_dir=curso / "cursos",
                 schemas_dir=curso / "schemas", login_max_intentos=3)
    a = create_app(s)
    a.state.banco = banco
    return a


def test_pagina_de_tests_explica_el_banco_rotatorio(app_rot):
    crear_usuario(app_rot)
    html = entrar(app_rot).get("/c/aif-c01/tests").text
    assert "Empezar simulacro" in html and "Cada intento saca 5 preguntas al azar de un banco de 9" in html


def test_intento_con_las_cuotas_por_dominio_y_tipo(app_rot):
    crear_usuario(app_rot)
    c = entrar(app_rot)
    ids = preguntas(app_rot, iniciar(c, modo="simulacro"))
    banco = app_rot.state.banco
    assert len(ids) == 5 and len(set(ids)) == 5
    assert Counter((banco[i]["dominio"], banco[i]["tipo"]) for i in ids) == Counter(
        {(1, "multiple_response"): 1, (2, "multiple_choice"): 1, (3, "multiple_choice"): 1, (4, "multiple_choice"): 1,
         (5, "multiple_choice"): 1})


def test_el_segundo_intento_prioriza_las_no_vistas_aunque_el_primero_se_abandone(app_rot):
    crear_usuario(app_rot)
    c = entrar(app_rot)
    primero = preguntas(app_rot, iniciar(c, modo="simulacro"))  # abandonado sin responder
    envejecer(app_rot)
    segundo = preguntas(app_rot, iniciar(c, modo="simulacro", estudio="1"))
    assert set(primero) & set(segundo) == {"S-009"}  # la única del Dominio 5
    assert set(primero) | set(segundo) == set(app_rot.state.banco)
    envejecer(app_rot)
    tercero = preguntas(app_rot, iniciar(c, modo="simulacro"))
    assert set(tercero) & set(segundo) == {"S-009"}


def test_la_rotacion_es_por_usuario(app_rot):
    crear_usuario(app_rot, "ana")
    crear_usuario(app_rot, "luis")
    primero = preguntas(app_rot, iniciar(entrar(app_rot, "ana"), modo="simulacro"))
    otro = preguntas(app_rot, iniciar(entrar(app_rot, "luis"), modo="simulacro"))
    envejecer(app_rot)
    segundo = preguntas(app_rot, iniciar(entrar(app_rot, "ana"), modo="simulacro"))
    assert len(otro) == 5 and set(primero) & set(segundo) == {"S-009"}  # el intento de luis no cuenta para la rotación de ana


def test_reanudar_conserva_preguntas_y_orden(app_rot):
    crear_usuario(app_rot)
    c = entrar(app_rot)
    iid = iniciar(c, modo="simulacro")
    ids = preguntas(app_rot, iid)
    banco = app_rot.state.banco
    for n in (1, 2):
        datos = {"r": ["b", "c"]} if banco[ids[n - 1]]["tipo"] == "multiple_response" else {"r": "b"}
        assert responder(c, iid, n, datos).status_code == 303
    r = c.get(f"/c/aif-c01/tests/{iid}", follow_redirects=False)
    assert r.headers["location"] == f"/c/aif-c01/tests/{iid}/p/3"
    assert preguntas(app_rot, iid) == ids
    assert ids[2] in c.get(f"/c/aif-c01/tests/{iid}/p/3").text
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    final = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    assert "2/5" in final and all(i in final for i in ids)


def test_intento_antiguo_y_pregunta_retirada(app_rot):
    uid = crear_usuario(app_rot)
    c = entrar(app_rot)
    with app_rot.state.sesiones() as db:  # intento hecho antes del cambio, con una pregunta que ya no existe
        i = Intento(usuario_id=uid, curso="aif-c01", modo="simulacro", limite_segundos=60,
                    preguntas=["S-001", "S-003", "S-005", "S-007", "S-099"], inicio=ahora() - timedelta(seconds=20))
        db.add(i)
        db.commit()
        iid = i.id
    assert c.get(f"/c/aif-c01/tests/{iid}", follow_redirects=False).headers["location"] == f"/c/aif-c01/tests/{iid}/p/1"
    assert responder(c, iid, 1, {"r": ["b", "c"]}).status_code == 303
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    final = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    assert "1/5" in final and "pregunta retirada" in final
    assert preguntas(app_rot, iid) == ["S-001", "S-003", "S-005", "S-007", "S-099"]
    # El siguiente intento evita las del antiguo (S-009 es la única del Dominio 5).
    assert sorted(preguntas(app_rot, iniciar(c, modo="simulacro"))) == ["S-002", "S-004", "S-006", "S-008", "S-009"]


def test_banco_que_no_permite_formar_el_examen(curso, tmp_path):
    from app.config import Settings
    from app.main import create_app

    con_banco(curso, {1: (2, 0), 2: (2, 0), 3: (2, 0), 4: (2, 0), 5: (1, 0)})  # sin respuesta múltiple en el Dominio 1
    app = create_app(Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/inf.db", courses_dir=curso / "cursos",
                              schemas_dir=curso / "schemas", login_max_intentos=3))
    crear_usuario(app)
    c = entrar(app)
    html = c.get("/c/aif-c01/tests").text
    assert "Empezar simulacro" not in html and "No disponible: el simulacro necesita 1 preguntas de tipo multiple_response del dominio 1" in html
    r = post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", modo="simulacro")
    assert r.status_code == 303 and r.headers["location"] == "/c/aif-c01/tests"
    assert "no permite formar el examen" in c.get("/c/aif-c01/tests").text


def test_doble_envio_reutiliza_el_intento(app_rot, monkeypatch):
    crear_usuario(app_rot)
    c = entrar(app_rot)
    a = iniciar(c, modo="simulacro")
    assert iniciar(c, modo="simulacro") == a  # doble clic en «Empezar simulacro»
    with app_rot.state.sesiones() as db:
        assert db.query(Intento).count() == 1
    from app.routes import quiz
    monkeypatch.setattr(quiz, "ahora", lambda: ahora() + timedelta(seconds=11))
    b = iniciar(c, modo="simulacro")
    assert b != a and set(preguntas(app_rot, a)) & set(preguntas(app_rot, b)) == {"S-009"}


def test_un_simulacro_terminado_no_se_reutiliza(app_rot):
    crear_usuario(app_rot)
    c = entrar(app_rot)
    a = iniciar(c, modo="simulacro")
    post(c, f"/c/aif-c01/tests/{a}/finalizar")
    assert iniciar(c, modo="simulacro") != a
