## Context

La consola corre en un contenedor de solo lectura, sin privilegios y sin Claude Code. Claude Code (CLI 2.1.330) está instalado en titan con la sesión de la cuenta del usuario y admite el modo sin interfaz: `claude -p` con `--output-format json` (devuelve `session_id`), `--resume <id>`, `--model`, `--tools`, `--allowedTools`, `--add-dir` y `--append-system-prompt`.

## Goals / Non-Goals

**Goals:** resolver dudas en conversación sin bloquear el test; que funcione aunque Claude tarde o la cuota esté agotada; no exponer la cuenta a otros usuarios.

**Non-Goals:** respuestas en streaming; usar la API de Anthropic con clave; que Claude modifique el curso (si detecta un error, lo dice y el usuario abre una issue); varios trabajadores en paralelo.

## Decisions

- **Cola en la base de datos de la consola** y trabajador fuera del contenedor. Tablas: `consulta` (usuario, curso, pregunta, intento opcional, `sesion_claude`, fechas) y `consulta_mensaje` (rol `usuario`/`claude`, texto, estado `pendiente`/`respondido`/`error`, fechas).
- **El trabajador no toca la base de datos:** usa una API interna (`GET /api/consultas/pendientes`, `POST /api/consultas/{id}/respuesta`) con `Authorization: Bearer <CONSULTAS_TOKEN>` comparado en tiempo constante. Así no hay dos procesos escribiendo en SQLite y el contenedor sigue cerrado. Sin token configurado, las rutas no existen.
- **Contexto de cada duda:** el trabajador recibe el enunciado, las opciones, la solución, la explicación, el banco, el módulo, la sección de teoría del objetivo y, si existe, la respuesta del usuario. En el primer mensaje se construye un prompt con todo eso; los siguientes van con `--resume` sobre la misma sesión.
- **«Siempre», también antes de responder:** si el usuario aún no ha respondido, Claude orienta sin revelar la solución, salvo que se la pida expresamente. El panel no detiene el cronómetro del simulacro.
- **Herramientas de solo lectura:** `--tools "Read,Grep,Glob,WebFetch,WebSearch"` y `--add-dir` del curso desplegado y de `libros-md` (los libros no se citan como fuente; se da la URL oficial). Directorio de trabajo vacío propio del trabajador. Sin `Bash`, `Edit` ni `Write`.
- **Modelo Sonnet** (`--model sonnet`), decisión del usuario.
- **De una en una y con reintento:** tiempo máximo por duda (5 min). Si la salida indica límite de uso o error transitorio, el mensaje vuelve a `pendiente` y el trabajador espera (15 min) antes de reintentar; tras 3 errores de otro tipo queda en `error` con el motivo visible.
- **Navegador:** formulario con CSRF; mientras haya mensajes pendientes, el panel se refresca solo cada 5 s (htmx, ya incluido). Respuestas en Markdown renderizado sin HTML.
- **Solo `admin`:** el panel, «Mis dudas» y las rutas de envío exigen rol `admin`.

## Risks / Trade-offs

- [Consumo de la cuota de la cuenta] → solo `admin`, una duda cada vez y modelo Sonnet.
- [Instrucciones dentro del contenido que lee Claude (por ejemplo, de los libros)] → solo herramientas de lectura sobre carpetas sin secretos; la respuesta es texto mostrado sin HTML.
- [El token en el `.env`] → mismo trato que `SECRET_KEY`; las rutas internas responden 404 sin token correcto.
- [Respuestas incorrectas de Claude] → el prompt exige citar la URL oficial; el panel recuerda que prevalece la documentación de AWS.
