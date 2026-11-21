"""Banco local opcional `libros.yaml`: preguntas de guías de estudio de terceros, solo en la instalación local."""
import re

import pytest
import yaml
from conftest import crear_usuario, entrar, post

from app.models import Intento


def libro(id_, correctas=("b",), dominio=3):
    return {"id": id_, "dominio": dominio, "tarea": "libros", "tipo": "multiple_response" if len(correctas) > 1 else "multiple_choice",
            "dificultad": "media", "origen": f"Libro de prueba, {id_}", "enunciado": f"Enunciado de la pregunta {id_} del libro",
            "opciones": [{"id": x, "texto": f"Opción {x}"} for x in "abcd"], "correctas": list(correctas),
            "explicacion": "Explicación del libro."}


def escribir_libros(curso, modulo, preguntas):
    f = curso / "cursos" / "aif-c01" / "modulos" / modulo / "libros.yaml"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(yaml.safe_dump(preguntas, allow_unicode=True), encoding="utf8")


@pytest.fixture
def app_libros(curso, tmp_path):
    from app.config import Settings
    from app.main import create_app

    escribir_libros(curso, "03-modelos-fundacionales", [libro("ELA-C5-1"), libro("ELA-C5-2", ("a", "c")),
                                                        {"id": "ROTA-1", "tipo": "multiple_choice"}])
    escribir_libros(curso, "06-simulacro", [libro(f"TAU-PE-{k}", dominio=1) for k in range(1, 4)])
    s = Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/libros.db", courses_dir=curso / "cursos",
                 schemas_dir=curso / "schemas", login_max_intentos=3)
    return create_app(s)


def iniciar(c, **datos):
    r = post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", **datos)
    assert r.status_code == 303, r.text
    return int(re.search(r"/c/aif-c01/tests/(\d+)", r.headers["location"]).group(1))


def ids(app, iid):
    with app.state.sesiones() as db:
        return list(db.get(Intento, iid).preguntas)


def test_carga_el_banco_y_descarta_las_incompletas(app_libros):
    c = app_libros.state.catalogo.get("aif-c01")
    crear_usuario(app_libros)
    html = entrar(app_libros).get("/c/aif-c01/tests").text
    assert "Preguntas de los libros" in html
    assert "Test final de los libros" in html and "Las 5 preguntas" in html
    assert "Test inicial y examen de práctica (3)" in html
    assert "ROTA-1" not in c.preguntas and any("ROTA-1" in a for a in c.avisos)
    assert c.preguntas["ELA-C5-1"]["banco"] == "libros" and c.modulos["03-modelos-fundacionales"].preguntas


def test_libros_por_modulo_todas_y_final(app_libros):
    crear_usuario(app_libros)
    c = entrar(app_libros)
    assert len(ids(app_libros, iniciar(c, modo="libros", filtro="06-simulacro", n="2"))) == 2
    assert sorted(ids(app_libros, iniciar(c, modo="libros", filtro="06-simulacro", n="1", todas="1"))) == ["TAU-PE-1", "TAU-PE-2", "TAU-PE-3"]
    assert sorted(ids(app_libros, iniciar(c, modo="libros", filtro="", todas="1"))) == \
        ["ELA-C5-1", "ELA-C5-2", "TAU-PE-1", "TAU-PE-2", "TAU-PE-3"]
    assert post(c, "/c/aif-c01/tests/iniciar", "/c/aif-c01/tests", modo="libros", filtro="00-base-aws").status_code == 400


def test_no_se_mezclan_con_examen_ni_simulacro(app_libros):
    crear_usuario(app_libros)
    c = entrar(app_libros)
    mixto = ids(app_libros, iniciar(c, modo="mixto", n="100"))
    assert mixto and not any(p.startswith(("ELA-", "TAU-")) for p in mixto)
    sim = ids(app_libros, iniciar(c, modo="simulacro"))
    assert all(p.startswith("S-") for p in sim)


def test_correccion_y_explicacion_sin_referencia(app_libros):
    crear_usuario(app_libros)
    c = entrar(app_libros)
    iid = iniciar(c, modo="libros", filtro="03-modelos-fundacionales", todas="1")
    orden = ids(app_libros, iid)
    n = orden.index("ELA-C5-2") + 1
    html = c.get(f"/c/aif-c01/tests/{iid}/p/{n}").text
    assert "Pregunta de los libros" in html and "Libro de prueba, ELA-C5-2" in html
    r = post(c, f"/c/aif-c01/tests/{iid}/responder", f"/c/aif-c01/tests/{iid}/p/{n}", n=n, r=["a", "c"])
    assert r.status_code in (200, 303)
    html = c.get(f"/c/aif-c01/tests/{iid}/p/{n}").text
    assert "Correcto" in html and "Explicación del libro." in html and "prevalece la documentación" in html
    res = post(c, f"/c/aif-c01/tests/{iid}/finalizar", f"/c/aif-c01/tests/{iid}/p/{n}")
    assert res.status_code in (200, 303)
