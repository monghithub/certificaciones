# laboratorio-modulo-02 Specification

## Purpose
TBD - created by archiving change iteracion-2-modulo-02-genai. Update Purpose after archive.
## Requirements
### Requirement: Laboratorio del playground de Bedrock
`modulos/02-fundamentos-genai/laboratorio.md` SHALL guiar el uso del playground de Amazon Bedrock variando la temperatura, top-p y la longitud máxima, y observando los *tokens* de entrada y de salida, con objetivo, relación con las tareas, requisitos (Región con Bedrock y procedimiento vigente de acceso a modelos), pasos por consola y equivalente opcional con la AWS CLI.

#### Scenario: Estudiante sin experiencia
- **WHEN** un estudiante junior sigue el laboratorio en una cuenta nueva
- **THEN** puede completarlo con los permisos indicados para la consola y la CLI

### Requirement: Coste y limpieza
El laboratorio SHALL incluir una estimación de coste con fuente oficial, un aviso de facturación, la recomendación de AWS Budgets y una sección de limpieza, y no SHALL crear recursos con coste por hora.

#### Scenario: Recursos persistentes
- **WHEN** el estudiante termina el laboratorio
- **THEN** no quedan recursos que generen coste y la limpieza indica qué revisar

