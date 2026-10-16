#!/usr/bin/env python3
"""Valida de cada curso: manifiesto, bancos de preguntas (modulos/*/preguntas.yaml), glosario y estilo e información de los diagramas."""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import yaml
from jsonschema import Draft202012Validator

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from curso import diagramas, glosario  # noqa: E402
from curso.manifiesto import Manifiesto, descubrir  # noqa: E402

TOLERANCIA = 10
PROHIBIDAS = re.compile(r"(todas|ninguna)( de)? las anteriores|all of the above|none of the above", re.I)
# Calidad del banco (ver AGENTS.md, «Calidad del banco de preguntas»)
ABSOLUTOS = re.compile(r"\b(siempre|nunca|cualquier[a]?|garantiza[r]?|todos los|todas las)\b", re.I)
MIN_ENUNCIADO = 80          # caracteres: por debajo suele ser una pregunta de definición, no un escenario
MAX_POSICION = 40           # % máximo de respuestas de opción múltiple en una misma letra
MIN_MC_POSICION = 12        # nº de preguntas de opción múltiple a partir del cual se comprueba el reparto


def normalizar(texto: str) -> str:
    """Enunciado en minúsculas, sin signos de puntuación ni espacios repetidos (para detectar copias)."""
    return " ".join(re.sub(r"[^\w\s]", " ", str(texto).lower()).split())


def tareas_oficiales(curso: Manifiesto) -> dict[int, set[str]]:
    resultado = {}
    for n in curso.dominios:
        f = curso.carpeta / "fuentes" / f"dominio-{n}.md"
        if f.exists():
            resultado[n] = set(re.findall(r"^## Task Statement (\d+\.\d+)\s*$", f.read_text(encoding="utf8"), re.M))
    return resultado


def objetivos_oficiales(curso: Manifiesto) -> dict[int, set[str]]:
    resultado = {}
    for n in curso.dominios:
        f = curso.carpeta / "fuentes" / f"dominio-{n}.md"
        if f.exists():
            resultado[n] = set(re.findall(r"\*\*(\d+\.\d+\.\d+)\*\*", f.read_text(encoding="utf8")))
    return resultado


def ids_de(items):
    return [i.get("id") for i in items or []]


def comprobar_pregunta(p: dict, curso: Manifiesto, tareas: dict[int, set[str]], objetivos: dict[int, set[str]] | None = None) -> list[str]:
    objetivos = objetivos or {}
    errs = []
    tipo = p.get("tipo")
    opc = set(ids_de(p.get("opciones")))
    pro = set(ids_de(p.get("prompts")))
    cor = p.get("correctas") or []
    if len(opc) != len(p.get("opciones") or []):
        errs.append("ids de opciones duplicados")
    if len(pro) != len(p.get("prompts") or []):
        errs.append("ids de prompts duplicados")
    if tipo in ("multiple_choice", "multiple_response", "ordering"):
        faltan = [c for c in cor if c not in opc]
        if faltan:
            errs.append(f"correctas referencia opciones inexistentes: {faltan}")
    if tipo == "matching":
        for par in cor:
            if len(par) == 2 and (par[0] not in pro or par[1] not in opc):
                errs.append(f"par inexistente en correctas: {par}")
        if len({par[0] for par in cor if par}) != len(cor):
            errs.append("un prompt aparece en más de un par")
        if pro and {par[0] for par in cor if par} != pro:
            errs.append("todos los prompts deben tener un par en correctas")
    if tipo == "ordering" and len(opc) < len(cor):
        errs.append("ordering: hay menos opciones que elementos en correctas")
    # distractores: toda opción incorrecta debe estar explicada
    if tipo in ("multiple_choice", "multiple_response"):
        incorrectas = opc - set(cor)
    elif tipo == "matching":
        incorrectas = opc - {par[1] for par in cor if len(par) == 2}
    else:
        incorrectas = set()
    dist = set((p.get("distractores") or {}).keys())
    for o in sorted(incorrectas - dist):
        errs.append(f"opción incorrecta '{o}' sin explicación en distractores")
    for o in sorted(dist - incorrectas):
        errs.append(f"distractores incluye '{o}', que no es una opción incorrecta")
    # dominio y tarea oficiales del curso
    d = p.get("dominio")
    t = p.get("tarea")
    if isinstance(d, int) and d not in curso.dominios:
        errs.append(f"dominio {d} no declarado en curso.yaml de {curso.slug}")
    elif isinstance(t, str) and isinstance(d, int):
        if not t.startswith(f"{d}."):
            errs.append(f"tarea '{t}' no pertenece al dominio {d}")
        elif d in tareas and t not in tareas[d]:
            errs.append(f"tarea '{t}' no existe en fuentes/dominio-{d}.md")
        elif d not in tareas:
            errs.append(f"falta fuentes/dominio-{d}.md")
    obj = p.get("objetivo")
    if isinstance(obj, str) and isinstance(d, int):
        if not obj.startswith(f"{d}."):
            errs.append(f"objetivo '{obj}' no pertenece al dominio {d}")
        elif isinstance(t, str) and not obj.startswith(f"{t}."):
            errs.append(f"objetivo '{obj}' no pertenece a la tarea {t}")
        elif d in objetivos and obj not in objetivos[d]:
            errs.append(f"objetivo '{obj}' no existe en fuentes/dominio-{d}.md")
    ref = p.get("referencia")
    if isinstance(ref, str) and curso.fuentes_oficiales and not referencia_oficial(ref, curso.fuentes_oficiales):
        errs.append(f"la referencia {ref} no pertenece a las fuentes oficiales del curso ({', '.join(curso.fuentes_oficiales)})")
    textos = [p.get("enunciado", "")] + [o.get("texto", "") for o in p.get("opciones") or []]
    if any(PROHIBIDAS.search(x) for x in textos):
        errs.append("contiene 'todas/ninguna de las anteriores'")
    opciones_txt = [str(o.get("texto", "")).strip().lower() for o in p.get("opciones") or []]
    if len(set(opciones_txt)) != len(opciones_txt):
        errs.append("hay opciones con el mismo texto")
    return errs


