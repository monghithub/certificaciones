"""Plantillas Jinja2 y utilidades de render."""
import hashlib
from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates

from .security import token_csrf

plantillas = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
ESTATICOS = Path(__file__).parent / "static"


def static(nombre: str) -> str:
    """URL de un fichero estático con su versión (fecha y tamaño): al cambiar el fichero cambia la URL y el navegador no usa copias viejas."""
    st = (ESTATICOS / nombre).stat()
    v = hashlib.md5(f"{st.st_mtime_ns}-{st.st_size}".encode()).hexdigest()[:10]
    return f"/static/{nombre}?v={v}"


def legible(p: dict, valor) -> list[str]:
    """Convierte una respuesta o una solución (ids) en líneas legibles con el texto de cada opción."""
    if not p or not valor:
        return []
    texto = {o["id"]: o["texto"] for o in p.get("opciones") or []}
    opcion = lambda i: f"{i}) {texto[i]}" if i in texto else str(i)  # noqa: E731
    if p.get("tipo") == "ordering":
        return [f"{k}.º {opcion(i)}" for k, i in enumerate(valor, 1)]
    if p.get("tipo") == "matching":
        izq = {x["id"]: x["texto"] for x in p.get("prompts") or []}
        return [f"{pid}. {izq.get(pid, '')} → {opcion(o)}" for pid, o in valor]
    return [opcion(i) for i in valor]


plantillas.env.globals["static"] = static
plantillas.env.globals["legible"] = legible
plantillas.env.filters["fecha"] = lambda d: d.strftime("%d/%m/%Y %H:%M") if d else "—"


def flash(request: Request, mensaje: str, nivel: str = "info"):
    request.session.setdefault("flash", []).append([nivel, mensaje])


def render(request: Request, nombre: str, status: int = 200, **ctx):
    ctx.setdefault("user", getattr(request.state, "user", None))
    ctx["csrf"] = token_csrf(request.session)
    ctx["min_password"] = request.app.state.settings.password_min_length
    curso = getattr(request.state, "curso", None)
    ctx.setdefault("curso", curso)
    ctx.setdefault("base", f"/c/{curso.manifiesto.slug}" if curso else "")
    ctx["flash"] = request.session.pop("flash", [])
    return plantillas.TemplateResponse(request, nombre, ctx, status_code=status)
