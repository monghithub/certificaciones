## ADDED Requirements

### Requirement: Tamaño y reparto del banco
`modulos/05-seguridad-gobierno/preguntas.yaml` SHALL contener al menos 60 preguntas originales `D5-NNN`, con al menos 15 por tarea y 3 por objetivo, con la proporción aproximada 60/20/10/10 por tipo, con la respuesta correcta de opción múltiple repartida entre las letras y con un reparto de dificultad cercano a 20/60/20.

#### Scenario: Banco válido
- **WHEN** se ejecutan `validar_preguntas.py` y `comprobar_cobertura.py --preguntas`
- **THEN** ambos terminan sin errores ni avisos para el módulo 05

### Requirement: Estilo de examen
Las preguntas SHALL seguir «Calidad del banco de preguntas» de `AGENTS.md`: escenario de negocio con una restricción que decide, distractores plausibles de servicios o técnicas vecinas, sin pistas ni absolutos, con explicaciones específicas, sin depender de datos pendientes de verificar y sin presentar como opción para clientes nuevos un servicio cerrado a ellos.

#### Scenario: Pregunta de definición literal
- **WHEN** una pregunta se limita a pedir la definición de un término sin escenario
- **THEN** se reescribe antes del cierre de la iteración
