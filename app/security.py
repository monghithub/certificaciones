"""Contraseñas (argon2), protección CSRF y limitación de intentos de login."""
import hmac
import re
import secrets
import time
from collections import defaultdict

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

_hasher = PasswordHasher()
HASH_FICTICIO = _hasher.hash("contraseña-ficticia-para-igualar-tiempos")
MIN_PASSWORD = 10  # valor por defecto; se puede cambiar con PASSWORD_MIN_LENGTH
USERNAME_RE = re.compile(r"^[a-z0-9._-]{3,64}$")


def hashear(password: str) -> str:
    return _hasher.hash(password)


def verificar(hash_: str, password: str) -> bool:
    try:
        return _hasher.verify(hash_, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def error_password(password: str, minimo: int = MIN_PASSWORD) -> str | None:
    if len(password) < minimo:
        return f"La contraseña debe tener al menos {minimo} caracteres."
    if len(password) > 256:
        return "La contraseña es demasiado larga."
    return None


def token_csrf(session: dict) -> str:
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


def csrf_valido(session: dict, recibido: str | None) -> bool:
    esperado = session.get("csrf")
    return bool(esperado and recibido and hmac.compare_digest(esperado, recibido))


class LimitadorLogin:
    """Bloquea temporalmente tras N fallos consecutivos por clave (usuario o IP). En memoria, por proceso."""

    def __init__(self, max_intentos: int, bloqueo_segundos: int, reloj=time.monotonic):
        self.max = max_intentos
        self.bloqueo = bloqueo_segundos
        self.reloj = reloj
        self._fallos: dict[str, list[float]] = defaultdict(list)

    def _vigentes(self, clave):
        limite = self.reloj() - self.bloqueo
        self._fallos[clave] = [t for t in self._fallos[clave] if t > limite]
        return self._fallos[clave]

    def bloqueado(self, *claves: str) -> bool:
        return any(len(self._vigentes(c)) >= self.max for c in claves)

    def fallo(self, *claves: str):
        for c in claves:
            self._vigentes(c).append(self.reloj())

    def exito(self, clave: str):
        self._fallos.pop(clave, None)
