## Why

El curso AIF-C01 (ver `promt.md`) necesita una base verificable antes de redactar ningún módulo: estructura del repositorio, reglas para colaboradores, esquema del banco de preguntas, herramientas de validación y CI, y las tareas oficiales transcritas de la guía de AWS contra las que se redactará todo el contenido. La Iteración 0 (sección 11 de `promt.md`) establece ese cimiento y se detiene para revisión humana.

## What Changes

- Crear el esqueleto del repositorio: `README.md` (presentación, índice, cómo estudiar, plan de 4 semanas, recomendación de examen de práctica de Skill Builder), `AGENTS.md`, `CHANGELOG.md`, `LICENSE` y directorios `fuentes/`, `modulos/00..06`, `schemas/`, `scripts/`, `.github/workflows/`.
- Consultar la guía oficial y revalidar los datos de la sección 4 de `promt.md`; documentar en `CHANGELOG.md` cualquier discrepancia (prevalece la guía oficial).
- Transcribir literalmente a `fuentes/dominio-1..5.md` las Task Statements y habilidades oficiales, con URL y fecha de consulta. Añadir referencias a las listas de servicios in scope / out of scope.
- Definir `schemas/pregunta.schema.json` (JSON Schema) para los cuatro tipos de pregunta.
- Implementar `scripts/validar_preguntas.py`: esquema, unicidad de `id`, referencias de `correctas`, número de correctas por tipo, existencia de `tarea` en `fuentes/dominio-N.md` y distribución por tipos.
- Implementar `scripts/quiz.py`: cuestionario interactivo en terminal desde los YAML.
- Crear `.github/workflows/ci.yml`: markdownlint, comprobación de enlaces (lychee), validación de preguntas (falla ante error) y aviso (sin romper la build) por marcadores `PENDIENTE DE VERIFICAR`.
- Fuera de alcance de esta iteración: contenido de los módulos 00–06, glosario y chuleta.

## Capabilities

### New Capabilities
- `repo-docs`: estructura del repositorio y documentación base (README, AGENTS, CHANGELOG, LICENSE, convenciones).
- `official-sources`: transcripción verificable de tareas y habilidades oficiales por dominio en `fuentes/dominio-N.md`, y revalidación de los datos de referencia del examen.
- `question-bank-schema`: formato del banco de preguntas y su JSON Schema.
- `question-validation`: validador `validar_preguntas.py` y reglas de coherencia.
- `quiz-cli`: cuestionario interactivo `quiz.py`.
- `ci-pipeline`: workflow de GitHub Actions.

### Modified Capabilities
<!-- Ninguna: `openspec/specs/` está vacío. -->

## Impact

- Repositorio actualmente casi vacío (solo `promt.md`, `.claude/`, `openspec/`); todo el contenido es nuevo y no hay cambios incompatibles.
- Dependencias de Python: `pyyaml`, `jsonschema`. CI: `markdownlint-cli2`, `lychee`.
- Requiere acceso web a `docs.aws.amazon.com` para la transcripción; los datos no verificables se marcan con `> ⚠️ PENDIENTE DE VERIFICAR:`.
- Sin banco de preguntas aún: el validador y el quiz se prueban con fixtures de test, no con preguntas del curso.
