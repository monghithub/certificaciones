import copy
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from conftest import FIX, con_repaso, escribir, pregunta_repaso, segundo_curso  # noqa: E402
from validar_preguntas import main, validar  # noqa: E402

BASE = yaml.safe_load((FIX / "valido.yaml").read_text(encoding="utf8"))


def errores(repo, preguntas, minimos=False):
    escribir(repo, preguntas)
    return validar(repo, minimos=minimos)[0]


def mutar(i, **cambios):
    p = copy.deepcopy(BASE)
    p[i].update(cambios)
    return p


def test_banco_valido(repo):
    assert errores(repo, BASE) == []
    assert main(["--raiz", str(repo), "--sin-minimos"]) == 0


def test_id_duplicado(repo):
    p = copy.deepcopy(BASE)
    p[1]["id"] = "D3-001"
    assert any("id duplicado" in e for e in errores(repo, p))


def test_correcta_inexistente(repo):
    assert any("inexistentes" in e for e in errores(repo, mutar(0, correctas=["z"])))


def test_multiple_choice_con_dos_correctas(repo):
    assert errores(repo, mutar(0, correctas=["a", "b"]))


def test_multiple_response_con_una_correcta(repo):
    assert errores(repo, mutar(1, correctas=["b"]))


def test_tarea_inexistente(repo):
    assert any("no existe en fuentes" in e for e in errores(repo, mutar(0, tarea="3.9")))


def test_tarea_de_otro_dominio(repo):
    assert any("no pertenece" in e for e in errores(repo, mutar(0, tarea="2.1")))


def test_distractor_sin_explicar(repo):
    p = copy.deepcopy(BASE)
    del p[0]["distractores"]["a"]
    assert any("sin explicación" in e for e in errores(repo, p))


def test_todas_las_anteriores(repo):
    p = copy.deepcopy(BASE)
    p[0]["opciones"][0]["texto"] = "Todas las anteriores"
    assert any("anteriores" in e for e in errores(repo, p))


def test_ordering_fuera_de_rango(repo):
    assert errores(repo, mutar(2, correctas=["a", "b"]))


def test_matching_prompt_sin_par(repo):
    p = copy.deepcopy(BASE)
    p[3]["correctas"] = [["1", "b"], ["2", "a"], ["2", "c"]]
    assert errores(repo, p)


def test_campo_obligatorio_ausente(repo):
    p = copy.deepcopy(BASE)
    del p[0]["explicacion"]
    assert errores(repo, p)


def test_minimos(repo):
    escribir(repo, BASE)
    assert any("mínimo 60" in e for e in validar(repo, minimos=True)[0])


def test_varios_errores_codigo_salida(repo, capsys):
    p = copy.deepcopy(BASE)
    p[0]["correctas"] = ["z"]
    p[1]["tarea"] = "3.9"
    escribir(repo, p)
    assert main(["--raiz", str(repo), "--sin-minimos"]) == 1
    assert capsys.readouterr().err.count("ERROR") >= 2


def mc_en_posicion(i, letra):
    """Copia de la pregunta base de opción múltiple con la respuesta correcta en `letra`."""
    q = copy.deepcopy(BASE[0])
    q["id"] = f"D3-{i + 1:03d}"
    textos = [o["texto"] for o in q["opciones"]]
    correcta = textos.pop(1)
    destino = "abcd".index(letra)
    textos.insert(destino, correcta)
    q["opciones"] = [{"id": l, "texto": t} for l, t in zip("abcd", textos)]
    q["correctas"] = [letra]
    q["distractores"] = {l: "Motivo." for l in "abcd" if l != letra}
    return q


def test_distribucion_aviso_sin_error(repo):
    escribir(repo, [mc_en_posicion(i, "abcd"[i % 4]) for i in range(60)])
    errs, avisos, _ = validar(repo, minimos=True)
    assert errs == [] and any("multiple_choice es el 100 %" in a for a in avisos), (errs, avisos)


def test_respuestas_concentradas_en_una_letra(repo):
    escribir(repo, [mc_en_posicion(i, "b") for i in range(12)])
    errs, _, _ = validar(repo, minimos=False)
    assert any("es «b» en el 100 %" in e for e in errs), errs


def test_opciones_repetidas(repo):
    p = copy.deepcopy(BASE)
    p[0]["opciones"][3]["texto"] = p[0]["opciones"][0]["texto"]
    assert any("mismo texto" in e for e in errores(repo, p))


def test_avisos_de_calidad(repo):
    p = copy.deepcopy(BASE)
    p[0]["opciones"][0]["texto"] = "Fine-tuning semanal, que siempre es la opción más barata"
    p[0]["enunciado"] = "¿Qué técnica usa datos propios para responder?"
    escribir(repo, p)
    errs, avisos, _ = validar(repo, minimos=False)
    assert errs == []
    assert any("términos absolutos" in a and "'a'" in a for a in avisos), avisos
    assert any("enunciado muy corto" in a for a in avisos), avisos


