import random
from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from curso.correccion import corregir

from ..content import Contenido
from ..deps import get_db, requiere_curso, requiere_usuario, verificar_csrf
from ..models import Intento, IntentoRespuesta, Usuario, ahora
from ..web import flash, render

router = APIRouter(prefix="/c/{curso}/tests", dependencies=[Depends(verificar_csrf)])


def _intento(db: Session, iid: int, usuario: Usuario, c: Contenido) -> Intento:
    i = db.get(Intento, iid)
    if not i or i.usuario_id != usuario.id or i.curso != c.manifiesto.slug:
        raise HTTPException(404, "Intento no encontrado")
    return i


def _caducado(i: Intento) -> bool:
    return i.fin is None and i.limite_segundos is not None and ahora() > i.inicio + timedelta(seconds=i.limite_segundos)


def _cerrar_si_caducado(db: Session, i: Intento):
    if _caducado(i):
        i.fin = i.inicio + timedelta(seconds=i.limite_segundos)
        db.commit()


def _segundos_restantes(i: Intento) -> int | None:
    if i.limite_segundos is None or i.fin:
        return None
    return max(0, int((i.inicio + timedelta(seconds=i.limite_segundos) - ahora()).total_seconds()))


@router.get("")
def inicio(request: Request, c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_usuario)):
    m = c.manifiesto
    modulos = [x for x in c.modulos.values() if x.preguntas and not x.es_simulacro]
    banco_sim = c.modulos.get(m.simulacro) if m.tiene_simulacro else None
    n_sim = len(banco_sim.preguntas) if banco_sim else 0
    dominios = sorted({c.preguntas[p]["dominio"] for x in modulos for p in x.preguntas})
    return render(request, "tests_inicio.html", modulos=modulos, dominios=dominios, n_sim=n_sim, nombres=m.dominios,
                  hay_simulacro=m.tiene_simulacro, sim_ok=m.tiene_simulacro and n_sim >= m.examen_preguntas,
                  sim_n=m.examen_preguntas, sim_min=m.examen_minutos)


@router.post("/iniciar")
def iniciar(request: Request, modo: str = Form(...), filtro: str = Form(""), n: int = Form(10),
            c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_usuario),
            db: Session = Depends(get_db)):
    m = c.manifiesto
    base = f"/c/{m.slug}"
    n = max(1, min(n, 100))
    limite = None
    if modo == "simulacro":
        if not m.tiene_simulacro:
            raise HTTPException(400, "Este curso no tiene simulacro")
        banco = c.modulos.get(m.simulacro)
        ids = sorted(banco.preguntas) if banco else []
        if len(ids) < m.examen_preguntas:
            flash(request, f"El simulacro necesita {m.examen_preguntas} preguntas y hay {len(ids)}.", "error")
            return RedirectResponse(f"{base}/tests", 303)
        ids, limite, filtro = ids[: m.examen_preguntas], m.examen_minutos * 60, ""
    else:
        fuente = [p for x in c.modulos.values() if not x.es_simulacro for p in x.preguntas]
        if modo == "modulo":
            if filtro not in c.modulos or c.modulos[filtro].es_simulacro:
                raise HTTPException(400, "Módulo no válido")
            fuente = c.modulos[filtro].preguntas
        elif modo == "dominio":
            if not filtro.isdigit():
                raise HTTPException(400, "Dominio no válido")
            fuente = [p for p in fuente if c.preguntas[p]["dominio"] == int(filtro)]
        elif modo == "mixto":
            filtro = ""
        else:
            raise HTTPException(400, "Modo no válido")
        if not fuente:
            flash(request, "No hay preguntas para ese filtro.", "error")
            return RedirectResponse(f"{base}/tests", 303)
        ids = random.sample(fuente, min(n, len(fuente)))
    i = Intento(usuario_id=usuario.id, curso=m.slug, modo=modo, filtro=filtro, limite_segundos=limite, preguntas=ids)
    db.add(i)
    db.commit()
    return RedirectResponse(f"{base}/tests/{i.id}", 303)


@router.get("/{iid}")
def continuar(iid: int, request: Request, c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_usuario), db: Session = Depends(get_db)):
    i = _intento(db, iid, usuario, c)
    _cerrar_si_caducado(db, i)
    if i.fin:
        return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/resultado", 303)
    hechas = {r.pregunta_id for r in i.respuestas}
    pendiente = next((k for k, p in enumerate(i.preguntas, 1) if p not in hechas), len(i.preguntas))
    return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/p/{pendiente}", 303)


def _vista_pregunta(c, pid: str):
    p = c.preguntas.get(pid)
    if not p:
        return None
    vista = {k: p.get(k) for k in ("id", "tipo", "enunciado", "opciones", "prompts", "tarea", "dominio")}
    vista["posiciones"] = len(p["correctas"]) if p["tipo"] == "ordering" else 0  # solo el nº de huecos, no la solución
    return vista


