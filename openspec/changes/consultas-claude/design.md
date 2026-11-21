## Context

Guía de implementación autocontenida: quien la implemente (persona u otra IA) no necesita la conversación en la que se decidió. Las decisiones del usuario están marcadas como tales y **no se cambian sin preguntarle**.

### Estado de partida (2026-11-21)

- Consola FastAPI + Jinja2 + htmx (`app/`), SQLite con SQLAlchemy y Alembic (`migrations/versions/0001`, `0002`), sesión firmada con CSRF (`app/security.py`, `app/deps.py:verificar_csrf`; htmx manda la cabecera `X-CSRF-Token` desde `base.html`).
- Rutas en `app/routes/*.py`, registradas en `app/main.py` (tupla de routers, línea ~70). Dependencias útiles: `requiere_usuario`, `requiere_admin`, `requiere_curso`, `get_db` (`app/deps.py`); render con `app/web.py:render`.
- Tests: `app/routes/quiz.py`. Página de pregunta `app/templates/pregunta.html` (recibe `p` = `vista_pregunta(c, pid)`, `i` = intento, `n`, `respondida`, `retro`); resultado `app/templates/resultado.html`.
- Preguntas en memoria: `Contenido.preguntas[pid]` con `banco` = `repaso` | `examen` | `libros` (el banco `libros` solo existe en titan, ver PR #39), `modulo`, `objetivo`, `explicacion`, `distractores`, `referencia` (opcional en `libros`). Sección de teoría de un objetivo: `Contenido.url_teoria(objetivo)`.
- Despliegue en titan: `~/Sistema/aplicaciones/certificaciones/` con `desplegar.sh` (clona `main` en `src/`, `docker compose up -d --build`), `compose.yaml` (puerto `127.0.0.1:8097`, `./src/cursos:/cursos:ro`, `./data:/data`), `.env` con `SECRET_KEY` y `ACCESO_LIBRE_USUARIO=admin`. Libros en Markdown en `~/Sistema/aplicaciones/certificaciones/libros-md/aif-c01/` (fuera de git, copyright).
- Claude Code en titan: `/home/monghit/.local/bin/claude` (2.1.330), con la sesión de la cuenta del usuario. Linger de systemd activo para `monghit` (hay servicios de usuario, por ejemplo `laya-enrutador.service`).

### Comportamiento verificado de `claude -p` (2026-11-21)

```bash
cd <DIR_FIJO> && claude -p "<mensaje>" --model sonnet --output-format json --tools "<herramientas>"
cd <DIR_FIJO> && claude -p "<mensaje>" --resume <session_id> --model sonnet --output-format json --tools "<herramientas>"
```

- Salida: un objeto JSON con, entre otros, `type: "result"`, `subtype: "success"`, `is_error: false`, `result` (texto de la respuesta, en Markdown), `session_id`, `terminal_reason`, `total_cost_usd`, `permission_denials`.
- `--resume` conserva la conversación y devuelve el mismo `session_id`.
- **Las sesiones se guardan por directorio de trabajo** (`~/.claude/projects/<ruta-del-cwd>/`): hay que lanzar siempre desde el **mismo** directorio, o `--resume` no encuentra la sesión.
- No se ha podido provocar el error de cuota agotada: detectarlo por `is_error: true` o código de salida ≠ 0 **y** texto que contenga `limit` / `usage limit` / `rate limit` / `overloaded` (sin distinguir mayúsculas). Ante la duda, tratarlo como transitorio.

## Goals / Non-Goals

**Goals:** resolver dudas en conversación sin bloquear el test; que funcione aunque Claude tarde o la cuota esté agotada; no exponer la cuenta a otros usuarios.

**Non-Goals:** streaming; API de Anthropic con clave; que Claude modifique el curso o el sistema; varios trabajadores en paralelo; notificaciones fuera de la consola.

## Decisions

### Decisiones del usuario (no cambiar sin preguntar)

1. **Cuándo:** «siempre»: en todos los modos (repaso, examen, mixto, dominio, falladas, libros y simulacro, también el cronometrado), antes y después de responder, y en la página de resultado.
2. **Modelo:** Sonnet (`--model sonnet`).
3. **Quién:** solo usuarios con rol `admin` (usa la cuenta de Claude del responsable).
4. **Fuentes:** teoría del curso, documentación oficial de AWS en la web y libros en Markdown de `libros-md`.

### Activación

- `Settings.consultas_token: str | None` desde `CONSULTAS_TOKEN` (vacío = `None`). Exigir al menos 32 caracteres si se define (`ConfiguracionError` si no).
- Sin token: no se registran las rutas de consultas ni se pinta el panel (pasar `consultas=bool(settings.consultas_token) and usuario.rol == "admin"` al contexto de las plantillas; lo más simple es calcularlo en `render` o en las rutas de `quiz.py`).

### Modelo de datos (migración `0003_consultas.py`, `down_revision = "0002"`)

```text
consulta
  id               PK
  usuario_id       FK usuario.id ON DELETE CASCADE, índice
  curso            String(64)
  pregunta_id      String(64)
  intento_id       FK intento.id ON DELETE SET NULL, nullable   (el intento desde el que se abrió la primera vez)
  sesion_claude    String(64), nullable                         (session_id de Claude Code)
  creada, actualizada  DateTime
  UNIQUE (usuario_id, curso, pregunta_id)                       (una conversación por pregunta y usuario)

consulta_mensaje
  id               PK
  consulta_id      FK consulta.id ON DELETE CASCADE, índice
  rol              String(16): "usuario" | "claude"
  texto            Text
  estado           String(16): "pendiente" | "procesando" | "respondido" | "error"   (solo tiene sentido en rol "usuario")
  intentos         Integer, default 0
  error            Text, nullable
  respondida_por   FK consulta_mensaje.id, nullable              (en el mensaje de Claude: a qué mensaje responde)
  creado           DateTime
```

Añadir las clases `Consulta` y `ConsultaMensaje` a `app/models.py` con la misma convención que `Intento`/`IntentoRespuesta` (relación `mensajes` ordenada por `id`).

### Rutas del navegador (`app/routes/consultas.py`, nuevo; `dependencies=[Depends(verificar_csrf)]`; todas con `requiere_admin` y `requiere_curso`)

| Método y ruta | Qué hace |
|---|---|
| `GET /c/{curso}/consultas/{pid}/panel?intento=<iid>` | Fragmento HTML del panel (conversación + formulario). Si hay algún mensaje `pendiente`/`procesando`, el contenedor lleva `hx-get` a sí mismo con `hx-trigger="every 5s"` y `hx-swap="outerHTML"`; si no, sin sondeo. |
| `POST /c/{curso}/consultas/{pid}` (campos `texto`, `intento` opcional) | Crea la `consulta` si no existe y un `consulta_mensaje` (`usuario`, `pendiente`). Texto de 1 a 2000 caracteres. Devuelve el panel (htmx) o redirige a la pregunta. Máximo 1 mensaje pendiente por conversación (si ya hay uno, error amable). |
| `GET /c/{curso}/dudas` | «Mis dudas»: lista de conversaciones del usuario (pregunta, último mensaje, estado, fecha) con enlace a la conversación. |
| `GET /c/{curso}/dudas/{cid}` | Conversación completa a página entera, con el enunciado, la solución y la explicación de la pregunta y el mismo panel. |

- El `pid` debe existir en `Contenido.preguntas` (404 si no).
- Renderizar las respuestas de Claude como Markdown **sin HTML** (`MarkdownIt("commonmark", {"html": False}).enable("table")`, como `app/content.py:_md`, sin la regla de conceptos) y con `rel="noopener noreferrer"` y `target="_blank"` en los enlaces.
- Enlace «Mis dudas» en la cabecera (`base.html`) solo si `consultas` es verdadero.

### API interna para el trabajador (en el mismo router o en otro sin CSRF ni sesión)

Autenticación: cabecera `Authorization: Bearer <CONSULTAS_TOKEN>`, comparada con `hmac.compare_digest`. Sin token configurado o token incorrecto → **404** (no revelar que existe). Excluir estas rutas del CSRF (no usan cookie).

| Método y ruta | Qué hace |
|---|---|
| `POST /api/consultas/siguiente` | Toma el mensaje `pendiente` más antiguo (o un `procesando` con `actualizado` > 15 min, por si el trabajador murió), lo pasa a `procesando`, suma 1 a `intentos` y devuelve el JSON de abajo. Si no hay ninguno, `204`. |
| `POST /api/consultas/mensajes/{mid}/respuesta` | Cuerpo `{"texto": "...", "sesion_claude": "..."}`: crea el mensaje `claude`, marca el del usuario `respondido`, guarda `sesion_claude` en la consulta. |
| `POST /api/consultas/mensajes/{mid}/reintentar` | Cuerpo `{"motivo": "..."}`: vuelve a `pendiente` (cuota agotada o error transitorio). |
| `POST /api/consultas/mensajes/{mid}/error` | Cuerpo `{"motivo": "..."}`: estado `error` con el motivo (se muestra en el panel con un botón «Reintentar» que lo devuelve a `pendiente`). |

JSON de `siguiente`:

```json
{
  "mensaje_id": 12,
  "consulta_id": 5,
  "sesion_claude": null,
  "texto": "¿Por qué no es Textract?",
  "curso": "aif-c01",
  "pregunta": {
    "id": "D1-023", "banco": "examen", "modulo": "01-fundamentos-ia-ml", "origen": null,
    "enunciado": "...", "tipo": "multiple_choice",
    "opciones": [{"id": "a", "texto": "..."}], "prompts": null,
    "correctas": ["b"], "explicacion": "...", "distractores": {"a": "..."},
    "referencia": "https://docs.aws.amazon.com/...",
    "teoria_url": "/c/aif-c01/modulo/01-fundamentos-ia-ml/teoria#...",
    "teoria_fichero": "modulos/01-fundamentos-ia-ml/README.md"
  },
  "respuesta_usuario": ["a"],
  "respondida": true
}
```

`respuesta_usuario`/`respondida`: la última respuesta del usuario a esa pregunta en el `intento_id` de la consulta (tabla `intento_respuesta`), o `null`/`false`.

### Trabajador (`scripts/consultas_trabajador.py`, en el repositorio; solo biblioteca estándar)

Configuración por variables de entorno:

| Variable | Por defecto | Uso |
|---|---|---|
| `CONSULTAS_URL` | `http://127.0.0.1:8097` | Base de la consola |
| `CONSULTAS_TOKEN` | — (obligatoria) | El mismo que en el `.env` de la consola |
| `CONSULTAS_CLAUDE` | `claude` | Ruta del ejecutable (en titan `/home/monghit/.local/bin/claude`) |
| `CONSULTAS_MODELO` | `sonnet` | Decisión del usuario |
| `CONSULTAS_DIR` | `~/.local/share/consultas-claude` | Directorio de trabajo **fijo** (las sesiones dependen de él) |
| `CONSULTAS_CURSOS` | — | Carpeta `cursos/` desplegada (en titan `~/Sistema/aplicaciones/certificaciones/src/cursos`) |
| `CONSULTAS_LIBROS` | — (opcional) | En titan `~/Sistema/aplicaciones/certificaciones/libros-md` |
| `CONSULTAS_ESPERA` | `10` | Segundos entre sondeos sin trabajo |
| `CONSULTAS_ESPERA_CUOTA` | `900` | Segundos de espera tras cuota agotada o error transitorio |
| `CONSULTAS_TIMEOUT` | `300` | Tiempo máximo de cada llamada a Claude |

Bucle: `POST siguiente` → si `204`, dormir `CONSULTAS_ESPERA` → si hay mensaje, llamar a Claude → `respuesta` / `reintentar` (y dormir `CONSULTAS_ESPERA_CUOTA`) / `error` (si `intentos` ≥ 3 o fallo no transitorio). Registrar en stdout (journald) una línea por mensaje: id, duración, coste (`total_cost_usd`), resultado. Señales: terminar limpio con SIGTERM.

Llamada (con `subprocess.run`, lista de argumentos, **nunca** `shell=True`; el mensaje se pasa por stdin o como argumento, sin interpolar en una shell):

```text
cwd = CONSULTAS_DIR
claude -p <prompt> --model sonnet --output-format json
       --tools "Read,Grep,Glob,WebFetch,WebSearch"
       --add-dir <CONSULTAS_CURSOS>/<curso> [--add-dir <CONSULTAS_LIBROS>]
       --append-system-prompt <instrucciones fijas>
       [--resume <sesion_claude>]
```

- Comprobar con `claude --help` en titan que esa combinación no pide permisos interactivos en `-p` (si `permission_denials` no está vacío o se queda esperando, añadir `--allowedTools` con las mismas herramientas o `--permission-mode` adecuado). **No** usar `--dangerously-skip-permissions`.
- Primer mensaje (sin `sesion_claude`): el prompt incluye el contexto completo (bloque «Pregunta» con enunciado, opciones, si ya respondió o no, y en ese caso su respuesta, la solución, la explicación, los distractores y la referencia; ruta del fichero de teoría) y al final la duda. Si `respondida` es falso, **no** incluir la solución en el prompt salvo que la duda la pida expresamente (palabras como «solución», «respuesta correcta», «cuál es»); así Claude no puede revelarla sin querer. Mensajes siguientes: solo la duda nueva (`--resume`).
- Si `--resume` falla porque la sesión no existe (directorio cambiado, sesión borrada), reintentar una vez como primer mensaje (con contexto) y guardar la sesión nueva.

Instrucciones fijas (`--append-system-prompt`), en español:

```text
Eres el tutor de la consola de estudio del curso {curso} (certificación AWS Certified AI Practitioner, nivel foundational).
Respondes dudas sobre una pregunta de test concreta, en español de España, claro y breve (máximo ~250 palabras salvo que pidan más),
manteniendo en inglés los nombres de servicios y términos del examen.
- Si el estudiante aún no ha respondido, orienta sin revelar la respuesta correcta, salvo que la pida expresamente.
- Apóyate en la teoría del curso (ficheros en {cursos}/{curso}/modulos y glosario.yaml) y verifica los datos en la documentación
  oficial de AWS (docs.aws.amazon.com, aws.amazon.com). Termina con la URL oficial que respalda lo principal.
- Los libros de {libros} son material de terceros de 2025: úsalos solo para entender el tema; si chocan con la documentación vigente,
  prevalece la documentación, y no cites el libro como fuente.
- Si detectas un error en la pregunta o en el curso, dilo claramente al final con «Posible error en el curso:».
- No ejecutes nada ni modifiques ficheros: solo lees y buscas.
```

### Interfaz

- **Panel** en `pregunta.html` (debajo de la tarjeta de la pregunta, también antes de responder y en el simulacro) y en cada pregunta de `resultado.html` (plegado con `<details>`): título «Preguntar a Claude», conversación (mensajes del usuario y de Claude, estados «En cola», «Pensando…», «Error: …» con «Reintentar»), `textarea` y botón «Enviar». Carga con `hx-get` del fragmento al abrir la página.
- Aviso fijo pequeño: «Responde Claude con la cuenta del responsable; puede equivocarse: prevalece la documentación oficial de AWS.»
- El formulario usa `hx-post` y `hx-target` al panel; no debe romper el `hx-boost` de la página ni enviar la respuesta del test.

### Despliegue en titan

1. `.env` de `~/Sistema/aplicaciones/certificaciones/`: `CONSULTAS_TOKEN=<openssl rand -hex 32>` y pasar la variable al contenedor en `compose.yaml` (`CONSULTAS_TOKEN: ${CONSULTAS_TOKEN:-}`), tanto en el del repo como en el del despliegue (comprobar cuál usa `desplegar.sh`: el de `~/Sistema/aplicaciones/certificaciones/compose.yaml`).
2. `./desplegar.sh` (cambia el código: reconstruye la imagen; la migración `0003` se aplica sola al arrancar).
3. Servicio de usuario `~/.config/systemd/user/consultas-claude.service`:

   ```ini
   [Unit]
   Description=Trabajador de «Preguntar a Claude» de la consola de certificaciones
   After=network-online.target

   [Service]
   Type=simple
   EnvironmentFile=/home/monghit/Sistema/aplicaciones/certificaciones/.env
   Environment=CONSULTAS_CLAUDE=/home/monghit/.local/bin/claude
   Environment=CONSULTAS_CURSOS=/home/monghit/Sistema/aplicaciones/certificaciones/src/cursos
   Environment=CONSULTAS_LIBROS=/home/monghit/Sistema/aplicaciones/certificaciones/libros-md
   ExecStart=/usr/bin/python3 /home/monghit/Sistema/aplicaciones/certificaciones/src/scripts/consultas_trabajador.py
   Restart=always
   RestartSec=30

   [Install]
   WantedBy=default.target
   ```

   `systemctl --user daemon-reload && systemctl --user enable --now consultas-claude`; logs con `journalctl --user -u consultas-claude -f`. Comprobar que el `PATH`/`HOME` del servicio permiten a `claude` encontrar su sesión (`~/.claude`).
4. Prueba de extremo a extremo: en `http://cursos.titan/c/aif-c01/tests`, empezar un test, preguntar una duda antes de responder (no debe revelar la solución), responder, preguntar otra (misma conversación, `--resume`), ver «Mis dudas». Parar el servicio, enviar una duda (queda «En cola»), arrancarlo y ver que se resuelve.
5. Inventario de `~/Sistema` (`CLAUDE.md` de ese repo): entrada en `registro.md`, servicio nuevo en `aplicaciones.md` si procede, commit con rutas propias.

## Risks / Trade-offs

- [Consumo de la cuota de la cuenta] → solo `admin`, una duda cada vez, modelo Sonnet, coste registrado en el log.
- [Instrucciones dentro del contenido que lee Claude (por ejemplo, de los libros)] → solo herramientas de lectura y búsqueda sobre carpetas sin secretos; la respuesta se muestra como Markdown sin HTML.
- [El token en el `.env`] → mismo trato que `SECRET_KEY`; las rutas internas responden 404 sin token correcto.
- [Acceso libre en la LAN: cualquiera entra como `admin`] → riesgo ya aceptado por el usuario para la consola; aquí implica que podrían usar su cuota. Mencionarlo en `docs/consola.md`.
- [Respuestas incorrectas] → se pide la URL oficial y el panel recuerda que prevalece la documentación.
- [Sesiones de Claude acumuladas en `~/.claude/projects/`] → aceptable; no borrar sesiones a mano.
