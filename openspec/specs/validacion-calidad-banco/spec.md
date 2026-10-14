# validacion-calidad-banco Specification

## Purpose
TBD - created by archiving change revision-calidad-iteracion-1. Update Purpose after archive.
## Requirements
### Requirement: Posición de la respuesta repartida
`validar_preguntas.py` SHALL fallar cuando, en un banco con al menos 12 preguntas de opción múltiple, más del 40 % tenga la respuesta correcta en la misma letra.

#### Scenario: Respuestas concentradas
- **WHEN** las 12 preguntas de opción múltiple de un banco tienen la respuesta en «b»
- **THEN** el validador informa de error

### Requirement: Opciones distintas
`validar_preguntas.py` SHALL fallar si una pregunta tiene dos opciones con el mismo texto.

#### Scenario: Opción duplicada
- **WHEN** dos opciones de una pregunta tienen el mismo texto
- **THEN** el validador informa de error

### Requirement: Avisos de calidad
`validar_preguntas.py` SHALL avisar, sin fallar, de los distractores con términos absolutos («siempre», «nunca», «cualquier», «garantiza») y de los enunciados de opción o respuesta múltiple de menos de 80 caracteres.

#### Scenario: Distractor con absoluto
- **WHEN** un distractor dice «siempre es la opción más barata»
- **THEN** el validador emite un `AVISO` con el id de la opción

### Requirement: Mínimo por objetivo
El manifiesto SHALL admitir `banco.minimo_por_objetivo`, y `comprobar_cobertura.py --preguntas` SHALL fallar si un objetivo oficial tiene menos preguntas que ese mínimo.

#### Scenario: Objetivo por debajo del mínimo
- **WHEN** un objetivo tiene 2 preguntas y el mínimo es 3
- **THEN** la comprobación informa de error con el objetivo y el número

