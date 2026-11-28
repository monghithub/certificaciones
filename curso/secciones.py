"""Secciones de un módulo y el fichero Markdown de cada una."""
from pathlib import Path

# Secciones clásicas (archivos directos en el módulo)
SECCIONES_CLASICAS = (
    ("teoria", "README.md", "Teoría"),
    ("servicios", "servicios.md", "Servicios"),
    ("trampas", "trampas.md", "Trampas habituales"),
    ("laboratorio", "laboratorio.md", "Laboratorio"),
)
FICHERO_DE = {id_: fichero for id_, fichero, _ in SECCIONES_CLASICAS}

def detectar_secciones(modulo_path: Path):
    """Detecta secciones: clásicas (README.md, etc) o modernas (subcarpetas con README.md)."""
    secciones = []

    # Primero, secciones clásicas
    for id_, fichero, titulo in SECCIONES_CLASICAS:
        ruta = modulo_path / fichero
        if ruta.is_file():
            secciones.append((id_, fichero, titulo))

    # Si no hay secciones clásicas, buscar subcarpetas con README.md
    if not secciones:
        for item in sorted(modulo_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                readme = item / "README.md"
                if readme.is_file():
                    # Usar nombre de carpeta como id,
                    # README.md como archivo relativo,
                    # nombre formateado como título
                    id_ = item.name
                    titulo = item.name.replace("-", " ").title()
                    secciones.append((id_, f"{item.name}/README.md", titulo))

    return tuple(secciones) if secciones else SECCIONES_CLASICAS

SECCIONES = SECCIONES_CLASICAS  # Mantener compatibilidad
