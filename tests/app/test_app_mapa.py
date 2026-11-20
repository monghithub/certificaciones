"""Mapa de servicios: cuadro por categoría oficial con iconos, alcance y módulos, más los diagramas de mapa-servicios.md."""
import yaml
from conftest import crear_usuario, entrar

from app.config import Settings
from app.main import create_app
from curso import glosario as glosario_mod

MOD = "03-modelos-fundacionales"
BEDROCK = "aws/Arch_Amazon-Bedrock_48.svg"
GLOSARIO = [
    {"id": "amazon-bedrock", "termino": "Amazon Bedrock", "alias": ["Bedrock"], "categoria": "servicio", "icono": BEDROCK,
     "definicion": "Modelos fundacionales por API, con <b>etiquetas</b> que no deben interpretarse.",
     "usar_cuando": "Para usar modelos por API.", "no_usar_cuando": "Para entrenar desde cero: SageMaker AI."},
    {"id": "amazon-bedrock-knowledge-bases", "termino": "Amazon Bedrock Knowledge Bases", "categoria": "servicio",
     "icono": BEDROCK, "definicion": "RAG gestionado sobre los datos propios de la empresa."},
    {"id": "amazon-s3", "termino": "Amazon S3", "alias": ["S3"], "categoria": "servicio",
     "definicion": "Almacenamiento de objetos escalable y duradero."},
    {"id": "amazon-guardduty", "termino": "Amazon GuardDuty", "categoria": "servicio",
     "definicion": "Detección de amenazas en la cuenta de AWS."},
    {"id": "herramienta-interna", "termino": "Herramienta Interna", "categoria": "servicio",
     "definicion": "Servicio ficticio que no figura en ninguna lista oficial."},
    {"id": "rag", "termino": "RAG", "categoria": "tecnica", "definicion": "Técnica que mejora las respuestas con datos externos."},
]
MAPA_MD = """# Mapa

```mermaid
flowchart LR
    A["✨ <b>Amazon Bedrock</b>"] --> B["🪣 <b>Amazon S3</b>"]
    class A gen
    class B dato
```

```nodos
A:
  concepto: amazon-bedrock
B:
  concepto: amazon-s3
```
"""


def montar(curso, tmp_path, glosario=GLOSARIO, mapa=MAPA_MD):
    c = curso / "cursos" / "aif-c01"
    if glosario is not None:
        (c / "glosario.yaml").write_text(yaml.safe_dump(glosario, allow_unicode=True), encoding="utf8")
    if mapa:
        (c / "mapa-servicios.md").write_text(mapa, encoding="utf8")
    (c / "modulos" / MOD / "servicios.md").write_text("# Servicios\n\n| Servicio | Cuándo |\n|---|---|\n| Amazon S3 | datos |\n| Amazon Bedrock | modelos |\n",
                                                      encoding="utf8")
    app = create_app(Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/m.db", courses_dir=curso / "cursos",
                              schemas_dir=curso / "schemas"))
    crear_usuario(app)
    return entrar(app)


def test_cuadro_por_categoria_oficial(curso, tmp_path):
    html = montar(curso, tmp_path).get("/c/aif-c01/mapa").text
    ml, alm = html.index("Aprendizaje automático e IA"), html.index("Almacenamiento")
    otros, fuera = html.index("Funcionalidades y otros servicios"), html.index("Fuera del alcance del examen")
    assert ml < alm < otros < fuera  # orden de la guía, luego el resto
    assert html.index("Amazon GuardDuty") > fuera and otros < html.index("Herramienta Interna") < fuera
    assert 'data-concepto="rag"' not in html.split('id="cuadro-titulo"')[1]  # solo servicios en el cuadro


def test_iconos_modulos_y_escapado(curso, tmp_path):
    html = montar(curso, tmp_path).get("/c/aif-c01/mapa").text
    assert html.count(f"/static/iconos/{BEDROCK}?v=") == 2  # Bedrock y su funcionalidad Knowledge Bases
    assert 'class="mapa-sin-icono"' in html
    assert f'href="/c/aif-c01/modulo/{MOD}/servicios"' in html
    assert "&lt;b&gt;etiquetas&lt;/b&gt;" in html and "<b>etiquetas</b>" not in html
    assert "Para entrenar desde cero: SageMaker AI." in html


def test_diagramas_y_enlace_en_el_menu(curso, tmp_path):
    c = montar(curso, tmp_path)
    html = c.get("/c/aif-c01/mapa").text
    assert 'class="diagrama"' in html and '"amazon-bedrock"' in html
    assert 'href="/c/aif-c01/mapa"' in c.get("/c/aif-c01/").text


def test_sin_mapa_md_solo_el_cuadro(curso, tmp_path):
    html = montar(curso, tmp_path, mapa=None).get("/c/aif-c01/mapa").text
    assert 'id="cuadro-titulo"' in html and 'class="diagrama"' not in html


def test_curso_sin_glosario_404(curso, tmp_path):
    assert montar(curso, tmp_path, glosario=None, mapa=None).get("/c/aif-c01/mapa").status_code == 404


def test_icono_inexistente_es_un_error(curso, tmp_path):
    g = [dict(GLOSARIO[0], icono="aws/No-Existe_48.svg")]
    (curso / "cursos" / "aif-c01" / "glosario.yaml").write_text(yaml.safe_dump(g, allow_unicode=True), encoding="utf8")
    errores = glosario_mod.validar(curso / "cursos" / "aif-c01", curso / "schemas")
    assert any("No-Existe_48.svg" in e for e in errores)
