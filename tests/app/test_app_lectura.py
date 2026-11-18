"""«Ponme a prueba»: pregunta del apartado visible durante la lectura, corregida al momento y sin registro."""
import pytest
import yaml
from conftest import FIX, con_repaso, crear_usuario, entrar, escribir, post, pregunta_repaso

from app.models import IntentoRespuesta

M = "03-modelos-fundacionales"
URL = "/c/aif-c01/lectura"
TEORIA = f"/c/aif-c01/modulo/{M}/teoria"


@pytest.fixture
def app_lectura(curso, tmp_path):
    from app.config import Settings
    from app.main import create_app

    con_repaso(curso)
    base = curso / "cursos" / "aif-c01" / "modulos"
    (base / M / "README.md").write_text(
        "# Modelos fundacionales\n\n## Mapa de cobertura\n\n| Objetivo | Sección |\n|---|---|\n"
        "| 3.1.1 | [Selección de modelos](#selección-de-modelos) |\n| 3.2.1 | [Prompts](#prompts) |\n\n"
        "## Selección de modelos\n\nTexto.\n\n### Detalle de coste\n\nTexto.\n\n## Prompts\n\nTexto.\n\n## Sin objetivo\n\nTexto.\n",
        encoding="utf8")
    (base / "06-simulacro" / "README.md").write_text("# Simulacro\n\nInstrucciones.\n", encoding="utf8")
    escribir(curso, [pregunta_repaso("R3-001"),
                     pregunta_repaso("R3-002", tarea="3.2", objetivo="3.2.1", enunciado="¿Qué es un prompt negativo?")],
             fichero="repaso.yaml")
    examen = yaml.safe_load((FIX / "valido.yaml").read_text(encoding="utf8"))
    examen[0]["objetivo"], examen[1]["objetivo"] = "3.1.1", "3.2.1"
    escribir(curso, examen)
    s = Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/lectura.db", courses_dir=curso / "cursos",
                 schemas_dir=curso / "schemas", login_max_intentos=3)
    return create_app(s)


@pytest.fixture
def c(app_lectura):
    crear_usuario(app_lectura)
    return entrar(app_lectura)


def pedir(c, anclas="", excluir="", modulo=M):
    r = c.get(f"{URL}/pregunta", params={"modulo": modulo, "anclas": anclas, "excluir": excluir})
    assert r.status_code == 200, r.text
    return r.json()


def corregir(c, **datos):
    return post(c, f"{URL}/corregir", TEORIA, **datos)


def test_boton_en_la_teoria_y_no_en_el_simulacro(c):
    html = c.get(TEORIA).text
    assert "data-ponme-a-prueba" in html and f'data-modulo="{M}"' in html and 'id="modal-pregunta"' in html
    assert "data-ponme-a-prueba" not in c.get("/c/aif-c01/modulo/06-simulacro/teoria").text


def test_pregunta_del_apartado_visible_primero_repaso(c):
    p = pedir(c, "detalle-de-coste,selección-de-modelos")   # un h3 sin objetivo hereda el del h2 que lo contiene
    assert (p["id"], p["ancla"], p["banco"]) == ("R3-001", "selección-de-modelos", "repaso")
    assert pedir(c, "prompts")["id"] == "R3-002"


def test_agotado_el_repaso_del_apartado_pasa_al_examen_y_despues_al_modulo(c):
    p = pedir(c, "selección-de-modelos", "R3-001")
    assert (p["id"], p["banco"]) == ("D3-001", "examen")
    p = pedir(c, "selección-de-modelos", "R3-001,D3-001")
    assert p["ancla"] is None and p["id"] == "R3-002"       # del módulo, y antes el repaso


def test_apartado_sin_preguntas_usa_el_modulo(c):
    p = pedir(c, "sin-objetivo")
    assert p["ancla"] is None and p["banco"] == "repaso" and not p["reiniciado"]


def test_vistas_todas_vuelve_a_empezar(c):
    p = pedir(c, "", "R3-001,R3-002,D3-001,D3-002,D3-003,D3-004")
    assert p["reiniciado"] is True


def test_no_se_envia_la_solucion(c):
    p = pedir(c, "selección-de-modelos", "R3-001")
    assert not {"correctas", "explicacion", "distractores"} & set(p)


def test_simulacro_y_modulo_sin_preguntas_no_admitidos(c):
    for modulo in ("06-simulacro", "00-base-aws", "no-existe"):
        assert c.get(f"{URL}/pregunta", params={"modulo": modulo}).status_code == 404


def test_corrige_con_explicacion_y_enlace_a_la_teoria(c):
    r = corregir(c, modulo=M, pid="R3-001", r="b")
    assert r.status_code == 200 and r.json()["correcta"] is True
    j = corregir(c, modulo=M, pid="R3-001", r="a").json()
    assert j["correcta"] is False and j["solucion"][0].startswith("b) ") and j["respuesta"][0].startswith("a) ")
    assert j["explicacion"] and j["referencia"].startswith("https://")
    assert j["teoria"] == f"{TEORIA}#selecci%C3%B3n-de-modelos"


def test_los_cuatro_tipos(c):
    assert corregir(c, modulo=M, pid="D3-002", r=["b", "c"]).json()["correcta"] is True
    assert corregir(c, modulo=M, pid="D3-003", o1="a", o2="b", o3="c", o4="d").json()["correcta"] is True
    assert corregir(c, modulo=M, pid="D3-004", m_1="b", m_2="a", m_3="c").json()["correcta"] is True


def test_respuesta_incompleta(c):
    r = corregir(c, modulo=M, pid="D3-003", o1="a", o2="a", o3="c", o4="d")
    assert r.status_code == 400 and "posición" in r.json()["error"]


def test_no_se_registra_nada(c, app_lectura):
    corregir(c, modulo=M, pid="R3-001", r="a")
    with app_lectura.state.sesiones() as db:
        assert db.query(IntentoRespuesta).count() == 0
    assert "Falladas (0)" in c.get("/c/aif-c01/tests").text


def test_seguridad(c):
    assert c.post(f"{URL}/corregir", data={"modulo": M, "pid": "R3-001", "r": "b"}, follow_redirects=False).status_code != 200
    assert corregir(c, modulo="06-simulacro", pid="S-001", r="b").status_code == 404
    assert corregir(c, modulo=M, pid="S-001", r="b").status_code == 404


def test_sin_matricula_404(app_lectura):
    crear_usuario(app_lectura, username="luis", cursos=())
    assert entrar(app_lectura, "luis").get(f"{URL}/pregunta", params={"modulo": M}).status_code == 404
