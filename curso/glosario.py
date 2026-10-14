"""Glosario de curso (cursos/<curso>/glosario.yaml): carga, validación y búsqueda de términos en el texto."""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from .manifiesto import RAIZ_REPO

CATEGORIAS = ("servicio", "concepto", "tecnica", "metrica")


@dataclass(frozen=True)
class Entrada:
    id: str
    termino: str
    categoria: str
    definicion: str
    alias: tuple[str, ...] = ()
    usar_cuando: str | None = None
    no_usar_cuando: str | None = None
    referencia: str | None = None
    enlaces: tuple[tuple[str, str], ...] = ()  # (texto, url) adicionales a `referencia`

    @property
    def nombres(self) -> tuple[str, ...]:
        return (self.termino, *self.alias)

    def a_json(self) -> dict:
        """Información para el modal: la misma estructura sirve para conceptos y para cajas de diagrama."""
        enlaces = ([{"texto": "Documentación oficial", "url": self.referencia}] if self.referencia else []) + \
                  [{"texto": t, "url": u} for t, u in self.enlaces]
        return {k: v for k, v in {
            "titulo": self.termino, "categoria": self.categoria, "texto": self.definicion,
            "usar_cuando": self.usar_cuando, "no_usar_cuando": self.no_usar_cuando, "enlaces": enlaces}.items() if v}


def _sensible(nombre: str) -> bool:
    """Siglas y términos cortos distinguen mayúsculas para evitar falsos positivos (RAG frente a «drag»)."""
    return nombre == nombre.upper() or len(nombre) <= 5


class Glosario:
    def __init__(self, entradas: list[Entrada]):
        self.entradas = {e.id: e for e in entradas}
        self._por_nombre = {n.lower(): e.id for e in entradas for n in e.nombres}
        nombres = sorted({n for e in entradas for n in e.nombres}, key=len, reverse=True)
        partes = [re.escape(n) if _sensible(n) else f"(?i:{re.escape(n)})" for n in nombres]
        self._regex = re.compile(r"(?<!\w)(?:" + "|".join(partes) + r")(?!\w)") if partes else None

    def __len__(self):
        return len(self.entradas)

    def __iter__(self):
        return iter(sorted(self.entradas.values(), key=lambda e: e.termino.lower()))

    def buscar(self, texto: str):
        """Coincidencias no solapadas, de izquierda a derecha y prefiriendo el término más largo: (inicio, fin, id)."""
        if not self._regex:
            return []
        return [(m.start(), m.end(), self._por_nombre[m.group(0).lower()]) for m in self._regex.finditer(texto)]

    def id_de(self, nombre: str) -> str | None:
        return self._por_nombre.get(nombre.strip().lower())


def _esquema(esquemas: Path | None) -> Draft202012Validator:
    ruta = (esquemas or RAIZ_REPO / "schemas") / "glosario.schema.json"
    return Draft202012Validator(json.loads(ruta.read_text(encoding="utf8")))


def leer(carpeta: Path, esquemas: Path | None = None) -> tuple[Glosario | None, list[str]]:
    """Lee carpeta/glosario.yaml. Devuelve (glosario o None si no existe o es inválido, errores)."""
    f = Path(carpeta) / "glosario.yaml"
    if not f.is_file():
        return None, []
    pref = f"{Path(carpeta).name}/glosario.yaml"
    try:
        datos = yaml.safe_load(f.read_text(encoding="utf8")) or []
    except yaml.YAMLError as e:
        return None, [f"{pref}: YAML inválido ({e})"]
    errores = [f"{pref}: [{'/'.join(map(str, e.path)) or '(raíz)'}] {e.message}"
               for e in sorted(_esquema(esquemas).iter_errors(datos), key=lambda e: list(map(str, e.path)))]
    if errores:
        return None, errores
    vistos_id: set[str] = set()
    nombres: dict[str, str] = {}
    entradas = []
    for d in datos:
        if d["id"] in vistos_id:
            errores.append(f"{pref}: id duplicado «{d['id']}»")
        vistos_id.add(d["id"])
        e = Entrada(id=d["id"], termino=d["termino"], categoria=d["categoria"], definicion=d["definicion"].strip(),
                    alias=tuple(d.get("alias") or ()), usar_cuando=d.get("usar_cuando"),
                    no_usar_cuando=d.get("no_usar_cuando"), referencia=d.get("referencia"),
                    enlaces=tuple((l["texto"], l["url"]) for l in d.get("enlaces") or ()))
        for n in e.nombres:
            previo = nombres.get(n.lower())
            if previo and previo != e.id:
                errores.append(f"{pref}: «{n}» está en «{previo}» y en «{e.id}»")
            nombres[n.lower()] = e.id
        entradas.append(e)
    return (None if errores else Glosario(entradas)), errores


_LIMPIEZA = [(re.compile(r"\[([^\]]*)\]\([^)]*\)"), r"\1"), (re.compile(r"[*_`]"), ""), (re.compile(r"<[^>]+>"), "")]


def servicios_de(texto: str) -> list[str]:
    """Primera columna de las filas de datos de las tablas Markdown de un servicios.md."""
    resultado, enc, en_tabla = [], False, False
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        s = linea.strip()
        if not s.startswith("|"):
            en_tabla = False
            continue
        celdas = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in celdas if c):
            en_tabla = True  # la fila anterior era la cabecera
            continue
        siguiente = lineas[i + 1].strip() if i + 1 < len(lineas) else ""
        if siguiente.startswith("|") and re.fullmatch(r"[|\s:\-]+", siguiente):
            continue  # cabecera
        if en_tabla and celdas and celdas[0]:
            nombre = celdas[0]
            for patron, sust in _LIMPIEZA:
                nombre = patron.sub(sust, nombre)
            resultado.append(nombre.strip())
    return resultado


def validar(carpeta: Path, esquemas: Path | None = None) -> list[str]:
    """Errores del glosario de un curso y de su cobertura de servicios. Sin glosario no hay errores."""
    carpeta = Path(carpeta)
    glosario, errores = leer(carpeta, esquemas)
    if glosario is None:
        return errores
    for e in glosario:
        if e.referencia and not e.referencia.startswith("https://"):
            errores.append(f"{carpeta.name}/glosario.yaml: «{e.id}» tiene una referencia que no es https")
    for f in sorted((carpeta / "modulos").glob("*/servicios.md")):
        for nombre in servicios_de(f.read_text(encoding="utf8")):
            if glosario.id_de(nombre) is None:
                errores.append(f"{carpeta.name}/modulos/{f.parent.name}/servicios.md: «{nombre}» no tiene entrada en el glosario")
    return errores
