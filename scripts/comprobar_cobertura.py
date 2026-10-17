#!/usr/bin/env python3
"""Comprueba que el mapa de cobertura de cada módulo cubre todos los objetivos oficiales y que hay preguntas por tarea
(banco de examen) y por objetivo (bancos de examen y de repaso).

Formato del mapa de cobertura (README.md del módulo): una tabla Markdown cuya primera columna es el id del
objetivo (p. ej. `1.2.3` o `CP.1`) y que enlaza en alguna celda a un encabezado del mismo README (`[texto](#ancla)`).
Los objetivos salen de cursos/<curso>/fuentes/<fichero>, según el bloque `cobertura` de curso.yaml.
"""
import argparse
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from curso.anclas import ancla, anclas_de  # noqa: E402,F401  (reexportadas: las usan los tests)
from curso.cobertura import grupo, mapa  # noqa: E402
from curso.manifiesto import Manifiesto, descubrir  # noqa: E402

ID_FUENTE = re.compile(r"\*\*((?:[A-Z]+|\d+)(?:\.\d+)+)\*\*")


def leer_banco(f: Path) -> list[dict]:
    datos = yaml.safe_load(f.read_text(encoding="utf8")) if f.is_file() else []
    return [p for p in datos or [] if isinstance(p, dict)]


def objetivos_de(fuente: Path) -> list[str]:
    return list(dict.fromkeys(ID_FUENTE.findall(fuente.read_text(encoding="utf8"))))


def comprobar_modulo(curso: Manifiesto, modulo: str, fichero: str, con_preguntas: bool, explicito: bool):
    """Devuelve (errores, lineas_resumen, comprobado)."""
    carpeta = curso.carpeta / "modulos" / modulo
    readme = carpeta / "README.md"
    fuente = curso.carpeta / "fuentes" / fichero
    pref = f"{curso.slug}/{modulo}"
    if not fuente.is_file():
        return [f"{pref}: falta la fuente fuentes/{fichero}"], [], True
    if not readme.is_file():
        return ([f"{pref}: falta README.md"], [], True) if explicito else ([], [], False)
    texto = readme.read_text(encoding="utf8")
    filas = mapa(texto)
    if not filas:
        return ([f"{pref}: el README no tiene mapa de cobertura"], [], True) if explicito else ([], [], False)
    errores, existentes = [], anclas_de(texto)
    objetivos = objetivos_de(fuente)
    for o in objetivos:
        if o not in filas:
            errores.append(f"{pref}: objetivo {o} no aparece en el mapa de cobertura")
        elif not filas[o]:
            errores.append(f"{pref}: objetivo {o} sin enlace a la sección que lo cubre")
        else:
            for a in filas[o]:
                if a not in existentes:
                    errores.append(f"{pref}: objetivo {o} enlaza a #{a}, que no existe en el README")
    errores += [f"{pref}: el mapa incluye {o}, que no existe en fuentes/{fichero}" for o in filas if o not in objetivos]

    preguntas = leer_banco(carpeta / "preguntas.yaml")
    repaso = leer_banco(carpeta / "repaso.yaml")
    por_tarea = Counter(p.get("tarea") for p in preguntas if isinstance(p, dict))
    por_objetivo = Counter(p.get("objetivo") for p in preguntas if isinstance(p, dict) and p.get("objetivo"))
    resumen = []
    tareas = list(dict.fromkeys(grupo(o) for o in objetivos))
    for t in tareas:
        propios = [o for o in objetivos if grupo(o) == t]
        cubiertos = [o for o in propios if o in filas and filas[o]]
        linea = f"{pref} {t}: {len(cubiertos)}/{len(propios)} objetivos"
        if preguntas:
            linea += f", {por_tarea.get(t, 0)} preguntas"
        if repaso:
            linea += f", {sum(1 for p in repaso if p.get('tarea') == t)} de repaso"
        resumen.append(linea)
    if con_preguntas and preguntas:
        minimo = curso.minimo_por_tarea or 1
        for t in tareas:
            if t[0].isdigit() and por_tarea.get(t, 0) < minimo:
                errores.append(f"{pref}: la tarea {t} tiene {por_tarea.get(t, 0)} preguntas, mínimo {minimo}")
        if por_objetivo:
            min_obj = curso.minimo_por_objetivo or 1
            for o in objetivos:
                if not o[0].isdigit():
                    continue
                n = por_objetivo.get(o, 0)
                if n == 0:
                    errores.append(f"{pref}: ninguna pregunta cubre el objetivo {o}")
                elif n < min_obj:
                    errores.append(f"{pref}: el objetivo {o} tiene {n} preguntas, mínimo {min_obj}")
        else:
            errores.append(f"{pref}: las preguntas no declaran `objetivo`; no se puede comprobar la cobertura por objetivo")
    if con_preguntas and curso.repaso_minimo_por_objetivo is not None:
        errores += comprobar_repaso(curso, pref, objetivos, repaso, fichero)
    return errores, resumen, True


