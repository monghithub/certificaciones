#!/usr/bin/env python3
"""Cuestionario interactivo en terminal a partir de cursos/<curso>/modulos/*/preguntas.yaml."""
import argparse
import random
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from curso.correccion import corregir  # noqa: E402
from curso.manifiesto import descubrir  # noqa: E402


def cargar(raiz: Path, curso: str, modulo=None, dominio=None, tipo=None) -> list[dict]:
    preguntas = []
    for f in sorted((raiz / "cursos" / curso / "modulos").glob("*/preguntas.yaml")):
        if modulo and not f.parent.name.startswith(modulo):
            continue
        preguntas += yaml.safe_load(f.read_text(encoding="utf8")) or []
    return [p for p in preguntas if (dominio is None or p["dominio"] == dominio) and (tipo is None or p["tipo"] == tipo)]


def parsear(p: dict, texto: str):
    """Convierte la entrada del usuario en respuesta. Lanza ValueError si el formato es inválido."""
    texto = texto.strip().lower()
    if not texto:
        raise ValueError("respuesta vacía")
    if p["tipo"] == "matching":
        pares = []
        for trozo in texto.replace(";", ",").split(","):
            a, sep, b = trozo.strip().partition("=")
            if not sep or not a.strip() or not b.strip():
                raise ValueError("usa el formato 1=a,2=b,3=c")
            pares.append([a.strip(), b.strip()])
        return pares
    elementos = [x for x in texto.replace(" ", ",").split(",") if x] if ("," in texto or " " in texto) else list(texto)
    if p["tipo"] == "multiple_choice" and len(elementos) != 1:
        raise ValueError("elige una sola opción")
    return elementos


def mostrar(p: dict, n: int, total: int):
    print(f"\n[{n}/{total}] {p['id']} · Tarea {p['tarea']} · {p['tipo']}")
    print(p["enunciado"].strip())
    if p["tipo"] == "matching":
        print("Elementos:")
        for x in p["prompts"]:
            print(f"  {x['id']}) {x['texto']}")
        print("Opciones:")
    for o in p["opciones"]:
        print(f"  {o['id']}) {o['texto']}")
    ayuda = {"multiple_choice": "una letra", "multiple_response": "letras, p. ej. a,c",
             "ordering": "secuencia, p. ej. c,a,b", "matching": "pares, p. ej. 1=b,2=a,3=c"}
    print(f"Respuesta ({ayuda[p['tipo']]}): ", end="")


def retroalimentacion(p: dict, ok: bool):
    print("✔ Correcto" if ok else f"✘ Incorrecto. Solución: {p['correctas']}")
    print(p["explicacion"].strip())
    for k, v in (p.get("distractores") or {}).items():
        print(f"  - {k}: {v}")
    print(f"Referencia: {p['referencia']}")


def main(argv=None, entrada=input):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raiz", type=Path, default=RAIZ)
    ap.add_argument("--curso", help="slug del curso (opcional si solo hay uno)")
    ap.add_argument("--modulo", help="prefijo del módulo, p. ej. 03")
    ap.add_argument("--dominio", type=int)
    ap.add_argument("--tipo", choices=["multiple_choice", "multiple_response", "ordering", "matching"])
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--semilla", type=int)
    a = ap.parse_args(argv)
    cursos, _ = descubrir(a.raiz / "cursos", a.raiz / "schemas")
    curso = a.curso
    if curso is None:
        if len(cursos) != 1:
            print("Indica el curso con --curso. Disponibles: " + (", ".join(cursos) or "ninguno"), file=sys.stderr)
            return 2
        curso = next(iter(cursos))
    elif curso not in cursos:
        print(f"Curso '{curso}' no encontrado. Disponibles: " + (", ".join(cursos) or "ninguno"), file=sys.stderr)
        return 2
    pool = cargar(a.raiz, curso, a.modulo, a.dominio, a.tipo)
    if not pool:
        print("No hay preguntas que cumplan el filtro.", file=sys.stderr)
        return 1
    rnd = random.Random(a.semilla)
    sel = rnd.sample(pool, min(a.n, len(pool)))
    aciertos = 0
    for i, p in enumerate(sel, 1):
        mostrar(p, i, len(sel))
        while True:
            try:
                r = parsear(p, entrada())
                break
            except ValueError as e:
                print(f"Entrada no válida ({e}): ", end="")
            except EOFError:
                print("\nInterrumpido.")
                return 130
        ok = corregir(p, r)
        aciertos += ok
        retroalimentacion(p, ok)
    print(f"\nResultado: {aciertos}/{len(sel)} ({100 * aciertos // len(sel)} %)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
