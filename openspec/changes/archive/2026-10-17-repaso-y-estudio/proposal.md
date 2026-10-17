## Why

El usuario quiere estudiar haciendo tests: «la idea es revisar conocimientos y estudiar a base de los test… que haciendo test se vayan quedando los conocimientos». Hoy solo hay preguntas de examen (escenarios largos) en los módulos 01–05 y ninguna en el módulo 00. Además pide que en todos los tests, también en los de examen, se pueda ver la explicación de cada pregunta al responderla: el simulacro solo la muestra al terminar.

## What Changes

- **Banco de repaso** por módulo (`modulos/NN-*/repaso.yaml`, ids `RN-NNN`): preguntas directas de conocimiento (un concepto, servicio o criterio por pregunta) para fijar lo leído antes de las de examen. Módulo 00 con preguntas de los conocimientos previos CP.1–CP.4 (dominio 0, tarea `CP`); módulos 01–05 con al menos 2 preguntas por objetivo oficial. Su contenido sale de la teoría ya verificada del módulo.
- **Esquema:** ids `R…`, dominio 0 y tarea/objetivo `CP`/`CP.N` para los conocimientos previos.
- **Manifiesto:** bloque `repaso` (mínimo por módulo, mínimo por objetivo y fuente de los conocimientos previos).
- **Validador y cobertura:** validan `repaso.yaml` (esquema, ids únicos en todo el curso, mínimos, cobertura por objetivo, sin copiar enunciados de los bancos de examen). El aviso de «enunciado muy corto» no se aplica al repaso.
- **Consola:**
  - Página de tests ordenada como ruta de estudio: 1) repaso de conocimientos (por módulo o todos), 2) preguntas de examen (por módulo, dominio o mixto), 3) repetir falladas, 4) simulacro.
  - Modo **repetir falladas**: preguntas (de repaso y de examen, no del simulacro) cuya última respuesta del usuario fue incorrecta.
  - Tras responder cada pregunta, en todos los modos: resultado, solución y un desplegable **«Ver explicación»** (explicación, por qué fallan las otras opciones, referencia oficial y enlace a la sección de teoría que cubre el objetivo).
  - Simulacro con casilla **«Modo estudio»**: muestra la corrección y la explicación pregunta a pregunta; sin marcarla se mantiene como hasta ahora.
  - Estadísticas: el dominio 0 se muestra como «Conocimientos previos».
- **CLI:** `quiz.py --repaso`.
- Documentación (`AGENTS.md` con las reglas del banco de repaso, README del curso, `docs/consola.md`, CHANGELOG, journal) y pruebas.

## Capabilities

### New Capabilities
- `banco-repaso`: bancos de repaso de conocimientos por módulo, incluido el módulo 00.

### Modified Capabilities
- `quiz-engine`: modos repaso y repetir falladas, explicación tras cada respuesta en todos los modos y modo estudio del simulacro.
- `question-validation`: validación y cobertura de los bancos de repaso.
- `question-bank-schema`: ids de repaso, dominio 0 y tarea `CP`.

## Impact

- Código: `schemas/`, `curso/manifiesto.py`, `curso/cobertura.py` (nuevo), `app/content.py`, `app/routes/quiz.py`, plantillas, `scripts/validar_preguntas.py`, `scripts/comprobar_cobertura.py`, `scripts/quiz.py`; sin migración de base de datos (el modo estudio del simulacro se guarda en `filtro`).
- Contenido: seis `repaso.yaml` (≈ 220 preguntas) y `curso.yaml`.
- Git: rama `aif-c01/repaso` con PR a `main`.
