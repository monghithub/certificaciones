"""«Preguntar a Claude»: dudas en conversación sobre las preguntas de los tests, resueltas en segundo plano.

Dos routers, que `app.main` solo registra si hay `CONSULTAS_TOKEN`:

- `router`: páginas y fragmentos htmx del navegador (solo `admin`, con CSRF de la sesión).
- `api`: API interna del trabajador (`scripts/consultas_trabajador.py`), con `Authorization: Bearer <CONSULTAS_TOKEN>`,
  sin cookie ni CSRF. Sin el token correcto responde 404, para no revelar que existe.
"""
import hmac
import json
from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse, Response
from markdown_it import MarkdownIt
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..content import Contenido
from ..deps import get_db, requiere_admin, requiere_curso, verificar_csrf
from ..models import Consulta, ConsultaMensaje, Intento, IntentoRespuesta, Usuario, ahora
from ..security import token_csrf
from ..web import flash, plantillas, render

router = APIRouter(prefix="/c/{curso}", dependencies=[Depends(verificar_csrf)])
api = APIRouter(prefix="/api/consultas")

MAX_TEXTO = 2000
MAX_RESPUESTA = 100_000
CADUCIDAD_PROCESANDO = timedelta(minutes=15)  # un «procesando» más antiguo se da por perdido (el trabajador murió)
ESPERANDO = ("pendiente", "procesando")
MAX_EN_ESPERA = 3  # dudas en cola o en curso por usuario, entre todas sus conversaciones
MAX_DIA = 30  # dudas por usuario en las últimas 24 h
ESTADOS = {"pendiente": "En cola", "procesando": "Pensando…", "respondido": "Respondida", "error": "Error"}


def _md() -> MarkdownIt:
    """Markdown de las respuestas de Claude: sin HTML crudo, sin imágenes (una imagen externa podría filtrar datos al
    cargarse; `![x](url)` queda como texto y enlace) y con los enlaces en otra pestaña."""
    md = MarkdownIt("commonmark", {"html": False}).enable("table").disable("image")

    def enlace(renderer, tokens, idx, options, env):
        tokens[idx].attrSet("target", "_blank")
        tokens[idx].attrSet("rel", "noopener noreferrer")
        return renderer.renderToken(tokens, idx, options, env)

    md.add_render_rule("link_open", enlace)
    return md


_markdown = _md()


def markdown_claude(texto: str) -> str:
    return _markdown.render(texto or "")


# ---------------------------------------------------------------- navegador

def _pregunta(c: Contenido, pid: str) -> dict:
    p = c.preguntas.get(pid)
    if not p:
        raise HTTPException(404, "Pregunta no encontrada")
    return p


def _consulta(db: Session, usuario: Usuario, c: Contenido, pid: str) -> Consulta | None:
    return db.execute(select(Consulta).where(Consulta.usuario_id == usuario.id, Consulta.curso == c.manifiesto.slug,
                                             Consulta.pregunta_id == pid)).scalar_one_or_none()


def _intento(db: Session, iid, usuario: Usuario, c: Contenido, pid: str) -> int | None:
    """Id del intento desde el que se pregunta, solo si es del usuario, del curso y contiene la pregunta."""
    try:
        iid = int(iid)
    except (TypeError, ValueError):
        return None
    i = db.get(Intento, iid)
    if not i or i.usuario_id != usuario.id or i.curso != c.manifiesto.slug or pid not in (i.preguntas or []):
        return None
    return i.id


def _mensajes(consulta: Consulta | None) -> list[dict]:
    salida = []
    for m in consulta.mensajes if consulta else []:
        salida.append({"id": m.id, "rol": m.rol, "texto": m.texto, "estado": m.estado, "etiqueta": ESTADOS.get(m.estado, m.estado),
                       "error": m.error, "html": markdown_claude(m.texto) if m.rol == "claude" else None, "creado": m.creado})
    return salida


def _ctx(request: Request, c: Contenido, pid: str, consulta: Consulta | None, intento: int | None, error: str | None = None) -> dict:
    mensajes = _mensajes(consulta)
    return {"base": f"/c/{c.manifiesto.slug}", "pid": pid, "intento": intento, "mensajes": mensajes, "error": error,
            "esperando": any(m["rol"] == "usuario" and m["estado"] in ESPERANDO for m in mensajes),
            "con_error": any(m["rol"] == "usuario" and m["estado"] == "error" for m in mensajes),
            "csrf": token_csrf(request.session), "max_texto": MAX_TEXTO}


def _fragmento(request: Request, nombre: str, ctx: dict) -> Response:
    """Fragmento htmx: sin la plantilla base ni los avisos de la sesión (se quedan para la página siguiente)."""
    return plantillas.TemplateResponse(request, nombre, ctx)


