from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from .. import stats
from ..content import Contenido
from ..deps import get_db, requiere_curso, requiere_usuario
from ..models import Usuario
from ..web import render

router = APIRouter(prefix="/c/{curso}")


@router.get("/estadisticas")
def mis_estadisticas(request: Request, c: Contenido = Depends(requiere_curso),
                     usuario: Usuario = Depends(requiere_usuario), db: Session = Depends(get_db)):
    slug = c.manifiesto.slug
    dominios, tareas = stats.aciertos_por(db, usuario.id, slug)
    return render(request, "estadisticas.html", progreso=stats.progreso_modulos(db, usuario.id, c), dominios=dominios,
                  tareas=tareas, debiles=stats.puntos_debiles(tareas), intentos=stats.intentos(db, usuario.id, slug),
                  posicion=stats.ultima_posicion(db, usuario.id, request.app.state.catalogo, slug), nombres=c.manifiesto.nombres_dominio)
