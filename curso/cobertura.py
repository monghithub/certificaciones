"""Mapa de cobertura de un README de módulo: tabla cuya primera columna es el id del objetivo (`1.2.3` o `CP.1`)
y que enlaza en alguna celda a encabezados del mismo README (`[texto](#ancla)`)."""
import re

FILA = re.compile(r"^\|\s*((?:[A-Z]+|\d+)(?:\.\d+)+)\s*\|(.*)$")
ENLACE = re.compile(r"\]\(#([^)\s]+)\)")


def mapa(markdown: str) -> dict[str, list[str]]:
    """Objetivo -> anclas que enlaza su fila del mapa de cobertura."""
    filas = {}
    for linea in markdown.splitlines():
        m = FILA.match(linea)
        if m:
            filas[m.group(1)] = ENLACE.findall(m.group(2))
    return filas


def grupo(id_: str) -> str:
    """Tarea a la que pertenece un objetivo: 1.2.3 -> 1.2; CP.1 -> CP."""
    partes = id_.split(".")
    return ".".join(partes[:2]) if partes[0].isdigit() else partes[0]
