## ADDED Requirements

### Requirement: Estadísticas del estudiante
El sistema SHALL mostrar a cada estudiante su progreso de lectura por módulo, su porcentaje de aciertos por dominio y tarea, el historial de intentos y los puntos débiles.

#### Scenario: Aciertos por dominio
- **WHEN** un estudiante abre sus estadísticas tras varios tests
- **THEN** ve el porcentaje de aciertos agregado por dominio y tarea

### Requirement: Vista de administración
El admin SHALL poder listar todos los usuarios con su última conexión, módulo y sección actual, número de intentos y media de aciertos, y consultar el detalle de cualquiera.

#### Scenario: Detalle de un estudiante
- **WHEN** el admin abre el detalle de un estudiante
- **THEN** ve su progreso por módulo, intentos y resultados por dominio

#### Scenario: Aislamiento entre estudiantes
- **WHEN** un estudiante intenta ver las estadísticas de otro
- **THEN** recibe 403
