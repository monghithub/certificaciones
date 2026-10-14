## Why

Hoy el repositorio y la consola asumen un único curso (AIF-C01): el contenido vive en `modulos/` y `fuentes/` en la raíz, los cinco dominios están fijados en el esquema y el validador, y todos los usuarios ven lo mismo. La intención es publicar más cursos y poder dar de alta a cada usuario en los cursos que le correspondan. Conviene hacerlo ahora, antes de escribir contenido, porque mover después los módulos, las rutas y los datos de progreso sería mucho más costoso.

## What Changes

- **Estructura del repositorio:** cada curso es autocontenido en `cursos/<slug>/` (`curso.yaml`, `fuentes/`, `modulos/`, y más adelante `glosario.md` y `chuleta.md`). El contenido actual se mueve a `cursos/aif-c01/`. En la raíz quedan las herramientas comunes (`schemas/`, `scripts/`, `app/`, `curso/`, CI, Docker) y la documentación de plataforma.
- **Manifiesto `curso.yaml` por curso** (con su JSON Schema `schemas/curso.schema.json`): identificador, título, dominios con sus pesos, parámetros del simulacro (preguntas y minutos) y mínimos del banco. Sustituye a los valores fijos del AIF-C01 que hoy están en el código.
- **Esquema de preguntas generalizado:** `dominio` y el formato de `id` dejan de limitarse a 1–5 y `D1…D5`; el validador comprueba el dominio contra el manifiesto del curso.
- **Herramientas por curso:** `validar_preguntas.py` y `quiz.py` aceptan `--curso`; sin él, el validador recorre todos los cursos.
- **Consola web multicurso:**
  - Catálogo de cursos descubierto en `COURSES_DIR` (sustituye a `COURSE_DIR`).
  - **Matrícula:** el admin da de alta a cada estudiante en uno o varios cursos; el estudiante solo ve y usa los suyos; el admin accede a todos. Se mantienen los roles globales `admin` y `estudiante`.
  - Rutas con prefijo `/c/<curso>/…`; pantalla «Mis cursos» como inicio (si solo hay un curso accesible, se entra directamente).
  - Progreso de lectura, intentos y estadísticas separados por curso.
  - Panel de administración: matrículas en el alta y en el detalle de usuario, y listado de cursos con su número de matriculados.
- **Migración de datos:** los progresos e intentos existentes pasan al curso `aif-c01` y los estudiantes actuales se matriculan en él, sin pérdida de información.
- **BREAKING:** cambian las URL de la consola (`/modulo/...` → `/c/aif-c01/modulo/...`), la variable `COURSE_DIR` pasa a `COURSES_DIR` y las rutas de los ficheros de contenido incluyen `cursos/aif-c01/`.
- Fuera de alcance: crear contenido de un segundo curso, roles distintos por curso, edición de cursos desde la web y autoinscripción.

## Capabilities

### New Capabilities
- `catalogo-cursos`: estructura `cursos/<slug>/`, manifiesto `curso.yaml` y su esquema, descubrimiento de cursos y herramientas (validador, quiz) que operan por curso.
- `matricula-cursos`: matrícula de usuarios en cursos, control de acceso por curso, selector «Mis cursos» y gestión desde administración.
- `progreso-por-curso`: progreso, intentos y estadísticas ligados a un curso, y migración de los datos existentes.

### Modified Capabilities
<!-- Los requisitos de las capacidades de los cambios anteriores (aún sin archivar en openspec/specs/) se amplían aquí; se tratan como nuevas para no depender de su archivo. -->

## Impact

- Código: `app/` (configuración, carga de contenido, modelos, migración 0002, rutas, plantillas), `scripts/validar_preguntas.py`, `scripts/quiz.py`, `schemas/`, `tests/`.
- Ficheros movidos: `fuentes/` y `modulos/` → `cursos/aif-c01/`. Se actualizan `README.md`, `AGENTS.md`, `docs/consola.md`, `compose.yaml`, `Dockerfile`, `.dockerignore`, `.github/workflows/ci.yml`, `.markdownlint-cli2.yaml` y `.lychee.toml`.
- Base de datos: migración Alembic 0002 (columna `curso` en `progreso_lectura` e `intento`, tabla `matricula`). El volumen Docker existente se migra al arrancar.
- Cambio `iteracion-1-modulos-00-01` (en curso): sus rutas pasarán a `cursos/aif-c01/modulos/…`; se ajustará al terminar este cambio.
