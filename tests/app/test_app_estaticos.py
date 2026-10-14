import re
import time
from pathlib import Path

from conftest import crear_usuario, entrar
from fastapi.testclient import TestClient

from app import web


def test_los_estaticos_se_revalidan_siempre(app):
    r = TestClient(app).get("/static/app.css")
    assert r.status_code == 200
    assert r.headers["cache-control"] == "no-cache"  # nunca «max-age»: el navegador no debe usar copias viejas
    assert r.headers.get("etag")


def test_las_paginas_enlazan_los_estaticos_con_version(app):
    crear_usuario(app)
    html = entrar(app).get("/c/aif-c01/").text
    for nombre in ("tema.js", "app.css", "htmx.min.js", "mermaid.min.js", "app.js"):
        assert re.search(rf'/static/{re.escape(nombre)}\?v=[0-9a-f]{{10}}', html), nombre
    assert html.index("tema.js") < html.index("app.css")  # el tema se fija antes de pintar


def test_la_version_cambia_cuando_cambia_el_fichero(tmp_path, monkeypatch):
    (tmp_path / "x.css").write_text("a{}", encoding="utf8")
    monkeypatch.setattr(web, "ESTATICOS", tmp_path)
    antes = web.static("x.css")
    assert antes == web.static("x.css")
    time.sleep(0.01)
    (tmp_path / "x.css").write_text("a{color:red}", encoding="utf8")
    assert web.static("x.css") != antes


def test_el_selector_de_tema_esta_en_la_cabecera(app):
    crear_usuario(app)
    html = entrar(app).get("/c/aif-c01/").text
    assert "data-alternar-tema" in html and "data-tema-etiqueta" in html


def test_css_sin_estilos_antiguos():
    css = (Path(__file__).resolve().parents[2] / "app" / "static" / "app.css").read_text(encoding="utf8")
    assert "max-age" not in css and "--acento-texto" not in css
    assert "button.concepto:hover" in css and "(hover: none)" in css
