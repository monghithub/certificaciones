"""soporte multicurso: columna curso en progreso e intentos, y tabla de matrículas

Revision ID: 0002
Revises: 0001

Los datos existentes pasan al curso 'aif-c01' y los estudiantes existentes se matriculan en él.
"""
import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

CURSO_INICIAL = "aif-c01"


def upgrade():
    op.create_table(
        "matricula",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("usuario_id", sa.Integer, sa.ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False),
        sa.Column("curso", sa.String(64), nullable=False),
        sa.Column("creado", sa.DateTime, nullable=False),
        sa.UniqueConstraint("usuario_id", "curso"),
    )
    op.create_index("ix_matricula_usuario_id", "matricula", ["usuario_id"])
    op.execute(sa.text(
        "INSERT INTO matricula (usuario_id, curso, creado) "
        "SELECT id, :curso, CURRENT_TIMESTAMP FROM usuario WHERE rol = 'estudiante'").bindparams(curso=CURSO_INICIAL))

    # intento: nueva columna (el valor por defecto solo sirve para las filas previas)
    op.add_column("intento", sa.Column("curso", sa.String(64), nullable=False, server_default=CURSO_INICIAL))
    op.create_index("ix_intento_curso", "intento", ["curso"])

    # progreso_lectura: la restricción única cambia, así que se recrea la tabla
    op.create_table(
        "progreso_lectura_nueva",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("usuario_id", sa.Integer, sa.ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False),
        sa.Column("curso", sa.String(64), nullable=False),
        sa.Column("modulo", sa.String(64), nullable=False),
        sa.Column("seccion", sa.String(64), nullable=False),
        sa.Column("completada", sa.Boolean, nullable=False),
        sa.Column("actualizado", sa.DateTime, nullable=False),
        sa.UniqueConstraint("usuario_id", "curso", "modulo", "seccion"),
    )
    op.execute(sa.text(
        "INSERT INTO progreso_lectura_nueva (id, usuario_id, curso, modulo, seccion, completada, actualizado) "
        "SELECT id, usuario_id, :curso, modulo, seccion, completada, actualizado FROM progreso_lectura").bindparams(curso=CURSO_INICIAL))
    op.drop_table("progreso_lectura")
    op.rename_table("progreso_lectura_nueva", "progreso_lectura")
    op.create_index("ix_progreso_lectura_usuario_id", "progreso_lectura", ["usuario_id"])


def downgrade():
    # Vuelve al esquema 0001. Si un usuario tiene la misma sección en varios cursos, se conserva la más reciente.
    op.create_table(
        "progreso_lectura_vieja",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("usuario_id", sa.Integer, sa.ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False),
        sa.Column("modulo", sa.String(64), nullable=False),
        sa.Column("seccion", sa.String(64), nullable=False),
        sa.Column("completada", sa.Boolean, nullable=False),
        sa.Column("actualizado", sa.DateTime, nullable=False),
        sa.UniqueConstraint("usuario_id", "modulo", "seccion"),
    )
    op.execute(
        "INSERT INTO progreso_lectura_vieja (usuario_id, modulo, seccion, completada, actualizado) "
        "SELECT usuario_id, modulo, seccion, completada, MAX(actualizado) FROM progreso_lectura "
        "GROUP BY usuario_id, modulo, seccion")
    op.drop_table("progreso_lectura")
    op.rename_table("progreso_lectura_vieja", "progreso_lectura")
    op.create_index("ix_progreso_lectura_usuario_id", "progreso_lectura", ["usuario_id"])
    op.drop_index("ix_intento_curso", table_name="intento")
    with op.batch_alter_table("intento") as batch:
        batch.drop_column("curso")
    op.drop_table("matricula")
