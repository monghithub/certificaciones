## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: Tipos del examen en el simulacro
Si el manifiesto de un curso declara `examen.tipos`, el validador SHALL dar un error por cada tipo de pregunta del simulacro que no figure en esa lista, y otro si `examen.distribucion` usa un tipo que no está en `examen.tipos`. Si el manifiesto no declara `examen.tipos`, el simulacro SHALL poder usar los cuatro tipos. Los bancos de los módulos SHALL seguir validándose con `banco.distribucion`.

#### Scenario: Pregunta de ordenación en el simulacro
- **WHEN** `examen.tipos` es `[multiple_choice, multiple_response]` y el simulacro contiene una pregunta `ordering`
- **THEN** el validador informa de un error que nombra el tipo y los tipos del examen

#### Scenario: Curso sin tipos declarados
- **WHEN** el manifiesto no declara `examen.tipos` y el simulacro contiene una pregunta `ordering`
- **THEN** el validador no informa de error por el tipo
