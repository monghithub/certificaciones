"""Dependencias de FastAPI: sesión de BD, usuario actual, roles y CSRF."""
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from .content import Contenido
from .models import Matricula, Usuario
from .security import csrf_valido


class CSRFInvalido(HTTPException):
    """El token del formulario no coincide con el de la sesión (formulario caducado, sesión expirada u otra pestaña)."""

    def __init__(self):
        super().__init__(403, "Token CSRF inválido")


class Redireccion(Exception):
    def __init__(self, url: str):
        self.url = url


def get_db(request: Request):
    with request.app.state.sesiones() as db:
        yield db


def usuario_sin_forzar(request: Request, db: Session = Depends(get_db)) -> Usuario:
    uid = request.session.get("uid")
    usuario = db.get(Usuario, uid) if uid else None
    if not usuario or not usuario.activo:
        request.session.clear()
        raise Redireccion("/login")
    request.state.user = usuario
    return usuario


def requiere_usuario(request: Request, usuario: Usuario = Depends(usuario_sin_forzar)) -> Usuario:
    if usuario.debe_cambiar_password:
        raise Redireccion("/cuenta/password")
    return usuario


def requiere_admin(usuario: Usuario = Depends(requiere_usuario)) -> Usuario:
    if usuario.rol != "admin":
        raise HTTPException(403, "Acceso restringido a administradores")
    return usuario


async def verificar_csrf(request: Request):
    if request.method in ("GET", "HEAD", "OPTIONS"):
        return
    recibido = request.headers.get("x-csrf-token")
    if not recibido:
        recibido = (await request.form()).get("csrf")
    if not csrf_valido(request.session, recibido):
        raise CSRFInvalido()


def cursos_accesibles(request: Request, db: Session, usuario: Usuario) -> list[Contenido]:
    """Cursos del catálogo a los que el usuario tiene acceso: todos para el admin, los matriculados para el resto."""
    catalogo = request.app.state.catalogo
    if usuario.rol == "admin":
        return list(catalogo)
    slugs = set(db.execute(select(Matricula.curso).where(Matricula.usuario_id == usuario.id)).scalars())
    return [c for c in catalogo if c.manifiesto.slug in slugs]


def requiere_curso(curso: str, request: Request, usuario: Usuario = Depends(requiere_usuario),
                   db: Session = Depends(get_db)) -> Contenido:
    """Resuelve el curso de la URL. 404 si no existe o el usuario no tiene acceso (no se revela su existencia)."""
    contenido = request.app.state.catalogo.get(curso)
    if not contenido or contenido not in cursos_accesibles(request, db, usuario):
        raise HTTPException(404, "Curso no encontrado")
    request.state.curso = contenido
    return contenido
