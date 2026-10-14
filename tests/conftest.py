import shutil
from pathlib import Path

import pytest
import yaml

RAIZ = Path(__file__).resolve().parent.parent
FIX = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def repo(tmp_path):
    """Repositorio mínimo: esquemas y el curso aif-c01 (manifiesto y fuentes reales) con un banco válido en el módulo 03."""
    shutil.copytree(RAIZ / "schemas", tmp_path / "schemas")
    curso = tmp_path / "cursos" / "aif-c01"
    curso.mkdir(parents=True)
    shutil.copy(RAIZ / "cursos" / "aif-c01" / "curso.yaml", curso / "curso.yaml")
    shutil.copytree(RAIZ / "cursos" / "aif-c01" / "fuentes", curso / "fuentes")
    (curso / "modulos" / "03-modelos-fundacionales").mkdir(parents=True)
    (curso / "modulos" / "06-simulacro").mkdir(parents=True)
    escribir(tmp_path, yaml.safe_load((FIX / "valido.yaml").read_text(encoding="utf8")))
    return tmp_path


def escribir(raiz, preguntas, modulo="03-modelos-fundacionales", curso="aif-c01"):
    d = raiz / "cursos" / curso / "modulos" / modulo
    d.mkdir(parents=True, exist_ok=True)
    (d / "preguntas.yaml").write_text(yaml.safe_dump(preguntas, allow_unicode=True), encoding="utf8")


def segundo_curso(raiz, slug="otro-curso"):
    """Crea un curso con dominios 1–2 distintos de AIF-C01, un módulo y 1 pregunta válida del dominio 2."""
    c = raiz / "cursos" / slug
    (c / "fuentes").mkdir(parents=True)
    (c / "modulos" / "01-base").mkdir(parents=True)
    (c / "curso.yaml").write_text(
        f"slug: {slug}\ntitulo: Curso de prueba\nidioma: es-ES\ndominios:\n"
        '  - {id: 1, nombre: "Uno", peso: 40}\n  - {id: 2, nombre: "Dos", peso: 60}\n'
        "banco:\n  minimo_por_modulo: 1\n", encoding="utf8")
    (c / "fuentes" / "dominio-2.md").write_text("# D2\n\n## Task Statement 2.1\n\nTexto.\n", encoding="utf8")
    p = yaml.safe_load((FIX / "valido.yaml").read_text(encoding="utf8"))[0]
    p.update(id="D2-001", dominio=2, tarea="2.1")
    escribir(raiz, [p], "01-base", slug)
    (c / "modulos" / "01-base" / "README.md").write_text("# Base\n\nTexto del otro curso.\n", encoding="utf8")
    return c


# ---------------------------------------------------------------- consola web
import re  # noqa: E402

PASSWORD = "contraseña-de-prueba-1"


@pytest.fixture
def curso(repo):
    """Repositorio con aif-c01: módulo 03 con teoría, servicios y preguntas, y simulacro de 3 preguntas (1 minuto)."""
    base_curso = repo / "cursos" / "aif-c01"
    m = base_curso / "modulos" / "03-modelos-fundacionales"
    (m / "README.md").write_text(
        "# Modelos fundacionales\n\nTexto con <script>alert(1)</script> y [malo](javascript:alert(1)).\n\n"
        "```mermaid\nflowchart LR\n  A --> B\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |\n", encoding="utf8")
    (m / "servicios.md").write_text("# Servicios\n\nAmazon Bedrock.\n", encoding="utf8")
    base = yaml.safe_load((FIX / "valido.yaml").read_text(encoding="utf8"))[:3]
    sim = []
    for k, p in enumerate(base, 1):
        q = dict(p)
        q["id"] = f"S-{k:03d}"
        sim.append(q)
    escribir(repo, sim, "06-simulacro")
    f = base_curso / "curso.yaml"
    f.write_text(f.read_text(encoding="utf8").replace("preguntas: 65", "preguntas: 3").replace("minutos: 90", "minutos: 1")
                 .replace("minimo_simulacro: 65", "minimo_simulacro: 3"), encoding="utf8")
    return repo


@pytest.fixture
def app(curso, tmp_path):
    from app.config import Settings
    from app.main import create_app

    s = Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/app.db", courses_dir=curso / "cursos",
                 schemas_dir=curso / "schemas", login_max_intentos=3)
    return create_app(s)


def crear_usuario(app, username="ana", rol="estudiante", password=PASSWORD, debe_cambiar=False, activo=True, cursos=("aif-c01",)):
    from app.models import Matricula, Usuario
    from app.security import hashear

    with app.state.sesiones() as db:
        u = Usuario(username=username, nombre=username.capitalize(), rol=rol, password_hash=hashear(password),
                    activo=activo, debe_cambiar_password=debe_cambiar)
        db.add(u)
        db.flush()
        if rol == "estudiante":
            for s in cursos:
                db.add(Matricula(usuario_id=u.id, curso=s))
        db.commit()
        return u.id


def token(cliente, ruta="/login") -> str:
    html = cliente.get(ruta).text
    return re.search(r'name="csrf" value="([^"]+)"', html).group(1) or ""


def entrar(app, username="ana", password=PASSWORD):
    from fastapi.testclient import TestClient

    c = TestClient(app)
    r = c.post("/login", data={"username": username, "password": password, "csrf": token(c)}, follow_redirects=False)
    assert r.status_code == 303, r.text
    return c


def post(cliente, ruta, ruta_token="/", **datos):
    datos["csrf"] = token(cliente, ruta_token)
    return cliente.post(ruta, data=datos, follow_redirects=False)


@pytest.fixture
def app_dos(curso, tmp_path):
    """Consola con dos cursos: aif-c01 y otro-curso (dominios 1–2)."""
    from app.config import Settings
    from app.main import create_app

    segundo_curso(curso)
    s = Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/dos.db", courses_dir=curso / "cursos",
                 schemas_dir=curso / "schemas", login_max_intentos=3)
    return create_app(s)
