"""Resultado por dominio y por tarea en la página de resultado de un intento."""
import re
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import unquote, urlsplit

import pytest
from conftest import banco_simulacro, crear_usuario, entrar, escribir, post, sustituir
from test_app_libros import app_libros, escribir_libros, libro  # noqa: F401 (fixture)
from test_app_quiz import iniciar, preguntas, responder
from test_app_repaso import app_repaso  # noqa: F401 (fixture)

from app import stats
from curso import simulacro
from curso.manifiesto import cargar_manifiesto
from app.models import Intento, IntentoRespuesta

RESP = {"D3-001": {"r": "b"}, "D3-002": {"r": ["b", "c"]}, "D3-003": {"o1": "a", "o2": "b", "o3": "c", "o4": "d"},
        "D3-004": {"m_1": "b", "m_2": "a", "m_3": "c"}}
MAPA_03 = ("# Modelos fundacionales\n\n## Mapa de cobertura\n\n| Objetivo | Sección |\n|---|---|\n"
           "| 3.1.2 | [Elección](#elección) |\n| 3.1.1 | [Selección de modelos](#selección-de-modelos) |\n\n"
           "## Selección de modelos\n\nTexto.\n\n## Elección\n\nTexto.\n")


def tabla(html):
    """Filas (texto de la celda de nombre, aciertos) de la tabla por dominio y el pie."""
    bloque = re.search(r'<div class="card" id="por-dominio">(.*?)</table>', html, re.S).group(1)
    filas = re.findall(r"<tr><td>(.*?)</td><td>(\d+/\d+)</td>", bloque, re.S)
    pie = re.search(r'<tfoot><tr><th scope="row">Total</th><td>(\d+/\d+)</td>', bloque).group(1)
    return [(re.sub(r"<[^>]+>", "", n).strip(), a) for n, a in filas], pie


def cuadra(app, iid, marcar_debiles=False):
    """El desglose suma exactamente el total del intento y sus aciertos."""
    with app.state.sesiones() as db:
        i = db.get(Intento, iid)
        d = stats.desglose_intento(i, app.state.catalogo.get("aif-c01"), marcar_debiles)
        assert sum(g["n"] for g in d["dominios"]) == d["total"] == len(i.preguntas)
        assert sum(g["ok"] for g in d["dominios"]) == d["ok"] == sum(1 for r in i.respuestas if r.correcta)
        if d["tareas"]:  # cuando se muestra, el desglose por tarea también suma el total
            assert sum(t["n"] for t in d["tareas"]) == d["total"] and sum(t["ok"] for t in d["tareas"]) == d["ok"]
        return d


def test_desglose_de_un_test_mixto_con_una_sin_responder(app, curso):
    (curso / "cursos" / "aif-c01" / "modulos" / "03-modelos-fundacionales" / "README.md").write_text(MAPA_03, encoding="utf8")
    app.state.catalogo.cargar()
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="mixto", n="4")
    ids = preguntas(app, iid)
    for n, pid in enumerate(ids[:3], 1):
        responder(c, iid, n, {"r": "a"} if pid == "D3-001" else RESP[pid])  # D3-001, fallada
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    html = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    esperado = 2 if "D3-001" in ids[:3] else 3
    filas, pie = tabla(html)
    assert filas == [("Dominio 3 · Aplicaciones de modelos fundacionales", f"{esperado}/4")] and pie == f"{esperado}/4"
    assert 'href="/c/aif-c01/modulo/03-modelos-fundacionales/teoria"' in html
    assert "1 sin responder: cuentan como falladas" in html
    assert "por debajo de tu media" not in html and "AWS no publica" not in html  # solo en el simulacro
    tareas = re.findall(r"<tr><td>(?:<a [^>]*>)?(Tarea [\d.]+)(?:</a>)?</td><td>(\d+/\d+)</td>", html)
    assert [t for t, _ in tareas] == ["Tarea 3.1", "Tarea 3.2", "Tarea 3.3", "Tarea 3.4"]
    assert sum(int(a.split("/")[1]) for _, a in tareas) == 4
    assert 'href="/c/aif-c01/modulo/03-modelos-fundacionales/teoria#selecci%C3%B3n-de-modelos">Tarea 3.1' in html  # 3.1.1 antes que 3.1.2
    assert html.index('id="por-dominio"') < html.index("D3-001 ·")  # antes de la lista de preguntas
    cuadra(app, iid)