def referencia_oficial(url: str, hosts: tuple[str, ...]) -> bool:
    """True si el host de `url` es uno de `hosts` o un subdominio suyo."""
    host = (urlparse(url).hostname or "").lower()
    return any(host == h or host.endswith("." + h) for h in hosts)


def avisos_calidad(p: dict) -> list[str]:
    """Heurísticas de calidad que no bloquean: pistas en los distractores y enunciados de definición."""
    avisos = []
    tipo = p.get("tipo")
    if tipo in ("multiple_choice", "multiple_response"):
        cor = set(p.get("correctas") or [])
        absolutas = [o["id"] for o in p.get("opciones") or [] if o.get("id") not in cor and ABSOLUTOS.search(str(o.get("texto", "")))]
        if absolutas:
            avisos.append(f"distractores con términos absolutos que delatan la respuesta: {absolutas}")
        if len(str(p.get("enunciado", ""))) < MIN_ENUNCIADO:
            avisos.append("enunciado muy corto: plantéalo como un escenario de negocio")
    return avisos


def _validar_curso(raiz: Path, curso: Manifiesto, validador, minimos: bool):
    errores, avisos, resumen = [], [], {}
    tareas = tareas_oficiales(curso)
    objetivos = objetivos_oficiales(curso)
    ids_vistos: dict[str, str] = {}
    enunciados_modulos: dict[str, str] = {}   # enunciado normalizado -> id (bancos de los módulos)
    enunciados_simulacro: list[tuple[str, str, str]] = []  # (fichero, id, enunciado normalizado)
    if curso.simulacro and not (curso.carpeta / "modulos" / curso.simulacro).is_dir():
        errores.append(f"{curso.slug}: el módulo de simulacro '{curso.simulacro}' no existe")
    for f in sorted((curso.carpeta / "modulos").glob("*/preguntas.yaml")):
        rel = f.relative_to(raiz)
        try:
            datos = yaml.safe_load(f.read_text(encoding="utf8")) or []
        except yaml.YAMLError as e:
            errores.append(f"{rel}: YAML inválido: {e}")
            continue
        if not isinstance(datos, list):
            errores.append(f"{rel}: se esperaba una lista de preguntas")
            continue
        for i, p in enumerate(datos):
            pid = p.get("id", f"#{i}") if isinstance(p, dict) else f"#{i}"
            for e in sorted(validador.iter_errors(p), key=lambda e: list(map(str, e.path))):
                ruta = "/".join(map(str, e.path)) or "(raíz)"
                errores.append(f"{rel}:{pid}: esquema [{ruta}]: {e.message}")
            if not isinstance(p, dict):
                continue
            errores += [f"{rel}:{pid}: {m}" for m in comprobar_pregunta(p, curso, tareas, objetivos)]
            avisos += [f"{rel}:{pid}: {m}" for m in avisos_calidad(p)]
            if pid in ids_vistos:
                errores.append(f"{rel}:{pid}: id duplicado (también en {ids_vistos[pid]})")
            ids_vistos[pid] = str(rel)
            if p.get("enunciado"):
                if f.parent.name == curso.simulacro:
                    enunciados_simulacro.append((str(rel), pid, normalizar(p["enunciado"])))
                else:
                    enunciados_modulos.setdefault(normalizar(p["enunciado"]), pid)
        tipos = Counter(p.get("tipo") for p in datos if isinstance(p, dict))
        posiciones = Counter((p.get("correctas") or [None])[0] for p in datos
                             if isinstance(p, dict) and p.get("tipo") == "multiple_choice")
        n_mc = sum(posiciones.values())
        if n_mc >= MIN_MC_POSICION:
            letra, veces = posiciones.most_common(1)[0]
            if 100 * veces / n_mc > MAX_POSICION:
                errores.append(f"{rel}: la respuesta correcta de opción múltiple es «{letra}» en el "
                               f"{100 * veces / n_mc:.0f} % de las preguntas (máximo {MAX_POSICION} %): reparte las posiciones")
        resumen[str(rel)] = (len(datos), tipos)
        n = len(datos)
        es_simulacro = f.parent.name == curso.simulacro
        exigido = curso.minimo_simulacro if es_simulacro else curso.minimo_por_modulo
        if minimos and n and exigido and n < exigido:
            errores.append(f"{rel}: {n} preguntas, mínimo {exigido}")
        if n and exigido and n >= exigido:
            for t, obj in curso.distribucion.items():
                real = 100 * tipos.get(t, 0) / n
                if abs(real - obj) > TOLERANCIA:
                    avisos.append(f"{rel}: {t} es el {real:.0f} % (objetivo ~{obj:g} %)")
    for rel, pid, texto in enunciados_simulacro:
        if texto in enunciados_modulos:
            errores.append(f"{rel}:{pid}: el simulacro debe ser inédito y repite el enunciado de {enunciados_modulos[texto]}")
    return errores, avisos, resumen


