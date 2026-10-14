"""Configuración de la aplicación, leída de variables de entorno."""
import os
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


class ConfiguracionError(RuntimeError):
    pass


def _entero(valor, defecto: int) -> int:
    if valor in (None, ""):
        return defecto
    try:
        n = int(valor)
    except ValueError:
        raise ConfiguracionError("PASSWORD_MIN_LENGTH debe ser un número entero") from None
    if n < 1:
        raise ConfiguracionError("PASSWORD_MIN_LENGTH debe ser al menos 1")
    return n


@dataclass(frozen=True)
class Settings:
    secret_key: str
    database_url: str = "sqlite:///data/app.db"
    courses_dir: Path = RAIZ / "cursos"
    schemas_dir: Path = RAIZ / "schemas"
    cookie_secure: bool = False
    session_max_age: int = 8 * 3600
    admin_username: str | None = None
    admin_password: str | None = None
    login_max_intentos: int = 5
    login_bloqueo_segundos: int = 300
    password_min_length: int = 10
    ejecutar_migraciones: bool = True

    @classmethod
    def desde_entorno(cls, env=None) -> "Settings":
        env = os.environ if env is None else env
        clave = env.get("SECRET_KEY", "")
        if len(clave) < 32:
            raise ConfiguracionError("SECRET_KEY es obligatoria y debe tener al menos 32 caracteres")
        return cls(
            secret_key=clave,
            database_url=env.get("DATABASE_URL", cls.database_url),
            courses_dir=Path(env.get("COURSES_DIR", str(RAIZ / "cursos"))),
            cookie_secure=env.get("COOKIE_SECURE", "false").lower() in ("1", "true", "yes"),
            password_min_length=_entero(env.get("PASSWORD_MIN_LENGTH"), 10),
            admin_username=env.get("ADMIN_USERNAME") or None,
            admin_password=env.get("ADMIN_PASSWORD") or None,
        )
