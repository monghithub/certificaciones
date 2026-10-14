import json
import re

import yaml
from conftest import crear_usuario, entrar
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

MOD = "03-modelos-fundacionales"
RUTA = f"/c/aif-c01/modulo/{MOD}"

GLOSARIO = [
    {"id": "bedrock", "termino": "Amazon Bedrock", "alias": ["Bedrock"], "categoria": "servicio",
     "definicion": "Servicio gestionado de modelos <b>fundacionales</b> & más, con </script> dentro.",
     "usar_cuando": "Para usar modelos por API.", "referencia": "https://docs.aws.amazon.com/bedrock/"},
    {"id": "bedrock-kb", "termino": "Amazon Bedrock Knowledge Bases", "alias": ["Knowledge Bases"], "categoria": "servicio",
     "definicion": "Integra información propia en aplicaciones de IA generativa con RAG."},
    {"id": "rag", "termino": "RAG", "categoria": "tecnica", "definicion": "Técnica que mejora las respuestas con datos externos."},
    {"id": "s3", "termino": "Amazon S3", "alias": ["S3"], "categoria": "servicio", "definicion": "Almacenamiento de objetos escalable."},
    {"id": "recall", "termino": "exhaustividad", "alias": ["recall"], "categoria": "metrica", "definicion": "Proporción de positivos reales detectados."},
]

README = """# Modelos

## Apartado uno

Amazon Bedrock ofrece modelos. Con Bedrock se usa RAG; y otra vez Amazon Bedrock y RAG. El drag no cuenta.

Un enlace a [Amazon Bedrock](https://example.com) y `Amazon Bedrock` en código no cuentan como nuevos.

```text
Amazon Bedrock RAG en bloque de código
```

## Apartado dos Amazon Bedrock

Aquí vuelve Amazon Bedrock en un apartado nuevo, junto a Amazon Bedrock Knowledge Bases.

| Servicio | Nota |
|---|---|
| Amazon S3 | guarda objetos |
| Amazon S3 | segunda fila |

```mermaid
flowchart LR
    A["Datos"] --> B["Amazon S3"]
    B --> C["Exhaustividad"]
```
"""


def montar(curso, tmp_path, glosario=GLOSARIO, readme=README):
    c = curso / "cursos" / "aif-c01"
    (c / "modulos" / MOD / "README.md").write_text(readme, encoding="utf8")
    if glosario is not None:
        (c / "glosario.yaml").write_text(yaml.safe_dump(glosario, allow_unicode=True), encoding="utf8")
    app = create_app(Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/g.db", courses_dir=curso / "cursos",
                              schemas_dir=curso / "schemas"))
    crear_usuario(app)
    return app, entrar(app)


def pagina(curso, tmp_path, **kw):
    app, c = montar(curso, tmp_path, **kw)
    return c.get(f"{RUTA}/teoria").text


def botones(html):
    return re.findall(r'<button type="button" class="concepto" data-concepto="([^"]+)">([^<]*)</button>', html)


def test_primera_aparicion_por_apartado(curso, tmp_path):
    html = pagina(curso, tmp_path)
    cuerpo = html.split('<h2 id="apartado-uno">Apartado uno</h2>')[1].split('<h2 id="apartado-dos')[0]
    ids = [i for i, _ in botones(cuerpo)]
    assert ids.count("bedrock") == 1 and ids.count("rag") == 1  # una sola vez pese a repetirse
    # se conserva el texto original de la primera aparición
    assert ("bedrock", "Amazon Bedrock") in botones(cuerpo)


def test_reinicia_en_cada_apartado_y_los_encabezados_no_son_botones(curso, tmp_path):
    html = pagina(curso, tmp_path)
    dos = html.split("Apartado dos")[1]
    assert ("bedrock", "Amazon Bedrock") in botones(dos)
    assert '<h2 id="apartado-dos-amazon-bedrock">Apartado dos Amazon Bedrock</h2>' in html  # encabezado intacto, sin botón


def test_prefiere_el_termino_mas_largo(curso, tmp_path):
    html = pagina(curso, tmp_path)
    assert ("bedrock-kb", "Amazon Bedrock Knowledge Bases") in botones(html)


def test_exclusiones_enlaces_codigo_y_palabras_parciales(curso, tmp_path):
    html = pagina(curso, tmp_path)
    assert re.search(r'<a href="https://example.com">Amazon Bedrock</a>', html)
    assert "<code>Amazon Bedrock</code>" in html
    assert "Amazon Bedrock RAG en bloque de código" in html and "concepto\" data-concepto=\"rag\">RAG</button> en bloque" not in html
    assert "drag" in html and "drag</button>" not in html


