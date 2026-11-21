## 0. Antes de empezar

- [x] 0.1 Leer `proposal.md`, `design.md` y `specs/consultas-claude/spec.md` de este cambio, y `AGENTS.md` raíz (flujo y reglas del repositorio)
- [x] 0.2 El usuario aprobó la propuesta (2026-11-21: «hazlo todo», que incluía la issue #40)
- [x] 0.3 Rama propia desde `main` (esta propuesta vive en `feat/consultas-claude`)

## 1. Consola

- [x] 1.1 `CONSULTAS_TOKEN` en `app/config.py` (`Settings.consultas_token`, mínimo 32 caracteres si se define) y en `.env.example`
- [x] 1.2 Modelos `Consulta` y `ConsultaMensaje` en `app/models.py` y migración `migrations/versions/0003_consultas.py`
- [x] 1.3 `app/routes/consultas.py`: panel (fragmento htmx con sondeo cada 5 s si hay pendientes), envío, «Mis dudas» y conversación; solo `admin`; con CSRF; registrar el router en `app/main.py` solo si hay token
- [x] 1.4 API interna con `Authorization: Bearer` (`siguiente`, `respuesta`, `reintentar`, `error`), 404 sin token correcto, fuera del CSRF de cookie, recuperación de mensajes `procesando` de más de 15 min
- [x] 1.5 Plantillas: panel en `pregunta.html` (antes y después de responder, todos los modos) y en `resultado.html`; `dudas.html`; enlace «Mis dudas» en `base.html`; Markdown sin HTML en las respuestas
- [x] 1.6 Pruebas en `tests/app/test_app_consultas.py`: desactivado por defecto, estudiante 403, CSRF, una conversación por pregunta, un pendiente a la vez, API con token correcto/incorrecto/ausente, ciclo `siguiente` → `respuesta`, `reintentar`, `error` y «Reintentar», recuperación de `procesando` caducado, panel con y sin sondeo, `respondida` y `respuesta_usuario` en el JSON

## 2. Trabajador

- [x] 2.1 `scripts/consultas_trabajador.py` (biblioteca estándar): configuración por entorno, bucle de sondeo, prompt del primer mensaje (sin solución si no ha respondido), `--resume` en los siguientes con caída a sesión nueva, herramientas de solo lectura, `cwd` fijo, timeout, cuota agotada → `reintentar` y espera, 3 errores → `error`, SIGTERM
- [x] 2.2 Comprobar en titan con `claude --help` y una llamada real que `-p` con `--tools "Read,Grep,Glob,WebFetch,WebSearch"` y `--add-dir` no se queda pidiendo permisos (`permission_denials` vacío); ajustar con `--allowedTools`/`--permission-mode` sin usar `--dangerously-skip-permissions`
- [x] 2.3 Pruebas en `tests/test_consultas_trabajador.py` con un `claude` simulado (script que imprime el JSON de `design.md`) y la API simulada: primer mensaje, `--resume`, sesión perdida, cuota agotada, timeout, error repetido, solución omitida si no ha respondido

## 3. Cierre y despliegue

- [x] 3.1 `docs/consola.md` (cómo activarlo, el trabajador, riesgos), `.env.example`, `CHANGELOG.md` y `docs/journal.md`
- [x] 3.2 Validadores y pruebas: `python scripts/validar_preguntas.py && python scripts/comprobar_cobertura.py --preguntas && python -m pytest`; markdownlint
- [x] 3.3 PR, CI en verde y fusión; archivar este cambio de OpenSpec (`openspec/changes/archive/<fecha>-consultas-claude`) y crear `openspec/specs/consultas-claude/spec.md`
- [x] 3.4 titan: `CONSULTAS_TOKEN` en el `.env` del despliegue y en su `compose.yaml`, `./desplegar.sh`, servicio de usuario `consultas-claude` (unidad en `design.md`), prueba de extremo a extremo de `design.md`
- [x] 3.5 Inventario de `~/Sistema` según su `CLAUDE.md`: `registro.md`, `aplicaciones.md` si procede, commit con rutas propias
- [x] 3.6 Cerrar la issue de seguimiento con el resumen
