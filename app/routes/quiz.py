import random
from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from curso import simulacro
from curso.correccion import corregir

from .. import stats
from ..content import Contenido
from ..deps import get_db, requiere_curso, requiere_usuario, verificar_csrf
from ..models import Intento, IntentoRespuesta, Usuario, ahora
from ..preguntas import leer_respuesta, vista_pregunta
from ..web import flash, render

router = APIRouter(prefix="/c/{curso}/tests", dependencies=[Depends(verificar_csrf)])
DOBLE_ENVIO = timedelta(seconds=10)  # un simulacro sin terminar más reciente que esto se reutiliza


def _intento(db: Session, iid: int, usuario: Usuario, c: Contenido) -> Intento:
    i = db.get(Intento, iid)
    if not i or i.usuario_id != usuario.id or i.curso != c.manifiesto.slug:
        raise HTTPException(404, "Intento no encontrado")
    return i


def _banco_simulacro(c: Contenido) -> list[dict]:
    """Preguntas del banco del simulacro del curso, en el orden del fichero (vacío si no tiene)."""
    mod = c.modulos.get(c.manifiesto.simulacro) if c.manifiesto.tiene_simulacro else None
    return [c.preguntas[p] for p in mod.preguntas] if mod else []


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
def inicio(request: Request, c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_usuario),
           db: Session = Depends(get_db)):
    m = c.manifiesto
    modulos = [x for x in c.modulos.values() if x.preguntas and not x.es_simulacro]
    repaso = [x for x in c.modulos.values() if x.repaso]
    banco_sim = _banco_simulacro(c)
    n_sim = len(banco_sim)
    sim_error = (simulacro.factible(m, banco_sim) or [None])[0] if m.tiene_simulacro else None
    dominios = sorted({c.preguntas[p]["dominio"] for x in modulos for p in x.preguntas})
    libros = [x for x in c.modulos.values() if x.libros]
    return render(request, "tests_inicio.html", modulos=modulos, repaso=repaso, n_repaso=sum(len(x.repaso) for x in repaso),
                  n_falladas=len(stats.falladas(db, usuario.id, c)), dominios=dominios, n_sim=n_sim, nombres=m.dominios,
                  hay_simulacro=m.tiene_simulacro, sim_ok=m.tiene_simulacro and n_sim >= m.examen_preguntas and not sim_error,
                  sim_error=sim_error, sim_rotatorio=m.tiene_simulacro and simulacro.rotatorio(m, banco_sim),
                  sim_n=m.examen_preguntas, sim_min=m.examen_minutos, libros=libros, n_libros=sum(len(x.libros) for x in libros))


@router.post("/iniciar")
def iniciar(request: Request, modo: str = Form(...), filtro: str = Form(""), n: int = Form(10), estudio: str = Form(""), todas: str = Form(""),
            c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_usuario),
            db: Session = Depends(get_db)):
    m = c.manifiesto
    base = f"/c/{m.slug}"
    n = max(1, min(n, 100))
    limite = None
    if modo == "libros":
        if filtro and (filtro not in c.modulos or not c.modulos[filtro].libros):
            raise HTTPException(400, "Módulo no válido")
        fuente = c.modulos[filtro].libros if filtro else [p for x in c.modulos.values() for p in x.libros]
        if not fuente:
            flash(request, "No hay preguntas de los libros.", "error")
            return RedirectResponse(f"{base}/tests", 303)
        # «Todas»: el test completo (también el final con todas las preguntas de los libros), sin el tope de 100.
        ids = random.sample(fuente, len(fuente) if todas else min(n, len(fuente)))
    elif modo == "simulacro":
        if not m.tiene_simulacro:
            raise HTTPException(400, "Este curso no tiene simulacro")
        anterior = db.execute(select(Intento).where(Intento.usuario_id == usuario.id, Intento.curso == m.slug,
                                                    Intento.modo == "simulacro")
                              .order_by(Intento.inicio.desc(), Intento.id.desc()).limit(1)).scalar()
        # Doble envío de «Empezar simulacro»: se reutiliza el intento recién creado en vez de abrir otro.
        if anterior and anterior.fin is None and not _caducado(anterior) and ahora() - anterior.inicio < DOBLE_ENVIO:
            return RedirectResponse(f"{base}/tests/{anterior.id}", 303)
        # Rotación: se prefieren las preguntas que no estaban en el intento de simulacro anterior (aunque se abandonara).
        try:
            ids = simulacro.extraer(m, _banco_simulacro(c), random.Random(), set(anterior.preguntas if anterior else ()))
        except ValueError as e:
            flash(request, str(e), "error")
            return RedirectResponse(f"{base}/tests", 303)
        # Modo estudio: corrección y explicación tras cada respuesta; se guarda en `filtro` (no hay otro filtro en el simulacro).
        limite, filtro = m.examen_minutos * 60, "estudio" if estudio else ""
    else:
        fuente = [p for x in c.modulos.values() if not x.es_simulacro for p in x.preguntas]
        if modo == "repaso":
            if filtro and (filtro not in c.modulos or not c.modulos[filtro].repaso):
                raise HTTPException(400, "Módulo no válido")
            fuente = c.modulos[filtro].repaso if filtro else [p for x in c.modulos.values() for p in x.repaso]
        elif modo == "falladas":
            fuente, filtro = stats.falladas(db, usuario.id, c), ""
        elif modo == "modulo":
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


def _sin_correccion(i: Intento) -> bool:
    """El simulacro no corrige hasta el final, salvo en modo estudio."""
    return i.modo == "simulacro" and i.filtro != "estudio"


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
    simulacro = _sin_correccion(i)
    retro = None
    if resp and not simulacro and p:
        retro = {"correcta": resp.correcta, "solucion": p["correctas"], "explicacion": p["explicacion"],
                 "distractores": p.get("distractores") or {}, "referencia": p.get("referencia"), "respuesta": resp.respuesta,
                 "teoria": c.url_teoria(p.get("objetivo"))}
    return render(request, "pregunta.html", i=i, n=n, total=len(i.preguntas), p=vista_pregunta(c, pid), pid=pid,
                  respondida=resp is not None, retro=retro, simulacro=simulacro,
                  restante=_segundos_restantes(i), hechas=len(i.respuestas))


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
        r = leer_respuesta(p, await request.form())
    except ValueError as e:
        flash(request, str(e), "error")
        return RedirectResponse(f"/c/{c.manifiesto.slug}/tests/{iid}/p/{n}", 303)
    db.add(IntentoRespuesta(intento_id=i.id, pregunta_id=pid, dominio=p["dominio"], tarea=p["tarea"], tipo=p["tipo"],
                            respuesta=r, correcta=corregir(p, r)))
    db.commit()
    if _sin_correccion(i):
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
        filas.append({"n": k, "id": pid, "p": p, "r": r, "retirada": p is None, "teoria": c.url_teoria(p.get("objetivo")) if p else None})
    ok = sum(1 for r in i.respuestas if r.correcta)
    total = len(i.preguntas)
    return render(request, "resultado.html", i=i, filas=filas, ok=ok, total=total, pct=round(100 * ok / total) if total else 0,
                  n_falladas=len(stats.falladas(db, usuario.id, c)))
