# quiz-cli Specification

## Purpose
TBD - created by archiving change iteracion-0-fundacion-curso. Update Purpose after archive.
## Requirements
### Requirement: Cuestionario interactivo
`scripts/quiz.py` SHALL ejecutar en terminal un cuestionario a partir de los YAML, admitiendo filtros `--modulo`, `--dominio`, `--tipo`, `--n` y `--semilla`, y los cuatro tipos de pregunta.

#### Scenario: Cuestionario filtrado
- **WHEN** se ejecuta `quiz.py --dominio 3 --n 5`
- **THEN** se plantean 5 preguntas del dominio 3 y se muestra la puntuación final

### Requirement: Corrección y retroalimentación
Tras cada respuesta, el script SHALL indicar si es correcta, mostrar la explicación y la explicación de los distractores. La corrección SHALL ser exacta (todas las correctas y ninguna más; orden exacto en ordering; pares exactos en matching).

#### Scenario: Respuesta múltiple parcial
- **WHEN** en una pregunta con correctas `[a, c]` el usuario responde `a`
- **THEN** se marca como incorrecta y se muestra la solución

#### Scenario: Sin preguntas disponibles
- **WHEN** no hay ningún YAML con preguntas que cumpla el filtro
- **THEN** el script informa del hecho y termina con código distinto de cero

