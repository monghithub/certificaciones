## Context

El repositorio contiene solo `promt.md` (especificación del curso), `.claude/` y `openspec/`. La Iteración 0 debe dejar listo el andamiaje y las herramientas de calidad para que las iteraciones 1–6 solo añadan contenido. El revisor es un arquitecto sénior; el destinatario del curso, un perfil junior. Todo dato sobre AWS debe ser trazable a la guía oficial y las dudas se marcan con `> ⚠️ PENDIENTE DE VERIFICAR:`.

## Goals / Non-Goals

**Goals:**
- Estructura del repositorio exactamente como la sección 5 de `promt.md` (los módulos 00–06 como directorios con `.gitkeep`).
- Fuentes oficiales transcritas literalmente (en inglés, tal como las publica AWS) y fechadas.
- Esquema + validador + quiz funcionales y probados con fixtures.
- CI que ejecute las cuatro comprobaciones de la sección 9.

**Non-Goals:**
- Redactar teoría, preguntas reales, laboratorios, glosario o chuleta.
- Publicar la versión `v1.0.0` o crear ramas por módulo.
- Parafrasear o traducir las tareas oficiales dentro de `fuentes/` (la traducción vive en los módulos).

## Decisions

1. **Esquema JSON en `schemas/pregunta.schema.json` (draft 2020-12), validado con `jsonschema`.** Un único esquema con `oneOf`/`if-then` por `tipo` para validar la forma de `correctas` (lista de ids; lista ordenada; lista de pares `[prompt_id, opcion_id]`). Alternativa: Pydantic; descartada porque la sección 5 exige un JSON Schema explícito reutilizable.

2. **Matching y ordering requieren campos adicionales.** El ejemplo de la sección 7 solo cubre `multiple_choice`. Para `matching` se añade `prompts: [{id, texto}]` (columna izquierda) junto a `opciones` (columna derecha); `correctas` son pares `[prompt_id, opcion_id]`. Para `ordering`, `correctas` es la lista ordenada de ids de `opciones` (3–5 elementos). `multiple_choice` tiene exactamente 1 correcta; `multiple_response`, ≥2. `matching` tiene 3–7 pares. Esta ampliación se documenta en `AGENTS.md` y en el esquema.

3. **`distractores` obligatorio para cada opción no correcta** (en `matching`, para cada opción no usada en ningún par; si todas se usan, puede quedar vacío). En `ordering` no hay distractores: la explicación justifica el orden.

4. **El validador es un único script sin dependencias propias salvo `pyyaml` y `jsonschema`.** Recorre `modulos/*/preguntas.yaml`, acumula todos los errores (no aborta al primero), imprime `fichero:id: mensaje` y sale con código 1 si hay alguno. La existencia de `tarea` se resuelve parseando `fuentes/dominio-N.md` con una regex sobre encabezados `Task Statement N.M` (formato fijado en la transcripción). La distribución por tipos (60/20/10/10 %) se informa y emite aviso fuera de tolerancia (±10 puntos) para bancos con ≥30 preguntas; no es error, porque la sección 7 dice "aproximada". Mínimo de 30 preguntas por módulo de dominio y 65 en el simulacro: error. Con `--sin-minimos` para fixtures/iteraciones intermedias; en CI los mínimos se aplican solo a módulos cuyo `preguntas.yaml` existe y no está vacío. Prohibido "todas/ninguna de las anteriores" (regex insensible a mayúsculas) y `id` con formato `D<dominio>-NNN` (simulacro: `S-NNN` con campo `dominio` 1–5).

5. **`quiz.py` con solo biblioteca estándar + `pyyaml`.** Opciones: `--modulo`, `--dominio`, `--n`, `--tipo`, `--semilla`. Muestra pregunta, recoge respuesta (letras; ordering: secuencia `c,a,b`; matching: `1=b,2=a`), muestra explicación y distractores, y puntuación final. La lógica de corrección se separa en funciones puras para poder testear sin E/S.

6. **Tests con `pytest` en `tests/` con fixtures YAML válidos e inválidos.** No se cuentan en la estructura oficial, pero el CI los ejecuta. Alternativa: sin tests; descartada porque el validador es la puerta de calidad de todo el curso.

7. **Transcripción de fuentes por descarga real de las páginas oficiales.** Se usa `curl`/WebFetch sobre las URLs de la sección 3 y se vuelca el texto literal. Cada `fuentes/dominio-N.md` lleva: URL, fecha de consulta, y secciones `## Task Statement N.M` con la lista de *skills* y *objectives* tal cual. Si la página no es accesible, se deja `> ⚠️ PENDIENTE DE VERIFICAR:` y no se inventa.

8. **CI en un único job Ubuntu**: `markdownlint-cli2` (config `.markdownlint-cli2.yaml` que excluye `fuentes/` si el texto literal rompe reglas y `openspec/`, `.claude/`), `lycheeverse/lychee-action`, `pip install pyyaml jsonschema pytest` + `python scripts/validar_preguntas.py`, y un paso `grep -rn` que emite `::warning` con `continue-on-error` implícito (siempre exit 0).

9. **Revalidación de datos de la sección 4** antes de crear ficheros: se contrastan duración, nº de preguntas, puntuación, tipos, coste, validez y pesos con la guía oficial. Las diferencias van a `CHANGELOG.md` y se propagan a `README.md`/`AGENTS.md`.

## Risks / Trade-offs

- [La estructura HTML de la guía puede variar o requerir JS] → Intentar descarga directa; si falla, WebFetch; si tampoco, marcar PENDIENTE y detener para revisión humana.
- [Los datos de la sección 4 pueden haber cambiado] → Prevalece la guía oficial; se registra en `CHANGELOG.md`.
- [Formato de `matching`/`ordering` no definido en `promt.md`] → Decisión 2; sujeto a revisión humana al cierre de la iteración.
- [`lychee` dará falsos positivos sobre URLs de AWS con límites de tasa] → Configurar reintentos y `accept = [200, 429]`.
- [markdownlint sobre texto literal de AWS] → Excluir o relajar reglas en `fuentes/` solo si es necesario.

## Open Questions

- ¿Licencia deseada para `LICENSE`? Por defecto, MIT para el código y CC BY 4.0 para el contenido, a confirmar en la revisión.
- ¿Nombre final del repositorio/directorio raíz (`aif-c01-curso` en `promt.md` vs. `aw-saif-c01` actual)? Se mantiene el actual y se ajustan los enlaces del README.
