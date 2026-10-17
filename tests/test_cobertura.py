import copy
import re
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from comprobar_cobertura import ancla, anclas_de, comprobar, main  # noqa: E402
from conftest import FIX, con_repaso, escribir, pregunta_repaso  # noqa: E402

MOD = "03-modelos-fundacionales"


def ids_dominio3(repo):
    t = (repo / "cursos" / "aif-c01" / "fuentes" / "dominio-3.md").read_text(encoding="utf8")
    return re.findall(r"\*\*(\d+\.\d+\.\d+)\*\*", t)


def readme(repo, omitir=(), ancla_rota=(), sin_enlace=()):
    filas = []
    for o in ids_dominio3(repo):
        if o in omitir:
            continue
        enlace = "" if o in sin_enlace else ("[x](#no-existe)" if o in ancla_rota else "[Teoría](#teoría-de-modelos)")
        filas.append(f"| {o} | Resumen | {enlace} |")
    texto = "# Modelos fundacionales\n\n## Mapa de cobertura\n\n| Objetivo | Descripción | Sección |\n|---|---|---|\n" + "\n".join(filas) + "\n\n## Teoría de modelos\n\nTexto.\n"
    (repo / "cursos" / "aif-c01" / "modulos" / MOD / "README.md").write_text(texto, encoding="utf8")


def preguntas(repo, por_tarea, con_objetivo=True):
    """Genera preguntas válidas: `por_tarea` = {"3.1": n, ...}; objetivo = k-ésimo objetivo de la tarea (rotando)."""
    base = yaml.safe_load((FIX / "valido.yaml").read_text(encoding="utf8"))[0]
    objetivos = ids_dominio3(repo)
    out, n = [], 0
    for tarea, cantidad in por_tarea.items():
        propios = [o for o in objetivos if o.startswith(tarea + ".")]
        for k in range(cantidad):
            n += 1
            p = copy.deepcopy(base)
            p.update(id=f"D3-{n:03d}", tarea=tarea)
            if con_objetivo:
                p["objetivo"] = propios[k % len(propios)]
            out.append(p)
    escribir(repo, out)


def test_ancla_estilo_github():
    assert ancla("Teoría de modelos") == "teoría-de-modelos"
    assert ancla("¿Qué es RAG? (v2)") == "qué-es-rag-v2"
    assert anclas_de("# A\n## A\n```\n# no\n```\n") == {"a", "a-1"}


def test_cobertura_completa(repo, capsys):
    readme(repo)
    errs, resumen = comprobar(repo, modulo="03")
    assert errs == []
    assert any(r.startswith("aif-c01/03-modelos-fundacionales 3.1: 6/6 objetivos") for r in resumen)
    assert main(["--raiz", str(repo), "--modulo", "03"]) == 0


def test_objetivo_ausente(repo):
    readme(repo, omitir={"3.2.3"})
    errs, _ = comprobar(repo, modulo="03")
    assert errs == ["aif-c01/03-modelos-fundacionales: objetivo 3.2.3 no aparece en el mapa de cobertura"]


def test_ancla_inexistente(repo):
    readme(repo, ancla_rota={"3.4.1"})
    errs, _ = comprobar(repo, modulo="03")
    assert any("3.4.1 enlaza a #no-existe" in e for e in errs)


def test_fila_sin_enlace(repo):
    readme(repo, sin_enlace={"3.1.1"})
    errs, _ = comprobar(repo, modulo="03")
    assert any("3.1.1 sin enlace" in e for e in errs)


def test_id_desconocido_en_el_mapa(repo):
    readme(repo)
    f = repo / "cursos" / "aif-c01" / "modulos" / MOD / "README.md"
    f.write_text(f.read_text(encoding="utf8").replace("## Teoría de modelos", "| 3.9.9 | Falso | [x](#teoría-de-modelos) |\n\n## Teoría de modelos"), encoding="utf8")
    errs, _ = comprobar(repo, modulo="03")
    assert any("3.9.9" in e and "no existe en fuentes" in e for e in errs)


def test_modulo_vacio_se_omite_pero_explicito_falla(repo):
    errs, resumen = comprobar(repo)  # sin README: se omite
    assert errs == [] and resumen == []
    errs, _ = comprobar(repo, modulo="03")
    assert any("falta README.md" in e for e in errs)
    assert main(["--raiz", str(repo)]) == 0
    assert main(["--raiz", str(repo), "--modulo", "03"]) == 1


