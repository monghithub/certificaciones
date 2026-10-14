"""esquema inicial

Revision ID: 0001
Revises:
"""
import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "usuario",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(64), nullable=False),
        sa.Column("nombre", sa.String(128), nullable=False),
        sa.Column("rol", sa.String(16), nullable=False),
        sa.Column("password_hash", sa.String(256), nullable=False),
        sa.Column("activo", sa.Boolean, nullable=False),
        sa.Column("debe_cambiar_password", sa.Boolean, nullable=False),
        sa.Column("creado", sa.DateTime, nullable=False),
        sa.Column("ultimo_acceso", sa.DateTime, nullable=True),
    )
    op.create_index("ix_usuario_username", "usuario", ["username"], unique=True)
    op.create_table(
        "progreso_lectura",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("usuario_id", sa.Integer, sa.ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False),
        sa.Column("modulo", sa.String(64), nullable=False),
        sa.Column("seccion", sa.String(64), nullable=False),
        sa.Column("completada", sa.Boolean, nullable=False),
        sa.Column("actualizado", sa.DateTime, nullable=False),
        sa.UniqueConstraint("usuario_id", "modulo", "seccion"),
    )
    op.create_index("ix_progreso_lectura_usuario_id", "progreso_lectura", ["usuario_id"])
    op.create_table(
        "intento",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("usuario_id", sa.Integer, sa.ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False),
        sa.Column("modo", sa.String(16), nullable=False),
        sa.Column("filtro", sa.String(64), nullable=False),
        sa.Column("inicio", sa.DateTime, nullable=False),
        sa.Column("fin", sa.DateTime, nullable=True),
        sa.Column("limite_segundos", sa.Integer, nullable=True),
        sa.Column("preguntas", sa.JSON, nullable=False),
    )
    op.create_index("ix_intento_usuario_id", "intento", ["usuario_id"])
    op.create_table(
        "intento_respuesta",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("intento_id", sa.Integer, sa.ForeignKey("intento.id", ondelete="CASCADE"), nullable=False),
        sa.Column("pregunta_id", sa.String(16), nullable=False),
        sa.Column("dominio", sa.Integer, nullable=False),
        sa.Column("tarea", sa.String(8), nullable=False),
        sa.Column("tipo", sa.String(24), nullable=False),
        sa.Column("respuesta", sa.JSON, nullable=False),
        sa.Column("correcta", sa.Boolean, nullable=False),
        sa.UniqueConstraint("intento_id", "pregunta_id"),
    )
    op.create_index("ix_intento_respuesta_intento_id", "intento_respuesta", ["intento_id"])


def downgrade():
    op.drop_table("intento_respuesta")
    op.drop_table("intento")
    op.drop_table("progreso_lectura")
    op.drop_table("usuario")
