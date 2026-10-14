import re

from conftest import crear_usuario, entrar, post, token
from fastapi.testclient import TestClient

from app.models import Intento, Matricula, ProgresoLectura, Usuario

A, B = "/c/aif-c01", "/c/otro-curso"


def _admin(app):
    crear_usuario(app, "root", "admin")
    return entrar(app, "root")


def _id(app, username):
    with app.state.sesiones() as db:
        return db.query(Usuario).filter_by(username=username).one().id


# ---------------------------------------------------------------- acceso
def test_estudiante_solo_ve_sus_cursos(app_dos):
    crear_usuario(app_dos, "ana", cursos=("aif-c01",))
    c = entrar(app_dos, "ana")
    assert c.get(f"{A}/").status_code == 200
    for ruta in (f"{B}/", f"{B}/tests", f"{B}/estadisticas", f"{B}/modulo/01-base/teoria"):
        assert c.get(ruta).status_code == 404, ruta
    assert post(c, f"{B}/tests/iniciar", f"{A}/tests", modo="mixto", n="1").status_code == 404


def test_curso_inexistente_404_igual_que_sin_acceso(app_dos):
    crear_usuario(app_dos, "ana", cursos=("aif-c01",))
    c = entrar(app_dos, "ana")
    assert c.get("/c/no-existe/").status_code == c.get(f"{B}/").status_code == 404


def test_admin_accede_a_todos_sin_matricula(app_dos):
    c = _admin(app_dos)
    assert c.get(f"{A}/").status_code == 200 and c.get(f"{B}/").status_code == 200
    assert "Texto del otro curso" in c.get(f"{B}/modulo/01-base/teoria").text


