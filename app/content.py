"""Carga del contenido del curso desde el sistema de ficheros (única fuente de verdad)."""
import json
import logging
import re
from urllib.parse import quote
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from markdown_it import MarkdownIt

from curso import glosario as glosario_mod
from curso.anclas import GeneradorAnclas
from curso.cobertura import mapa as mapa_cobertura
from curso.secciones import SECCIONES
from curso.manifiesto import Manifiesto

log = logging.getLogger(__name__)

MODULO_RE = re.compile(r"^(\d{2})-[a-z0-9-]+$")


@dataclass
class Seccion:
    id: str
    titulo: str
    ruta: Path


@dataclass
class Modulo:
    id: str
    numero: str
    titulo: str
    secciones: list[Seccion] = field(default_factory=list)
    preguntas: list[str] = field(default_factory=list)  # banco de examen (preguntas.yaml)
    repaso: list[str] = field(default_factory=list)  # banco de repaso de conocimientos (repaso.yaml)
    es_simulacro: bool = False


def _boton_concepto(texto: str, id_: str) -> str:
    return f'<button type="button" class="concepto" data-concepto="{_escapar(id_)}">{_escapar(texto)}</button>'


def _md(contenido: "Contenido | None" = None) -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table")

    def fence(_renderer, tokens, idx, options, env):
        tok = tokens[idx]
        if tok.info.strip() == "mermaid":
            n = env.get("n_diagramas", 0)
            env["n_diagramas"] = n + 1
            return f'<figure class="diagrama" data-diagrama="{n}"><pre class="mermaid">{_escapar(tok.content)}</pre></figure>\n'
        if tok.info.strip() == "nodos":  # información de las cajas del diagrama anterior: se consume, no se muestra
            n = env.get("n_diagramas", 0) - 1
            if n >= 0:
                try:
                    datos = yaml.safe_load(tok.content)
                except yaml.YAMLError:
                    datos = None
                if isinstance(datos, dict):
                    env.setdefault("nodos", {})[n] = datos
            return ""
        lang = tok.info.strip().split(" ")[0]
        clase = f' class="language-{_escapar(lang)}"' if lang else ""
        return f"<pre><code{clase}>{_escapar(tok.content)}</code></pre>\n"

    md.add_render_rule("fence", fence)

    def conceptos(state):
        g = contenido.glosario if contenido else None
        if g is None:
            return
        usados = state.env.setdefault("conceptos", set())
        vistos: set[str] = set()  # primera aparición de cada concepto en cada apartado
        en_encabezado = False
        for tok in state.tokens:
            if tok.type == "heading_open":
                vistos.clear()
                en_encabezado = True
            elif tok.type == "heading_close":
                en_encabezado = False
            elif tok.type == "inline" and not en_encabezado and tok.children:
                nuevos, en_enlace = [], 0
                for hijo in tok.children:
                    if hijo.type == "link_open":
                        en_enlace += 1
                    elif hijo.type == "link_close":
                        en_enlace -= 1
                    if hijo.type == "text" and not en_enlace:
                        nuevos.extend(_marcar(state, hijo.content, g.buscar(hijo.content), vistos, usados))
                    else:
                        nuevos.append(hijo)
                tok.children = nuevos

    md.core.ruler.after("inline", "conceptos", conceptos)

    def ids_de_encabezados(state):
        """Pone un id a cada encabezado (formato GitHub) para que funcionen los enlaces #ancla."""
        gen = GeneradorAnclas()
        toks = state.tokens
        for i, tok in enumerate(toks):
            if tok.type == "heading_open" and i + 1 < len(toks) and toks[i + 1].type == "inline":
                texto = "".join(h.content for h in toks[i + 1].children or [] if h.type in ("text", "code_inline"))
                tok.attrSet("id", gen.unica(texto))

    md.core.ruler.before("conceptos", "ids_encabezados", ids_de_encabezados)
    return md


