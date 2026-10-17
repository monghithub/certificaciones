from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .. import stats
from ..deps import get_db, requiere_admin, verificar_csrf
from ..models import ROLES, Matricula, Usuario
from ..security import USERNAME_RE, error_password, hashear
from ..web import flash, render

router = APIRouter(prefix="/admin", dependencies=[Depends(verificar_csrf), Depends(requiere_admin)])


def _admins_activos(db: Session, excluyendo: int | None = None) -> int:
    q = select(func.count()).select_from(Usuario).where(Usuario.rol == "admin", Usuario.activo.is_(True))
    if excluyendo is not None:
        q = q.where(Usuario.id != excluyendo)
    return db.scalar(q)


def _usuario(db: Session, uid: int) -> Usuario:
    u = db.get(Usuario, uid)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    return u


@router.get("/usuarios")
def listado(request: Request, db: Session = Depends(get_db)):
    catalogo = request.app.state.catalogo
    return render(request, "admin_usuarios.html", filas=stats.resumen_usuarios(db, catalogo), avisos=catalogo.avisos)


@router.get("/cursos")
def cursos(request: Request, db: Session = Depends(get_db)):
    catalogo = request.app.state.catalogo
    matriculados = dict(db.execute(select(Matricula.curso, func.count()).group_by(Matricula.curso)).all())
    filas = [{"curso": c, "matriculados": matriculados.get(c.manifiesto.slug, 0),
              "modulos": len(c.modulos), "preguntas": len(c.preguntas)} for c in catalogo]
    return render(request, "admin_cursos.html", filas=filas, avisos=catalogo.avisos)


@router.get("/usuarios/nuevo")
def nuevo_form(request: Request):
    return render(request, "admin_nuevo.html", roles=ROLES, datos={}, cursos=list(request.app.state.catalogo))


@router.post("/usuarios/nuevo")
async def nuevo(request: Request, username: str = Form(""), nombre: str = Form(""), rol: str = Form("estudiante"),
                password: str = Form(""), db: Session = Depends(get_db)):
    catalogo = request.app.state.catalogo
    elegidos = [s for s in (await request.form()).getlist("cursos")]
    username = username.strip().lower()
    nombre = nombre.strip()
    error = None
    if not USERNAME_RE.match(username):
        error = "El usuario debe tener 3–64 caracteres: letras minúsculas, números, punto, guion o guion bajo."
    elif not nombre or len(nombre) > 128:
        error = "Indica un nombre (máximo 128 caracteres)."
    elif rol not in ROLES:
        error = "Rol no válido."
    elif any(catalogo.get(s) is None for s in elegidos):
        error = "Alguno de los cursos elegidos no existe."
    elif db.scalar(select(Usuario.id).where(Usuario.username == username)):
        error = "Ya existe un usuario con ese nombre de usuario."
    else:
        error = error_password(password, request.app.state.settings.password_min_length)
    if error:
        return render(request, "admin_nuevo.html", 400, roles=ROLES, error=error, cursos=list(catalogo),
                      datos={"username": username, "nombre": nombre, "rol": rol, "cursos": elegidos})
    u = Usuario(username=username, nombre=nombre, rol=rol, password_hash=hashear(password), activo=True, debe_cambiar_password=True)
    db.add(u)
    db.flush()
    for s in dict.fromkeys(elegidos):
        db.add(Matricula(usuario_id=u.id, curso=s))
    db.commit()
    flash(request, f"Usuario «{username}» creado. Deberá cambiar la contraseña al entrar.", "ok")
    return RedirectResponse(f"/admin/usuarios/{u.id}", 303)


@router.get("/usuarios/{uid}")
def detalle(uid: int, request: Request, curso: str | None = None, db: Session = Depends(get_db)):
    u = _usuario(db, uid)
    catalogo = request.app.state.catalogo
    matriculas = stats.matriculas(db, uid)
    # Si el usuario es admin accede a todos los cursos; se ofrecen sus matrículas y, si no tiene, los del catálogo.
    candidatos = [s for s in matriculas if catalogo.get(s)] or [c.manifiesto.slug for c in catalogo]
    actual = curso if curso in candidatos else (candidatos[0] if candidatos else None)
    ctx = {"u": u, "roles": ROLES, "matriculas": matriculas, "catalogo": catalogo, "candidatos": candidatos,
           "actual": actual, "huerfanas": [s for s in matriculas if not catalogo.get(s)]}
    if actual:
        c = catalogo.get(actual)
        dominios, tareas = stats.aciertos_por(db, uid, actual)
        ctx.update(progreso=stats.progreso_modulos(db, uid, c), dominios=dominios, tareas=tareas,
                   debiles=stats.puntos_debiles(tareas), intentos=stats.intentos(db, uid, actual),
                   posicion=stats.ultima_posicion(db, uid, catalogo, actual), base=f"/c/{actual}", nombres=c.manifiesto.nombres_dominio)
    return render(request, "admin_usuario.html", **ctx)


@router.post("/usuarios/{uid}/matricula")
def matricula(uid: int, request: Request, curso: str = Form(""), accion: str = Form(""), db: Session = Depends(get_db)):
    _usuario(db, uid)
    existente = db.execute(select(Matricula).where(Matricula.usuario_id == uid, Matricula.curso == curso)).scalar_one_or_none()
    if accion == "alta":
        if request.app.state.catalogo.get(curso) is None:
            flash(request, "Ese curso no existe en el catálogo.", "error")
        elif existente:
            flash(request, "El usuario ya está matriculado en ese curso.", "info")
        else:
            db.add(Matricula(usuario_id=uid, curso=curso))
            db.commit()
            flash(request, f"Matriculado en «{curso}».", "ok")
    elif accion == "baja":
        if existente:
            db.delete(existente)
            db.commit()
            flash(request, f"Matrícula en «{curso}» retirada (el historial se conserva).", "ok")
    else:
        flash(request, "Acción no válida.", "error")
    return RedirectResponse(f"/admin/usuarios/{uid}", 303)


@router.post("/usuarios/{uid}/editar")
def editar(uid: int, request: Request, nombre: str = Form(""), rol: str = Form(""), activo: str = Form(""),
           db: Session = Depends(get_db)):
    u = _usuario(db, uid)
    quiere_activo = activo == "1"
    if rol not in ROLES or not nombre.strip():
        flash(request, "Datos no válidos.", "error")
    elif u.rol == "admin" and u.activo and (rol != "admin" or not quiere_activo) and _admins_activos(db, excluyendo=u.id) == 0:
        flash(request, "No se puede degradar ni desactivar al último administrador activo.", "error")
    else:
        u.nombre, u.rol, u.activo = nombre.strip()[:128], rol, quiere_activo
        db.commit()
        flash(request, "Usuario actualizado.", "ok")
    return RedirectResponse(f"/admin/usuarios/{uid}", 303)


@router.post("/usuarios/{uid}/password")
def restablecer(uid: int, request: Request, password: str = Form(""), db: Session = Depends(get_db)):
    u = _usuario(db, uid)
    error = error_password(password, request.app.state.settings.password_min_length)
    if error:
        flash(request, error, "error")
    else:
        u.password_hash = hashear(password)
        u.debe_cambiar_password = True
        db.commit()
        flash(request, "Contraseña restablecida. Deberá cambiarla al entrar.", "ok")
    return RedirectResponse(f"/admin/usuarios/{uid}", 303)


@router.post("/recargar")
def recargar(request: Request):
    request.app.state.catalogo.cargar()
    flash(request, "Catálogo de cursos recargado desde disco.", "ok")
    return RedirectResponse("/admin/usuarios", 303)