def test_validar_todos_los_cursos_y_uno_concreto(repo, capsys):
    c = segundo_curso(repo)
    escribir(repo, [dict(BASE[0], correctas=["z"])])  # error solo en aif-c01
    assert main(["--raiz", str(repo), "--sin-minimos"]) == 1
    assert "aif-c01" in capsys.readouterr().err
    assert main(["--raiz", str(repo), "--curso", "otro-curso"]) == 0
    assert c.exists()


def test_segundo_curso_con_otros_dominios_valida_sin_cambios(repo):
    segundo_curso(repo)
    errs, _, resumen = validar(repo)
    assert any("otro-curso" in r for r in resumen) and not [e for e in errs if "otro-curso" in e]


def test_dominio_no_declarado_en_el_manifiesto(repo):
    c = segundo_curso(repo)
    p = yaml.safe_load((FIX / "valido.yaml").read_text(encoding="utf8"))[0]
    p.update(id="D4-001", dominio=4, tarea="4.1")
    escribir(repo, [p], "01-base", "otro-curso")
    errs, _, _ = validar(repo)
    assert any("dominio 4 no declarado" in e for e in errs) and c.exists()


def test_los_ids_pueden_repetirse_entre_cursos(repo):
    segundo_curso(repo)
    p = copy.deepcopy(BASE[0])
    p.update(id="D2-001", dominio=2, tarea="2.1")  # existe en aif-c01 (tarea 2.1) y en otro-curso
    escribir(repo, [p], "02-fundamentos-genai")
    errs, _, _ = validar(repo)
    assert not [e for e in errs if "duplicado" in e]


@pytest.mark.parametrize("manifiesto,mensaje", [
    ("slug: distinto\ntitulo: X Y Z\nidioma: es-ES\ndominios: [{id: 1, nombre: A, peso: 100}]\n", "no coincide con la carpeta"),
    ("slug: mal\ntitulo: X Y Z\nidioma: es-ES\ndominios: [{id: 1, nombre: A, peso: 95}]\n", "sumar 100"),
    ("slug: mal\ntitulo: X Y Z\nidioma: es-ES\ndominios: [{id: 1, nombre: A, peso: 50}, {id: 1, nombre: B, peso: 50}]\n", "duplicados"),
    ("slug: mal\ntitulo: X Y Z\nidioma: es-ES\ndominios: []\n", "dominios"),
    ("slug: mal\ntitulo: X Y Z\nidioma: es-ES\ndominios: [{id: 1, nombre: A, peso: 100}]\nexamen: {preguntas: 5, minutos: 5}\n", "simulacro"),
])
def test_manifiestos_invalidos(repo, manifiesto, mensaje):
    c = repo / "cursos" / "mal"
    c.mkdir()
    (c / "curso.yaml").write_text(manifiesto, encoding="utf8")
    errs, _, _ = validar(repo)
    assert any("mal:" in e and mensaje in e for e in errs), errs


def test_modulo_de_simulacro_inexistente(repo):
    f = repo / "cursos" / "aif-c01" / "curso.yaml"
    f.write_text(f.read_text(encoding="utf8").replace("simulacro: 06-simulacro", "simulacro: 09-nada"), encoding="utf8")
    errs, _, _ = validar(repo)
    assert any("simulacro '09-nada' no existe" in e for e in errs)


def test_referencia_fuera_de_las_fuentes_oficiales(repo):
    p = copy.deepcopy(BASE)
    p[0]["referencia"] = "https://learn.microsoft.com/es-es/azure/"
    assert any("no pertenece a las fuentes oficiales" in e for e in errores(repo, p))


def test_referencia_en_subdominio_de_una_fuente_oficial(repo):
    p = copy.deepcopy(BASE)
    p[0]["referencia"] = "https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html"
    assert errores(repo, p) == []


def test_curso_de_otro_proveedor_con_sus_fuentes(repo):
    c = segundo_curso(repo)
    f = c / "curso.yaml"
    f.write_text(f.read_text(encoding="utf8").replace(
        "idioma: es-ES\n", "proveedor: Microsoft\nfuentes_oficiales: [learn.microsoft.com]\nidioma: es-ES\n"), encoding="utf8")
    p = yaml.safe_load((c / "modulos" / "01-base" / "preguntas.yaml").read_text(encoding="utf8"))
    p[0]["referencia"] = "https://learn.microsoft.com/es-es/credentials/"
    (c / "modulos" / "01-base" / "preguntas.yaml").write_text(yaml.safe_dump(p, allow_unicode=True), encoding="utf8")
    errs, _, _ = validar(repo, minimos=False, cursos=[c.name])
    assert errs == [], errs
    p[0]["referencia"] = "https://docs.aws.amazon.com/bedrock/"
    (c / "modulos" / "01-base" / "preguntas.yaml").write_text(yaml.safe_dump(p, allow_unicode=True), encoding="utf8")
    errs, _, _ = validar(repo, minimos=False, cursos=[c.name])
    assert any("no pertenece a las fuentes oficiales" in e for e in errs), errs


