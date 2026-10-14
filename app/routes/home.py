from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .. import stats
from ..deps import cursos_accesibles, get_db, requiere_usuario, verificar_csrf
from ..models import Usuario
from ..web import render

router = APIRouter(dependencies=[Depends(verificar_csrf)])


@router.get("/")
def inicio(request: Request, usuario: Usuario = Depends(requiere_usuario), db: Session = Depends(get_db)):
    cursos = cursos_accesibles(request, db, usuario)
    if len(cursos) == 1:
        return RedirectResponse(f"/c/{cursos[0].manifiesto.slug}/", 303)
    filas = []
    for c in cursos:
        progreso = stats.progreso_modulos(db, usuario.id, c)
        total = sum(f["total"] for f in progreso)
        hechas = sum(f["hechas"] for f in progreso)
        filas.append({"curso": c, "pct": round(100 * hechas / total) if total else 0, "total": total, "hechas": hechas,
                      "posicion": stats.ultima_posicion(db, usuario.id, request.app.state.catalogo, c.manifiesto.slug)})
    return render(request, "cursos.html", filas=filas)