@pytest.fixture
def app_sim(curso, tmp_path):
    """Simulacro rotatorio de 5 (1 pregunta por dominio) con teoría solo en los módulos 01 y 03."""
    from app.config import Settings
    from app.main import create_app

    f = curso / "cursos" / "aif-c01" / "curso.yaml"
    f.write_text(sustituir(f.read_text(encoding="utf8"), (r"^  preguntas: 3$", "  preguntas: 5")), encoding="utf8")
    escribir(curso, banco_simulacro({1: (0, 2), 2: (2, 0), 3: (2, 0), 4: (2, 0), 5: (1, 0)}), "06-simulacro")
    m = curso / "cursos" / "aif-c01" / "modulos"
    (m / "01-fundamentos-ia-ml").mkdir(parents=True, exist_ok=True)
    (m / "01-fundamentos-ia-ml" / "README.md").write_text("# Fundamentos\n\n## Mapa de cobertura\n\n| Objetivo | Sección |\n|---|---|\n"
                                                         "| 1.1.1 | [Términos](#términos) |\n\n## Términos\n\nTexto.\n", encoding="utf8")
    (m / "03-modelos-fundacionales" / "README.md").write_text(MAPA_03, encoding="utf8")
    s = Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/sim.db", courses_dir=curso / "cursos",
                 schemas_dir=curso / "schemas", login_max_intentos=3)
    return create_app(s)


def _responder_simulacro(app, c, iid, acierta, salta=()):
    banco = app.state.catalogo.get("aif-c01").preguntas
    for n, pid in enumerate(preguntas(app, iid), 1):
        d = banco[pid]["dominio"]
        if d in salta:
            continue
        ok = d in acierta
        mr = banco[pid]["tipo"] == "multiple_response"
        responder(c, iid, n, {"r": (["b", "c"] if ok else ["a"]) if mr else ("b" if ok else "a")})


def test_simulacro_marca_los_dominios_por_debajo_de_la_media_y_enlaza_la_teoria(app_sim):
    crear_usuario(app_sim)
    c = entrar(app_sim)
    iid = iniciar(c, modo="simulacro")
    # Acierta los dominios 2, 3 y 4, falla el 1 y deja sin responder el 5: global 3/5 (60 %).
    _responder_simulacro(app_sim, c, iid, acierta={2, 3, 4}, salta={5})
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    html = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    filas, pie = tabla(html)
    assert [a for _, a in filas] == ["0/1", "1/1", "1/1", "1/1", "0/1"] and pie == "3/5"
    debiles = [n for n, _ in filas if "por debajo de tu media" in n]
    assert [n.split(" ·")[0] for n in debiles] == ["Dominio 1", "Dominio 5"]
    assert "AWS no publica un corte por dominio" in html and "Meets competencies" in html
    assert 'href="/c/aif-c01/modulo/01-fundamentos-ia-ml/teoria">Dominio 1' in html
    assert 'href="/c/aif-c01/modulo/03-modelos-fundacionales/teoria">Dominio 3' in html
    assert ">Dominio 2 · " in html and 'teoria">Dominio 2' not in html  # el módulo 02 no tiene teoría en la prueba
    assert 'teoria#t%C3%A9rminos">Tarea 1.1</a>' in html and 'teoria#selecci%C3%B3n-de-modelos">Tarea 3.1</a>' in html
    assert re.search(r"Para repasar primero: .*Dominio 1.*Dominio 5", html)
    cuadra(app_sim, iid)


def test_simulacro_con_todo_acertado_no_marca_ninguno(app_sim):
    crear_usuario(app_sim)
    c = entrar(app_sim)
    iid = iniciar(c, modo="simulacro")
    _responder_simulacro(app_sim, c, iid, acierta={1, 2, 3, 4, 5})
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    html = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    assert tabla(html)[1] == "5/5" and "por debajo de tu media" not in html and "Para repasar primero" not in html


def test_preguntas_retiradas_y_sin_responder(app_sim):
    uid = crear_usuario(app_sim)
    c = entrar(app_sim)
    with app_sim.state.sesiones() as db:
        i = Intento(usuario_id=uid, curso="aif-c01", modo="simulacro", limite_segundos=60,
                    preguntas=["S-003", "S-099", "S-098", "S-005"])
        db.add(i)
        db.flush()
        db.add_all([IntentoRespuesta(intento_id=i.id, pregunta_id=pid, dominio=2, tarea="2.1", tipo="multiple_choice",
                                     respuesta=["b"], correcta=ok) for pid, ok in (("S-099", False), ("S-003", True))])
        db.commit()
        iid = i.id
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    html = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    filas, pie = tabla(html)
    assert filas == [("Dominio 2 · Fundamentos de IA generativa", "1/1"),
                     ("Dominio 3 · Aplicaciones de modelos fundacionales · por debajo de tu media", "0/1"),
                     ("Preguntas retiradas del contenido", "0/2")] and pie == "1/4"
    assert "1 sin responder: cuentan como falladas" in html  # S-005; la retirada sin responder se cuenta aparte
    assert "2 preguntas retiradas del contenido (1 sin responder): cuentan en su propia fila" in html
    d = cuadra(app_sim, iid, marcar_debiles=True)
    assert [t["tarea"] for t in d["tareas"]] == ["2.1", "3.1", "retiradas"]
    # Las retiradas (0 % frente al 25 % global) nunca se marcan; el Dominio 3 (0 %), sí.
    assert [g["clave"] for g in d["dominios"] if g["debil"]] == [3]