def test_referencia_no_https_rechazada_por_el_esquema(repo):
    p = copy.deepcopy(BASE)
    p[0]["referencia"] = "http://docs.aws.amazon.com/bedrock/"
    assert any("referencia" in e for e in errores(repo, p))


def test_simulacro_repite_enunciado_de_un_modulo(repo):
    p = copy.deepcopy(BASE[0])
    p.update(id="S-001", enunciado=p["enunciado"].upper() + "  ")
    escribir(repo, [p], "06-simulacro")
    errs = validar(repo, minimos=False)[0]
    assert any("simulacro debe ser inédito" in e and "D3-001" in e for e in errs)


def test_simulacro_con_enunciado_nuevo(repo):
    p = copy.deepcopy(BASE[0])
    p.update(id="S-001", enunciado="Una empresa de logística quiere un escenario distinto de los del banco del módulo para el simulacro.")
    escribir(repo, [p], "06-simulacro")
    assert not any("inédito" in e for e in validar(repo, minimos=False)[0])


def test_simulacro_muy_parecido_genera_aviso(repo):
    p = copy.deepcopy(BASE[0])
    p.update(id="S-001", enunciado=p["enunciado"].replace("semanalmente", "cada semana"))
    escribir(repo, [p], "06-simulacro")
    errs, avisos, _ = validar(repo, minimos=False)
    assert not any("inédito" in e for e in errs)
    assert any("se parece mucho a D3-001" in a for a in avisos)


def test_simulacro_con_enunciado_repetido_dentro_del_simulacro(repo):
    a = copy.deepcopy(BASE[0]); a.update(id="S-001", enunciado="Un escenario nuevo y distinto de los módulos para el simulacro del curso.")
    b = copy.deepcopy(a); b["id"] = "S-002"
    escribir(repo, [a, b], "06-simulacro")
    assert any("del propio simulacro" in e for e in validar(repo, minimos=False)[0])


# ------------------------------------------------------------- bancos de repaso
def repaso(repo, preguntas, modulo="03-modelos-fundacionales"):
    escribir(repo, preguntas, modulo, fichero="repaso.yaml")


def test_repaso_valido_con_conocimientos_previos(repo):
    con_repaso(repo)
    repaso(repo, [pregunta_repaso()])
    repaso(repo, [pregunta_repaso("R0-001", dominio=0, tarea="CP", objetivo="CP.2", enunciado="¿Quién cifra tus datos?")], "00-base-aws")
    errs, avisos, resumen = validar(repo, minimos=False)
    assert errs == [], errs
    assert not any("repaso.yaml" in a and "enunciado muy corto" in a for a in avisos)  # el repaso admite preguntas directas
    assert any(r.endswith("00-base-aws/repaso.yaml") for r in resumen)


def test_dominio_0_solo_en_repaso_con_previos(repo):
    p = mutar(0, dominio=0, tarea="CP", objetivo="CP.1")
    assert any("dominio 0" in e for e in errores(repo, p))  # banco de examen
    repaso(repo, [pregunta_repaso("R0-001", dominio=0, tarea="CP", objetivo="CP.1")], "00-base-aws")
    assert any("dominio 0" in e for e in validar(repo, minimos=False)[0])  # curso sin `repaso.previos`


def test_repaso_con_objetivo_previo_inexistente_o_tarea_cp_fuera_del_dominio_0(repo):
    con_repaso(repo)
    repaso(repo, [pregunta_repaso("R0-001", dominio=0, tarea="CP", objetivo="CP.9")], "00-base-aws")
    repaso(repo, [pregunta_repaso("R3-001", tarea="CP", objetivo="3.1.1")])
    errs = validar(repo, minimos=False)[0]
    assert any("CP.9" in e for e in errs) and any("solo se admite en el dominio 0" in e for e in errs)


def test_repaso_no_copia_preguntas_de_examen(repo):
    con_repaso(repo)
    repaso(repo, [pregunta_repaso(enunciado=BASE[0]["enunciado"])])
    assert any("no debe copiar preguntas de examen" in e for e in validar(repo, minimos=False)[0])


def test_ids_de_repaso_unicos_en_el_curso_y_minimo(repo):
    con_repaso(repo, minimo_por_modulo=3)
    repaso(repo, [pregunta_repaso(), pregunta_repaso(enunciado="Otra pregunta de repaso distinta")])
    errs = validar(repo)[0]
    assert any("id duplicado" in e for e in errs) and any("repaso.yaml: 2 preguntas, mínimo 3" in e for e in errs)


def test_simulacro_sin_banco_de_repaso(repo):
    con_repaso(repo)
    repaso(repo, [pregunta_repaso()], "06-simulacro")
    assert any("no lleva banco de repaso" in e for e in validar(repo, minimos=False)[0])