def comprobar_repaso(curso: Manifiesto, pref: str, objetivos: list[str], repaso: list[dict], fichero: str) -> list[str]:
    """Cobertura del banco de repaso: cada objetivo del módulo con al menos `repaso.minimo_por_objetivo` preguntas."""
    if not repaso:
        return [f"{pref}: falta el banco de repaso (repaso.yaml)"]
    minimo = curso.repaso_minimo_por_objetivo
    por_objetivo = Counter(p.get("objetivo") for p in repaso)
    errores = [f"{pref}: repaso: el objetivo {o} tiene {por_objetivo.get(o, 0)} preguntas, mínimo {minimo}"
               for o in objetivos if por_objetivo.get(o, 0) < minimo]
    errores += [f"{pref}: repaso: {p.get('id')} declara el objetivo {p.get('objetivo')}, que no está en fuentes/{fichero}"
                for p in repaso if p.get("objetivo") not in objetivos]
    return errores


def comprobar(raiz: Path, cursos=None, modulo=None, con_preguntas=False):
    manifiestos, errores = descubrir(raiz / "cursos", raiz / "schemas")
    if cursos:
        faltan = [c for c in cursos if c not in manifiestos]
        manifiestos = {k: v for k, v in manifiestos.items() if k in cursos}
        errores = [e for e in errores if any(e.startswith(f"{c}:") for c in cursos)] + [f"curso '{c}' no encontrado o inválido" for c in faltan]
    resumen, comprobados = [], 0
    for curso in manifiestos.values():
        for mod, fichero in curso.cobertura.items():
            if modulo and not mod.startswith(modulo):
                continue
            e, r, hecho = comprobar_modulo(curso, mod, fichero, con_preguntas, explicito=bool(modulo))
            errores += e
            resumen += r
            comprobados += hecho
    if modulo and not comprobados and not errores:
        errores.append(f"módulo '{modulo}' no encontrado en el bloque `cobertura` de los cursos indicados")
    return errores, resumen


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", type=Path, default=RAIZ)
    ap.add_argument("--curso", action="append", help="slug del curso (repetible); por defecto, todos")
    ap.add_argument("--modulo", help="prefijo del módulo, p. ej. 01 (si se indica, se exige que tenga mapa)")
    ap.add_argument("--preguntas", action="store_true", help="comprobar también preguntas por tarea y por objetivo")
    a = ap.parse_args(argv)
    errores, resumen = comprobar(a.raiz, a.curso, a.modulo, a.preguntas)
    for r in resumen:
        print(r)
    if not resumen and not errores:
        print("No hay módulos con mapa de cobertura todavía.")
    for e in errores:
        print(f"ERROR {e}", file=sys.stderr)
    if errores:
        print(f"{len(errores)} error(es).", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
