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


def _orden_tarea(t: str) -> tuple:
    return tuple(int(x) if x.isdigit() else -1 for x in t.split("."))


def _dominio_oficial(p: dict, m) -> int | None:
    """Dominio oficial de una pregunta (del manifiesto, o 0 con tarea CP en cursos con conocimientos previos), o None.
    Robusto ante tipos inesperados: solo vale un entero (no un bool, ni una lista)."""
    d, t = p.get("dominio"), p.get("tarea")
    if type(d) is not int:
        return None
    if d in m.dominios:
        return d
    return 0 if d == 0 and t == "CP" and 0 in m.nombres_dominio else None


def _tarea_oficial(p: dict, m) -> str | None:
    """Tarea oficial de una pregunta: `N.M` de un dominio del manifiesto (aunque no sea el de la pregunta: la tarea
    pertenece a su propio dominio en las fuentes) o `CP`; None si no la tiene (p. ej., la tarea `libros`)."""
    t = p.get("tarea")
    if not isinstance(t, str):
        return None
    if t == "CP":
        return t if 0 in m.nombres_dominio else None
    prefijo, punto, resto = t.partition(".")
    return t if punto and prefijo.isdigit() and resto.isdigit() and int(prefijo) in m.dominios else None


def _pct(ok: int, n: int) -> int:
    return round(100 * ok / n) if n else 0


def desglose_intento(i: Intento, contenido: Contenido, marcar_debiles: bool = False) -> dict:
    """Aciertos de un intento por dominio y por tarea, calculados con `i.preguntas` (las sin responder cuentan como
    falladas), así que los dominios suman el total del intento, y las tareas también cuando se muestran (filas «Sin tarea
    oficial» y «Preguntas retiradas»). Grupos especiales de dominio: `otros` (sin dominio oficial, como algunas de los
    libros) y `retiradas` (ids que ya no existen en el contenido). Con `marcar_debiles`, se marcan los dominios oficiales
    cuyo porcentaje mostrado queda por debajo del global mostrado (criterio relativo: no hay cortes oficiales por dominio)."""
    m = contenido.manifiesto
    nombres = m.nombres_dominio
    acierto = {r.pregunta_id: r.correcta for r in i.respuestas}
    grupos: dict = {}
    tareas: dict = {}
    sin_responder = retiradas_sin_responder = 0
    for pid in i.preguntas:
        p = contenido.preguntas.get(pid)
        ok = int(bool(acierto.get(pid)))
        if pid not in acierto:
            if p is None:
                retiradas_sin_responder += 1
            else:
                sin_responder += 1
        if p is None:
            clave, tarea = "retiradas", "retiradas"
        else:
            d = _dominio_oficial(p, m)
            clave = "otros" if d is None else d
            tarea = _tarea_oficial(p, m) or "otras"
        for destino, k in ((grupos, clave), (tareas, tarea)):
            g = destino.setdefault(k, {"clave": k, "n": 0, "ok": 0})
            g["n"] += 1
            g["ok"] += ok
    total = len(i.preguntas)
    ok_total = sum(g["ok"] for g in grupos.values())
    pct_total = _pct(ok_total, total)
    filas = []
    for clave in sorted(k for k in grupos if isinstance(k, int)) + [k for k in ("otros", "retiradas") if k in grupos]:
        g = grupos[clave]
        if clave == 0:
            nombre = nombres[0]["nombre"]
        elif isinstance(clave, int):
            nombre = f"Dominio {clave} · {nombres[clave]['nombre']}"
        else:
            nombre = "Sin dominio oficial" if clave == "otros" else "Preguntas retiradas del contenido"
        g.update(nombre=nombre, pct=_pct(g["ok"], g["n"]), url=contenido.url_dominio(clave) if isinstance(clave, int) else None)
        g["debil"] = marcar_debiles and isinstance(clave, int) and g["pct"] < pct_total
        filas.append(g)
    oficiales = sorted((k for k in tareas if k not in ("otras", "retiradas")), key=_orden_tarea)
    filas_tarea = []
    for k in oficiales + [k for k in ("otras", "retiradas") if k in tareas] if oficiales else []:
        t = tareas[k]
        nombre = {"CP": "Conocimientos previos", "otras": "Sin tarea oficial", "retiradas": "Preguntas retiradas del contenido"}
        t.update(tarea=k, nombre=nombre.get(k, f"Tarea {k}"), pct=_pct(t["ok"], t["n"]),
                 url=contenido.url_tarea(k) if k in oficiales else None)
        filas_tarea.append(t)
    por_dominio = [g["n"] for g in filas if isinstance(g["clave"], int)]
    return {"dominios": filas, "tareas": filas_tarea, "total": total, "ok": ok_total, "pct": pct_total,
            "sin_responder": sin_responder, "retiradas": grupos.get("retiradas", {}).get("n", 0),
            "retiradas_sin_responder": retiradas_sin_responder,
            "min_por_dominio": min(por_dominio, default=0), "max_por_dominio": max(por_dominio, default=0),
            "debiles": [g for g in filas if g["debil"]]}


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
