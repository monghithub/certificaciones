from conftest import PASSWORD, crear_usuario, entrar, post, token
from fastapi.testclient import TestClient

from app.models import Usuario


def _admin(app):
    crear_usuario(app, "root", "admin")
    return entrar(app, "root")


def test_alta_de_estudiante_y_primer_acceso(app):
    c = _admin(app)
    r = post(c, "/admin/usuarios/nuevo", "/admin/usuarios/nuevo", username="Luis", nombre="Luis P", rol="estudiante", password="temporal-larga-1")
    assert r.status_code == 303
    nuevo = TestClient(app)
    r = nuevo.post("/login", data={"username": "luis", "password": "temporal-larga-1", "csrf": token(nuevo)}, follow_redirects=False)
    assert r.status_code == 303
    assert nuevo.get("/", follow_redirects=False).headers["location"] == "/cuenta/password"


def test_alta_usuario_duplicado_o_invalido(app):
    c = _admin(app)
    crear_usuario(app, "ana")
    ruta = "/admin/usuarios/nuevo"
    assert post(c, ruta, ruta, username="ana", nombre="Ana", rol="estudiante", password="temporal-larga-1").status_code == 400
    assert post(c, ruta, ruta, username="a b", nombre="Ana", rol="estudiante", password="temporal-larga-1").status_code == 400
    assert post(c, ruta, ruta, username="nuevo", nombre="N", rol="superuser", password="temporal-larga-1").status_code == 400
    assert post(c, ruta, ruta, username="nuevo", nombre="N", rol="estudiante", password="corta").status_code == 400


def test_desactivar_conserva_historial(app):
    c = _admin(app)
    uid = crear_usuario(app, "ana")
    r = post(c, f"/admin/usuarios/{uid}/editar", nombre="Ana", rol="estudiante", activo="0")
    assert r.status_code == 303
    with app.state.sesiones() as db:
        assert db.get(Usuario, uid).activo is False
    assert "desactivado" in c.get("/admin/usuarios").text


def test_no_se_puede_degradar_ni_desactivar_al_ultimo_admin(app):
    c = _admin(app)
    with app.state.sesiones() as db:
        rid = db.query(Usuario).filter_by(username="root").one().id
    post(c, f"/admin/usuarios/{rid}/editar", nombre="Root", rol="estudiante", activo="1")
    post(c, f"/admin/usuarios/{rid}/editar", nombre="Root", rol="admin", activo="0")
    with app.state.sesiones() as db:
        u = db.get(Usuario, rid)
        assert u.rol == "admin" and u.activo
    crear_usuario(app, "otro", "admin")
    post(c, f"/admin/usuarios/{rid}/editar", nombre="Root", rol="estudiante", activo="1")
    with app.state.sesiones() as db:
        assert db.get(Usuario, rid).rol == "estudiante"


def test_restablecer_password(app):
    c = _admin(app)
    uid = crear_usuario(app, "ana")
    assert post(c, f"/admin/usuarios/{uid}/password", password="corta").status_code == 303
    with app.state.sesiones() as db:
        assert db.get(Usuario, uid).debe_cambiar_password is False  # contraseña inválida: no se cambia
    post(c, f"/admin/usuarios/{uid}/password", password="nueva-temporal-12")
    with app.state.sesiones() as db:
        assert db.get(Usuario, uid).debe_cambiar_password is True
    nuevo = TestClient(app)
    r = nuevo.post("/login", data={"username": "ana", "password": "nueva-temporal-12", "csrf": token(nuevo)}, follow_redirects=False)
    assert r.status_code == 303


def test_usuario_inexistente_404(app):
    c = _admin(app)
    assert c.get("/admin/usuarios/999").status_code == 404
