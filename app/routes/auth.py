from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..deps import get_db, usuario_sin_forzar, verificar_csrf
from ..models import Usuario, ahora
from ..security import HASH_FICTICIO, error_password, hashear, verificar
from ..web import flash, render

router = APIRouter(dependencies=[Depends(verificar_csrf)])


def _ip(request: Request) -> str:
    return request.client.host if request.client else "desconocida"


@router.get("/login")
def login_form(request: Request):
    if request.session.get("uid"):
        return RedirectResponse("/", 303)
    return render(request, "login.html")


@router.post("/login")
def login(request: Request, username: str = Form(""), password: str = Form(""), db: Session = Depends(get_db)):
    username = username.strip().lower()
    limitador = request.app.state.limitador
    claves = (f"u:{username}", f"ip:{_ip(request)}")
    if limitador.bloqueado(*claves):
        return render(request, "login.html", 429, error="Demasiados intentos fallidos. Inténtalo de nuevo en unos minutos.")
    usuario = db.execute(select(Usuario).where(Usuario.username == username)).scalar_one_or_none()
    # Se verifica siempre un hash para igualar tiempos y no revelar si el usuario existe.
    valido = verificar(usuario.password_hash if usuario else HASH_FICTICIO, password)
    if not (usuario and usuario.activo and valido):
        limitador.fallo(*claves)
        return render(request, "login.html", 401, error="Usuario o contraseña incorrectos.")
    limitador.exito(claves[0])
    csrf_previo = request.session.get("csrf")
    request.session.clear()
    request.session["uid"] = usuario.id
    if csrf_previo:
        request.session["csrf"] = csrf_previo
    usuario.ultimo_acceso = ahora()
    db.commit()
    return RedirectResponse("/", 303)


@router.post("/logout")
def logout(request: Request):
    # Se conserva el token CSRF: así los formularios abiertos en otras pestañas (p. ej. el de acceso) siguen siendo válidos.
    csrf = request.session.get("csrf")
    request.session.clear()
    if csrf:
        request.session["csrf"] = csrf
    return RedirectResponse("/login", 303)


@router.get("/cuenta/password")
def password_form(request: Request, usuario: Usuario = Depends(usuario_sin_forzar)):
    return render(request, "password.html")


@router.post("/cuenta/password")
def password_cambiar(request: Request, actual: str = Form(""), nueva: str = Form(""), repetir: str = Form(""),
                     usuario: Usuario = Depends(usuario_sin_forzar), db: Session = Depends(get_db)):
    error = None
    if not verificar(usuario.password_hash, actual):
        error = "La contraseña actual no es correcta."
    elif nueva != repetir:
        error = "Las contraseñas nuevas no coinciden."
    elif nueva == actual:
        error = "La nueva contraseña debe ser distinta de la actual."
    else:
        error = error_password(nueva, request.app.state.settings.password_min_length)
    if error:
        return render(request, "password.html", 400, error=error)
    usuario.password_hash = hashear(nueva)
    usuario.debe_cambiar_password = False
    db.commit()
    flash(request, "Contraseña actualizada.", "ok")
    return RedirectResponse("/", 303)
