from conftest import crear_usuario, entrar, post
from test_app_quiz import RESP, iniciar, preguntas, responder

from app import stats


def _hacer_test(app, c, aciertos):
    iid = iniciar(c, modo="mixto", n="4")
    for n, pid in enumerate(preguntas(app, iid), 1):
        datos = RESP[pid] if pid in aciertos else {"r": "d"} if pid == "D3-001" else {"r": "a"} if pid == "D3-002" else RESP[pid]
        if pid in ("D3-003", "D3-004") and pid not in aciertos:
            datos = {"o1": "d", "o2": "c", "o3": "b", "o4": "a"} if pid == "D3-003" else {"m_1": "a", "m_2": "b", "m_3": "c"}
        responder(c, iid, n, datos)
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    return iid


def test_agregacion_por_dominio_y_tarea(app):
    uid = crear_usuario(app)
    c = entrar(app)
    _hacer_test(app, c, aciertos={"D3-001", "D3-002"})
    with app.state.sesiones() as db:
        dominios, tareas = stats.aciertos_por(db, uid, "aif-c01")
    assert dominios == [{"dominio": 3, "n": 4, "ok": 2, "pct": 50}]
    assert {t["tarea"]: t["pct"] for t in tareas} == {"3.1": 100, "3.2": 100, "3.3": 0, "3.4": 0}
    html = c.get("/c/aif-c01/estadisticas").text
    assert "Dominio 3" in html and "50 %" in html


def test_puntos_debiles_exigen_minimo_de_respuestas(app):
    uid = crear_usuario(app)
    c = entrar(app)
    for _ in range(3):
        _hacer_test(app, c, aciertos={"D3-001", "D3-002"})
    with app.state.sesiones() as db:
        _, tareas = stats.aciertos_por(db, uid, "aif-c01")
    assert {t["tarea"] for t in stats.puntos_debiles(tareas)} == {"3.3", "3.4"}
    assert stats.puntos_debiles([{"tarea": "3.3", "n": 2, "ok": 0, "pct": 0}]) == []


def test_historial_de_intentos(app):
    crear_usuario(app)
    c = entrar(app)
    iid = _hacer_test(app, c, aciertos={"D3-001"})
    html = c.get("/c/aif-c01/estadisticas").text
    assert f"/c/aif-c01/tests/{iid}/resultado" in html and "mixto" in html


def test_aislamiento_entre_estudiantes(app):
    crear_usuario(app, "ana")
    bid = crear_usuario(app, "bea")
    a = entrar(app, "ana")
    _hacer_test(app, a, aciertos={"D3-001"})
    assert a.get(f"/admin/usuarios/{bid}").status_code == 403
    b = entrar(app, "bea")
    assert "Aún no hay respuestas" in b.get("/c/aif-c01/estadisticas").text


def test_vista_admin_listado_y_detalle(app):
    crear_usuario(app, "root", "admin")
    aid = crear_usuario(app, "ana")
    a = entrar(app, "ana")
    a.get("/c/aif-c01/modulo/03-modelos-fundacionales/trampas")  # no existe: 404, sin efecto
    a.get("/c/aif-c01/modulo/03-modelos-fundacionales/servicios")
    _hacer_test(app, a, aciertos={"D3-001", "D3-002", "D3-003", "D3-004"})
    r = entrar(app, "root")
    listado = r.get("/admin/usuarios").text
    assert "ana" in listado and "03 · Servicios" in listado and "100 %" in listado
    detalle = r.get(f"/admin/usuarios/{aid}").text
    assert "Dominio 3" in detalle and "100 %" in detalle and "03 · Modelos fundacionales — Servicios" in detalle