def test_repaso_con_conocimientos_previos(app_repaso):  # noqa: F811
    crear_usuario(app_repaso)
    c = entrar(app_repaso)
    iid = iniciar(c, modo="repaso", n="10")
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    html = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    filas, pie = tabla(html)
    assert [n for n, _ in filas] == ["Conocimientos previos", "Dominio 3 · Aplicaciones de modelos fundacionales"] and pie == "0/3"
    assert 'href="/c/aif-c01/modulo/00-base-aws/teoria">Conocimientos previos' in html
    assert re.search(r"<tr><td>Conocimientos previos</td><td>0/1</td>", html)  # fila de la tarea CP (sin mapa: sin enlace)
    cuadra(app_repaso, iid)


def test_libros_sin_dominio_oficial(app_libros, curso):  # noqa: F811
    sin_dominio = libro("SIN-1")
    sin_dominio.pop("dominio")
    escribir_libros(curso, "03-modelos-fundacionales", [libro("ELA-C5-1"), sin_dominio])
    app_libros.state.catalogo.cargar()
    crear_usuario(app_libros)
    c = entrar(app_libros)
    iid = iniciar(c, modo="libros", filtro="03-modelos-fundacionales", n="5")
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    html = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    filas, pie = tabla(html)
    assert [n for n, _ in filas] == ["Dominio 3 · Aplicaciones de modelos fundacionales", "Sin dominio oficial"] and pie == "0/2"
    assert "Desglose por tarea" not in html  # la tarea «libros» no es oficial
    cuadra(app_libros, iid)


def test_resultado_con_el_contenido_real_de_aif_c01(tmp_path):
    """Simulacro con el contenido real: responde 12, finaliza y comprueba la tabla por dominio."""
    from pathlib import Path

    from app.config import Settings
    from app.main import create_app

    raiz = Path(__file__).resolve().parent.parent.parent
    app = create_app(Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/real.db", courses_dir=raiz / "cursos",
                              schemas_dir=raiz / "schemas", login_max_intentos=3))
    crear_usuario(app)
    c = entrar(app)
    iid = iniciar(c, modo="simulacro")
    banco = app.state.catalogo.get("aif-c01").preguntas
    for n, pid in enumerate(preguntas(app, iid)[:12], 1):
        p = banco[pid]
        resp = p["correctas"] if n % 3 else [o["id"] for o in p["opciones"] if o["id"] not in p["correctas"]][:1]
        responder(c, iid, n, {"r": resp if p["tipo"] == "multiple_response" else resp[0]})
    post(c, f"/c/aif-c01/tests/{iid}/finalizar")
    html = c.get(f"/c/aif-c01/tests/{iid}/resultado").text
    filas, pie = tabla(html)
    cuotas = simulacro.cuotas_dominio(app.state.catalogo.get("aif-c01").manifiesto)
    assert [n.split(" ·")[0] for n, _ in filas] == [f"Dominio {d}" for d in sorted(cuotas)]
    assert [int(a.split("/")[1]) for _, a in filas] == [cuotas[d] for d in sorted(cuotas)] and pie == "8/65"
    assert "53 sin responder" in html
    enlaces = re.findall(r'<a href="(/c/aif-c01/modulo/[^"]+)">((?:Dominio|Tarea) [^<]+)</a>', html)
    tareas = re.findall(r"<tr><td>(?:<a [^>]*>)?Tarea \d+\.\d+", html)
    assert len([e for e in enlaces if e[1].startswith("Tarea")]) == len(tareas) > 0  # todas las tareas enlazadas
    assert len({e for e in enlaces if e[1].startswith("Dominio")}) == len(cuotas)
    for url, _ in set(enlaces):  # cada destino existe y su ancla es un id del HTML
        partes = urlsplit(url)
        r = c.get(partes.path)
        assert r.status_code == 200, url
        if partes.fragment:
            assert f'id="{unquote(partes.fragment)}"' in r.text, url
    cuadra(app, iid, marcar_debiles=True)



# ---------------------------------------------------------------- casos límite del desglose
AIF = cargar_manifiesto(Path(__file__).resolve().parent.parent.parent / "cursos" / "aif-c01")


