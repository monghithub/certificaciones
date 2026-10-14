## Context

El contenido del curso vive en Git como Markdown y YAML (Iteración 0 y siguientes). La consola es un consumidor de ese contenido más un almacén de usuarios y actividad. Pocos usuarios (un grupo de estudio), un único servidor, perfil de mantenimiento junior-sénior.

## Goals / Non-Goals

**Goals:**
- Un único servicio desplegable con `docker compose up`.
- Contenido siempre sincronizado con el repositorio; sin duplicar fuentes de verdad.
- Gestión de usuarios con dos roles y trazabilidad del progreso.
- Seguridad razonable por defecto (hash de contraseña, CSRF, cookies seguras, límite de intentos).

**Non-Goals:**
- Alta disponibilidad, escalado horizontal o multi-tenant.
- SSO, registro público, recuperación de contraseña por correo.
- Edición del curso desde la web.

## Decisions

1. **FastAPI + Jinja2 + HTMX, sin SPA.** Un solo lenguaje con los scripts; sin toolchain de frontend. Alternativa: Next.js, descartada por complejidad.
2. **SQLite con SQLAlchemy y Alembic.** Cero administración para pocos usuarios; el fichero se monta como volumen. Migración a Postgres posible cambiando la URL. Alternativa: Postgres desde el inicio, descartada por sobredimensionada.
3. **Contenido cargado desde el sistema de ficheros al arrancar** (`COURSE_DIR`), indexado en memoria: módulos, secciones y preguntas validadas con el esquema de la Iteración 0. Las preguntas se identifican por `id`; los intentos guardan `id` y respuesta, no copia de la pregunta. Si cambia una pregunta, los intentos históricos se conservan; si se elimina, se muestran como "pregunta retirada".
4. **Reutilizar el módulo de corrección de `scripts/quiz.py`.** Se extrae a un paquete importable (`curso/correccion.py`) usado por la CLI y la web, para evitar dos implementaciones.
5. **Autenticación propia.** Hash con argon2 (`argon2-cffi`), sesión en cookie firmada (`HttpOnly`, `SameSite=Lax`, `Secure` tras proxy TLS), CSRF por token en formularios HTMX, limitación de intentos de login por usuario e IP. El primer admin se crea con un comando `python -m app.crear_admin` o con variables de entorno en el primer arranque; nunca con credenciales por defecto. Las contraseñas temporales obligan a cambio en el primer inicio.
6. **Roles**: `admin` (gestiona usuarios, ve todas las estadísticas, también puede estudiar) y `estudiante` (solo sus datos). Autorización centralizada en dependencias de FastAPI, no en cada vista.
7. **Modelo de datos**: `usuario`, `progreso_lectura` (usuario, módulo, sección, fecha), `intento` (usuario, modo, módulo/dominio, inicio, fin, puntuación) e `intento_respuesta` (intento, pregunta_id, tarea, tipo, respuesta, correcta). Las estadísticas por dominio/tarea salen de agregaciones sobre `intento_respuesta`.
8. **Simulacro cronometrado** con selección fija de 65 preguntas del módulo 06; el servidor guarda la hora de inicio y rechaza respuestas fuera de 90 minutos. Se muestra el porcentaje de aciertos con el aviso de que no equivale a la escala 100–1.000 del examen real (aprobado con 700), cuya conversión no es pública; no se inventa ninguna equivalencia.
9. **Renderizado de Markdown** con `markdown-it-py`, sanitizado, y Mermaid cargado desde un fichero local empaquetado (sin CDN) para uso sin internet.
10. **Despliegue**: `Dockerfile` multi-stage no root, `compose.yaml` con volumen para la base de datos y montaje solo lectura del directorio del curso. Copia de seguridad: comando documentado para `sqlite3 .backup`.
11. **Tests**: pytest con `httpx` para rutas, y pruebas de autorización por rol; CI añade el job de la app.

## Risks / Trade-offs

- [SQLite con escrituras concurrentes] → Activar WAL; volumen esperado bajo.
- [Datos personales y contraseñas] → argon2, cookies seguras, sin logs de credenciales, documentar qué se guarda.
- [Contenido y base de datos desincronizados al cambiar ids] → Intentos guardan `id`; el validador de Iteración 0 impide ids duplicados.
- [El admin ve datos de todos] → Documentado; sin exportaciones masivas en esta fase.
- [Alcance creciente] → Fases: (1) auth y usuarios, (2) navegación, (3) tests, (4) estadísticas.

## Open Questions

- ¿Dominio y proxy TLS previstos (Caddy, nginx, Traefik)?
- ¿Idioma de la interfaz solo en español de España? Se asume que sí.
- ¿Cuántos usuarios esperas aproximadamente?
