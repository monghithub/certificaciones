"""Fábrica de la aplicación FastAPI."""
import logging
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func, select
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .config import Settings
from .catalogo import Catalogo
from .db import crear_motor, crear_sesionmaker
from .deps import CSRFInvalido, Redireccion
from .migraciones import migrar
from .models import Usuario
from .routes import admin, auth, course, home, quiz, stats
from .security import LimitadorLogin, error_password, hashear
from .web import flash, render

log = logging.getLogger("app")
CSP = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       "frame-ancestors 'none'; form-action 'self'; base-uri 'self'")


class CabecerasSeguridad(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        r = await call_next(request)
        r.headers["Content-Security-Policy"] = CSP
        r.headers["X-Content-Type-Options"] = "nosniff"
        r.headers["X-Frame-Options"] = "DENY"
        r.headers["Referrer-Policy"] = "same-origin"
        r.headers["Cache-Control"] = "no-store" if not request.url.path.startswith("/static") else "no-cache"
        return r


def crear_admin_inicial(sesiones, username: str, password: str, nombre: str | None = None, minimo: int = 10) -> bool:
    """Crea el primer admin solo si no hay ningún usuario. Devuelve True si lo creó."""
    error = error_password(password, minimo)
    if error:
        raise ValueError(error)
    with sesiones() as db:
        if db.scalar(select(func.count()).select_from(Usuario)):
            return False
        db.add(Usuario(username=username.lower(), nombre=nombre or username, rol="admin", password_hash=hashear(password),
                       activo=True, debe_cambiar_password=True))
        db.commit()
        return True


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.desde_entorno()
    motor = crear_motor(settings.database_url)
    if settings.ejecutar_migraciones:
        migrar(motor)
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, title="Consola AIF-C01")
    app.state.settings = settings
    app.state.motor = motor
    app.state.sesiones = crear_sesionmaker(motor)
    app.state.catalogo = Catalogo(settings.courses_dir, settings.schemas_dir)
    app.state.limitador = LimitadorLogin(settings.login_max_intentos, settings.login_bloqueo_segundos)

    app.add_middleware(CabecerasSeguridad)
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, session_cookie="sesion", same_site="lax",
                       https_only=settings.cookie_secure, max_age=settings.session_max_age)
    app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")
    for r in (auth.router, home.router, course.router, quiz.router, stats.router, admin.router):
        app.include_router(r)

    @app.exception_handler(Redireccion)
    async def _redir(request: Request, exc: Redireccion):
        return RedirectResponse(exc.url, 303)

    @app.exception_handler(CSRFInvalido)
    async def _csrf(request: Request, exc: CSRFInvalido):
        """Formulario caducado: no se ejecuta la acción, pero en vez de un 403 seco se explica y se ofrece repetir."""
        if request.url.path == "/login":
            return render(request, "login.html", 403,
                          error="El formulario había caducado (la sesión expiró o se usó otra pestaña). Vuelve a introducir tus datos.")
        flash(request, "El formulario había caducado y no se ha enviado. Vuelve a intentarlo.", "error")
        origen = urlsplit(request.headers.get("referer", ""))
        mismo_sitio = origen.netloc == request.url.netloc and origen.path.startswith("/")
        destino = origen.path + (f"?{origen.query}" if origen.query else "") if mismo_sitio else "/"
        return RedirectResponse(destino, 303)

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException):
        textos = {403: "No tienes permiso para ver esta página.", 404: "No se ha encontrado la página.",
                  400: "Solicitud no válida."}
        return render(request, "error.html", exc.status_code, codigo=exc.status_code,
                      mensaje=textos.get(exc.status_code, str(exc.detail)))

    if settings.admin_username and settings.admin_password:
        if crear_admin_inicial(app.state.sesiones, settings.admin_username, settings.admin_password,
                               minimo=settings.password_min_length):
            log.warning("Administrador inicial «%s» creado; deberá cambiar la contraseña al entrar.", settings.admin_username)
    return app
