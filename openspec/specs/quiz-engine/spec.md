# quiz-engine Specification

## Purpose
TBD - created by archiving change consola-web-curso. Update Purpose after archive.
## Requirements
### Requirement: Cuestionarios
El sistema SHALL permitir iniciar cuestionarios por módulo, por dominio o mixtos, con número de preguntas configurable, soportando los tipos multiple_choice, multiple_response, ordering y matching.

#### Scenario: Cuestionario por dominio
- **WHEN** un estudiante inicia un test del dominio 3 con 10 preguntas
- **THEN** se le presentan 10 preguntas del dominio 3 sin repetir

### Requirement: Corrección y explicaciones
El sistema SHALL corregir con las mismas reglas que `scripts/quiz.py` (respuesta exacta) y mostrar al terminar cada pregunta, o al final según el modo, la explicación y la de cada distractor.

#### Scenario: Respuesta múltiple incompleta
- **WHEN** correctas son [a, c] y el estudiante marca solo a
- **THEN** se marca incorrecta

### Requirement: Simulacro cronometrado
El sistema SHALL ofrecer el simulacro del módulo 06 con 65 preguntas y límite de 90 minutos medido en servidor, sin mostrar explicaciones hasta finalizar.

#### Scenario: Tiempo agotado
- **WHEN** transcurren 90 minutos desde el inicio
- **THEN** el intento se cierra y las preguntas sin responder cuentan como incorrectas

### Requirement: Registro de intentos
Cada respuesta SHALL guardarse con el id de pregunta, dominio, tarea, respuesta dada y acierto, asociada a su intento y usuario.

#### Scenario: Pregunta retirada del contenido
- **WHEN** un intento histórico referencia un id que ya no existe
- **THEN** el historial lo muestra como "pregunta retirada" sin errores

