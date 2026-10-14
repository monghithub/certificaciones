import json
import re

import yaml
from conftest import crear_usuario, entrar
from test_app_glosario import GLOSARIO, MOD, RUTA

from app.config import Settings
from app.main import create_app

README = """# Modelos

## Apartado uno

Texto.

```mermaid
flowchart LR
    A["🪣 Amazon S3"] --> B["🧩 Paso propio"]
    B --> C["⚙️ Otro paso"]
    class A dato
    class B,C proceso
```

```nodos
A:
  concepto: s3
  enlaces:
    - {texto: "Guía de S3", url: "https://docs.aws.amazon.com/s3"}
    - {texto: "Malo", url: "javascript:alert(1)"}
    - {texto: "Inseguro", url: "http://inseguro.example"}
B:
  titulo: Paso propio
  texto: Explicación <b>propia</b> del paso.
  usar_cuando: Siempre.
  seccion: 03-modelos-fundacionales/servicios#detalle-final
C:
  concepto: bedrock
  titulo: Otro título
  texto: Texto sustituido.
  seccion: 03-modelos-fundacionales/no-existe#x
```

## Apartado dos

```mermaid
flowchart TB
    subgraph G["📦 Grupo"]
        X["🧪 Dentro"]
    end
    class X ml
```

```nodos
G:
  titulo: El grupo
  texto: Caja que contiene otras.
X:
  concepto: rag
```
"""


def montar(curso, tmp_path, readme=README, servicios="# Servicios\n\n## Detalle final\n\nTexto.\n"):
    c = curso / "cursos" / "aif-c01"
    (c / "modulos" / MOD / "README.md").write_text(readme, encoding="utf8")
    (c / "modulos" / MOD / "servicios.md").write_text(servicios, encoding="utf8")
    (c / "glosario.yaml").write_text(yaml.safe_dump(GLOSARIO, allow_unicode=True), encoding="utf8")
    app = create_app(Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/c.db", courses_dir=curso / "cursos", schemas_dir=curso / "schemas"))
    crear_usuario(app)
    return entrar(app)


def datos(html):
    return json.loads(re.search(r'id="datos-glosario">(.*?)</script>', html, re.S).group(1))


def test_el_bloque_nodos_no_se_muestra_y_los_diagramas_se_indexan(curso, tmp_path):
    html = montar(curso, tmp_path).get(f"{RUTA}/teoria").text
    visible = html.split('id="datos-glosario"')[0]  # lo que ve el usuario, sin el bloque de datos JSON
    assert "concepto: s3" not in visible and "Explicación" not in visible and "language-nodos" not in visible
    assert html.count('<figure class="diagrama" data-diagrama="') == 2
    assert 'data-diagrama="0"' in html and 'data-diagrama="1"' in html


def test_caja_con_concepto_y_enlaces_filtrados(curso, tmp_path):
    d = datos(montar(curso, tmp_path).get(f"{RUTA}/teoria").text)["diagramas"]
    a = d["0"]["A"]
    assert a["titulo"] == "Amazon S3" and a["categoria"] == "servicio" and "Almacenamiento de objetos" in a["texto"]
    assert a["enlaces"] == [{"texto": "Guía de S3", "url": "https://docs.aws.amazon.com/s3"}]  # sin javascript: ni http:


def test_caja_con_datos_propios_y_enlace_al_curso(curso, tmp_path):
    d = datos(montar(curso, tmp_path).get(f"{RUTA}/teoria").text)["diagramas"]
    b = d["0"]["B"]
    assert b["titulo"] == "Paso propio" and b["usar_cuando"] == "Siempre." and "<b>propia</b>" in b["texto"]  # texto plano, sin interpretar
    assert b["enlaces"] == [{"texto": "Ver en el curso", "url": f"/c/aif-c01/modulo/{MOD}/servicios#detalle-final"}]


def test_los_campos_de_la_caja_sustituyen_a_los_del_concepto(curso, tmp_path):
    c = datos(montar(curso, tmp_path).get(f"{RUTA}/teoria").text)["diagramas"]["0"]["C"]
    assert c["titulo"] == "Otro título" and c["texto"] == "Texto sustituido."
    assert c["enlaces"] == [{"texto": "Documentación oficial", "url": "https://docs.aws.amazon.com/bedrock/"}]  # conserva los del concepto; la sección inexistente se omite


def test_subgrupos_y_segundo_diagrama(curso, tmp_path):
    d = datos(montar(curso, tmp_path).get(f"{RUTA}/teoria").text)["diagramas"]["1"]
    assert d["G"]["titulo"] == "El grupo" and d["X"]["titulo"] == "RAG"


def test_encabezados_con_id_y_enlaces_internos(curso, tmp_path):
    c = montar(curso, tmp_path)
    assert '<h2 id="apartado-uno">' in c.get(f"{RUTA}/teoria").text
    assert '<h2 id="detalle-final">' in c.get(f"{RUTA}/servicios").text


def test_encabezados_repetidos_y_con_formato(curso, tmp_path):
    readme = "# Título\n\n## Datos\n\nA\n\n## Datos\n\nB\n\n## Con `código` y **negrita**\n\nC\n\n## ¿Qué es RAG? (v2)\n"
    html = montar(curso, tmp_path, readme=readme).get(f"{RUTA}/teoria").text
    assert 'id="datos"' in html and 'id="datos-1"' in html and 'id="con-código-y-negrita"' in html and 'id="qué-es-rag-v2"' in html


def test_nodos_con_yaml_roto_se_ignora_sin_romper(curso, tmp_path):
    readme = "# T\n\n```mermaid\nflowchart LR\n    A[\"🧩 Uno\"]\n    class A proceso\n```\n\n```nodos\nA: [\n```\n"
    r = montar(curso, tmp_path, readme=readme).get(f"{RUTA}/teoria")
    assert r.status_code == 200 and '<figure class="diagrama"' in r.text
    assert "diagramas\": {}" in r.text or "datos-glosario" not in r.text


def test_bloque_nodos_sin_diagrama_previo_se_ignora(curso, tmp_path):
    r = montar(curso, tmp_path, readme="# T\n\n```nodos\nA:\n  titulo: x\n```\n").get(f"{RUTA}/teoria")
    assert r.status_code == 200 and "titulo: x" not in r.text