def _es_htmx(request: Request) -> bool:
    return request.headers.get("hx-request") == "true"


def _limite(db: Session, usuario: Usuario) -> str | None:
    """Tope de gasto de la cuota: dudas en espera a la vez y dudas en las últimas 24 h, por usuario."""
    base = (select(func.count()).select_from(ConsultaMensaje).join(Consulta)
            .where(Consulta.usuario_id == usuario.id, ConsultaMensaje.rol == "usuario"))
    if db.scalar(base.where(ConsultaMensaje.estado.in_(ESPERANDO))) >= MAX_EN_ESPERA:
        return (f"Ya tienes {MAX_EN_ESPERA} dudas esperando respuesta en este u otros tests: espera a que Claude "
                "responda alguna antes de enviar otra.")
    if db.scalar(base.where(ConsultaMensaje.creado > ahora() - timedelta(hours=24))) >= MAX_DIA:
        return f"Has llegado al máximo de {MAX_DIA} dudas en 24 horas, para no agotar la cuota de Claude. Inténtalo más tarde."
    return None


def _volver(c: Contenido, db: Session, consulta: Consulta | None, pid: str, intento: int | None) -> RedirectResponse:
    """Sin htmx: vuelve a la pregunta del test si se conoce, o a la conversación."""
    base = f"/c/{c.manifiesto.slug}"
    if intento:
        i = db.get(Intento, intento)
        return RedirectResponse(f"{base}/tests/{i.id}/p/{i.preguntas.index(pid) + 1}", 303)
    return RedirectResponse(f"{base}/dudas/{consulta.id}" if consulta else f"{base}/dudas", 303)


@router.get("/consultas/{pid}/panel")
def panel(pid: str, request: Request, intento: str | None = None, c: Contenido = Depends(requiere_curso),
          usuario: Usuario = Depends(requiere_admin), db: Session = Depends(get_db)):
    _pregunta(c, pid)
    iid = _intento(db, intento, usuario, c, pid)
    return _fragmento(request, "_consulta.html", _ctx(request, c, pid, _consulta(db, usuario, c, pid), iid))


@router.get("/consultas/{pid}/mensajes")
def mensajes(pid: str, request: Request, intento: str | None = None, c: Contenido = Depends(requiere_curso),
             usuario: Usuario = Depends(requiere_admin), db: Session = Depends(get_db)):
    """Solo la conversación: es lo que se sondea cada 5 s mientras hay una duda en curso (no toca el formulario)."""
    _pregunta(c, pid)
    iid = _intento(db, intento, usuario, c, pid)
    return _fragmento(request, "_consulta_mensajes.html", _ctx(request, c, pid, _consulta(db, usuario, c, pid), iid))


@router.post("/consultas/{pid}")
def enviar(pid: str, request: Request, texto: str = Form(""), intento: str = Form(""), c: Contenido = Depends(requiere_curso),
           usuario: Usuario = Depends(requiere_admin), db: Session = Depends(get_db)):
    _pregunta(c, pid)
    iid = _intento(db, intento, usuario, c, pid)
    consulta = _consulta(db, usuario, c, pid)
    texto = texto.strip()
    error = None
    if not texto:
        error = "Escribe tu duda antes de enviarla."
    elif len(texto) > MAX_TEXTO:
        error = f"La duda es demasiado larga (máximo {MAX_TEXTO} caracteres)."
    elif consulta and any(m.rol == "usuario" and m.estado in ESPERANDO for m in consulta.mensajes):
        error = "Ya hay una duda en curso en esta conversación: espera a que Claude la responda para enviar otra."
    else:
        error = _limite(db, usuario)
    if not error:
        if not consulta:
            try:
                consulta = Consulta(usuario_id=usuario.id, curso=c.manifiesto.slug, pregunta_id=pid, intento_id=iid)
                db.add(consulta)
                db.flush()
            except IntegrityError:  # otra petición simultánea creó la conversación: se usa esa
                db.rollback()
                consulta = _consulta(db, usuario, c, pid)
        elif consulta.intento_id is None and iid:
            consulta.intento_id = iid
        consulta.mensajes.append(ConsultaMensaje(rol="usuario", texto=texto, estado="pendiente"))
        consulta.actualizada = ahora()
        db.commit()
    if _es_htmx(request):
        return _fragmento(request, "_consulta.html", _ctx(request, c, pid, consulta, iid, error))
    if error:
        flash(request, error, "error")
    return _volver(c, db, consulta, pid, iid)


