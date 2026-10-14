## Why

El curso AIF-C01 se publicará como Markdown y YAML en el repositorio, pero estudiar así no permite seguir el avance de cada alumno ni hacer los tests con comodidad. Se necesita una consola web donde los estudiantes recorran el índice, lean los módulos y hagan los cuestionarios, y donde un administrador gestione los usuarios y vea sus estadísticas y por dónde van.

## What Changes

- Nueva aplicación web (`app/`) con FastAPI, SQLite y plantillas HTML con HTMX, empaquetada con Docker (`docker compose`).
- Autenticación con usuario y contraseña propios, con roles `admin` y `estudiante`. No hay registro público: solo el admin da de alta usuarios.
- Panel de administración: alta, edición, desactivación y restablecimiento de contraseña de usuarios; consulta del progreso y estadísticas de cada uno.
- Navegación del curso: índice de módulos, renderizado de `README.md`, `servicios.md`, `trampas.md` y `laboratorio.md` (con diagramas Mermaid), y marca de "lo último que leyó".
- Motor de tests: cuestionarios por módulo, dominio o simulacro, con los cuatro tipos de pregunta, corrección, explicaciones y modo simulacro cronometrado (65 preguntas / 90 minutos).
- Estadísticas del estudiante: progreso por módulo, aciertos por dominio y tarea, historial de intentos.
- Importación de contenido desde los ficheros del repositorio (única fuente de verdad); la app no edita el contenido del curso.
- **Dependencia**: reutiliza `schemas/pregunta.schema.json` y la lógica de corrección de la Iteración 0 (`iteracion-0-fundacion-curso`). Se implementa después de ella.
- Fuera de alcance: SSO, edición de contenido desde la web, despliegue en AWS, correo electrónico.

## Capabilities

### New Capabilities
- `auth-roles`: inicio y cierre de sesión, sesiones seguras y control de acceso por rol.
- `user-admin`: alta, edición, desactivación y gestión de contraseñas de usuarios por el admin.
- `course-navigation`: índice del curso, lectura de módulos y seguimiento de la última posición.
- `quiz-engine`: cuestionarios, corrección, simulacro cronometrado y registro de intentos.
- `progress-stats`: estadísticas y progreso por estudiante, y vista de administración.
- `deployment`: contenedor, `docker compose`, configuración por variables de entorno y copias de seguridad.

### Modified Capabilities
<!-- Ninguna. -->

## Impact

- Código nuevo en `app/` (Python 3.12, FastAPI, SQLAlchemy, Jinja2, HTMX), `Dockerfile` y `compose.yaml`; el CI se amplía con tests de la app.
- Almacena datos personales (usuarios y su actividad): contraseñas con hash, sesión con cookie `HttpOnly`/`SameSite`, protección CSRF y sin secretos en el repositorio.
- Requiere que existan `modulos/*` y `preguntas.yaml`; con el contenido vacío la app funciona con fixtures.