def test_tablas_y_conceptos_en_diagramas(curso, tmp_path):
    html = pagina(curso, tmp_path)
    assert html.count('data-concepto="s3"') == 1  # primera fila de la tabla; la segunda es texto
    assert '<pre class="mermaid">' in html and "Amazon S3&quot;]" in html  # el diagrama sigue siendo código Mermaid
    datos = json.loads(re.search(r'id="datos-glosario">(.*?)</script>', html, re.S).group(1))["conceptos"]
    assert "recall" not in datos  # solo aparece dentro del diagrama: las cajas llevan su propia información
    assert "s3" in datos and "bedrock" in datos


def test_los_datos_incluyen_solo_los_conceptos_usados(curso, tmp_path):
    glos = GLOSARIO + [{"id": "inutil", "termino": "Zxcvb", "categoria": "concepto", "definicion": "No aparece en la página."}]
    html = pagina(curso, tmp_path, glosario=glos)
    datos = json.loads(re.search(r'id="datos-glosario">(.*?)</script>', html, re.S).group(1))["conceptos"]
    assert "inutil" not in datos and datos["bedrock"]["titulo"] == "Amazon Bedrock"
    assert datos["bedrock"]["enlaces"] == [{"texto": "Documentación oficial", "url": "https://docs.aws.amazon.com/bedrock/"}]


def test_datos_json_no_pueden_romper_la_pagina(curso, tmp_path):
    html = pagina(curso, tmp_path)
    bloque = re.search(r'id="datos-glosario">(.*?)</script>', html, re.S).group(1)
    assert "</script>" not in bloque and "<b>" not in bloque and "\\u003c" in bloque
    assert json.loads(bloque)["conceptos"]["bedrock"]["texto"].startswith("Servicio gestionado de modelos <b>fundacionales</b> & más")
    assert html.count("</script>") == html.count("<script")  # nada se ha colado fuera del bloque


def test_texto_del_contenido_se_escapa_en_el_boton(curso, tmp_path):
    glos = [{"id": "i-d", "termino": "R&D", "categoria": "concepto", "definicion": "Investigación y desarrollo de productos."}]
    html = pagina(curso, tmp_path, glosario=glos, readme="# T\n\nSe invierte en R&D cada año.\n")
    assert '<button type="button" class="concepto" data-concepto="i-d">R&amp;D</button>' in html


def test_curso_sin_glosario_se_muestra_como_antes(curso, tmp_path):
    app, c = montar(curso, tmp_path, glosario=None)
    r = c.get(f"{RUTA}/teoria")
    assert r.status_code == 200 and 'class="concepto"' not in r.text and "datos-glosario" not in r.text
    assert "Amazon Bedrock ofrece modelos." in r.text
    g = c.get("/c/aif-c01/glosario")
    assert g.status_code == 200 and "todavía no tiene glosario" in g.text
    assert "/c/aif-c01/glosario" not in c.get("/c/aif-c01/").text  # sin enlace en la navegación


def test_glosario_invalido_no_rompe_el_curso(curso, tmp_path):
    app, c = montar(curso, tmp_path, glosario=[{"id": "mal id", "termino": "X"}])
    assert c.get(f"{RUTA}/teoria").status_code == 200
    assert any("glosario" in a for a in app.state.catalogo.avisos)


def test_pagina_de_glosario(curso, tmp_path):
    app, c = montar(curso, tmp_path)
    r = c.get("/c/aif-c01/glosario")
    assert r.status_code == 200
    assert "5 conceptos" in r.text and 'data-filtro-glosario' in r.text
    assert [t for _, t in re.findall(r'data-concepto="([^"]+)"><span class="cat[^>]*>[^<]*</span>\s*([^<]*)</button>', r.text)] \
        == ["Amazon Bedrock", "Amazon Bedrock Knowledge Bases", "Amazon S3", "exhaustividad", "RAG"]
    assert "/c/aif-c01/glosario" in c.get("/c/aif-c01/").text


def test_glosario_respeta_el_acceso_al_curso(curso, tmp_path):
    app, _ = montar(curso, tmp_path)
    crear_usuario(app, "otro", cursos=())
    assert entrar(app, "otro").get("/c/aif-c01/glosario").status_code == 404
    assert TestClient(app).get("/c/aif-c01/glosario", follow_redirects=False).status_code == 303
