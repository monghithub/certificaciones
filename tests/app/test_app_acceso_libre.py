"""Modo de acceso libre (ACCESO_LIBRE_USUARIO): entrar sin login con un usuario fijo, solo para redes locales."""
import pytest
from conftest import crear_usuario, token
from fastapi.testclient import TestClient


def consola(curso, tmp_path, usuario):
    from app.config import Settings
    from app.main import create_app

    s = Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/libre.db", courses_dir=curso / "cursos",
                 schemas_dir=curso / "schemas", login_max_intentos=3, acceso_libre_usuario=usuario)
    return create_app(s)


@pytest.fixture
def libre(curso, tmp_path):
    app = consola(curso, tmp_path, "admin")
    crear_usuario(app, "admin", rol="admin")
    return app


def test_entra_sin_login_con_el_usuario_configurado(libre):
    c = TestClient(libre)
    r = c.get("/", follow_redirects=False)
    assert r.status_code in (200, 303) and "/login" not in r.headers.get("location", "")
    html = c.get("/c/aif-c01/").text
    assert "Acceso libre (red local)" in html and "Salir" not in html and "(admin)" in html
    assert c.get("/login", follow_redirects=False).headers["location"] == "/"
    assert c.get("/admin/usuarios").status_code == 200


def test_csrf_se_mantiene(libre):
    c = TestClient(libre)
    c.get("/")
    r = c.post("/c/aif-c01/tests/iniciar", data={"modo": "mixto", "n": "1"}, follow_redirects=False)
    assert r.status_code == 403 or "/tests/" not in r.headers.get("location", "")


def test_por_defecto_exige_login(app):
    crear_usuario(app, "admin", rol="admin")
    r = TestClient(app).get("/", follow_redirects=False)
    assert r.headers["location"] == "/login"


@pytest.mark.parametrize("activo", [True, False])
def test_usuario_inexistente_o_desactivado_exige_login(curso, tmp_path, activo):
    app = consola(curso, tmp_path, "nadie" if activo else "luis")
    crear_usuario(app, "luis", activo=activo)
    c = TestClient(app)
    assert c.get("/", follow_redirects=False).headers["location"] == "/login"
    assert c.get("/login").status_code == 200


def test_con_token_csrf_los_formularios_funcionan(libre):
    c = TestClient(libre)
    datos = {"modo": "mixto", "n": "1", "csrf": token(c, "/c/aif-c01/tests")}
    r = c.post("/c/aif-c01/tests/iniciar", data=datos, follow_redirects=False)
    assert r.status_code == 303 and "/c/aif-c01/tests/" in r.headers["location"]
