import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from generar_glosario import generar, main  # noqa: E402

ENTRADAS = [
    {"id": "zeta", "termino": "Zeta", "categoria": "concepto", "definicion": "Último término del glosario de prueba."},
    {"id": "etica", "termino": "ética", "alias": ["ethics"], "categoria": "concepto",
     "definicion": "Término con tilde y minúscula inicial para comprobar el orden."},
    {"id": "amazon-s3", "termino": "Amazon S3", "alias": ["S3"], "categoria": "servicio",
     "definicion": "Almacenamiento de objetos de prueba.", "usar_cuando": "Para guardar ficheros.",
     "no_usar_cuando": "Como base de datos.", "referencia": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html"},
]


def preparar(tmp_path):
    curso = tmp_path / "cursos" / "demo"
    curso.mkdir(parents=True)
    (curso / "curso.yaml").write_text("slug: demo\ntitulo: Curso de prueba\n", encoding="utf8")
    (curso / "glosario.yaml").write_text(yaml.safe_dump(ENTRADAS, allow_unicode=True), encoding="utf8")
    return curso


def test_orden_alfabetico_sin_tildes_y_campos(tmp_path):
    texto = generar(preparar(tmp_path))
    assert texto.startswith("# Glosario: Curso de prueba")
    assert texto.index("**Amazon S3**") < texto.index("**ética**") < texto.index("**Zeta**")
    assert "## E" in texto and "(ethics)" in texto
    assert "  - Usar cuando: Para guardar ficheros." in texto
    assert "  - Referencia: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>" in texto


def test_comprobar_detecta_glosario_desactualizado(tmp_path):
    curso = preparar(tmp_path)
    assert main(["--raiz", str(tmp_path), "--comprobar"]) == 1          # aún no existe glosario.md
    assert main(["--raiz", str(tmp_path)]) == 0                          # lo genera
    assert main(["--raiz", str(tmp_path), "--comprobar"]) == 0
    entradas = ENTRADAS + [{"id": "nuevo", "termino": "Nuevo", "categoria": "concepto",
                            "definicion": "Entrada añadida sin regenerar el Markdown."}]
    (curso / "glosario.yaml").write_text(yaml.safe_dump(entradas, allow_unicode=True), encoding="utf8")
    assert main(["--raiz", str(tmp_path), "--comprobar"]) == 1


def test_glosario_del_repositorio_esta_al_dia():
    raiz = Path(__file__).resolve().parent.parent
    assert main(["--raiz", str(raiz), "--comprobar"]) == 0
