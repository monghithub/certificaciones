import re
from datetime import timedelta

import pytest
from conftest import crear_usuario, entrar, post

from app.models import Intento, IntentoRespuesta

RESP = {
    "D3-001": {"r": "b"},
    "D3-002": {"r": ["b", "c"]},
    "D3-003": {"o1": "a", "o2": "b", "o3": "c", "o4": "d"},
    "D3-004": {"m_1": "b", "m_2": "a", "m_3": "c"},
}


def iniciar(c, **datos):
    r = post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", **datos)
    assert r.status_code == 303
    return int(re.search(r"/c/aif-c01/tests/(\d+)", r.headers["location"]).group(1))


def preguntas(app, iid):
    with app.state.sesiones() as db:
        return list(db.get(Intento, iid).preguntas)


def responder(c, iid, n, datos):
    return post(c, f"/c/aif-c01/tests/{iid}/responder", f"/c/aif-c01/tests/{iid}/p/{n}", n=n, **datos)


def test_cuestionario_por_dominio_sin_repetir(app):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="dominio", filtro="3", n="4")
    ids = preguntas(app, iid)
    assert sorted(ids) == ["D3-001", "D3-002", "D3-003", "D3-004"]


def test_filtro_vacio_vuelve_al_inicio(app):
    crear_usuario(app)
    c = entrar(app)
    r = post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", modo="dominio", filtro="2", n="5")
    assert r.status_code == 303 and r.headers["location"] == "/c/aif-c01/tests"
    assert post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", modo="modulo", filtro="../x", n="5").status_code == 400


def test_los_cuatro_tipos_se_corrigen_y_muestran_explicacion(app):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="mixto", n="4")
    for n, pid in enumerate(preguntas(app, iid), 1):
        assert responder(c, iid, n, RESP[pid]).status_code == 303
        html = c.get(f"/c/aif-c01/tests/{iid}/p/{n}").text
        assert "Correcto" in html and "Ver explicación" in html and "Referencia oficial:" in html
    with app.state.sesiones() as db:
        assert all(r.correcta for r in db.query(IntentoRespuesta))
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    assert "4/4" in c.get(f"/c/aif-c01/tests/{iid}/resultado").text


def test_respuesta_multiple_incompleta_es_incorrecta(app):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="mixto", n="4")
    n = preguntas(app, iid).index("D3-002") + 1
    responder(c, iid, n, {"r": "b"})
    html = c.get(f"/c/aif-c01/tests/{iid}/p/{n}").text
    assert "Incorrecto" in html and "Solución:" in html and "Zero-shot" in html


def test_no_se_filtra_la_solucion_antes_de_responder(app):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="mixto", n="4")
    n = preguntas(app, iid).index("D3-001") + 1
    html = c.get(f"/c/aif-c01/tests/{iid}/p/{n}").text
    assert "RAG incorpora contenido" not in html and "Reentrenar cada semana" not in html


def test_respuesta_incompleta_no_se_registra(app):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="mixto", n="4")
    n = preguntas(app, iid).index("D3-004") + 1
    responder(c, iid, n, {"m_1": "b"})
    with app.state.sesiones() as db:
        assert db.query(IntentoRespuesta).count() == 0


def test_no_se_puede_responder_dos_veces(app):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="mixto", n="4")
    n = preguntas(app, iid).index("D3-001") + 1
    responder(c, iid, n, {"r": "b"})
    responder(c, iid, n, {"r": "a"})
    with app.state.sesiones() as db:
        r = db.query(IntentoRespuesta).one()
        assert r.correcta is True


def test_intento_ajeno_404(app):
    crear_usuario(app, "ana")
    crear_usuario(app, "bea")
    a, b = entrar(app, "ana"), entrar(app, "bea")
    iid = iniciar(a, modo="mixto", n="2")
    for ruta in (f"/c/aif-c01/tests/{iid}", f"/c/aif-c01/tests/{iid}/p/1", f"/c/aif-c01/tests/{iid}/resultado"):
        assert b.get(ruta).status_code == 404
    assert responder(b, iid, 1, {"r": "a"}).status_code == 404


def test_sin_responder_cuenta_como_incorrecta(app):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="mixto", n="4")
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    html = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    assert "0/4" in html and html.count("Sin responder") == 4


