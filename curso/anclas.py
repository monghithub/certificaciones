"""Anclas de encabezados Markdown con el mismo formato que GitHub (minúsculas, sin signos, espacios como guiones)."""
import re
from collections import Counter

ENCABEZADO = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_ENLACE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_FORMATO = re.compile(r"[*~`]")


def ancla(texto: str) -> str:
    t = _FORMATO.sub("", _ENLACE.sub(r"\1", texto)).strip().lower()
    t = re.sub(r"[^\w\s-]", "", t, flags=re.UNICODE)
    return re.sub(r"\s", "-", t)


class GeneradorAnclas:
    """Genera anclas únicas dentro de un documento: la repetida lleva el sufijo -1, -2…"""

    def __init__(self):
        self._vistas: Counter = Counter()

    def unica(self, texto: str) -> str:
        base = ancla(texto)
        n = self._vistas[base]
        self._vistas[base] += 1
        return base if n == 0 else f"{base}-{n}"


def anclas_de(markdown: str) -> set[str]:
    gen, resultado, en_codigo = GeneradorAnclas(), set(), False
    for linea in markdown.splitlines():
        if linea.lstrip().startswith("```"):
            en_codigo = not en_codigo
        m = None if en_codigo else ENCABEZADO.match(linea)
        if m:
            resultado.add(gen.unica(m.group(2)))
    return resultado
