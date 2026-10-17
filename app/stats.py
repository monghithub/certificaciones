"""Consultas de progreso y estadísticas por usuario."""
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from .catalogo import Catalogo
from .content import Contenido
from .models import Intento, IntentoRespuesta, Matricula, ProgresoLectura, Usuario

# func.sum sobre una columna Boolean devolvería un bool; se suma un entero explícito.
SUMA_ACIERTOS = func.sum(case((IntentoRespuesta.correcta.is_(True), 1), else_=0))
UMBRAL_DEBIL = 70
MIN_RESPUESTAS_DEBIL = 3


def progreso_modulos(db: Session, uid: int, contenido: Contenido) -> list[dict]:
    curso = contenido.manifiesto.slug
    filas = db.execute(select(ProgresoLectura).where(ProgresoLectura.usuario_id == uid, ProgresoLectura.curso == curso)).scalars().all()
    vistas = {(f.modulo, f.seccion): f for f in filas}
    resultado = []
    for mod in contenido.modulos.values():
        total = len(mod.secciones)
        hechas = sum(1 for s in mod.secciones if vistas.get((mod.id, s.id)) and vistas[(mod.id, s.id)].completada)
        abiertas = sum(1 for s in mod.secciones if (mod.id, s.id) in vistas)
        estado = "completado" if total and hechas == total else "en curso" if abiertas else "sin empezar"
        resultado.append({"modulo": mod, "total": total, "hechas": hechas, "estado": estado,
                          "completadas": {s.id for s in mod.secciones if vistas.get((mod.id, s.id)) and vistas[(mod.id, s.id)].completada}})
    return resultado


def ultima_posicion(db: Session, uid: int, catalogo: Catalogo, curso: str | None = None) -> dict | None:
    """Última sección abierta, en un curso concreto o (si curso es None) en cualquiera del catálogo."""
    q = select(ProgresoLectura).where(ProgresoLectura.usuario_id == uid).order_by(ProgresoLectura.actualizado.desc())
    if curso:
        q = q.where(ProgresoLectura.curso == curso)
    for f in db.execute(q).scalars():
        contenido = catalogo.get(f.curso)
        mod = contenido.modulos.get(f.modulo) if contenido else None
        sec = next((s for s in mod.secciones if s.id == f.seccion), None) if mod else None
        if sec:
            return {"curso": contenido, "modulo": mod, "seccion": sec, "fecha": f.actualizado}
    return None


def aciertos_por(db: Session, uid: int, curso: str) -> tuple[list[dict], list[dict]]:
    """Devuelve (por_dominio, por_tarea) con n, aciertos y porcentaje."""
    q = (select(IntentoRespuesta.dominio, IntentoRespuesta.tarea, func.count(), SUMA_ACIERTOS)
         .join(Intento).where(Intento.usuario_id == uid, Intento.curso == curso).group_by(IntentoRespuesta.dominio, IntentoRespuesta.tarea))
    tareas, dominios = [], {}
    for d, t, n, ok in db.execute(q):
        ok = int(ok or 0)
        tareas.append({"dominio": d, "tarea": t, "n": n, "ok": ok, "pct": round(100 * ok / n)})
        a = dominios.setdefault(d, {"dominio": d, "n": 0, "ok": 0})
        a["n"] += n
        a["ok"] += ok
    for a in dominios.values():
        a["pct"] = round(100 * a["ok"] / a["n"])
    return sorted(dominios.values(), key=lambda x: x["dominio"]), sorted(tareas, key=lambda x: x["tarea"])


def falladas(db: Session, uid: int, contenido: Contenido) -> list[str]:
    """Preguntas (de repaso y de examen, no del simulacro) cuya última respuesta del usuario fue incorrecta."""
    q = (select(IntentoRespuesta.pregunta_id, IntentoRespuesta.correcta).join(Intento)
         .where(Intento.usuario_id == uid, Intento.curso == contenido.manifiesto.slug).order_by(IntentoRespuesta.id))
    ultima = dict(db.execute(q).all())
    simulacro = contenido.manifiesto.simulacro
    return sorted(pid for pid, ok in ultima.items()
                  if not ok and pid in contenido.preguntas and contenido.preguntas[pid]["modulo"] != simulacro)


def puntos_debiles(tareas: list[dict]) -> list[dict]:
    debiles = [t for t in tareas if t["n"] >= MIN_RESPUESTAS_DEBIL and t["pct"] < UMBRAL_DEBIL]
    return sorted(debiles, key=lambda t: t["pct"])[:5]


def resumen_intento(i: Intento) -> dict:
    total = len(i.preguntas)
    ok = sum(1 for r in i.respuestas if r.correcta)
    return {"intento": i, "total": total, "ok": ok, "pct": round(100 * ok / total) if total else 0,
            "respondidas": len(i.respuestas), "cerrado": i.fin is not None}


def intentos(db: Session, uid: int, curso: str, limite: int = 50) -> list[dict]:
    filas = db.execute(select(Intento).where(Intento.usuario_id == uid, Intento.curso == curso).order_by(Intento.inicio.desc()).limit(limite)).scalars().all()
    return [resumen_intento(i) for i in filas]


def matriculas(db: Session, uid: int) -> list[str]:
    return list(db.execute(select(Matricula.curso).where(Matricula.usuario_id == uid).order_by(Matricula.curso)).scalars())


def resumen_usuarios(db: Session, catalogo: Catalogo) -> list[dict]:
    usuarios = db.execute(select(Usuario).order_by(Usuario.username)).scalars().all()
    n_intentos = dict(db.execute(select(Intento.usuario_id, func.count()).group_by(Intento.usuario_id)).all())
    aciertos = {u: (n, int(ok or 0)) for u, n, ok in db.execute(
        select(Intento.usuario_id, func.count(), SUMA_ACIERTOS).join(IntentoRespuesta).group_by(Intento.usuario_id))}
    cursos_de: dict[int, list[str]] = {}
    for uid, curso in db.execute(select(Matricula.usuario_id, Matricula.curso).order_by(Matricula.curso)):
        cursos_de.setdefault(uid, []).append(curso)
    resultado = []
    for u in usuarios:
        n, ok = aciertos.get(u.id, (0, 0))
        resultado.append({"usuario": u, "cursos": cursos_de.get(u.id, []), "posicion": ultima_posicion(db, u.id, catalogo),
                          "intentos": n_intentos.get(u.id, 0), "pct": round(100 * ok / n) if n else None})
    return resultado