def test_pregunta_retirada_en_el_historial(app, curso):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="mixto", n="4")
    n = preguntas(app, iid).index("D3-001") + 1
    responder(c, iid, n, {"r": "b"})
    import yaml
    f = curso / "cursos" / "aif-c01" / "modulos" / "03-modelos-fundacionales" / "preguntas.yaml"
    f.write_text(yaml.safe_dump([p for p in yaml.safe_load(f.read_text()) if p["id"] != "D3-001"], allow_unicode=True))
    app.state.catalogo.cargar()
    assert "pregunta retirada" in c.get(f"/c/aif-c01/tests/{iid}/p/{n}").text
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    resultado = c.get(f"/c/aif-c01/tests/{iid}/resultado")
    assert resultado.status_code == 200 and "pregunta retirada" in resultado.text


# ------------------------------------------------------------------ simulacro
def test_simulacro_sin_preguntas_suficientes(app, curso):
    f = curso / "cursos" / "aif-c01" / "curso.yaml"
    f.write_text(f.read_text(encoding="utf8").replace("preguntas: 3", "preguntas: 65"), encoding="utf8")
    app.state.catalogo.cargar()
    crear_usuario(app)
    c = entrar(app)
    r = post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", modo="simulacro")
    assert r.headers["location"] == "/c/aif-c01/tests"
    assert "No disponible" in c.get("/c/aif-c01/tests").text


def test_simulacro_oculta_explicaciones_hasta_finalizar(app):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="simulacro")
    assert preguntas(app, iid) == ["S-001", "S-002", "S-003"]
    html = c.get(f"/c/aif-c01/tests/{iid}/p/1").text
    assert 'id="cronometro"' in html
    responder(c, iid, 1, {"r": "b"})
    html = c.get(f"/c/aif-c01/tests/{iid}/p/1").text
    assert "Respuesta registrada" in html and "RAG incorpora" not in html
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    final = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    assert "1/3" in final and "RAG incorpora" in final and "orientativo" in final


def test_simulacro_se_cierra_a_los_90_minutos(app, monkeypatch):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="simulacro")
    responder(c, iid, 1, {"r": "b"})
    with app.state.sesiones() as db:
        limite = db.get(Intento, iid).limite_segundos
    assert limite == 60  # configurado a 1 minuto en la fixture
    from app.routes import quiz
    from app.models import ahora
    monkeypatch.setattr(quiz, "ahora", lambda: ahora() + timedelta(seconds=limite + 5))
    r = responder(c, iid, 2, {"r": "a"})
    assert r.headers["location"].endswith("/resultado")
    with app.state.sesiones() as db:
        i = db.get(Intento, iid)
        assert i.fin is not None and len(i.respuestas) == 1  # la respuesta tardía no se registra
    assert "1/3" in c.get(f"/c/aif-c01/tests/{iid}/resultado").text


def test_simulacro_del_curso_aif_c01_es_de_65_preguntas_y_90_minutos():
    from pathlib import Path

    from curso.manifiesto import cargar_manifiesto
    m = cargar_manifiesto(Path(__file__).resolve().parent.parent.parent / "cursos" / "aif-c01")
    assert (m.examen_preguntas, m.examen_minutos, m.simulacro) == (65, 90, "06-simulacro")
    assert {d: v["peso"] for d, v in m.dominios.items()} == {1: 20, 2: 24, 3: 28, 4: 14, 5: 14}


def test_curso_sin_simulacro_no_lo_ofrece(app, curso):
    f = curso / "cursos" / "aif-c01" / "curso.yaml"
    t = f.read_text(encoding="utf8")
    t = t.replace("simulacro: 06-simulacro\nexamen:\n  preguntas: 3\n  minutos: 1\n", "")
    f.write_text(t, encoding="utf8")
    app.state.catalogo.cargar()
    crear_usuario(app)
    c = entrar(app)
    assert "Empezar simulacro" not in c.get("/c/aif-c01/tests").text
    assert post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", modo="simulacro").status_code == 400


def test_la_solucion_se_muestra_con_el_texto_de_las_opciones(app):
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="mixto", n="4")
    ids = preguntas(app, iid)
    malas = {"D3-001": {"r": "a"}, "D3-002": {"r": ["a", "b"]}, "D3-003": {"o1": "d", "o2": "c", "o3": "b", "o4": "a"},
             "D3-004": {"m_1": "a", "m_2": "b", "m_3": "c"}}
    for n, pid in enumerate(ids, 1):
        responder(c, iid, n, malas[pid])
        html = c.get(f"/c/aif-c01/tests/{iid}/p/{n}").text
        assert "Incorrecto" in html and "[[" not in html and "['" not in html and 'class="solucion"' in html
        if pid == "D3-003":
            assert "1.º" in html
        if pid == "D3-004":
            assert "→" in html
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    final = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    assert "[[" not in final and "['" not in final and final.count('class="solucion"') == 8
