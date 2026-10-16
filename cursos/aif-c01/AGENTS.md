# Reglas propias del curso AIF-C01

Complementan el [`AGENTS.md`](../../AGENTS.md) raíz, que contiene las reglas comunes a todos los cursos. La especificación completa del curso está en [`promt.md`](promt.md). Ante cualquier discrepancia con AWS, prevalece la guía oficial.

## Curso y nivel

**AWS Certified AI Practitioner (AIF-C01)**, nivel *foundational*: qué servicio o técnica aplicar y por qué, no cómo implementarlo. Iteraciones: 0 (cimientos), 1 (módulos 00 y 01), 2 a 5 (módulos 02 a 05, un dominio por iteración) y 6 (simulacro, `chuleta.md`, glosario y revisión cruzada de cobertura).

## Fuentes oficiales

- Primaria: la [guía oficial AIF-C01](https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html) y sus subpáginas (dominios 1–5, servicios in/out of scope, revisiones), transcritas en `fuentes/`.
- Secundarias: la documentación de cada servicio en `docs.aws.amazon.com`, la página de la certificación y AWS Skill Builder. `fuentes_oficiales` en `curso.yaml`: `docs.aws.amazon.com` y `aws.amazon.com`.
- Fuera de alcance según la guía: desarrollar modelos, ingeniería de datos o *features*, ajuste de hiperparámetros, *pipelines*, análisis matemático, implantar protocolos de seguridad o marcos de gobierno. Solo se mencionan para reconocerlos.

## Criterios de decisión que hay que reforzar

Gestionado frente a medida; prompt engineering → RAG → *fine-tuning* → preentrenamiento continuado (coste y esfuerzo); *on-demand* frente a Provisioned Throughput; métrica de evaluación según el problema.

## Disponibilidad y nombres de servicios de AWS (a 2026-10-14)

- Cerrados a clientes nuevos (a 2026-10-16): SageMaker Model Monitor, SageMaker Clarify, SageMaker Ground Truth, Amazon Augmented AI (A2I), SageMaker Role Manager, AWS Audit Manager y Amazon Bedrock Agents (ahora *Classic*; AWS remite a Amazon Bedrock AgentCore). Si el examen pregunta por ellos sin decir que el cliente sea nuevo, siguen siendo la respuesta esperada.
- Fuera de alcance aunque aparezcan en la documentación de seguridad: Amazon GuardDuty, IAM Identity Center, AWS Security Hub, AWS WAF, Amazon Cognito (ver `fuentes/servicios-alcance.md`); solo se mencionan para reconocerlos.
- SageMaker Experiments es ahora *Experiments Classic*; AWS recomienda MLflow en SageMaker AI.
- Desde el 3 de diciembre de 2024, el servicio de ML se llama Amazon SageMaker AI y «Amazon SageMaker» designa una plataforma unificada que lo incluye.
- Las guías de decisión de AWS indican su *Last updated*; la guía de ML de mayo de 2024 está desactualizada en, por ejemplo, el soporte de *endpoints* de VPC (consulta la lista de AWS PrivateLink).
- Comprueba siempre `fuentes/servicios-alcance.md` y menciona los servicios in scope relevantes en cada objetivo de «servicios por etapa».

## Banco de preguntas

- Distractores habituales del curso: Textract/Rekognition, Transcribe/Polly, Comprehend/Lex, Canvas/SageMaker AI, inferencia *serverless*/asíncrona/por lotes, Bedrock/SageMaker AI/JumpStart, AgentCore/Strands Agents/Bedrock Agents Classic, *on-demand*/Provisioned Throughput.
- El conjunto oficial de práctica de AWS Skill Builder (20 preguntas) solo se recomienda como control final; no se copia.

## Laboratorios

- Región con Amazon Bedrock y el procedimiento vigente de acceso a modelos.
- Permisos: la consola suele necesitar las políticas administradas de solo lectura del servicio (por ejemplo, `ComprehendReadOnly`), y la CLI admite una política de mínimo privilegio.
- Capa gratuita de AWS: desde julio de 2025, las cuentas nuevas reciben créditos y eligen entre un plan gratuito de seis meses y un plan de pago. Recomienda AWS Budgets antes de empezar.
- Limpieza obligatoria con especial atención a Knowledge Bases, colecciones de OpenSearch Serverless, *endpoints* de SageMaker AI y Provisioned Throughput.