def _marcar(state, texto: str, coincidencias, vistos: set[str], usados: set[str]):
    """Parte un texto en tokens `text` y botones de concepto (solo la primera aparición de cada concepto)."""
    from markdown_it.token import Token
    salida, cursor = [], 0

    def texto_plano(s):
        if s:
            tk = Token("text", "", 0)
            tk.content = s
            salida.append(tk)

    for ini, fin, id_ in coincidencias:
        if id_ in vistos:
            continue
        vistos.add(id_)
        usados.add(id_)
        texto_plano(texto[cursor:ini])
        tk = Token("html_inline", "", 0)
        tk.content = _boton_concepto(texto[ini:fin], id_)
        salida.append(tk)
        cursor = fin
    texto_plano(texto[cursor:])
    return salida or [_texto(texto)]


def _texto(s: str):
    from markdown_it.token import Token
    tk = Token("text", "", 0)
    tk.content = s
    return tk


def _escapar(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


class Contenido:
    """Contenido de un curso: módulos, secciones y preguntas validadas."""

    def __init__(self, manifiesto: Manifiesto, esquemas: Path):
        self.manifiesto = manifiesto
        self.raiz = manifiesto.carpeta
        self.esquemas = Path(esquemas)
        self.modulos: dict[str, Modulo] = {}
        self.preguntas: dict[str, dict] = {}  # todas, de examen y de repaso; p["banco"] dice de cuál
        self.teoria: dict[str, tuple[str, str]] = {}  # objetivo -> (módulo, ancla) según los mapas de cobertura
        self.avisos: list[str] = []
        self.glosario: glosario_mod.Glosario | None = None
        self._md = _md(self)
        self._html: dict[tuple[str, str], tuple[str, set[str]]] = {}
        self.cargar()

    def cargar(self):
        self.modulos, self.preguntas, self.teoria, self.avisos, self._html = {}, {}, {}, [], {}
        self.glosario, errores = glosario_mod.leer(self.raiz, self.esquemas)
        self.avisos += errores
        esquema = self.esquemas / "pregunta.schema.json"
        validador = Draft202012Validator(json.loads(esquema.read_text(encoding="utf8"))) if esquema.exists() else None
        base = self.raiz / "modulos"
        for d in sorted(base.iterdir()) if base.is_dir() else []:
            m = MODULO_RE.match(d.name)
            if not d.is_dir() or not m:
                continue
            titulo = d.name[3:].replace("-", " ").capitalize()
            readme = d / "README.md"
            if readme.exists():
                texto = readme.read_text(encoding="utf8")
                for objetivo, anclas in mapa_cobertura(texto).items():
                    if anclas:
                        self.teoria.setdefault(objetivo, (d.name, anclas[0]))
                for linea in texto.splitlines():
                    if linea.startswith("# "):
                        titulo = linea[2:].strip()
                        break
            mod = Modulo(d.name, m.group(1), titulo, es_simulacro=d.name == self.manifiesto.simulacro)
            mod.secciones = [Seccion(i, t, d / f) for i, f, t in SECCIONES if (d / f).is_file()]
            self.modulos[mod.id] = mod
            self._cargar_preguntas(d, mod, validador)
            if not mod.es_simulacro:
                self._cargar_preguntas(d, mod, validador, repaso=True)

    def _cargar_preguntas(self, d: Path, mod: Modulo, validador, repaso: bool = False):
        f = d / ("repaso.yaml" if repaso else "preguntas.yaml")
        if not f.is_file():
            return
        try:
            datos = yaml.safe_load(f.read_text(encoding="utf8")) or []
        except yaml.YAMLError as e:
            self.avisos.append(f"{mod.id}: YAML inválido ({e})")
            return
        for p in datos if isinstance(datos, list) else []:
            if not isinstance(p, dict) or "id" not in p:
                self.avisos.append(f"{mod.id}: pregunta sin id ignorada")
                continue
            errs = list(validador.iter_errors(p)) if validador else []
            if errs:
                self.avisos.append(f"{mod.id}:{p['id']}: no cumple el esquema ({errs[0].message})")
                continue
            if p["dominio"] not in self.manifiesto.dominios and not (repaso and p["dominio"] == 0 and self.manifiesto.previos):
                self.avisos.append(f"{mod.id}:{p['id']}: dominio {p['dominio']} no declarado en curso.yaml, ignorada")
                continue
            if p["id"] in self.preguntas:
                self.avisos.append(f"{mod.id}:{p['id']}: id duplicado, ignorada")
                continue
            p["modulo"] = mod.id
            p["banco"] = "repaso" if repaso else "examen"
            self.preguntas[p["id"]] = p
            (mod.repaso if repaso else mod.preguntas).append(p["id"])

    def url_teoria(self, objetivo: str | None) -> str | None:
        """Sección de teoría que cubre un objetivo, según el mapa de cobertura de los README."""
        destino = self.teoria.get(objetivo or "")
        return self._url_seccion(f"{destino[0]}/teoria#{destino[1]}") if destino else None

    def _url_seccion(self, destino: str) -> str | None:
        """`modulo/seccion#ancla` -> URL interna del curso, o None si el módulo o la sección no existen."""
        ruta, _, ancla = destino.partition("#")
        modulo, _, seccion = ruta.partition("/")
        mod = self.modulos.get(modulo)
        if not mod or not any(s.id == seccion for s in mod.secciones):
            return None
        return f"/c/{self.manifiesto.slug}/modulo/{modulo}/{seccion}" + (f"#{quote(ancla, safe='-_')}" if ancla else "")

    def info_caja(self, entrada) -> dict | None:
        """Información de una caja de diagrama: parte del concepto del glosario (si lo hay) y la completan o sustituyen sus propios datos."""
        if not isinstance(entrada, dict):
            return None
        info: dict = {}
        if self.glosario and isinstance(entrada.get("concepto"), str) and entrada["concepto"] in self.glosario.entradas:
            info = self.glosario.entradas[entrada["concepto"]].a_json()
        for origen, destino in (("titulo", "titulo"), ("texto", "texto"), ("usar_cuando", "usar_cuando"), ("no_usar_cuando", "no_usar_cuando")):
            if isinstance(entrada.get(origen), str) and entrada[origen].strip():
                info[destino] = entrada[origen].strip()
        enlaces = list(info.get("enlaces", []))
        for e in entrada.get("enlaces") or []:
            if isinstance(e, dict) and isinstance(e.get("url"), str) and e["url"].startswith("https://") and e.get("texto"):
                enlaces.append({"texto": str(e["texto"]), "url": e["url"]})
        if isinstance(entrada.get("seccion"), str) and (url := self._url_seccion(entrada["seccion"])):
            enlaces.append({"texto": "Ver en el curso", "url": url})
        if enlaces:
            info["enlaces"] = enlaces
        return info if info.get("titulo") or info.get("texto") else None

    def seccion(self, modulo: str, seccion: str) -> tuple[str, set[str], dict] | None:
        """HTML de una sección, los ids de los conceptos del glosario que usa y la información de las cajas de sus diagramas."""
        mod = self.modulos.get(modulo)
        sec = next((s for s in mod.secciones if s.id == seccion), None) if mod else None
        if not sec:
            return None
        clave = (modulo, seccion)
        if clave not in self._html:
            env: dict = {}
            html = self._md.render(sec.ruta.read_text(encoding="utf8"), env)
            diagramas = {str(n): {str(k): i for k, v in cajas.items() if (i := self.info_caja(v))}
                         for n, cajas in env.get("nodos", {}).items()}
            self._html[clave] = (html, set(env.get("conceptos", ())), diagramas)
        return self._html[clave]

    def seccion_html(self, modulo: str, seccion: str) -> str | None:
        r = self.seccion(modulo, seccion)
        return r[0] if r else None

    def datos_conceptos(self, ids) -> dict:
        """Datos de los conceptos indicados, listos para incrustar como JSON en la página."""
        if not self.glosario:
            return {}
        return {i: self.glosario.entradas[i].a_json() for i in sorted(ids) if i in self.glosario.entradas}

    def datos_pagina(self, ids, diagramas: dict | None = None) -> dict:
        return {"conceptos": self.datos_conceptos(ids), "diagramas": diagramas or {}}
