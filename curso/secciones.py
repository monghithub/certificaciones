"""Secciones de un módulo y el fichero Markdown de cada una."""

SECCIONES = (
    ("teoria", "README.md", "Teoría"),
    ("servicios", "servicios.md", "Servicios"),
    ("trampas", "trampas.md", "Trampas habituales"),
    ("laboratorio", "laboratorio.md", "Laboratorio"),
)
FICHERO_DE = {id_: fichero for id_, fichero, _ in SECCIONES}