def test_anonimo_a_curso_redirige_a_login(app_dos):
    r = TestClient(app_dos).get(f"{A}/", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/login"


def test_intento_de_otro_curso_es_404(app_dos):
    crear_usuario(app_dos, "ana", cursos=("aif-c01", "otro-curso"))
    c = entrar(app_dos, "ana")
    r = post(c, f"{A}/tests/iniciar", f"{A}/tests", modo="mixto", n="2")
    iid = int(re.search(r"/tests/(\d+)", r.headers["location"]).group(1))
    assert c.get(f"{A}/tests/{iid}/p/1").status_code == 200
    assert c.get(f"{B}/tests/{iid}/p/1").status_code == 404
    assert c.get(f"{B}/tests/{iid}/resultado").status_code == 404


# ---------------------------------------------------------------- selector
def test_selector_con_dos_cursos(app_dos):
    crear_usuario(app_dos, "ana", cursos=("aif-c01", "otro-curso"))
    c = entrar(app_dos, "ana")
    html = c.get("/").text
    assert "Mis cursos" in html and "AWS Certified AI Practitioner" in html and "Curso de prueba" in html


def test_un_solo_curso_entra_directo(app_dos):
    crear_usuario(app_dos, "ana", cursos=("otro-curso",))
    c = entrar(app_dos, "ana")
    r = c.get("/", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == f"{B}/"


def test_estudiante_sin_cursos_ve_aviso(app_dos):
    crear_usuario(app_dos, "ana", cursos=())
    c = entrar(app_dos, "ana")
    r = c.get("/")
    assert r.status_code == 200 and "no tienes cursos asignados" in r.text


# ---------------------------------------------------------------- progreso por curso
def test_progreso_independiente_por_curso(app_dos):
    crear_usuario(app_dos, "ana", cursos=("aif-c01", "otro-curso"))
    c = entrar(app_dos, "ana")
    post(c, f"{A}/modulo/03-modelos-fundacionales/teoria/completar")
    assert "1 de 2 secciones completadas" in c.get(f"{A}/").text
    assert "0 de 1 secciones completadas" in c.get(f"{B}/").text
    with app_dos.state.sesiones() as db:
        assert [f.curso for f in db.query(ProgresoLectura)] == ["aif-c01"]


def test_estadisticas_por_curso(app_dos):
    crear_usuario(app_dos, "ana", cursos=("aif-c01", "otro-curso"))
    c = entrar(app_dos, "ana")
    r = post(c, f"{B}/tests/iniciar", f"{B}/tests", modo="mixto", n="1")
    iid = int(re.search(r"/tests/(\d+)", r.headers["location"]).group(1))
    post(c, f"{B}/tests/{iid}/responder", f"{B}/tests/{iid}/p/1", n="1", r="b")
    post(c, f"{B}/tests/{iid}/finalizar")
    assert "Dominio 2" in c.get(f"{B}/estadisticas").text and "Dos" in c.get(f"{B}/estadisticas").text
    assert "Aún no hay respuestas" in c.get(f"{A}/estadisticas").text
    with app_dos.state.sesiones() as db:
        assert db.query(Intento).one().curso == "otro-curso"


def test_cuestionarios_no_mezclan_cursos(app_dos):
    crear_usuario(app_dos, "ana", cursos=("aif-c01", "otro-curso"))
    c = entrar(app_dos, "ana")
    r = post(c, f"{B}/tests/iniciar", f"{B}/tests", modo="mixto", n="50")
    iid = int(re.search(r"/tests/(\d+)", r.headers["location"]).group(1))
    with app_dos.state.sesiones() as db:
        assert db.get(Intento, iid).preguntas == ["D2-001"]  # aif-c01 tiene 7 preguntas más


def test_simulacro_de_curso_sin_el_no_se_ofrece(app_dos):
    crear_usuario(app_dos, "ana", cursos=("otro-curso",))
    c = entrar(app_dos, "ana")
    assert "Empezar simulacro" not in c.get(f"{B}/tests").text
    assert post(c, f"{B}/tests/iniciar", f"{B}/tests", modo="simulacro").status_code == 400


# ---------------------------------------------------------------- administración
def test_alta_con_matricula(app_dos):
    c = _admin(app_dos)
    t = token(c, "/admin/usuarios/nuevo")
    r = c.post("/admin/usuarios/nuevo", data={"username": "luis", "nombre": "Luis", "rol": "estudiante", "password": "temporal-larga-1",
                                              "cursos": ["otro-curso"], "csrf": t}, follow_redirects=False)
    assert r.status_code == 303
    with app_dos.state.sesiones() as db:
        assert [m.curso for m in db.query(Matricula).filter_by(usuario_id=_id(app_dos, "luis"))] == ["otro-curso"]


def test_alta_con_curso_inexistente_se_rechaza(app_dos):
    c = _admin(app_dos)
    t = token(c, "/admin/usuarios/nuevo")
    r = c.post("/admin/usuarios/nuevo", data={"username": "luis", "nombre": "Luis", "rol": "estudiante", "password": "temporal-larga-1",
                                              "cursos": ["fantasma"], "csrf": t}, follow_redirects=False)
    assert r.status_code == 400
    with app_dos.state.sesiones() as db:
        assert db.query(Usuario).filter_by(username="luis").count() == 0


def test_matricular_y_retirar_conserva_historial(app_dos):
    uid = crear_usuario(app_dos, "ana", cursos=("aif-c01",))
    ana = entrar(app_dos, "ana")
    r = post(ana, f"{A}/tests/iniciar", f"{A}/tests", modo="mixto", n="2")
    iid = int(re.search(r"/tests/(\d+)", r.headers["location"]).group(1))
    admin = _admin(app_dos)
    post(admin, f"/admin/usuarios/{uid}/matricula", "/admin/usuarios", curso="otro-curso", accion="alta")
    assert ana.get(f"{B}/").status_code == 200
    post(admin, f"/admin/usuarios/{uid}/matricula", "/admin/usuarios", curso="aif-c01", accion="baja")
    assert ana.get(f"{A}/").status_code == 404
    assert ana.get(f"{A}/tests/{iid}/p/1").status_code == 404
    with app_dos.state.sesiones() as db:
        assert db.query(Intento).count() == 1  # el historial sigue en la base de datos
    post(admin, f"/admin/usuarios/{uid}/matricula", "/admin/usuarios", curso="aif-c01", accion="alta")
    assert ana.get(f"{A}/tests/{iid}/p/1").status_code == 200


def test_matricular_en_curso_inexistente_o_repetida(app_dos):
    uid = crear_usuario(app_dos, "ana", cursos=("aif-c01",))
    admin = _admin(app_dos)
    post(admin, f"/admin/usuarios/{uid}/matricula", "/admin/usuarios", curso="fantasma", accion="alta")
    post(admin, f"/admin/usuarios/{uid}/matricula", "/admin/usuarios", curso="aif-c01", accion="alta")
    post(admin, f"/admin/usuarios/{uid}/matricula", "/admin/usuarios", curso="aif-c01", accion="rara")
    with app_dos.state.sesiones() as db:
        assert [m.curso for m in db.query(Matricula).filter_by(usuario_id=uid)] == ["aif-c01"]


def test_estudiante_no_gestiona_matriculas(app_dos):
    uid = crear_usuario(app_dos, "ana", cursos=("aif-c01",))
    ana = entrar(app_dos, "ana")
    assert post(ana, f"/admin/usuarios/{uid}/matricula", f"{A}/", curso="otro-curso", accion="alta").status_code == 403
    assert ana.get("/admin/cursos").status_code == 403


def test_listado_de_cursos_y_usuarios(app_dos):
    crear_usuario(app_dos, "ana", cursos=("aif-c01", "otro-curso"))
    crear_usuario(app_dos, "bea", cursos=("aif-c01",))
    admin = _admin(app_dos)
    cursos = admin.get("/admin/cursos").text
    assert "aif-c01" in cursos and "otro-curso" in cursos
    assert re.search(r"<code>aif-c01</code></td><td>\d+</td><td>\d+</td>\s*<td>[^<]*</td><td>2</td>", cursos)
    usuarios = admin.get("/admin/usuarios").text
    assert "aif-c01, otro-curso" in usuarios


def test_detalle_de_usuario_con_selector_de_curso(app_dos):
    uid = crear_usuario(app_dos, "ana", cursos=("aif-c01", "otro-curso"))
    ana = entrar(app_dos, "ana")
    ana.get(f"{B}/modulo/01-base/teoria")
    admin = _admin(app_dos)
    html = admin.get(f"/admin/usuarios/{uid}?curso=otro-curso").text
    assert "Curso de prueba" in html
    assert "01 · Base — Teoría" in html  # última lectura de ana en ese curso
    assert f"/admin/usuarios/{uid}?curso=aif-c01" in html
    assert admin.get(f"/admin/usuarios/{uid}?curso=fantasma").status_code == 200  # curso desconocido: cae al primero


def test_curso_roto_no_impide_el_arranque_ni_afecta_a_los_demas(app_dos, curso):
    from app.config import Settings
    from app.main import create_app

    roto = curso / "cursos" / "roto"
    roto.mkdir()
    (roto / "curso.yaml").write_text("slug: roto\ntitulo: [\n", encoding="utf8")
    app = create_app(Settings(secret_key="k" * 40, database_url=f"sqlite:///{curso}/roto.db", courses_dir=curso / "cursos",
                              schemas_dir=curso / "schemas"))
    assert set(app.state.catalogo.cursos) == {"aif-c01", "otro-curso"}
    assert any("roto" in a for a in app.state.catalogo.avisos)
    crear_usuario(app, "root", "admin")
    assert "roto" in entrar(app, "root").get("/admin/cursos").text


def test_recargar_incorpora_un_curso_nuevo(app_dos, curso):
    from conftest import segundo_curso

    admin = _admin(app_dos)
    assert admin.get("/c/tercero/").status_code == 404
    segundo_curso(curso, "tercero")
    post(admin, "/admin/recargar", "/admin/cursos")
    assert admin.get("/c/tercero/").status_code == 200
    assert "tercero" in admin.get("/admin/cursos").text


def test_matricula_huerfana_se_marca_como_no_disponible(app_dos):
    uid = crear_usuario(app_dos, "ana", cursos=("aif-c01", "desaparecido"))
    admin = _admin(app_dos)
    assert "curso no disponible" in admin.get(f"/admin/usuarios/{uid}").text
    ana = entrar(app_dos, "ana")
    assert ana.get("/c/desaparecido/").status_code == 404
