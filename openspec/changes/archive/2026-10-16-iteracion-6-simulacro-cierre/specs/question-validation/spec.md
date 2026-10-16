## ADDED Requirements

### Requirement: Simulacro inédito
`scripts/validar_preguntas.py` SHALL informar de un error cuando el enunciado de una pregunta del módulo de simulacro coincida, tras normalizarlo (minúsculas, sin signos de puntuación ni espacios repetidos), con el de una pregunta de los bancos de los módulos.

#### Scenario: Enunciado copiado
- **WHEN** una pregunta del simulacro repite el enunciado de una pregunta del módulo 03
- **THEN** el validador informa del error con los dos ids y termina con código 1