def test_readme_sin_mapa(repo):
    (repo / "cursos" / "aif-c01" / "modulos" / MOD / "README.md").write_text("# Solo texto\n", encoding="utf8")
    assert comprobar(repo)[0] == []
    assert any("no tiene mapa" in e for e in comprobar(repo, modulo="03")[0])


def test_modulo_inexistente(repo):
    errs, _ = comprobar(repo, modulo="09")
    assert any("no encontrado" in e for e in errs)


def test_preguntas_por_tarea_y_objetivo(repo):
    readme(repo)
    preguntas(repo, {"3.1": 18, "3.2": 18, "3.3": 18, "3.4": 18})
    errs, resumen = comprobar(repo, modulo="03", con_preguntas=True)
    assert errs == [], errs
    assert "aif-c01/03-modelos-fundacionales 3.1: 6/6 objetivos, 18 preguntas" in resumen


def test_tarea_sin_preguntas_suficientes(repo):
    readme(repo)
    preguntas(repo, {"3.1": 18, "3.2": 18, "3.3": 18, "3.4": 2})
    errs, _ = comprobar(repo, modulo="03", con_preguntas=True)
    assert any("tarea 3.4 tiene 2 preguntas, mínimo 15" in e for e in errs)


def test_objetivo_con_pocas_preguntas(repo):
    readme(repo)
    preguntas(repo, {"3.1": 12, "3.2": 18, "3.3": 18, "3.4": 18})  # 3.1: 6 objetivos con 2 preguntas cada uno
    errs, _ = comprobar(repo, modulo="03", con_preguntas=True)
    assert any("el objetivo 3.1.1 tiene 2 preguntas, mínimo 3" in e for e in errs), errs


def test_objetivo_sin_pregunta(repo):
    readme(repo)
    preguntas(repo, {"3.1": 5, "3.2": 8, "3.3": 8, "3.4": 8})  # 3.1.6 queda sin cubrir
    errs, _ = comprobar(repo, modulo="03", con_preguntas=True)
    assert any("ninguna pregunta cubre el objetivo 3.1.6" in e for e in errs)


def test_preguntas_sin_campo_objetivo(repo):
    readme(repo)
    preguntas(repo, {"3.1": 8, "3.2": 8, "3.3": 8, "3.4": 8}, con_objetivo=False)
    errs, _ = comprobar(repo, modulo="03", con_preguntas=True)
    assert any("no declaran `objetivo`" in e for e in errs)


@pytest.mark.parametrize("objetivo,mensaje", [("3.1.9", "no existe en fuentes"), ("2.1.1", "no pertenece al dominio"), ("3.2.1", "no pertenece a la tarea")])
def test_validador_comprueba_el_campo_objetivo(repo, objetivo, mensaje):
    from validar_preguntas import validar
    p = yaml.safe_load((FIX / "valido.yaml").read_text(encoding="utf8"))[0]  # tarea 3.1
    p["objetivo"] = objetivo
    escribir(repo, [p])
    errs, _, _ = validar(repo, minimos=False)
    assert any(mensaje in e for e in errs), errs


def test_fuente_de_conocimientos_previos_del_curso_real():
    from comprobar_cobertura import objetivos_de
    real = Path(__file__).resolve().parent.parent / "cursos" / "aif-c01" / "fuentes"
    assert objetivos_de(real / "conocimientos-previos.md") == ["CP.1", "CP.2", "CP.3", "CP.4"]
    assert len(objetivos_de(real / "dominio-1.md")) == 17


def test_cobertura_del_repaso(repo):
    readme(repo)
    preguntas(repo, {"3.1": 18, "3.2": 18, "3.3": 18, "3.4": 18})
    con_repaso(repo, minimo_por_objetivo=1)
    errs, _ = comprobar(repo, modulo="03", con_preguntas=True)
    assert any("falta el banco de repaso" in e for e in errs)
    objetivos = ids_dominio3(repo)
    banco = [pregunta_repaso(f"R3-{k:03d}", tarea=o.rsplit(".", 1)[0], objetivo=o, enunciado=f"Pregunta de repaso {k}")
             for k, o in enumerate(objetivos[1:], 1)]  # sin el primer objetivo
    escribir(repo, banco, MOD, fichero="repaso.yaml")
    errs, resumen = comprobar(repo, modulo="03", con_preguntas=True)
    assert errs == [f"aif-c01/{MOD}: repaso: el objetivo {objetivos[0]} tiene 0 preguntas, mínimo 1"], errs
    assert any(r.endswith("de repaso") for r in resumen)