@router.post("/consultas/{pid}/reintentar")
def reintentar(pid: str, request: Request, intento: str = Form(""), c: Contenido = Depends(requiere_curso),
               usuario: Usuario = Depends(requiere_admin), db: Session = Depends(get_db)):
    """Devuelve a la cola las dudas de la conversación que acabaron en error."""
    _pregunta(c, pid)
    iid = _intento(db, intento, usuario, c, pid)
    consulta = _consulta(db, usuario, c, pid)
    if not consulta:
        raise HTTPException(404, "Conversación no encontrada")
    error = _limite(db, usuario)
    if not error:
        for m in consulta.mensajes:
            if m.rol == "usuario" and m.estado == "error":
                m.estado, m.error, m.intentos, m.actualizado = "pendiente", None, 0, ahora()
        db.commit()
    if _es_htmx(request):
        ctx = _ctx(request, c, pid, consulta, iid)
        ctx["error_reintento"] = error
        return _fragmento(request, "_consulta_mensajes.html", ctx)
    if error:
        flash(request, error, "error")
    return _volver(c, db, consulta, pid, iid)


def _estado_consulta(consulta: Consulta) -> str:
    ultimo = next((m for m in reversed(consulta.mensajes) if m.rol == "usuario"), None)
    return ultimo.estado if ultimo else "respondido"


@router.get("/dudas")
def dudas(request: Request, c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_admin),
          db: Session = Depends(get_db)):
    consultas = db.execute(select(Consulta).where(Consulta.usuario_id == usuario.id, Consulta.curso == c.manifiesto.slug)
                           .order_by(Consulta.actualizada.desc(), Consulta.id.desc())).scalars().all()
    filas = []
    for k in consultas:
        p = c.preguntas.get(k.pregunta_id)
        ultimo = k.mensajes[-1] if k.mensajes else None
        estado = _estado_consulta(k)
        filas.append({"id": k.id, "pid": k.pregunta_id, "enunciado": p["enunciado"] if p else None, "estado": estado,
                      "etiqueta": ESTADOS.get(estado, estado), "ultimo": ultimo, "actualizada": k.actualizada,
                      "n": len(k.mensajes)})
    return render(request, "dudas.html", filas=filas)


@router.get("/dudas/{cid}")
def duda(cid: int, request: Request, c: Contenido = Depends(requiere_curso), usuario: Usuario = Depends(requiere_admin),
         db: Session = Depends(get_db)):
    k = db.get(Consulta, cid)
    if not k or k.usuario_id != usuario.id or k.curso != c.manifiesto.slug:
        raise HTTPException(404, "Conversación no encontrada")
    p = c.preguntas.get(k.pregunta_id)
    ctx = _ctx(request, c, k.pregunta_id, k, None)
    return render(request, "duda.html", consulta=k, p=p, teoria=c.url_teoria(p.get("objetivo")) if p else None, **ctx)


# ---------------------------------------------------------------- API interna del trabajador

def requiere_token(request: Request):
    """Token correcto y petición directa: la API solo la usa el trabajador del anfitrión contra 127.0.0.1; lo que
    llega con X-Forwarded-For viene a través del proxy (la red local) y se rechaza igual que un token incorrecto."""
    if request.headers.get("x-forwarded-for") is not None or request.headers.get("forwarded") is not None:
        raise HTTPException(404, "No encontrado")
    esperado = request.app.state.settings.consultas_token or ""
    cabecera = request.headers.get("authorization", "")
    recibido = cabecera[7:].strip() if cabecera[:7].lower() == "bearer " else ""
    if not esperado or not recibido or not hmac.compare_digest(esperado.encode(), recibido.encode()):
        raise HTTPException(404, "No encontrado")


async def _cuerpo(request: Request) -> dict:
    try:
        datos = json.loads(await request.body() or b"{}")
    except (ValueError, UnicodeDecodeError):
        raise HTTPException(400, "JSON no válido") from None
    if not isinstance(datos, dict):
        raise HTTPException(400, "JSON no válido")
    return datos


def _mensaje_en_curso(db: Session, mid: int, datos: dict) -> ConsultaMensaje:
    """Mensaje del usuario en «procesando» y en el mismo reparto que entregó /siguiente (si no, otro trabajador o un
    reparto posterior lo tiene: 409)."""
    m = db.get(ConsultaMensaje, mid)
    if not m or m.rol != "usuario":
        raise HTTPException(404, "Mensaje no encontrado")
    if m.estado != "procesando" or datos.get("reparto") != m.repartos:
        raise HTTPException(409, "El mensaje no está en curso en este reparto")
    return m


def _motivo(datos: dict) -> str:
    return str(datos.get("motivo") or "Sin detalle")[:2000]


