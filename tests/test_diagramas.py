import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from curso import diagramas  # noqa: E402
from curso.diagramas import es_emoji, extraer  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent

BUENO = """# Doc

## Apartado detalle

Texto.

```mermaid
flowchart LR
    A["🧩 Uno"] --> B["🚀 Dos"]
    class A proceso
    class B accion
```

```nodos
A:
  titulo: Uno
  texto: Paso uno.
B:
  concepto: rag
  enlaces:
    - {texto: "Más", url: "https://docs.aws.amazon.com/x"}
  seccion: 03-modelos-fundacionales/servicios#apartado-detalle
```
"""


@pytest.fixture
def curso_md(repo):
    c = repo / "cursos" / "aif-c01"
    (c / "glosario.yaml").write_text(yaml.safe_dump([{"id": "rag", "termino": "RAG", "categoria": "tecnica", "definicion": "Técnica que mejora las respuestas con datos externos."}], allow_unicode=True), encoding="utf8")
    (c / "modulos" / "03-modelos-fundacionales" / "servicios.md").write_text("# S\n\n## Apartado detalle\n\nx\n", encoding="utf8")

    def poner(texto, nombre="modulos/03-modelos-fundacionales/README.md"):
        (c / nombre).write_text(texto, encoding="utf8")
        return diagramas.validar(c, repo / "schemas")
    return poner


def test_diagrama_conforme(curso_md):
    assert curso_md(BUENO) == []


def test_el_curso_real_cumple_las_reglas():
    assert diagramas.validar(RAIZ / "cursos" / "aif-c01", RAIZ / "schemas") == []


def test_sin_diagramas(curso_md):
    assert curso_md("# Nada\n\nSolo texto.\n") == []


def test_es_emoji():
    assert all(es_emoji(c) for c in "🧩🚀⚡🖥🪣🪪🏋❓✨⚙☁")
    assert not any(es_emoji(c) for c in "A1 -<¿é")


@pytest.mark.parametrize("cambio,mensaje", [
    (('A["🧩 Uno"]', 'A["Uno"]'), "debe empezar por un emoji"),
    (("class A proceso", "class A rojo"), "clase «rojo» no válida"),
    (("class A proceso\n", "classDef x fill:#f00\n    class A proceso\n"), "classDef"),
    (("class A proceso\n    class B accion", "class A proceso"), "el nodo «B» no tiene clase"),
    (("class B accion", "class B accion\n    class Z accion"), "«Z», que no existe"),
    (("flowchart LR", "sequenceDiagram"), "solo se admiten diagramas «flowchart»"),
    (("flowchart LR", "graph LR"), "solo se admiten diagramas «flowchart» (este es «graph»)"),
])
def test_reglas_de_estilo(curso_md, cambio, mensaje):
    errs = curso_md(BUENO.replace(*cambio))
    assert any(mensaje in e for e in errs), errs
    assert all("README.md: diagrama 1 (línea" in e for e in errs)


def test_nodo_citado_sin_declarar(curso_md):
    errs = curso_md(BUENO.replace('A["🧩 Uno"] --> B["🚀 Dos"]', 'A["🧩 Uno"] --> B["🚀 Dos"]\n    B --> C'))
    assert any("«C» no tiene etiqueta" in e for e in errs), errs


def test_subgrupo_necesita_emoji_e_informacion(curso_md):
    texto = BUENO.replace("    class A proceso", '    subgraph G["Grupo"]\n        D["🧪 Dentro"]\n    end\n    class D ml\n    class A proceso')
    errs = curso_md(texto)
    assert any("«G» debe empezar por un emoji" in e or "etiqueta de «G»" in e for e in errs)
    assert any("«G» no tiene información" in e for e in errs) and any("«D» no tiene información" in e for e in errs)


def test_subgrupo_conforme(curso_md):
    texto = BUENO.replace("    class A proceso", '    subgraph G["📦 Grupo"]\n        D["🧪 Dentro"]\n    end\n    class D ml\n    class A proceso').replace("B:\n  concepto: rag", "G:\n  titulo: Grupo\n  texto: Caja que contiene otras.\nD:\n  concepto: rag\nB:\n  concepto: rag")
    assert curso_md(texto) == []


def test_etiquetas_de_arista_no_son_nodos(curso_md):
    texto = BUENO.replace('A["🧩 Uno"] --> B["🚀 Dos"]', 'A["🧩 Uno"] -->|"deriva"| B["🚀 Dos"]\n    B -->|"reentrenar"| A')
    assert curso_md(texto) == []


def test_formas_de_nodo(curso_md):
    texto = '''```mermaid
flowchart TB
    A(["👤 Redondeado"]) --> B[("🪣 Cilindro")] --> C{"❓ Decisión"}
    C --> D["🧩 Normal"] & E["⚙️ Otro"]
    class A,B,C,D,E dato
```

```nodos
A: {titulo: A, texto: a}
B: {titulo: B, texto: b}
C: {titulo: C, texto: c}
D: {titulo: D, texto: d}
E: {titulo: E, texto: e}
```
'''
    assert curso_md(texto) == []


