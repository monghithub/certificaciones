"""Catálogo de cursos: descubre cursos/<slug>/curso.yaml y carga el contenido de cada uno."""
import logging
from pathlib import Path

from curso.manifiesto import descubrir

from .content import Contenido

log = logging.getLogger(__name__)


class Catalogo:
    def __init__(self, dir_cursos: Path, esquemas: Path):
        self.dir_cursos = Path(dir_cursos)
        self.esquemas = Path(esquemas)
        self.cursos: dict[str, Contenido] = {}
        self.avisos: list[str] = []
        self.cargar()

    def cargar(self):
        manifiestos, errores = descubrir(self.dir_cursos, self.esquemas)
        cursos, avisos = {}, [f"Curso omitido: {e}" for e in errores]
        for slug, m in manifiestos.items():
            try:
                c = Contenido(m, self.esquemas)
            except Exception as e:  # un curso roto no debe impedir el arranque ni afectar a los demás
                avisos.append(f"Curso omitido: {slug}: {e}")
                continue
            cursos[slug] = c
            avisos += [f"{slug}: {a}" for a in c.avisos]
        self.cursos, self.avisos = cursos, avisos
        for a in avisos:
            log.warning("catálogo: %s", a)

    def get(self, slug: str) -> Contenido | None:
        return self.cursos.get(slug)

    def __iter__(self):
        return iter(self.cursos.values())

    def __len__(self):
        return len(self.cursos)
