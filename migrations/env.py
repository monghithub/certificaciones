from alembic import context

from app.models import Base  # noqa: F401  (registra los modelos)

config = context.config
target_metadata = Base.metadata


def run_migrations_online():
    # La URL o la conexión las inyecta app.migraciones; si no, se usa sqlalchemy.url.
    conexion = config.attributes.get("connection")
    if conexion is None:
        from app.db import crear_motor
        motor = crear_motor(config.get_main_option("sqlalchemy.url"))
        with motor.connect() as conexion:
            context.configure(connection=conexion, target_metadata=target_metadata, render_as_batch=True)
            with context.begin_transaction():
                context.run_migrations()
    else:
        context.configure(connection=conexion, target_metadata=target_metadata, render_as_batch=True)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
