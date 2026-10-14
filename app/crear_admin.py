"""Crea un administrador: python -m app.crear_admin USUARIO [--nombre NOMBRE]

La contraseña se pide por terminal (o se toma de ADMIN_PASSWORD). Pensado para el primer arranque.
"""
import argparse
import getpass
import os
import sys

from .config import Settings
from .db import crear_motor, crear_sesionmaker
from .migraciones import migrar
from .models import Usuario
from .security import USERNAME_RE, error_password, hashear
from sqlalchemy import select


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("username")
    ap.add_argument("--nombre")
    a = ap.parse_args(argv)
    username = a.username.lower()
    if not USERNAME_RE.match(username):
        print("Usuario no válido (3–64 caracteres: a-z, 0-9, . _ -).", file=sys.stderr)
        return 2
    password = os.environ.get("ADMIN_PASSWORD") or getpass.getpass("Contraseña: ")
    s = Settings.desde_entorno()
    if error := error_password(password, s.password_min_length):
        print(error, file=sys.stderr)
        return 2
    motor = crear_motor(s.database_url)
    migrar(motor)
    with crear_sesionmaker(motor)() as db:
        if db.scalar(select(Usuario.id).where(Usuario.username == username)):
            print("Ya existe un usuario con ese nombre.", file=sys.stderr)
            return 1
        db.add(Usuario(username=username, nombre=a.nombre or username, rol="admin", password_hash=hashear(password),
                       activo=True, debe_cambiar_password=True))
        db.commit()
    print(f"Administrador «{username}» creado. Deberá cambiar la contraseña al iniciar sesión.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