@router.get("/{iid}/p/{n}")
def ver(iid: int, n: int, request: Request, c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_usuario), db: Session = Depends(get_db)):
    i = _intento(db, iid, usuario, c)
    _cerrar_si_caducado(db, i)
    if i.fin:
        return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/resultado", 303)
    if not 1 <= n <= len(i.preguntas):
        raise HTTPException(404, "Pregunta fuera de rango")
    pid = i.preguntas[n - 1]
    p = c.preguntas.get(pid)
    resp = next((r for r in i.respuestas if r.pregunta_id == pid), None)
    simulacro = i.modo == "simulacro"
    retro = None
    if resp and not simulacro and p:
        retro = {"correcta": resp.correcta, "solucion": p["correctas"], "explicacion": p["explicacion"],
                 "distractores": p.get("distractores") or {}, "referencia": p["referencia"], "respuesta": resp.respuesta}
    return render(request, "pregunta.html", i=i, n=n, total=len(i.preguntas), p=_vista_pregunta(c, pid), pid=pid,
                  respondida=resp is not None, retro=retro, simulacro=simulacro,
                  restante=_segundos_restantes(i), hechas=len(i.respuestas))


def _leer_respuesta(p: dict, form) -> list:
    """Convierte el formulario en respuesta validada. Lanza ValueError si es incompleta o inválida."""
    opciones = {o["id"] for o in p["opciones"]}
    tipo = p["tipo"]
    if tipo == "multiple_choice":
        r = form.getlist("r")
        if len(r) != 1 or r[0] not in opciones:
            raise ValueError("Elige una opción.")
        return r
    if tipo == "multiple_response":
        r = form.getlist("r")
        if not r or not set(r) <= opciones:
            raise ValueError("Elige al menos una opción.")
        return sorted(set(r))
    if tipo == "ordering":
        r = [form.get(f"o{k}") for k in range(1, len(p["correctas"]) + 1)]
        if None in r or "" in r or not set(r) <= opciones or len(set(r)) != len(r):
            raise ValueError("Indica un elemento distinto en cada posición.")
        return r
    prompts = {x["id"] for x in p["prompts"]}
    pares = [[pid, form.get(f"m_{pid}")] for pid in sorted(prompts)]
    if any(o not in opciones for _, o in pares):
        raise ValueError("Empareja todos los elementos.")
    return pares


@router.post("/{iid}/responder")
async def responder(iid: int, request: Request, n: int = Form(...), c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_usuario),
                    db: Session = Depends(get_db)):
    i = _intento(db, iid, usuario, c)
    _cerrar_si_caducado(db, i)
    if i.fin:
        return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/resultado", 303)
    if not 1 <= n <= len(i.preguntas):
        raise HTTPException(404, "Pregunta fuera de rango")
    pid = i.preguntas[n - 1]
    p = c.preguntas.get(pid)
    if not p:
        flash(request, "Esta pregunta ya no está disponible.", "error")
        return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/p/{min(n + 1, len(i.preguntas))}", 303)
    if any(r.pregunta_id == pid for r in i.respuestas):
        return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/p/{n}", 303)
    try:
        r = _leer_respuesta(p, await request.form())
    except ValueError as e:
        flash(request, str(e), "error")
        return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/p/{n}", 303)
    db.add(IntentoRespuesta(intento_id=i.id, pregunta_id=pid, dominio=p["dominio"], tarea=p["tarea"], tipo=p["tipo"],
                            respuesta=r, correcta=corregir(p, r)))
    db.commit()
    if i.modo == "simulacro":
        siguiente = next((k for k, q in enumerate(i.preguntas, 1) if k > n and q not in {x.pregunta_id for x in i.respuestas} | {pid}), None)
        return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/p/{siguiente}" if siguiente else f"/c/{c.manifiesto.slug}/tests/{iid}/p/{n}", 303)
    return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/p/{n}", 303)


@router.post("/{iid}/finalizar")
def finalizar(iid: int, c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_usuario), db: Session = Depends(get_db)):
    i = _intento(db, iid, usuario, c)
    if not i.fin:
        i.fin = ahora()
        db.commit()
    return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/resultado", 303)


@router.get("/{iid}/resultado")
def resultado(iid: int, request: Request, c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_usuario), db: Session = Depends(get_db)):
    i = _intento(db, iid, usuario, c)
    _cerrar_si_caducado(db, i)
    if not i.fin:
        return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}", 303)
    por_pregunta = {r.pregunta_id: r for r in i.respuestas}
    filas = []
    for k, pid in enumerate(i.preguntas, 1):
        p, r = c.preguntas.get(pid), por_pregunta.get(pid)
        filas.append({"n": k, "id": pid, "p": p, "r": r, "retirada": p is None})
    ok = sum(1 for r in i.respuestas if r.correcta)
    total = len(i.preguntas)
    return render(request, "resultado.html", i=i, filas=filas, ok=ok, total=total, pct=round(100 * ok / total) if total else 0)
