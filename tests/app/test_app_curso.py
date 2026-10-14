from conftest import crear_usuario, entrar, post


def test_indice_con_modulos_y_estado(app):
    crear_usuario(app)
    c = entrar(app)
    html = c.get("/c/aif-c01/").text
    assert "03 · Modelos fundacionales" in html and "sin empezar" in html
    assert "Sin contenido todavía" in html  # los módulos vacíos no fallan


def test_lectura_sanitizada_con_mermaid_y_tablas(app):
    crear_usuario(app)
    c = entrar(app)
    html = c.get("/c/aif-c01/modulo/03-modelos-fundacionales/teoria").text
    assert '<pre class="mermaid">flowchart LR' in html
    assert "<table>" in html
    assert "<script>alert(1)" not in html and "&lt;script&gt;" in html
    assert 'href="javascript:' not in html


def test_seccion_inexistente_o_traversal(app):
    crear_usuario(app)
    c = entrar(app)
    assert c.get("/c/aif-c01/modulo/03-modelos-fundacionales/laboratorio").status_code == 404
    assert c.get("/c/aif-c01/modulo/..%2F..%2Fetc/teoria").status_code == 404
    assert c.get("/c/aif-c01/modulo/03-modelos-fundacionales/..%2FREADME").status_code == 404


def test_progreso_y_continuar(app):
    crear_usuario(app)
    c = entrar(app)
    c.get("/c/aif-c01/modulo/03-modelos-fundacionales/servicios")
    html = c.get("/c/aif-c01/").text
    assert "Continuar donde lo dejaste" in html and "/c/aif-c01/modulo/03-modelos-fundacionales/servicios" in html
    assert "en curso" in html
    post(c, "/c/aif-c01/modulo/03-modelos-fundacionales/teoria/completar")
    post(c, "/c/aif-c01/modulo/03-modelos-fundacionales/servicios/completar")
    assert "completado" in c.get("/c/aif-c01/").text
    post(c, "/c/aif-c01/modulo/03-modelos-fundacionales/servicios/completar")  # alterna
    assert "1 de 2 secciones completadas" in c.get("/c/aif-c01/").text


def test_progreso_independiente_por_usuario(app):
    crear_usuario(app, "ana")
    crear_usuario(app, "bea")
    a, b = entrar(app, "ana"), entrar(app, "bea")
    post(a, "/c/aif-c01/modulo/03-modelos-fundacionales/teoria/completar")
    assert "1 de 2 secciones completadas" in a.get("/").text
    assert "0 de 2 secciones completadas" in b.get("/").text
