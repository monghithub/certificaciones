import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from conftest import escribir  # noqa: E402

from curso.glosario import Glosario, Entrada, leer, servicios_de, validar  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent


def entrada(id_, termino, alias=(), categoria="concepto", **kw):
    return {"id": id_, "termino": termino, "alias": list(alias), "categoria": categoria,
            "definicion": "Definición de prueba suficientemente larga.", **kw}


def glosario_en(repo, entradas):
    (repo / "cursos" / "aif-c01" / "glosario.yaml").write_text(yaml.safe_dump(entradas, allow_unicode=True), encoding="utf8")
    return repo / "cursos" / "aif-c01"


def mini(*entradas):
    return Glosario([Entrada(id=e["id"], termino=e["termino"], categoria="concepto", definicion="x" * 30, alias=tuple(e.get("alias", ()))) for e in entradas])


# ------------------------------------------------------------------ búsqueda
def test_busca_por_termino_y_alias_sin_distinguir_mayusculas():
    g = mini({"id": "bedrock", "termino": "Amazon Bedrock", "alias": ["Bedrock"]})
    assert g.buscar("Usamos amazon bedrock y BEDROCK.") == [(7, 21, "bedrock"), (24, 31, "bedrock")]


def test_prefiere_el_termino_mas_largo():
    g = mini({"id": "b", "termino": "Amazon Bedrock", "alias": ["Bedrock"]}, {"id": "k", "termino": "Amazon Bedrock Knowledge Bases", "alias": ["Knowledge Bases"]})
    r = g.buscar("Amazon Bedrock Knowledge Bases")
    assert r == [(0, 30, "k")]


def test_limites_de_palabra():
    g = mini({"id": "ia", "termino": "IA"}, {"id": "ml", "termino": "ML"})
    assert g.buscar("PAIRS CIA HTML") == []
    assert [x[2] for x in g.buscar("la IA y el ML.")] == ["ia", "ml"]


def test_siglas_distinguen_mayusculas():
    g = mini({"id": "rag", "termino": "RAG"})
    assert g.buscar("drag y rag") == []
    assert [x[2] for x in g.buscar("con RAG")] == ["rag"]


def test_palabras_largas_no_distinguen_mayusculas_y_aceptan_acentos():
    g = mini({"id": "ml", "termino": "aprendizaje automático"})
    assert [x[2] for x in g.buscar("El Aprendizaje Automático es")] == ["ml"]


def test_caracteres_especiales_se_escapan():
    g = mini({"id": "x", "termino": "AWS Identity (IAM)"})
    assert g.buscar("ver AWS Identity (IAM) aquí")[0][2] == "x"


def test_glosario_vacio():
    assert Glosario([]).buscar("cualquier texto") == []


# ------------------------------------------------------------------ servicios.md
def test_servicios_de_extrae_la_primera_columna():
    md = "# T\n\n| Servicio | Caso | No usar |\n|---|---|---|\n| **Amazon S3** | x | y |\n| [AWS Lambda](u) | x | y |\n\n| Otra | b |\n|---|---|\n| `Kiro` | z |\n"
    assert servicios_de(md) == ["Amazon S3", "AWS Lambda", "Kiro"]


# ------------------------------------------------------------------ validación
def test_glosario_real_del_curso_es_valido_y_cubre_los_servicios():
    assert validar(RAIZ / "cursos" / "aif-c01", RAIZ / "schemas") == []


def test_sin_glosario_no_hay_errores(repo):
    assert validar(repo / "cursos" / "aif-c01", repo / "schemas") == []
    assert leer(repo / "cursos" / "aif-c01", repo / "schemas") == (None, [])


@pytest.mark.parametrize("cambio,mensaje", [
    ({"categoria": "otra"}, "categoria"),
    ({"id": "Mal Id"}, "id"),
    ({"definicion": "corta"}, "definicion"),
    ({"referencia": "http://inseguro.example"}, "referencia"),
])
def test_entrada_invalida(repo, cambio, mensaje):
    d = glosario_en(repo, [dict(entrada("a-b", "Término uno"), **cambio)])
    errs = validar(d, repo / "schemas")
    assert errs and any(mensaje in e for e in errs), errs


def test_id_duplicado_y_alias_duplicado(repo):
    d = glosario_en(repo, [entrada("uno", "Uno", ["Bedrock"]), entrada("uno", "Otro"), entrada("dos", "Dos", ["bedrock"])])
    errs = " ".join(validar(d, repo / "schemas"))
    assert "id duplicado «uno»" in errs and "«bedrock» está en «uno» y en «dos»" in errs


def test_servicio_sin_entrada(repo):
    d = glosario_en(repo, [entrada("ec2", "Amazon EC2", categoria="servicio")])
    m = d / "modulos" / "03-modelos-fundacionales"
    (m / "servicios.md").write_text("| Servicio | Uso |\n|---|---|\n| Amazon EC2 | x |\n| Amazon Rekognition | y |\n", encoding="utf8")
    errs = validar(d, repo / "schemas")
    assert errs == ["aif-c01/modulos/03-modelos-fundacionales/servicios.md: «Amazon Rekognition» no tiene entrada en el glosario"]


def test_yaml_roto(repo):
    (repo / "cursos" / "aif-c01" / "glosario.yaml").write_text("- id: [\n", encoding="utf8")
    assert any("YAML inválido" in e for e in validar(repo / "cursos" / "aif-c01", repo / "schemas"))


def test_el_validador_general_incluye_el_glosario(repo, capsys):
    from validar_preguntas import main
    glosario_en(repo, [entrada("uno", "Uno"), entrada("uno", "Otro")])
    assert main(["--raiz", str(repo), "--sin-minimos"]) == 1
    assert "id duplicado" in capsys.readouterr().err
