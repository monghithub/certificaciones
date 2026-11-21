> Seguimiento: [issue #40](https://github.com/monghithub/certificaciones/issues/40). Guía de implementación en `design.md`.

## Why

Durante los tests surgen dudas que la explicación de la pregunta no resuelve. El usuario quiere «hacer preguntas a la IA que resolviera en background o cuando pudiera usando una sesión en segundo plano de Claude Code con esta cuenta […] poder irlas resolviendo en el propio navegador en modo conversación».

## What Changes

- **«Preguntar a Claude»** en cada pregunta de los tests (repaso, examen, mixto, dominio, falladas, libros y simulacro, antes o después de responder; decisión del usuario: «siempre»): un panel de conversación por pregunta. La duda se guarda como pendiente, el usuario sigue con el test y la respuesta aparece sola cuando llega. Se puede seguir preguntando en la misma conversación.
- **Página «Mis dudas»** (`/c/<curso>/dudas`) con todas las conversaciones del usuario, su estado y enlace a la pregunta.
- **Solo para `admin`** (decisión del usuario: usa la cuenta de Claude del responsable). Los estudiantes no ven el panel.
- **Desactivado por defecto:** solo existe si se define `CONSULTAS_TOKEN`.
- **Trabajador en el anfitrión** (`scripts/consultas_trabajador.py`): recoge las dudas pendientes por una API interna protegida con el token, las resuelve de una en una con Claude Code sin interfaz (`claude -p`, modelo Sonnet, `--resume` para seguir la conversación) y devuelve la respuesta. Si se agota la cuota de la cuenta, espera y reintenta: las dudas quedan en cola.
- **Fuentes que puede consultar Claude** (decisión del usuario): la teoría del curso (módulos, glosario, trampas), la documentación oficial de AWS en la web y, en titan, los libros de estudio en Markdown. Solo herramientas de lectura y búsqueda; sin terminal ni edición.
- Migración `0003` (tablas de consultas), documentación y pruebas.

## Capabilities

### New Capabilities
- `consultas-claude`: dudas en conversación sobre las preguntas de los tests, resueltas en segundo plano por Claude Code.

### Modified Capabilities
- Ninguna: sin `CONSULTAS_TOKEN`, la consola no cambia.

## Impact

- Código: `app/models.py`, `migrations/versions/0003_consultas.py`, `app/routes/consultas.py` (nuevo), `app/config.py`, `app/templates/pregunta.html`, `resultado.html`, `dudas.html` (nuevo), `base.html` (enlace), `scripts/consultas_trabajador.py` (nuevo).
- Despliegue en titan: `CONSULTAS_TOKEN` en el `.env` y un servicio de usuario de systemd para el trabajador. Inventario de `Sistema`.
- Coste: cada duda consume la cuota de la cuenta de Claude, compartida con las sesiones interactivas.