def datos_pregunta(c: Contenido, p: dict) -> dict:
    datos = {k: p.get(k) for k in ("id", "banco", "modulo", "origen", "enunciado", "tipo", "opciones", "prompts", "correctas",
                                   "explicacion", "distractores", "referencia")}
    datos["teoria_url"] = c.url_teoria(p.get("objetivo"))
    datos["teoria_fichero"] = f"modulos/{p['modulo']}/README.md" if p.get("modulo") else None
    return datos


@api.post("/siguiente", dependencies=[Depends(requiere_token)])
def siguiente(request: Request, db: Session = Depends(get_db)):
    """Toma la duda pendiente más antigua (o una «procesando» caducada) y la marca como «procesando»."""
    catalogo = request.app.state.catalogo
    while True:
        caducada = ahora() - CADUCIDAD_PROCESANDO
        repartible = or_(ConsultaMensaje.estado == "pendiente",
                         and_(ConsultaMensaje.estado == "procesando", ConsultaMensaje.actualizado < caducada))
        mid = db.execute(select(ConsultaMensaje.id).where(ConsultaMensaje.rol == "usuario", repartible)
                         .order_by(ConsultaMensaje.id).limit(1)).scalar_one_or_none()
        if mid is None:
            return Response(status_code=204)
        # Reparto atómico: solo uno de dos repartos simultáneos cambia la fila; el otro sigue con la siguiente.
        r = db.execute(update(ConsultaMensaje).where(ConsultaMensaje.id == mid, repartible)
                       .values(estado="procesando", intentos=ConsultaMensaje.intentos + 1,
                               repartos=ConsultaMensaje.repartos + 1, actualizado=ahora())
                       .execution_options(synchronize_session=False))
        db.commit()
        if r.rowcount == 0:
            continue
        m = db.get(ConsultaMensaje, mid)
        db.refresh(m)
        k = m.consulta
        c = catalogo.get(k.curso)
        p = c.preguntas.get(k.pregunta_id) if c else None
        if not p:  # curso o pregunta retirados: no hay contexto que dar a Claude
            m.estado, m.error, m.actualizado = "error", "La pregunta ya no forma parte del curso.", ahora()
            db.commit()
            continue
        r = None
        if k.intento_id:
            r = db.execute(select(IntentoRespuesta).where(IntentoRespuesta.intento_id == k.intento_id,
                                                          IntentoRespuesta.pregunta_id == k.pregunta_id)).scalar_one_or_none()
        return JSONResponse({"mensaje_id": m.id, "consulta_id": k.id, "sesion_claude": k.sesion_claude, "texto": m.texto,
                             "intentos": m.intentos, "reparto": m.repartos, "curso": k.curso, "pregunta": datos_pregunta(c, p),
                             "respuesta_usuario": r.respuesta if r else None, "respondida": r is not None})


@api.post("/mensajes/{mid}/respuesta", dependencies=[Depends(requiere_token)])
async def respuesta(mid: int, request: Request, db: Session = Depends(get_db)):
    datos = await _cuerpo(request)
    texto = datos.get("texto")
    sesion = datos.get("sesion_claude")
    if not isinstance(texto, str) or not texto.strip() or len(texto) > MAX_RESPUESTA:
        raise HTTPException(400, "Texto no válido")
    if sesion is not None and (not isinstance(sesion, str) or len(sesion) > 64):
        raise HTTPException(400, "Sesión no válida")
    m = _mensaje_en_curso(db, mid, datos)
    k = m.consulta
    k.mensajes.append(ConsultaMensaje(rol="claude", texto=texto.strip(), estado="respondido", respondida_por=m.id))
    m.estado, m.error, m.actualizado = "respondido", None, ahora()
    if sesion:
        k.sesion_claude = sesion
    k.actualizada = ahora()
    db.commit()
    return {"ok": True}


@api.post("/mensajes/{mid}/reintentar", dependencies=[Depends(requiere_token)])
async def reintentar_api(mid: int, request: Request, db: Session = Depends(get_db)):
    """Vuelve a la cola (cuota agotada o error transitorio). Con `"contar": false` no gasta un intento."""
    datos = await _cuerpo(request)
    m = _mensaje_en_curso(db, mid, datos)
    m.estado, m.error, m.actualizado = "pendiente", _motivo(datos), ahora()
    if datos.get("contar") is False:
        m.intentos = max(0, (m.intentos or 0) - 1)
    db.commit()
    return {"ok": True}


@api.post("/mensajes/{mid}/error", dependencies=[Depends(requiere_token)])
async def error_api(mid: int, request: Request, db: Session = Depends(get_db)):
    datos = await _cuerpo(request)
    m = _mensaje_en_curso(db, mid, datos)
    m.estado, m.error, m.actualizado = "error", _motivo(datos), ahora()
    m.consulta.actualizada = ahora()
    db.commit()
    return {"ok": True}
