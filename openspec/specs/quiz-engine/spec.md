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

### Requirement: Modo repaso
La consola SHALL ofrecer tests de repaso de conocimientos por módulo o de todos los módulos, con corrección tras cada respuesta, separados de los tests de examen (módulo, dominio, mixto), que no incluyen preguntas de repaso.

#### Scenario: Repaso del módulo 00
- **WHEN** el estudiante inicia un repaso del módulo 00
- **THEN** el test contiene solo preguntas de `00-base-aws/repaso.yaml`

### Requirement: Repetir falladas
La consola SHALL ofrecer un modo con las preguntas de repaso y de examen (no del simulacro) cuya última respuesta del estudiante fue incorrecta.

#### Scenario: Pregunta corregida
- **WHEN** el estudiante falla una pregunta y en un intento posterior la acierta
- **THEN** deja de aparecer en «repetir falladas»

### Requirement: Explicación tras cada respuesta
En todos los modos con corrección inmediata, tras responder una pregunta la consola SHALL mostrar si es correcta, la solución y un desplegable «Ver explicación» con la explicación, los motivos de las opciones incorrectas, la referencia oficial y, si el objetivo está en un mapa de cobertura, el enlace a la sección de teoría.

#### Scenario: Enlace a la teoría
- **WHEN** el estudiante responde una pregunta del objetivo 1.1.1
- **THEN** la explicación enlaza a la sección del módulo 01 que el mapa de cobertura asocia a 1.1.1

### Requirement: Modo estudio del simulacro
Al iniciar el simulacro, el estudiante SHALL poder marcar «Modo estudio»: con él, cada respuesta muestra la corrección y la explicación; sin él, el simulacro no muestra correcciones hasta el final.

#### Scenario: Simulacro normal
- **WHEN** el estudiante inicia el simulacro sin modo estudio y responde una pregunta
- **THEN** no ve la corrección hasta el resultado final