def _desglose(preguntas, respuestas, marcar_debiles=False, ids=None):
    """Desglose con un contenido mínimo: `preguntas` = {id: dict}, `respuestas` = {id: acierto}."""
    contenido = SimpleNamespace(manifiesto=AIF, preguntas=preguntas, url_dominio=lambda d: None, url_tarea=lambda t: None)
    i = SimpleNamespace(preguntas=ids or list(preguntas),
                        respuestas=[SimpleNamespace(pregunta_id=k, correcta=v) for k, v in respuestas.items()])
    return stats.desglose_intento(i, contenido, marcar_debiles)


def test_no_se_marca_un_dominio_con_el_mismo_porcentaje_redondeado():
    # Dominio 1: 11/16 (68,75 % → 69 %); Dominio 2: 7/10 (70 %). Global: 18/26 (69,2 % → 69 %).
    preguntas = {f"A{k}": {"dominio": 1, "tarea": "1.1"} for k in range(16)} | {f"B{k}": {"dominio": 2, "tarea": "2.1"} for k in range(10)}
    respuestas = {f"A{k}": k < 11 for k in range(16)} | {f"B{k}": k < 7 for k in range(10)}
    d = _desglose(preguntas, respuestas, marcar_debiles=True)
    assert d["pct"] == 69 and [(g["clave"], g["pct"], g["debil"]) for g in d["dominios"]] == [(1, 69, False), (2, 70, False)]
    respuestas["A10"] = False  # 10/16 → 63 %, global 17/26 → 65 %
    assert [g["debil"] for g in _desglose(preguntas, respuestas, marcar_debiles=True)["dominios"]] == [True, False]


def test_tipos_inesperados_no_rompen_el_desglose():
    preguntas = {"L1": {"dominio": [1], "tarea": "libros"}, "L2": {"dominio": True, "tarea": 7}, "L3": {"dominio": 1.0, "tarea": "1.1"},
                 "L4": {"dominio": 0, "tarea": "libros"}, "L5": {"dominio": 9, "tarea": "9.1"}}
    d = _desglose(preguntas, {"L1": True, "L3": True})
    assert [g["clave"] for g in d["dominios"]] == ["otros"] and d["dominios"][0]["n"] == 5 and d["ok"] == 2
    assert [t["tarea"] for t in d["tareas"]] == ["1.1", "otras"]  # 1.1 es una tarea oficial aunque el dominio no lo sea


def test_tarea_de_otro_dominio_y_orden_numerico():
    preguntas = {"P1": {"dominio": 3, "tarea": "2.1"}, "P2": {"dominio": 1, "tarea": "1.10"}, "P3": {"dominio": 1, "tarea": "1.2"},
                 "P4": {"dominio": 1, "tarea": "libros"}}
    d = _desglose(preguntas, {"P1": True})
    assert [t["tarea"] for t in d["tareas"]] == ["1.2", "1.10", "2.1", "otras"]
    assert sum(t["n"] for t in d["tareas"]) == d["total"] == 4


def test_url_tarea_toma_el_primer_objetivo_en_orden_numerico(app):
    c = app.state.catalogo.get("aif-c01")
    c.teoria = {"1.2.10": ("x", "a"), "1.2.2": ("x", "b"), "1.20.1": ("x", "c")}
    c.url_teoria = lambda o: o
    assert c.url_tarea("1.2") == "1.2.2" and c.url_tarea("1.20") == "1.20.1" and c.url_tarea("1.3") is None


def test_libros_con_dominio_o_tarea_de_tipo_raro(app_libros, curso, caplog):  # noqa: F811
    raros = [libro("F-1", dominio=1.0), libro("L-1", dominio=[1]), libro("B-1", dominio=True), libro("T-1"), libro("X-1", dominio=1.5)]
    raros[3]["tarea"] = 5
    escribir_libros(curso, "03-modelos-fundacionales", raros)
    app_libros.state.catalogo.cargar()
    c = app_libros.state.catalogo.get("aif-c01")
    assert c.preguntas["F-1"]["dominio"] == 1 and type(c.preguntas["F-1"]["dominio"]) is int
    for pid in ("L-1", "B-1", "T-1", "X-1"):
        assert pid not in c.preguntas
        assert any(f"libros.yaml:{pid}: dominio o tarea no válidos" in a for a in c.avisos), c.avisos
    crear_usuario(app_libros)
    cl = entrar(app_libros)
    iid = iniciar(cl, modo="libros", filtro="03-modelos-fundacionales", n="5")
    post(cl, f"/c/aif-c01/tests/{iid}/finalizar")
    filas, pie = tabla(cl.get(f"/c/aif-c01/tests/{iid}/resultado").text)
    assert filas == [("Dominio 1 · Fundamentos de IA y ML", "0/1")] and pie == "0/1"
