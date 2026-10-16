## ADDED Requirements

### Requirement: Laboratorio de mínimo privilegio, registro y auditoría
`modulos/05-seguridad-gobierno/laboratorio.md` SHALL guiar la creación de una política IAM de mínimo privilegio para invocar un único modelo de Amazon Bedrock, la comprobación de un acceso denegado, la activación del registro de invocaciones en CloudWatch Logs y la consulta de ese registro y del historial de eventos de CloudTrail, con objetivo, relación con las tareas, requisitos, pasos por consola y equivalente opcional con la AWS CLI.

#### Scenario: Estudiante sin experiencia
- **WHEN** un estudiante junior sigue el laboratorio en una cuenta nueva
- **THEN** puede completarlo con los permisos indicados

### Requirement: Coste y limpieza
El laboratorio SHALL incluir una estimación de coste con fuente oficial, un aviso de facturación, la recomendación de AWS Budgets, preguntas de reflexión con respuestas orientativas y una sección de limpieza que desactive el registro de invocaciones y borre el grupo de registros, el rol y la política, y no SHALL crear recursos con coste por hora.

#### Scenario: Recursos persistentes
- **WHEN** el estudiante termina el laboratorio
- **THEN** no quedan recursos que generen coste y la limpieza indica qué revisar
