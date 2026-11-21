## MODIFIED Requirements

### Requirement: Simulacro cronometrado

El sistema SHALL ofrecer el simulacro del módulo que declara el manifiesto con `examen.preguntas` preguntas compuestas según la capacidad `simulacro-rotatorio` (65 en AIF-C01) y límite de `examen.minutos` medido en servidor (90 en AIF-C01), sin mostrar explicaciones hasta finalizar.

#### Scenario: Tiempo agotado

- **WHEN** transcurren 90 minutos desde el inicio
- **THEN** el intento se cierra y las preguntas sin responder cuentan como incorrectas

#### Scenario: Composición del intento

- **WHEN** el estudiante inicia el simulacro de AIF-C01 con un banco de 82 preguntas
- **THEN** el intento tiene 65 preguntas con el reparto oficial por dominio y tipo
