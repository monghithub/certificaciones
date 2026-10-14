# question-bank-schema Specification

## Purpose
TBD - created by archiving change iteracion-0-fundacion-curso. Update Purpose after archive.
## Requirements
### Requirement: JSON Schema de preguntas
`schemas/pregunta.schema.json` SHALL definir el formato de cada pregunta con los campos `id`, `dominio`, `tarea`, `tipo`, `dificultad`, `enunciado`, `opciones`, `correctas`, `explicacion`, `distractores` y `referencia`, con `tipo` ∈ {multiple_choice, multiple_response, ordering, matching} y `dificultad` ∈ {baja, media, alta}.

#### Scenario: Pregunta válida de opción múltiple
- **WHEN** una pregunta `multiple_choice` tiene todos los campos y una sola opción en `correctas`
- **THEN** valida contra el esquema

#### Scenario: Campo obligatorio ausente
- **WHEN** a una pregunta le falta `explicacion`
- **THEN** la validación contra el esquema falla

### Requirement: Formato de ordering y matching
Para `ordering`, `correctas` SHALL ser la lista ordenada de 3 a 5 ids de opción. Para `matching`, la pregunta SHALL incluir `prompts` (id, texto) y `correctas` SHALL ser una lista de 3 a 7 pares `[prompt_id, opcion_id]`.

#### Scenario: Matching válido
- **WHEN** una pregunta `matching` define 4 `prompts` y 4 pares en `correctas`
- **THEN** valida contra el esquema

#### Scenario: Ordering fuera de rango
- **WHEN** una pregunta `ordering` tiene 2 elementos en `correctas`
- **THEN** la validación falla

