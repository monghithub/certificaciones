#!/usr/bin/env python3
"""Genera cursos/<curso>/glosario.md a partir de cursos/<curso>/glosario.yaml (la fuente de verdad).

El Markdown ordena los términos alfabéticamente, con sus alias (en inglés y en español), categoría, definición,
cuándo usarlo o no y la referencia oficial. Con --comprobar no escribe nada y falla si algún glosario.md no
coincide con el que se generaría (lo usa la CI).
"""
import argparse
import sys
import unicodedata
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent

CATEGORIAS = {"servicio": "Servicio", "concepto": "Concepto", "tecnica": "Técnica", "metrica": "Métrica"}


PREFIJOS = ("amazon ", "aws ")  # se ignoran al ordenar: «Amazon S3» va con la S


def _clave(texto: str) -> str:
    """Clave de orden: sin tildes, en minúsculas y sin los prefijos de marca de PREFIJOS."""
    clave = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    for prefijo in PREFIJOS:
        if clave.startswith(prefijo):
            return clave[len(prefijo):]
    return clave


def generar(curso: Path) -> str:
    entradas = yaml.safe_load((curso / "glosario.yaml").read_text(encoding="utf8")) or []
    titulo = curso.name
    manifiesto = curso / "curso.yaml"
    if manifiesto.is_file():
        titulo = (yaml.safe_load(manifiesto.read_text(encoding="utf8")) or {}).get("titulo", titulo)
    lineas = [
        f"# Glosario: {titulo}",
        "",
        "Términos del curso en orden alfabético, con sus variantes en inglés y en español. "
        "**Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: "
        "no lo edites a mano; edita el YAML y vuelve a generarlo. Los servicios se ordenan sin los prefijos «Amazon» "
        "y «AWS» (Amazon S3 aparece en la S).",
        "",
        f"Total: {len(entradas)} términos.",
    ]
    letra_actual = None
    for e in sorted(entradas, key=lambda e: _clave(e["termino"])):
        inicial = _clave(e["termino"])[:1].upper()
        letra = inicial if inicial.isalpha() else "#"
        if letra != letra_actual:
            lineas += ["", f"## {letra}", ""]
            letra_actual = letra
        cabecera = f"- **{e['termino']}**"
        if e.get("alias"):
            cabecera += " (" + ", ".join(e["alias"]) + ")"
        cabecera += f". *{CATEGORIAS.get(e['categoria'], e['categoria'])}.* {e['definicion']}"
        lineas.append(cabecera)
        if e.get("usar_cuando"):
            lineas.append(f"  - Usar cuando: {e['usar_cuando']}")
        if e.get("no_usar_cuando"):
            lineas.append(f"  - No usar cuando: {e['no_usar_cuando']}")
        if e.get("referencia"):
            lineas.append(f"  - Referencia: <{e['referencia']}>")
    return "\n".join(lineas) + "\n"


def cursos_con_glosario(raiz: Path, slugs=None) -> list[Path]:
    carpetas = sorted(p.parent for p in (raiz / "cursos").glob("*/glosario.yaml"))
    return [c for c in carpetas if not slugs or c.name in slugs]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", type=Path, default=RAIZ)
    ap.add_argument("--curso", action="append", help="slug del curso (repetible); por defecto, todos")
    ap.add_argument("--comprobar", action="store_true", help="no escribir; fallar si glosario.md está desactualizado")
    a = ap.parse_args(argv)
    desactualizados = []
    cursos = cursos_con_glosario(a.raiz, a.curso)
    faltan = sorted(set(a.curso or []) - {c.name for c in cursos})
    if faltan:
        print(f"ERROR curso no encontrado o sin glosario.yaml: {', '.join(faltan)}", file=sys.stderr)
        return 1
    for curso in cursos:
        destino = curso / "glosario.md"
        texto = generar(curso)
        actual = destino.read_text(encoding="utf8") if destino.is_file() else None
        if a.comprobar:
            if actual != texto:
                desactualizados.append(destino)
        elif actual != texto:
            destino.write_text(texto, encoding="utf8")
            print(f"generado {destino.relative_to(a.raiz)}")
    for d in desactualizados:
        print(f"ERROR {d.relative_to(a.raiz)} no coincide con glosario.yaml: ejecuta python scripts/generar_glosario.py", file=sys.stderr)
    if desactualizados:
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
