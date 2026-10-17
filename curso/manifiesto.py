"""Lectura y validación de manifiestos de curso (cursos/<slug>/curso.yaml)."""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

RAIZ_REPO = Path(__file__).resolve().parent.parent
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")
NOMBRE_PREVIOS = "Conocimientos previos"
TIPOS = ("multiple_choice", "multiple_response", "ordering", "matching")


@dataclass(frozen=True)
class Manifiesto:
    slug: str
    titulo: str
    idioma: str
    carpeta: Path
    proveedor: str | None = None
    fuentes_oficiales: tuple[str, ...] = ()  # hosts aceptados en `referencia` (vacío: cualquier https)
    dominios: dict[int, dict] = field(default_factory=dict)  # id -> {"nombre", "peso"}
    simulacro: str | None = None
    examen_preguntas: int | None = None
    examen_minutos: int | None = None
    minimo_por_modulo: int | None = None
    minimo_simulacro: int | None = None
    minimo_por_tarea: int | None = None
    minimo_por_objetivo: int | None = None
    cobertura: dict[str, str] = field(default_factory=dict)  # módulo -> fichero de fuentes que debe cubrir
    distribucion: dict[str, float] = field(default_factory=dict)
    repaso_minimo_por_modulo: int | None = None
    repaso_minimo_por_objetivo: int | None = None
    previos: str | None = None  # fuente de los conocimientos previos (dominio 0, tarea CP), si el curso los evalúa en el repaso

    @property
    def nombres_dominio(self) -> dict[int, dict]:
        """Dominios del manifiesto más el 0 (conocimientos previos) si el curso lo usa."""
        return ({0: {"nombre": NOMBRE_PREVIOS, "peso": 0}} if self.previos else {}) | self.dominios

    @property
    def tiene_simulacro(self) -> bool:
        return bool(self.simulacro and self.examen_preguntas and self.examen_minutos)


class ManifiestoError(ValueError):
    pass


def _esquema(esquemas: Path | None) -> Draft202012Validator:
    ruta = (esquemas or RAIZ_REPO / "schemas") / "curso.schema.json"
    return Draft202012Validator(json.loads(ruta.read_text(encoding="utf8")))


def cargar_manifiesto(carpeta: Path, esquemas: Path | None = None) -> Manifiesto:
    """Lee y valida carpeta/curso.yaml. Lanza ManifiestoError con un mensaje legible."""
    carpeta = Path(carpeta)
    f = carpeta / "curso.yaml"
    if not f.is_file():
        raise ManifiestoError(f"{carpeta.name}: falta curso.yaml")
    try:
        datos = yaml.safe_load(f.read_text(encoding="utf8"))
    except yaml.YAMLError as e:
        raise ManifiestoError(f"{carpeta.name}: curso.yaml no es YAML válido ({e})") from e
    if not isinstance(datos, dict):
        raise ManifiestoError(f"{carpeta.name}: curso.yaml debe ser un objeto")
    errs = sorted(_esquema(esquemas).iter_errors(datos), key=lambda e: list(map(str, e.path)))
    if errs:
        e = errs[0]
        ruta = "/".join(map(str, e.path)) or "(raíz)"
        raise ManifiestoError(f"{carpeta.name}: curso.yaml [{ruta}]: {e.message}")
    if datos["slug"] != carpeta.name:
        raise ManifiestoError(f"{carpeta.name}: el slug '{datos['slug']}' no coincide con la carpeta")
    ids = [d["id"] for d in datos["dominios"]]
    if len(set(ids)) != len(ids):
        raise ManifiestoError(f"{carpeta.name}: ids de dominio duplicados")
    if abs(sum(d["peso"] for d in datos["dominios"]) - 100) > 1e-6:
        raise ManifiestoError(f"{carpeta.name}: los pesos de los dominios deben sumar 100")
    banco = datos.get("banco") or {}
    examen = datos.get("examen") or {}
    repaso = datos.get("repaso") or {}
    return Manifiesto(
        slug=datos["slug"], titulo=datos["titulo"], idioma=datos["idioma"], carpeta=carpeta,
        proveedor=datos.get("proveedor"), fuentes_oficiales=tuple(datos.get("fuentes_oficiales") or ()),
        dominios={d["id"]: {"nombre": d["nombre"], "peso": d["peso"]} for d in datos["dominios"]},
        simulacro=datos.get("simulacro"), examen_preguntas=examen.get("preguntas"), examen_minutos=examen.get("minutos"),
        minimo_por_modulo=banco.get("minimo_por_modulo"), minimo_simulacro=banco.get("minimo_simulacro"),
        minimo_por_tarea=banco.get("minimo_por_tarea"), minimo_por_objetivo=banco.get("minimo_por_objetivo"),
        cobertura=dict(datos.get("cobertura") or {}),
        distribucion=dict(banco.get("distribucion") or {}),
        repaso_minimo_por_modulo=repaso.get("minimo_por_modulo"), repaso_minimo_por_objetivo=repaso.get("minimo_por_objetivo"),
        previos=repaso.get("previos"),
    )


def descubrir(dir_cursos: Path, esquemas: Path | None = None) -> tuple[dict[str, Manifiesto], list[str]]:
    """Devuelve (cursos válidos por slug, errores). Una carpeta sin curso.yaml se ignora; una con curso.yaml inválido da error."""
    cursos: dict[str, Manifiesto] = {}
    errores: list[str] = []
    dir_cursos = Path(dir_cursos)
    if not dir_cursos.is_dir():
        return cursos, errores
    for d in sorted(p for p in dir_cursos.iterdir() if p.is_dir() and not p.name.startswith(".")):
        if not (d / "curso.yaml").exists():
            continue
        try:
            cursos[d.name] = cargar_manifiesto(d, esquemas)
        except ManifiestoError as e:
            errores.append(str(e))
    return cursos, errores
