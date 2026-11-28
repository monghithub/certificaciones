# Glosario: Python para backend

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## A

- **Anotación de tipo** (type hints, anotaciones de tipo). *Concepto.* Indicación del tipo de una variable, parámetro o retorno (nombre: str). Python no la comprueba al ejecutar; la usan herramientas como mypy, Pydantic o FastAPI.
  - Referencia: <https://docs.python.org/3/library/typing.html>

## B

- **Bucle de eventos** (event loop, asyncio). *Concepto.* Mecanismo de asyncio que ejecuta corrutinas en un solo hilo y cambia de una a otra cuando esperan con await. Una llamada bloqueante lo detiene para todas.
  - Referencia: <https://docs.python.org/3/library/asyncio.html>

## C

- **Corrutina** (async def, await, corrutinas). *Concepto.* Función declarada con async def que puede suspenderse con await mientras espera, cediendo el control al bucle de eventos.
  - Referencia: <https://docs.python.org/3/library/asyncio-task.html>

## D

- **Dependencia de FastAPI** (Depends, dependency_overrides). *Técnica.* Función que FastAPI ejecuta para obtener un valor que necesita la ruta (una sesión de base de datos, el usuario actual); en pruebas se sustituye con dependency_overrides.
  - Referencia: <https://fastapi.tiangolo.com/tutorial/dependencies/>

## F

- **FastAPI**. *Herramienta.* Framework web de Python que usa las anotaciones de tipo para validar peticiones con Pydantic, inyectar dependencias y generar la documentación OpenAPI.
  - Referencia: <https://fastapi.tiangolo.com/tutorial/dependencies/>
- **Fichero de bloqueo** (uv.lock, lockfile). *Concepto.* Fichero que fija las versiones exactas de todas las dependencias, directas e indirectas, para que todos los entornos instalen lo mismo.
  - Referencia: <https://docs.astral.sh/uv/concepts/projects/sync/>

## I

- **Importación diferida** (lazy import). *Concepto.* Importación que no carga el módulo hasta su primer uso (lazy import, PEP 810, Python 3.15); acelera el arranque.
  - Referencia: <https://peps.python.org/pep-0810/>

## M

- **mypy**. *Herramienta.* Comprobador estático de tipos de Python: analiza las anotaciones sin ejecutar el código.
  - Referencia: <https://mypy.readthedocs.io/en/stable/>

## P

- **Pydantic** (BaseModel). *Herramienta.* Biblioteca de validación de datos basada en anotaciones de tipo: convierte y valida la entrada y serializa la salida.
  - Referencia: <https://docs.pydantic.dev/latest/concepts/models/>
- **pydantic-settings** (BaseSettings). *Herramienta.* Extensión de Pydantic para cargar la configuración desde variables de entorno y ficheros .env, con tipos y validación.
  - Referencia: <https://docs.pydantic.dev/latest/concepts/pydantic_settings/>
- **pyproject.toml**. *Herramienta.* Fichero estándar que describe un proyecto de Python: nombre, versión de Python requerida, dependencias y configuración de herramientas.
  - Referencia: <https://packaging.python.org/en/latest/guides/writing-pyproject-toml/>

## R

- **Ruff**. *Herramienta.* Analizador estático (linter) y formateador de Python escrito en Rust, muy rápido.
  - Referencia: <https://docs.astral.sh/ruff/>

## S

- **SQLAlchemy** (Mapped, mapped_column). *Herramienta.* Biblioteca de acceso a bases de datos de Python con un ORM; desde la versión 2.0 las clases se declaran con Mapped y mapped_column, compatibles con los tipos.
  - Referencia: <https://docs.sqlalchemy.org/en/21/orm/quickstart.html>

## U

- **uv**. *Herramienta.* Gestor de proyectos y dependencias de Python de Astral: crea entornos, instala versiones de Python, resuelve dependencias y genera un fichero de bloqueo (uv.lock).
  - Referencia: <https://docs.astral.sh/uv/concepts/projects/>
