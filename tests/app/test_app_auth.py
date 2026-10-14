import re

import pytest
from conftest import PASSWORD, crear_usuario, entrar, post, token
from fastapi.testclient import TestClient

from app.config import ConfiguracionError, Settings
from app.main import crear_admin_inicial
from app.models import Usuario


def test_anonimo_redirige_a_login(app):
    c = TestClient(app)
    r = c.get("/", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/login"


def test_login_correcto_y_logout(app):
    crear_usuario(app)
    c = entrar(app)
    assert c.get("/").status_code == 200
    assert post(c, "/logout").status_code == 303
    assert c.get("/", follow_redirects=False).headers["location"] == "/login"


def test_login_error_generico(app):
    crear_usuario(app)
    c = TestClient(app)
    mal_pass = c.post("/login", data={"username": "ana", "password": "x", "csrf": token(c)})
    no_user = c.post("/login", data={"username": "nadie", "password": "x", "csrf": token(c)})
    assert mal_pass.status_code == no_user.status_code == 401
    assert "Usuario o contraseña incorrectos" in mal_pass.text and "Usuario o contraseña incorrectos" in no_user.text


def test_bloqueo_tras_varios_fallos(app):
    crear_usuario(app)
    c = TestClient(app)
    for _ in range(3):
        c.post("/login", data={"username": "ana", "password": "x", "csrf": token(c)})
    r = c.post("/login", data={"username": "ana", "password": PASSWORD, "csrf": token(c)})
    assert r.status_code == 429


def test_login_sin_csrf_rechazado(app):
    crear_usuario(app)
    c = TestClient(app)
    c.get("/login")
    assert c.post("/login", data={"username": "ana", "password": PASSWORD}).status_code == 403
    assert c.post("/login", data={"username": "ana", "password": PASSWORD, "csrf": "falso"}).status_code == 403


def test_csrf_por_cabecera_htmx(app):
    crear_usuario(app)
    c = entrar(app)
    t = token(c, "/")
    assert c.post("/logout", headers={"X-CSRF-Token": t}, follow_redirects=False).status_code == 303


def test_estudiante_no_accede_a_admin(app):
    crear_usuario(app)
    c = entrar(app)
    assert c.get("/admin/usuarios").status_code == 403
    assert c.get("/admin/usuarios/nuevo").status_code == 403
    assert post(c, "/admin/usuarios/nuevo", username="x", nombre="x", rol="admin", password="y" * 12).status_code == 403


def test_password_solo_como_hash(app):
    crear_usuario(app)
    with app.state.sesiones() as db:
        u = db.query(Usuario).one()
        assert u.password_hash.startswith("$argon2") and PASSWORD not in u.password_hash


def test_password_temporal_obliga_a_cambiar(app):
    crear_usuario(app, debe_cambiar=True)
    c = entrar(app)
    r = c.get("/c/aif-c01/tests", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/cuenta/password"
    r = post(c, "/cuenta/password", "/cuenta/password", actual="mal", nueva="otra-contraseña-larga", repetir="otra-contraseña-larga")
    assert r.status_code == 400
    r = post(c, "/cuenta/password", "/cuenta/password", actual=PASSWORD, nueva="otra-contraseña-larga", repetir="otra-contraseña-larga")
    assert r.status_code == 303
    assert c.get("/c/aif-c01/tests", follow_redirects=False).status_code == 200


@pytest.mark.parametrize("nueva,repetir", [("corta", "corta"), ("otra-contraseña-larga", "distinta-contraseña")])
def test_password_nueva_invalida(app, nueva, repetir):
    crear_usuario(app)
    c = entrar(app)
    assert post(c, "/cuenta/password", "/cuenta/password", actual=PASSWORD, nueva=nueva, repetir=repetir).status_code == 400


def test_usuario_desactivado_pierde_la_sesion(app):
    uid = crear_usuario(app)
    c = entrar(app)
    with app.state.sesiones() as db:
        db.get(Usuario, uid).activo = False
        db.commit()
    assert c.get("/", follow_redirects=False).headers["location"] == "/login"
    nuevo = TestClient(app)
    r = nuevo.post("/login", data={"username": "ana", "password": PASSWORD, "csrf": token(nuevo)})
    assert r.status_code == 401


def test_cabeceras_de_seguridad_y_cookie(app):
    c = TestClient(app)
    r = c.get("/login")
    assert "default-src 'self'" in r.headers["content-security-policy"]
    assert r.headers["x-frame-options"] == "DENY"
    assert "httponly" in r.headers["set-cookie"].lower() and "samesite=lax" in r.headers["set-cookie"].lower()


def test_sin_secret_key_no_arranca():
    with pytest.raises(ConfiguracionError):
        Settings.desde_entorno({})
    with pytest.raises(ConfiguracionError):
        Settings.desde_entorno({"SECRET_KEY": "corta"})


def test_admin_inicial_solo_si_no_hay_usuarios(app):
    assert crear_admin_inicial(app.state.sesiones, "Root", PASSWORD) is True
    assert crear_admin_inicial(app.state.sesiones, "otro", PASSWORD) is False
    c = entrar(app, "root")
    assert c.get("/", follow_redirects=False).headers["location"] == "/cuenta/password"
    with pytest.raises(ValueError):
        crear_admin_inicial(app.state.sesiones, "x", "corta")


def test_longitud_minima_de_password_configurable(app, curso, tmp_path):
    from app.config import Settings
    from app.main import create_app

    s = Settings.desde_entorno({"SECRET_KEY": "k" * 40, "PASSWORD_MIN_LENGTH": "4",
                                "DATABASE_URL": f"sqlite:///{tmp_path}/corta.db", "COURSE_DIR": str(curso)})
    assert s.password_min_length == 4
    corta = create_app(s)
    crear_usuario(corta, "root", "admin")
    c = entrar(corta, "root")
    assert post(c, "/admin/usuarios/nuevo", "/admin/usuarios/nuevo", username="luis", nombre="Luis", rol="estudiante", password="1234").status_code == 303
    assert post(c, "/admin/usuarios/nuevo", "/admin/usuarios/nuevo", username="bea", nombre="Bea", rol="estudiante", password="123").status_code == 400
    # por defecto sigue exigiendo 10
    por_defecto = _admin_por_defecto(app)
    assert post(por_defecto, "/admin/usuarios/nuevo", "/admin/usuarios/nuevo",
                username="x1", nombre="X", rol="estudiante", password="1234").status_code == 400


def _admin_por_defecto(app):
    crear_usuario(app, "root", "admin")
    return entrar(app, "root")


@pytest.mark.parametrize("valor", ["0", "abc", "-3"])
def test_longitud_minima_invalida(valor):
    with pytest.raises(ConfiguracionError):
        Settings.desde_entorno({"SECRET_KEY": "k" * 40, "PASSWORD_MIN_LENGTH": valor})


# ------------------------------------------------------------------ formularios caducados (CSRF)
def test_login_con_formulario_caducado_explica_y_permite_repetir(app):
    crear_usuario(app)
    c = TestClient(app)
    viejo = token(c)
    c.cookies.clear()  # la sesión del navegador expiró con la página abierta
    r = c.post("/login", data={"username": "ana", "password": PASSWORD, "csrf": viejo}, follow_redirects=False)
    assert r.status_code == 403 and "El formulario había caducado" in r.text
    assert "No tienes permiso" not in r.text
    nuevo = re.search(r'name="csrf" value="([^"]+)"', r.text).group(1)  # la página trae un formulario válido
    r = c.post("/login", data={"username": "ana", "password": PASSWORD, "csrf": nuevo}, follow_redirects=False)
    assert r.status_code == 303


def test_salir_en_otra_pestana_no_invalida_el_formulario_de_acceso(app):
    crear_usuario(app)
    crear_usuario(app, "jose")
    c = TestClient(app)
    pestana_a = token(c)                                   # formulario de acceso abierto en una pestaña
    c.post("/login", data={"username": "ana", "password": PASSWORD, "csrf": token(c)}, follow_redirects=False)
    post(c, "/logout")                                     # en otra pestaña se entra y se sale
    r = c.post("/login", data={"username": "jose", "password": PASSWORD, "csrf": pestana_a}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/"


def test_formulario_caducado_fuera_del_login_vuelve_atras_con_aviso_y_no_actua(app):
    crear_usuario(app)
    c = entrar(app)
    r = c.post("/c/aif-c01/modulo/03-modelos-fundacionales/teoria/completar", data={"csrf": "caducado"},
               headers={"referer": "http://testserver/c/aif-c01/modulo/03-modelos-fundacionales/teoria"}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/c/aif-c01/modulo/03-modelos-fundacionales/teoria"
    html = c.get(r.headers["location"]).text
    assert "El formulario había caducado y no se ha enviado" in html
    assert "1 de 2" not in c.get("/c/aif-c01/").text  # la sección no se marcó como completada


def test_formulario_caducado_no_redirige_a_otro_sitio(app):
    crear_usuario(app)
    c = entrar(app)
    r = c.post("/logout", data={"csrf": "caducado"}, headers={"referer": "https://malicioso.example/robo"}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/"
