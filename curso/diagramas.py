"""Validación de los diagramas Mermaid de un curso: estilo único del proyecto e información en cada caja.

Reglas (ver AGENTS.md):
  * solo `flowchart`; sin `classDef`;
  * la etiqueta de cada nodo y de cada subgrupo empieza por un emoji;
  * cada nodo tiene una clase semántica válida (`class A,B tipo`);
  * justo después del diagrama hay un bloque ```nodos con la información de **cada** nodo y subgrupo.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import glosario as glosario_mod
from .anclas import anclas_de
from .secciones import FICHERO_DE

CLASES = ("ia", "ml", "dl", "gen", "dato", "proceso", "servicio", "accion", "aviso", "decision")
CAMPOS_CAJA = {"concepto", "titulo", "texto", "usar_cuando", "no_usar_cuando", "enlaces", "seccion"}

_FENCE = re.compile(r"^(\s*)(`{3,})\s*([\w-]*)\s*$")
_ABRE = r"(?:\(\[|\[\(|\(\(|\[\[|\{\{|\[|\(|\{)"
_CIERRA = r"(?:\]\)|\)\]|\)\)|\]\]|\}\}|\]|\)|\})"
_NODO = re.compile(rf'(?<![\w|"-])([A-Za-z_][\w-]*)\s*{_ABRE}\s*"([^"]*)"\s*{_CIERRA}')
_SUBGRUPO = re.compile(r'^\s*subgraph\s+([A-Za-z_][\w-]*)\s*\[\s*"([^"]*)"\s*\]\s*$')
_SUBGRUPO_SIN_ETIQUETA = re.compile(r"^\s*subgraph\s+([A-Za-z_][\w-]*)\s*$")
_CLASE = re.compile(r"^\s*class\s+([\w,\s-]+?)\s+([\w-]+)\s*;?\s*$")
_FLECHA = re.compile(r"(?:<?[-=]{2,}[->ox]?|-\.+->?)")
_PALABRAS = {"end", "direction", "subgraph", "class", "flowchart", "graph", "TB", "TD", "BT", "RL", "LR", "style", "linkStyle", "click"}


@dataclass
class Diagrama:
    indice: int
    linea: int
    codigo: str
    info_texto: str | None = None
    errores: list[str] = field(default_factory=list)
    nodos: dict[str, str] = field(default_factory=dict)       # id -> etiqueta
    subgrupos: dict[str, str] = field(default_factory=dict)
    clases: dict[str, str] = field(default_factory=dict)       # id -> clase


def es_emoji(c: str) -> bool:
    o = ord(c)
    return 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or 0x2B00 <= o <= 0x2BFF or 0x2300 <= o <= 0x23FF or 0x2190 <= o <= 0x21FF or o in (0x00A9, 0x00AE, 0x203C, 0x2049, 0x2122, 0x2139)


def _bloques(texto: str):
    """Bloques de código del Markdown: (info, contenido, línea de apertura (1), línea de cierre (1))."""
    resultado, lineas, i = [], texto.splitlines(), 0
    while i < len(lineas):
        m = _FENCE.match(lineas[i])
        if m:
            valla, info, ini, cuerpo = m.group(2), m.group(3), i, []
            i += 1
            while i < len(lineas) and not re.match(rf"^\s*{valla}\s*$", lineas[i]):
                cuerpo.append(lineas[i])
                i += 1
            resultado.append((info, "\n".join(cuerpo), ini + 1, i + 1))
        i += 1
    return resultado


def extraer(texto: str) -> list[Diagrama]:
    """Diagramas Mermaid del documento con su bloque `nodos` si va inmediatamente detrás (solo líneas en blanco entre ambos)."""
    lineas = texto.splitlines()
    bloques = _bloques(texto)
    diagramas = []
    for k, (info, cuerpo, ini, fin) in enumerate(bloques):
        if info != "mermaid":
            continue
        d = Diagrama(indice=len(diagramas) + 1, linea=ini, codigo=cuerpo)
        if k + 1 < len(bloques) and bloques[k + 1][0] == "nodos":
            entre = lineas[fin: bloques[k + 1][2] - 1]
            if all(not l.strip() for l in entre):
                d.info_texto = bloques[k + 1][1]
        _analizar(d)
        diagramas.append(d)
    return diagramas


def _analizar(d: Diagrama):
    lineas = [l for l in d.codigo.splitlines() if l.strip() and not l.strip().startswith("%%")]
    if not lineas:
        d.errores.append("diagrama vacío")
        return
    cabecera = lineas[0].split()[0]
    if cabecera != "flowchart":
        d.errores.append(f"solo se admiten diagramas «flowchart» (este es «{cabecera}»)")
        return
    declarados: set[str] = set()
    for l in lineas[1:]:
        if l.strip().startswith("classDef"):
            d.errores.append("no se permite «classDef»: el color se asigna con «class A,B tipo»")
            continue
        m = _SUBGRUPO.match(l)
        if m:
            d.subgrupos[m.group(1)] = m.group(2)
            continue
        m = _SUBGRUPO_SIN_ETIQUETA.match(l)
        if m:
            d.subgrupos[m.group(1)] = ""
            continue
        m = _CLASE.match(l)
        if m:
            for i in re.split(r"[,\s]+", m.group(1).strip()):
                if i:
                    d.clases[i] = m.group(2)
            continue
        for nid, etiqueta in _NODO.findall(l):
            d.nodos.setdefault(nid, etiqueta)
            declarados.add(nid)
    # nodos citados en una flecha sin haber declarado su etiqueta
    for l in lineas[1:]:
        if not _FLECHA.search(l) or _SUBGRUPO.match(l) or _CLASE.match(l):
            continue
        sin = _NODO.sub(lambda m: m.group(1), l)
        sin = re.sub(r"\|[^|]*\|", " ", sin)
        for parte in _FLECHA.split(sin):
            for nid in re.findall(r"(?<![\w-])[A-Za-z_][\w-]*", parte.replace("&", " ")):
                if nid not in d.nodos and nid not in d.subgrupos and nid not in _PALABRAS:
                    d.nodos.setdefault(nid, "")


def _comprobar_estilo(d: Diagrama):
    for nid, etiqueta in {**d.nodos, **d.subgrupos}.items():
        if not etiqueta:
            d.errores.append(f"«{nid}» no tiene etiqueta entre comillas con emoji (declárala como {nid}[\"🧩 Texto\"])")
        elif not es_emoji(etiqueta.lstrip()[:1] or " "):
            d.errores.append(f"la etiqueta de «{nid}» debe empezar por un emoji («{etiqueta[:30]}»)")
    for nid in d.nodos:
        c = d.clases.get(nid)
        if c is None:
            d.errores.append(f"el nodo «{nid}» no tiene clase semántica (usa «class {nid} {'|'.join(CLASES[:3])}|…»)")
    for nid, c in d.clases.items():
        if nid not in d.nodos and nid not in d.subgrupos:
            d.errores.append(f"«class» se aplica a «{nid}», que no existe en el diagrama")
        elif c not in CLASES:
            d.errores.append(f"clase «{c}» no válida para «{nid}» (permitidas: {', '.join(CLASES)})")


def _url_https(u) -> bool:
    return isinstance(u, str) and re.fullmatch(r"https://\S+", u) is not None


def _comprobar_info(d: Diagrama, glos, carpeta: Path):
    cajas = {**d.nodos, **d.subgrupos}
    if not cajas:
        return
    if d.info_texto is None:
        d.errores.append("falta el bloque ```nodos inmediatamente después del diagrama, con la información de cada caja")
        return
    try:
        info = yaml.safe_load(d.info_texto)
    except yaml.YAMLError as e:
        d.errores.append(f"el bloque «nodos» no es YAML válido ({str(e).splitlines()[0]})")
        return
    if not isinstance(info, dict):
        d.errores.append("el bloque «nodos» debe ser un mapa «id: información»")
        return
    for nid in cajas:
        if nid not in info:
            d.errores.append(f"la caja «{nid}» no tiene información en el bloque «nodos»")
    for nid, e in info.items():
        if nid not in cajas:
            d.errores.append(f"«nodos» incluye «{nid}», que no es una caja del diagrama")
            continue
        _comprobar_caja(d, str(nid), e, glos, carpeta)


def _comprobar_caja(d: Diagrama, nid: str, e, glos, carpeta: Path):
    if not isinstance(e, dict):
        d.errores.append(f"la información de «{nid}» debe ser un mapa")
        return
    for k in e:
        if k not in CAMPOS_CAJA:
            d.errores.append(f"«{nid}»: campo desconocido «{k}» (permitidos: {', '.join(sorted(CAMPOS_CAJA))})")
    concepto = e.get("concepto")
    if concepto is not None:
        if glos is None:
            d.errores.append(f"«{nid}»: usa «concepto» pero el curso no tiene glosario")
        elif concepto not in glos.entradas:
            d.errores.append(f"«{nid}»: el concepto «{concepto}» no existe en el glosario")
    elif not (isinstance(e.get("titulo"), str) and e["titulo"].strip() and isinstance(e.get("texto"), str) and e["texto"].strip()):
        d.errores.append(f"«{nid}»: indica «concepto» o bien «titulo» y «texto»")
    enlaces = e.get("enlaces")
    if enlaces is not None:
        if not isinstance(enlaces, list):
            d.errores.append(f"«{nid}»: «enlaces» debe ser una lista")
        else:
            for l in enlaces:
                if not (isinstance(l, dict) and l.get("texto") and _url_https(l.get("url"))):
                    d.errores.append(f"«{nid}»: cada enlace necesita «texto» y una «url» https ({l})")
    if "seccion" in e:
        _comprobar_seccion(d, nid, e["seccion"], carpeta)


def _comprobar_seccion(d: Diagrama, nid: str, destino, carpeta: Path):
    m = re.fullmatch(r"([\w-]+)/([\w-]+)(?:#(.+))?", destino) if isinstance(destino, str) else None
    if not m:
        d.errores.append(f"«{nid}»: «seccion» debe ser «modulo/seccion» o «modulo/seccion#ancla» ({destino})")
        return
    modulo, seccion, ancla = m.groups()
    fichero = FICHERO_DE.get(seccion)
    ruta = carpeta / "modulos" / modulo / fichero if fichero else None
    if not ruta or not ruta.is_file():
        d.errores.append(f"«{nid}»: la sección «{modulo}/{seccion}» no existe")
    elif ancla and ancla not in anclas_de(ruta.read_text(encoding="utf8")):
        d.errores.append(f"«{nid}»: el ancla «#{ancla}» no existe en «{modulo}/{seccion}»")


def validar(carpeta: Path, esquemas: Path | None = None) -> list[str]:
    """Errores de estilo e información de todos los diagramas de los Markdown de un curso."""
    carpeta = Path(carpeta)
    glos, _ = glosario_mod.leer(carpeta, esquemas)
    errores = []
    for f in sorted(carpeta.rglob("*.md")):
        texto = f.read_text(encoding="utf8")
        if "```mermaid" not in texto:
            continue
        for d in extraer(texto):
            if not any("solo se admiten" in e for e in d.errores):  # otro tipo de diagrama: ya no se analiza más
                _comprobar_estilo(d)
                _comprobar_info(d, glos, carpeta)
            rel = f.relative_to(carpeta.parent)
            errores += [f"{rel}: diagrama {d.indice} (línea {d.linea}): {e}" for e in d.errores]
    return errores