# ------------------------------------------------------------------ información de las cajas
def test_falta_el_bloque_nodos(curso_md):
    errs = curso_md(BUENO.split("```nodos")[0])
    assert any("falta el bloque ```nodos" in e for e in errs)


def test_el_bloque_nodos_debe_ir_pegado_al_diagrama(curso_md):
    errs = curso_md(BUENO.replace("```\n\n```nodos", "```\n\nTexto en medio.\n\n```nodos"))
    assert any("falta el bloque ```nodos" in e for e in errs)


def test_caja_sin_informacion_y_entrada_huerfana(curso_md):
    errs = curso_md(BUENO.replace("B:\n  concepto: rag", "Z:\n  concepto: rag"))
    assert any("la caja «B» no tiene información" in e for e in errs)
    assert any("«nodos» incluye «Z»" in e for e in errs)


@pytest.mark.parametrize("cambio,mensaje", [
    (("concepto: rag", "concepto: no-existe"), "el concepto «no-existe» no existe"),
    (("  titulo: Uno\n  texto: Paso uno.", "  titulo: Uno"), "indica «concepto» o bien «titulo» y «texto»"),
    (("https://docs.aws.amazon.com/x", "http://inseguro.example"), "«url» https"),
    (("https://docs.aws.amazon.com/x", "javascript:alert(1)"), "«url» https"),
    (("seccion: 03-modelos-fundacionales/servicios#apartado-detalle", "seccion: 03-modelos-fundacionales/servicios#no-existe"), "ancla «#no-existe»"),
    (("seccion: 03-modelos-fundacionales/servicios#apartado-detalle", "seccion: 03-modelos-fundacionales/laboratorio"), "la sección «03-modelos-fundacionales/laboratorio» no existe"),
    (("seccion: 03-modelos-fundacionales/servicios#apartado-detalle", "seccion: mal formato"), "«seccion» debe ser"),
    (("concepto: rag", "concepto: rag\n  campo_raro: 1"), "campo desconocido «campo_raro»"),
    (("  titulo: Uno\n  texto: Paso uno.", "  titulo: Uno\n  texto: Paso uno.\n  enlaces: x"), "«enlaces» debe ser una lista"),
])
def test_validacion_de_la_informacion(curso_md, cambio, mensaje):
    errs = curso_md(BUENO.replace(*cambio))
    assert any(mensaje in e for e in errs), errs


def test_yaml_de_nodos_roto(curso_md):
    errs = curso_md(BUENO.replace("A:\n  titulo: Uno", "A: [\n  titulo: Uno"))
    assert any("no es YAML válido" in e for e in errs)


def test_concepto_sin_glosario(curso_md, repo):
    curso_md("# x\n")
    (repo / "cursos" / "aif-c01" / "glosario.yaml").unlink()
    errs = diagramas.validar(repo / "cursos" / "aif-c01", repo / "schemas")
    assert errs == []  # el README del fixture no tiene diagramas
    (repo / "cursos" / "aif-c01" / "modulos" / "03-modelos-fundacionales" / "README.md").write_text(BUENO, encoding="utf8")
    errs = diagramas.validar(repo / "cursos" / "aif-c01", repo / "schemas")
    assert any("el curso no tiene glosario" in e for e in errs)


def test_varios_diagramas_se_numeran_y_se_validan_por_separado(curso_md):
    malo = BUENO.replace('A["🧩 Uno"]', 'A["Uno"]')
    errs = curso_md(BUENO + "\n" + malo)
    assert errs and all("diagrama 2" in e for e in errs)


def test_se_validan_tambien_los_markdown_fuera_de_los_modulos(curso_md):
    errs = curso_md(BUENO.replace('A["🧩 Uno"]', 'A["Uno"]'), nombre="README.md")
    assert any("README.md: diagrama 1" in e for e in errs)


def test_extraer_empareja_cada_diagrama_con_su_bloque():
    d = extraer(BUENO + "\n```mermaid\nflowchart LR\n    X[\"🧩 x\"]\n```\n")
    assert len(d) == 2 and d[0].info_texto is not None and d[1].info_texto is None
    assert d[0].nodos == {"A": "🧩 Uno", "B": "🚀 Dos"} and d[0].clases == {"A": "proceso", "B": "accion"}


def test_integrado_en_el_validador_general(repo, capsys):
    from validar_preguntas import main
    (repo / "cursos" / "aif-c01" / "modulos" / "03-modelos-fundacionales" / "README.md").write_text(BUENO.replace('A["🧩 Uno"]', 'A["Uno"]'), encoding="utf8")
    assert main(["--raiz", str(repo), "--sin-minimos"]) == 1
    assert "debe empezar por un emoji" in capsys.readouterr().err
