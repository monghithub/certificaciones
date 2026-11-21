"""consultas a Claude: conversaciones por pregunta y sus mensajes

Revision ID: 0003
Revises: 0002
"""
import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "consulta",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("usuario_id", sa.Integer, sa.ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False),
        sa.Column("curso", sa.String(64), nullable=False),
        sa.Column("pregunta_id", sa.String(64), nullable=False),
        sa.Column("intento_id", sa.Integer, sa.ForeignKey("intento.id", ondelete="SET NULL"), nullable=True),
        sa.Column("sesion_claude", sa.String(64), nullable=True),
        sa.Column("creada", sa.DateTime, nullable=False),
        sa.Column("actualizada", sa.DateTime, nullable=False),
        sa.UniqueConstraint("usuario_id", "curso", "pregunta_id"),
    )
    op.create_index("ix_consulta_usuario_id", "consulta", ["usuario_id"])
    op.create_table(
        "consulta_mensaje",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("consulta_id", sa.Integer, sa.ForeignKey("consulta.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rol", sa.String(16), nullable=False),
        sa.Column("texto", sa.Text, nullable=False),
        sa.Column("estado", sa.String(16), nullable=False),
        sa.Column("intentos", sa.Integer, nullable=False, server_default="0"),
        sa.Column("error", sa.Text, nullable=True),
        sa.Column("respondida_por", sa.Integer, sa.ForeignKey("consulta_mensaje.id"), nullable=True),
        sa.Column("creado", sa.DateTime, nullable=False),
        sa.Column("actualizado", sa.DateTime, nullable=False),
    )
    op.create_index("ix_consulta_mensaje_consulta_id", "consulta_mensaje", ["consulta_id"])
    op.create_index("ix_consulta_mensaje_estado", "consulta_mensaje", ["estado"])


def downgrade():
    op.drop_table("consulta_mensaje")
    op.drop_table("consulta")
