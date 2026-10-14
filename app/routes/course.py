import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import stats
from ..content import Contenido
from ..deps import get_db, requiere_curso, requiere_usuario, verificar_csrf
from ..models import ProgresoLectura, Usuario, ahora
from ..web import render

router = APIRouter(prefix="/c/{curso}", dependencies=[Depends(verificar_csrf)])


@router.get("/")
def indice(request: Request, c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_usuario),
           db: Session = Depends(get_db)):
    return render(request, "indice.html", progreso=stats.progreso_modulos(db, usuario.id, c),
                  continuar=stats.ultima_posicion(db, usuario.id, request.app.state.catalogo, c.manifiesto.slug))


def _seccion(c: Contenido, modulo: str, seccion: str):
    r = c.seccion(modulo, seccion)
    if r is None:
        raise HTTPException(404, "Sección no encontrada")
    return c.modulos[modulo], next(s for s in c.modulos[modulo].secciones if s.id == seccion), r[0], r[1], r[2]


def datos_json(datos: dict) -> str:
    """JSON apto para incrustar en un <script type="application/json">: el < se escapa para no cerrar la etiqueta."""
    return json.dumps(datos, ensure_ascii=False).replace("<", "\\u003c").replace("&", "\\u0026")


def _fila(db: Session, uid: int, curso: str, modulo: str, seccion: str) -> ProgresoLectura:
    fila = db.execute(select(ProgresoLectura).where(
        ProgresoLectura.usuario_id == uid, ProgresoLectura.curso == curso, ProgresoLectura.modulo == modulo,
        ProgresoLectura.seccion == seccion)).scalar_one_or_none()
    if not fila:
        fila = ProgresoLectura(usuario_id=uid, curso=curso, modulo=modulo, seccion=seccion, completada=False)
        db.add(fila)
    return fila


@router.get("/modulo/{modulo}/{seccion}")
def leer(modulo: str, seccion: str, request: Request, c: Contenido = Depends(requiere_curso),
         usuario: Usuario = Depends(requiere_usuario), db: Session = Depends(get_db)):
    mod, sec, html, ids, diagramas = _seccion(c, modulo, seccion)
    fila = _fila(db, usuario.id, c.manifiesto.slug, modulo, seccion)
    fila.actualizado = ahora()
    db.commit()
    return render(request, "seccion.html", mod=mod, sec=sec, html=html, completada=fila.completada,
                  datos_conceptos=datos_json(c.datos_pagina(ids, diagramas)))


@router.post("/modulo/{modulo}/{seccion}/completar")
def completar(modulo: str, seccion: str, c: Contenido = Depends(requiere_curso),
              usuario: Usuario = Depends(requiere_usuario), db: Session = Depends(get_db)):
    _seccion(c, modulo, seccion)
    fila = _fila(db, usuario.id, c.manifiesto.slug, modulo, seccion)
    fila.completada = not fila.completada
    fila.actualizado = ahora()
    db.commit()
    return RedirectResponse(f"/c/{c.manifiesto.slug}/modulo/{modulo}/{seccion}", 303)


@router.get("/glosario")
def glosario(request: Request, c: Contenido = Depends(requiere_curso)):
    entradas = list(c.glosario) if c.glosario else []
    return render(request, "glosario.html", entradas=entradas, hay_glosario=c.glosario is not None,
                  datos_conceptos=datos_json(c.datos_pagina([e.id for e in entradas])))
