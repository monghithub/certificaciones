## ADDED Requirements

### Requirement: Laboratorio de Amazon Bedrock Guardrails
`modulos/04-ia-responsable/laboratorio.md` SHALL guiar la creación y prueba de un *guardrail* con filtros de contenido, un tema denegado, un filtro de información sensible y una comprobación de *grounding* contextual, con objetivo, relación con las tareas, requisitos, pasos por consola y equivalente opcional con la AWS CLI.

#### Scenario: Estudiante sin experiencia
- **WHEN** un estudiante junior sigue el laboratorio en una cuenta nueva
- **THEN** puede completarlo con los permisos indicados para la consola y la CLI

### Requirement: Coste y limpieza
El laboratorio SHALL incluir una estimación de coste con fuente oficial, un aviso de facturación, la recomendación de AWS Budgets, preguntas de reflexión con respuestas orientativas y una sección de limpieza que borre el *guardrail*, y no SHALL crear recursos con coste por hora.

#### Scenario: Recursos persistentes
- **WHEN** el estudiante termina el laboratorio
- **THEN** no quedan recursos que generen coste y la limpieza indica qué revisar
