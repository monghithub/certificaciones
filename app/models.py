"""Modelo de datos: usuarios, progreso de lectura e intentos de cuestionario."""
from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base

ROLES = ("admin", "estudiante")


def ahora() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Usuario(Base):
    __tablename__ = "usuario"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(128))
    rol: Mapped[str] = mapped_column(String(16))
    password_hash: Mapped[str] = mapped_column(String(256))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    debe_cambiar_password: Mapped[bool] = mapped_column(Boolean, default=True)
    creado: Mapped[datetime] = mapped_column(DateTime, default=ahora)
    ultimo_acceso: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Matricula(Base):
    """Acceso de un usuario a un curso. El curso se identifica por su slug (viven en el sistema de ficheros)."""
    __tablename__ = "matricula"
    __table_args__ = (UniqueConstraint("usuario_id", "curso"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="CASCADE"), index=True)
    curso: Mapped[str] = mapped_column(String(64))
    creado: Mapped[datetime] = mapped_column(DateTime, default=ahora)


class ProgresoLectura(Base):
    __tablename__ = "progreso_lectura"
    __table_args__ = (UniqueConstraint("usuario_id", "curso", "modulo", "seccion"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="CASCADE"), index=True)
    curso: Mapped[str] = mapped_column(String(64))
    modulo: Mapped[str] = mapped_column(String(64))
    seccion: Mapped[str] = mapped_column(String(64))
    completada: Mapped[bool] = mapped_column(Boolean, default=False)
    actualizado: Mapped[datetime] = mapped_column(DateTime, default=ahora)


class Intento(Base):
    __tablename__ = "intento"
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="CASCADE"), index=True)
    curso: Mapped[str] = mapped_column(String(64), index=True)
    modo: Mapped[str] = mapped_column(String(16))  # modulo | dominio | mixto | simulacro
    filtro: Mapped[str] = mapped_column(String(64), default="")
    inicio: Mapped[datetime] = mapped_column(DateTime, default=ahora)
    fin: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    limite_segundos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preguntas: Mapped[list] = mapped_column(JSON)  # ids de pregunta en orden
    respuestas: Mapped[list["IntentoRespuesta"]] = relationship(
        back_populates="intento", cascade="all, delete-orphan", order_by="IntentoRespuesta.id"
    )


class IntentoRespuesta(Base):
    __tablename__ = "intento_respuesta"
    __table_args__ = (UniqueConstraint("intento_id", "pregunta_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    intento_id: Mapped[int] = mapped_column(ForeignKey("intento.id", ondelete="CASCADE"), index=True)
    pregunta_id: Mapped[str] = mapped_column(String(16))
    dominio: Mapped[int] = mapped_column(Integer)
    tarea: Mapped[str] = mapped_column(String(8))
    tipo: Mapped[str] = mapped_column(String(24))
    respuesta: Mapped[list] = mapped_column(JSON)
    correcta: Mapped[bool] = mapped_column(Boolean)
    intento: Mapped[Intento] = relationship(back_populates="respuestas")
