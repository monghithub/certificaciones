# question-validation Specification

## Purpose
TBD - created by archiving change iteracion-0-fundacion-curso. Update Purpose after archive.
## Requirements
### Requirement: Validación de bancos de preguntas
`scripts/validar_preguntas.py` SHALL validar todos los `modulos/*/preguntas.yaml` contra el esquema y SHALL terminar con código distinto de cero si detecta cualquier error, tras informar de todos los errores encontrados con fichero e `id`.

#### Scenario: Banco correcto
- **WHEN** todos los bancos son válidos
- **THEN** el script imprime un resumen y termina con código 0

#### Scenario: Varios errores
- **WHEN** hay dos preguntas inválidas
- **THEN** el script informa de ambas y termina con código 1

### Requirement: Comprobaciones de coherencia
El validador SHALL comprobar: unicidad de `id`; que `correctas` referencie opciones/prompts existentes; número de correctas coherente con el tipo (1 en multiple_choice, ≥2 en multiple_response); que cada opción incorrecta tenga entrada en `distractores`; que `tarea` exista en `fuentes/dominio-N.md`; y la ausencia de "todas las anteriores"/"ninguna de las anteriores".

#### Scenario: Id duplicado
- **WHEN** dos preguntas comparten `id`
- **THEN** se reporta error

#### Scenario: Tarea inexistente
- **WHEN** una pregunta del dominio 2 usa `tarea: "2.9"` y no existe en `fuentes/dominio-2.md`
- **THEN** se reporta error

#### Scenario: Distractor sin explicar
- **WHEN** una opción incorrecta no aparece en `distractores`
- **THEN** se reporta error

### Requirement: Mínimos y distribución
El validador SHALL exigir al menos 30 preguntas por módulo de dominio con banco no vacío y 65 en el simulacro, e informar de la distribución por tipos, avisando cuando se aleje más de 10 puntos porcentuales de 60/20/10/10 (o del reparto de `banco.distribucion`). En el simulacro, si el manifiesto declara `examen.distribucion`, el aviso SHALL usar ese reparto. Una opción `--sin-minimos` SHALL desactivar la exigencia de mínimos.

#### Scenario: Banco con menos de 30
- **WHEN** un módulo de dominio tiene 12 preguntas y no se pasa `--sin-minimos`
- **THEN** se reporta error

#### Scenario: Distribución desviada
- **WHEN** un banco de 30 preguntas tiene 100 % multiple_choice
- **THEN** se emite aviso sin error

#### Scenario: Reparto del simulacro
- **WHEN** el simulacro solo tiene preguntas de opción múltiple y `examen.distribucion` es `{multiple_choice: 100}`
- **THEN** el validador no avisa de que falten preguntas de ordenación o de emparejamiento

### Requirement: Simulacro inédito
`scripts/validar_preguntas.py` SHALL informar de un error cuando el enunciado de una pregunta del módulo de simulacro coincida, tras normalizarlo (minúsculas, sin signos de puntuación ni espacios repetidos), con el de una pregunta de los bancos de los módulos.

#### Scenario: Enunciado copiado
- **WHEN** una pregunta del simulacro repite el enunciado de una pregunta del módulo 03
- **THEN** el validador informa del error con los dos ids y termina con código 1

### Requirement: Validación de los bancos de repaso
`scripts/validar_preguntas.py` SHALL validar cada `modulos/*/repaso.yaml` con el esquema y las comprobaciones de coherencia de los bancos, exigir ids únicos en todo el curso, admitir dominio 0 solo en bancos de repaso de cursos con `repaso.previos`, exigir el mínimo `repaso.minimo_por_modulo` y dar error si un enunciado repite el de una pregunta de examen.

#### Scenario: Dominio 0 en un banco de examen
- **WHEN** una pregunta de `preguntas.yaml` usa dominio 0
- **THEN** el validador informa del error y termina con código 1

### Requirement: Tipos del examen en el simulacro
Si el manifiesto de un curso declara `examen.tipos`, el validador SHALL dar un error por cada tipo de pregunta del simulacro que no figure en esa lista, y otro si `examen.distribucion` usa un tipo que no está en `examen.tipos`. Si el manifiesto no declara `examen.tipos`, el simulacro SHALL poder usar los cuatro tipos. Los bancos de los módulos SHALL seguir validándose con `banco.distribucion`.

#### Scenario: Pregunta de ordenación en el simulacro
- **WHEN** `examen.tipos` es `[multiple_choice, multiple_response]` y el simulacro contiene una pregunta `ordering`
- **THEN** el validador informa de un error que nombra el tipo y los tipos del examen

#### Scenario: Curso sin tipos declarados
- **WHEN** el manifiesto no declara `examen.tipos` y el simulacro contiene una pregunta `ordering`
- **THEN** el validador no informa de error por el tipo
