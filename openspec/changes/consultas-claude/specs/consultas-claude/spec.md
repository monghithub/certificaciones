## ADDED Requirements

### Requirement: Preguntar a Claude en los tests
Si `CONSULTAS_TOKEN` está definido, cada pregunta de un test SHALL mostrar al usuario `admin` un panel «Preguntar a Claude», antes y después de responder y en todos los modos, incluido el simulacro. Enviar una duda SHALL guardarla como pendiente sin bloquear el test.

#### Scenario: Duda pendiente
- **WHEN** el admin escribe una duda en una pregunta y la envía
- **THEN** la duda aparece en el panel como pendiente y puede seguir con el test

#### Scenario: Estudiante
- **WHEN** un estudiante abre una pregunta
- **THEN** no ve el panel y las rutas de consultas le responden 403

#### Scenario: Desactivado por defecto
- **WHEN** `CONSULTAS_TOKEN` no está definido
- **THEN** no hay panel ni rutas de consultas

### Requirement: Conversación
Cada pregunta SHALL tener una conversación por usuario. Las respuestas SHALL aparecer en el panel sin recargar la página y el usuario SHALL poder seguir preguntando en la misma conversación.

#### Scenario: Respuesta en segundo plano
- **WHEN** el trabajador devuelve la respuesta de una duda pendiente
- **THEN** el panel la muestra en unos segundos sin recargar

#### Scenario: Mis dudas
- **WHEN** el admin abre «Mis dudas»
- **THEN** ve sus conversaciones con su estado y enlace a la pregunta

### Requirement: Trabajador con Claude Code
El trabajador SHALL recoger las dudas pendientes por la API interna con el token, resolverlas de una en una con Claude Code (modelo Sonnet, solo herramientas de lectura y búsqueda) y continuar la sesión de Claude en los mensajes siguientes. Si no hay cuota, SHALL reintentar más tarde sin perder la duda.

#### Scenario: Token incorrecto
- **WHEN** se llama a la API interna sin el token correcto
- **THEN** responde 404

#### Scenario: Cuota agotada
- **WHEN** Claude Code informa de que se ha alcanzado el límite de uso
- **THEN** la duda sigue pendiente y se reintenta más tarde

#### Scenario: Antes de responder
- **WHEN** el admin pregunta antes de haber respondido la pregunta
- **THEN** Claude le orienta sin dar la solución, salvo que la pida expresamente
