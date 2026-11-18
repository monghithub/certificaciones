"""Preguntas durante la lectura: una pregunta tipo test del apartado visible, corregida al momento y sin registro."""
import random

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from curso.correccion import corregir as es_correcta

from ..content import Contenido, Modulo
from ..deps import requiere_curso, verificar_csrf
from ..preguntas import leer_respuesta, vista_pregunta
from ..web import legible

router = APIRouter(prefix="/c/{curso}/lectura", dependencies=[Depends(verificar_csrf)])

MAX_ANCLAS = 10
MAX_EXCLUIR = 500


def _modulo(c: Contenido, modulo: str) -> Modulo:
    mod = c.modulos.get(modulo)
    if not mod or mod.es_simulacro or not (mod.repaso or mod.preguntas):
        raise HTTPException(404, "Módulo sin preguntas")
    return mod


def _lista(texto: str, maximo: int) -> list[str]:
    return [x for x in (texto or "").split(",") if x][:maximo]


def elegir(c: Contenido, mod: Modulo, anclas: list[str], excluir: set[str]) -> tuple[str, str | None, bool]:
    """(pregunta, ancla de la que sale o None si sale del módulo, reiniciado).

    Recorre las anclas de la más concreta a la más general; en cada una, primero el repaso y después el examen.
    Si ninguna tiene preguntas sin ver, se toma del módulo; si ya se vieron todas, se vuelve a empezar."""
    bancos = (mod.repaso, mod.preguntas)
    for ancla in anclas:
        objetivos = set(c.objetivos_ancla.get((mod.id, ancla), ()))
        if not objetivos:
            continue
        for banco in bancos:
            libres = [p for p in banco if c.preguntas[p].get("objetivo") in objetivos and p not in excluir]
            if libres:
                return random.choice(libres), ancla, False
    for banco in bancos:
        libres = [p for p in banco if p not in excluir]
        if libres:
            return random.choice(libres), None, False
    return random.choice(mod.repaso or mod.preguntas), None, True


@router.get("/pregunta")
def pregunta(modulo: str, anclas: str = "", excluir: str = "", c: Contenido = Depends(requiere_curso)):
    mod = _modulo(c, modulo)
    pid, ancla, reiniciado = elegir(c, mod, _lista(anclas, MAX_ANCLAS), set(_lista(excluir, MAX_EXCLUIR)))
    return {**vista_pregunta(c, pid), "ancla": ancla, "reiniciado": reiniciado}


@router.post("/corregir")
async def corregir(request: Request, c: Contenido = Depends(requiere_curso)):
    form = await request.form()
    mod = _modulo(c, form.get("modulo", ""))
    pid = form.get("pid", "")
    if pid not in mod.repaso and pid not in mod.preguntas:
        raise HTTPException(404, "Pregunta no encontrada")
    p = c.preguntas[pid]
    try:
        r = leer_respuesta(p, form)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    return {"correcta": es_correcta(p, r), "solucion": legible(p, p["correctas"]), "respuesta": legible(p, r),
            "explicacion": p["explicacion"], "distractores": p.get("distractores") or {}, "referencia": p["referencia"],
            "teoria": c.url_teoria(p.get("objetivo"))}
