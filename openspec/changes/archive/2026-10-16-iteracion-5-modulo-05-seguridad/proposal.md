## Why

Los módulos 00 a 04 están completos e integrados en `main`. El Dominio 5 (Seguridad, cumplimiento y gobierno de soluciones de IA) pesa el 14 % del examen y exige reconocer los servicios de AWS que protegen un sistema de IA (IAM, cifrado, Macie, PrivateLink, AgentCore Identity, Policy in AgentCore, Guardrails), el origen de los datos, la ingeniería de datos segura, las consideraciones de seguridad y privacidad, la detección de alucinaciones y los servicios, estrategias y procesos de gobierno y cumplimiento. Es la Iteración 5 de `cursos/aif-c01/promt.md`; el usuario pidió continuar «con todo hasta el final».

## What Changes

- **Módulo 05 (`cursos/aif-c01/modulos/05-seguridad-gobierno/`):**
  - `README.md` con objetivos, mapa de cobertura de los 8 objetivos de las tareas 5.1 y 5.2, teoría con diagramas Mermaid y ejemplos de negocio, puntos clave y referencias oficiales.
  - `servicios.md` y `trampas.md`.
  - `laboratorio.md`: política IAM de mínimo privilegio para un modelo concreto de Amazon Bedrock, registro de invocaciones en CloudWatch Logs y auditoría con el historial de eventos de CloudTrail, sin recursos con coste por hora.
- **Banco del Dominio 5:** al menos 60 preguntas originales (mínimo 15 por tarea y 3 por objetivo); objetivo orientativo de 66 a 72.
- **Glosario:** entradas para cada servicio y concepto nuevo (KMS, Macie, Secrets Manager, Config, Inspector, Artifact, Trusted Advisor, Well-Architected Tool, Lake Formation, Glacier, AgentCore Identity, Policy in AgentCore, registro de invocaciones, linaje, catálogo, tecnologías de mejora de la privacidad, residencia, retención, AI Security Scoping Matrix…).
- **Revisión independiente** del módulo al cerrarlo.
- Actualización de `CHANGELOG.md`, `docs/journal.md`, el estado del README y la comprobación e2e del módulo 05.
- Fuera de alcance: el módulo 06 y cambios funcionales de la consola o de las herramientas.

## Capabilities

### New Capabilities
- `modulo-05-seguridad-gobierno`: teoría, servicios, trampas y cobertura completa del Dominio 5.
- `banco-preguntas-dominio-5`: banco de al menos 60 preguntas del Dominio 5 con reparto por tareas, objetivos, tipos, posiciones y dificultad.
- `laboratorio-modulo-05`: laboratorio guiado de mínimo privilegio, registro y auditoría en Amazon Bedrock con coste y limpieza.

### Modified Capabilities
<!-- Ninguna. -->

## Impact

- Ficheros nuevos en `cursos/aif-c01/modulos/05-seguridad-gobierno/` y entradas nuevas en `cursos/aif-c01/glosario.yaml`.
- La consola muestra el módulo y sus preguntas sin cambios de código.
- Requiere verificar en `docs.aws.amazon.com` y `aws.amazon.com` la protección de datos, el cifrado, PrivateLink, la retención de datos y el registro de invocaciones de Bedrock, AgentCore Identity y Policy, Macie, KMS, Secrets Manager, Lake Formation, Glue Data Catalog y Data Quality, Config, Inspector, Artifact, CloudTrail, Trusted Advisor, Audit Manager, Well-Architected Tool, S3 Lifecycle, CloudWatch Logs, la inferencia entre Regiones y la AI Security Scoping Matrix.
- Git: rama `aif-c01/modulo-05` con PR a `main`.
