# laboratorio-modulo-03 Specification

## Purpose
TBD - created by archiving change iteracion-3-modulo-03-fm. Update Purpose after archive.
## Requirements
### Requirement: Laboratorio de prompt engineering y Prompt Management
`modulos/03-modelos-fundacionales/laboratorio.md` SHALL guiar la comparación de técnicas de *prompt engineering* (zero-shot, few-shot, chain-of-thought, instrucciones negativas) y el uso de Amazon Bedrock Prompt Management (plantilla con variables, versiones y comparación), con objetivo, relación con las tareas, requisitos, pasos por consola y equivalente opcional con la AWS CLI.

#### Scenario: Estudiante sin experiencia
- **WHEN** un estudiante junior sigue el laboratorio en una cuenta nueva
- **THEN** puede completarlo con los permisos indicados para la consola y la CLI

### Requirement: Coste y limpieza
El laboratorio SHALL incluir una estimación de coste con fuente oficial, un aviso de facturación, la recomendación de AWS Budgets, preguntas de reflexión con respuestas orientativas y una sección de limpieza que borre el *prompt* creado, y no SHALL crear recursos con coste por hora.

#### Scenario: Recursos persistentes
- **WHEN** el estudiante termina el laboratorio
- **THEN** no quedan recursos que generen coste y la limpieza indica qué revisar