def validar(raiz: Path, minimos: bool = True, cursos: list[str] | None = None):
    """Valida los cursos de raiz/cursos (o solo los indicados). Devuelve (errores, avisos, resumen)."""
    raiz = Path(raiz)
    validador = Draft202012Validator(json.loads((raiz / "schemas" / "pregunta.schema.json").read_text(encoding="utf8")))
    manifiestos, errores = descubrir(raiz / "cursos", raiz / "schemas")
    avisos, resumen = [], {}
    if cursos is not None:
        faltan = [c for c in cursos if c not in manifiestos]
        errores = [e for e in errores if any(e.startswith(f"{c}:") for c in cursos)]
        errores += [f"curso '{c}' no encontrado o inválido" for c in faltan if not any(e.startswith(f"{c}:") for e in errores)]
        manifiestos = {k: v for k, v in manifiestos.items() if k in cursos}
    for curso in manifiestos.values():
        e, a, r = _validar_curso(raiz, curso, validador, minimos)
        errores += e + glosario.validar(curso.carpeta, raiz / "schemas") + diagramas.validar(curso.carpeta, raiz / "schemas")
        avisos += a
        resumen.update(r)
    return errores, avisos, resumen


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raiz", type=Path, default=RAIZ, help="raíz del repositorio")
    ap.add_argument("--curso", action="append", help="slug del curso a validar (repetible); por defecto, todos")
    ap.add_argument("--sin-minimos", action="store_true", help="no exigir nº mínimo de preguntas")
    a = ap.parse_args(argv)
    errores, avisos, resumen = validar(a.raiz, minimos=not a.sin_minimos, cursos=a.curso)
    for r, (n, tipos) in resumen.items():
        print(f"{r}: {n} preguntas {dict(tipos)}")
    if not resumen:
        print("No hay bancos de preguntas todavía.")
    for w in avisos:
        print(f"AVISO {w}")
    for e in errores:
        print(f"ERROR {e}", file=sys.stderr)
    if errores:
        print(f"{len(errores)} error(es).", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
