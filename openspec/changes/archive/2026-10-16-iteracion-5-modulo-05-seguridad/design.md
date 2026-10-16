## Context

El Dominio 5 tiene 2 tareas y 8 objetivos (`fuentes/dominio-5.md`, guía v1.1) y pesa el 14 %. La tarea 5.1 trata de los métodos para proteger sistemas de IA (servicios, citación y origen de los datos, ingeniería de datos segura, consideraciones de seguridad y privacidad, alucinaciones y *grounding*) y la 5.2, del gobierno y el cumplimiento (servicios, estrategias de gobierno de datos y procesos). El módulo 00 presentó IAM, la responsabilidad compartida, CloudTrail y CloudWatch; el 04, Guardrails y Model Cards.

## Goals / Non-Goals

**Goals:**
- Cubrir los 8 objetivos con definición, criterio de decisión, ejemplo de negocio y trampa.
- Reflejar el estado vigente: Audit Manager cerrado a clientes nuevos; Bedrock no comparte entradas y salidas con los proveedores ni las usa para entrenar, con la retención de datos por Región y la detección de abusos; la *Generative AI Security Scoping Matrix* publicada ahora como *AI Security Scoping Matrix*.
- Un banco de unas 66–72 preguntas que pase todos los controles sin avisos, con al menos un 18 % de dificultad baja y la correcta como opción más larga en torno a un 25 %.
- Un laboratorio de coste mínimo, sin recursos con coste por hora.

**Non-Goals:**
- Implantar protocolos de seguridad o marcos de gobierno (fuera de alcance según la guía): solo se reconocen.
- Servicios fuera de alcance (por ejemplo, AWS Clean Rooms): solo se mencionan.

## Decisions

- **Teoría por tarea:**
  - 5.1: responsabilidad compartida por forma de uso (Bedrock, SageMaker AI, EC2); privacidad de Bedrock; tabla de servicios (IAM, cifrado con KMS y TLS, Macie, PrivateLink, AgentCore Identity, Policy in AgentCore, Guardrails, Secrets Manager) con diagrama de defensa en capas; citas, linaje, catálogo y Model Cards; calidad de datos, tecnologías de privacidad, control de acceso e integridad con ejemplo de seudonimización; consideraciones de seguridad y privacidad (CloudTrail frente al registro de invocaciones, control de acceso antes del contexto, tipos de inyección, exceso de autonomía); alucinaciones con ejemplo de umbrales de *grounding*.
  - 5.2: Config, Inspector, Artifact, CloudTrail, Trusted Advisor (más CloudWatch, Well-Architected Tool, Audit Manager y gobierno de ML) con diagrama y tabla «pregunta del auditor → servicio»; ciclo de vida, registro, residencia, monitorización, observación y retención con ejemplo de S3 Lifecycle; políticas, cadencia y estrategias de revisión, marcos (Scoping Matrix con diagrama de ámbitos), transparencia y formación.
- **Laboratorio:** política IAM que solo permite invocar Amazon Nova Micro a través de su perfil de inferencia (condición `bedrock:InferenceProfileArn`), prueba de acceso denegado con otro modelo, registro de invocaciones en CloudWatch Logs con retención de 1 día, consulta del registro (identidad, *prompt* y respuesta) y del historial de eventos de CloudTrail, y limpieza.
- **Banco:** unas 68 preguntas (≈41 MC, 14 MR, 6 ORD, 7 MAT), de 7 a 10 por objetivo. Distractores vecinos: Config/CloudTrail/Inspector/Artifact/Trusted Advisor, KMS/Secrets Manager, Macie/Guardrails, PrivateLink/IAM, AgentCore Identity/Policy, citas/linaje/catálogo, Glue Data Catalog/Lake Formation, ámbitos de la Scoping Matrix.

## Risks / Trade-offs

- [Cambios recientes en la retención de datos de Bedrock] → se cita la página vigente y se resume sin depender de detalles de modelos concretos.
- [Nombres que cambian (Scoping Matrix, QuickSight/Quick)] → se usa el nombre de la guía del examen y se indica el vigente.
- [Coste del laboratorio] → ingesta de registros mínima, retención de 1 día, Budgets y limpieza.

## Open Questions

- Ninguna bloqueante.
