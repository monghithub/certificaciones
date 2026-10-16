# Servicios del módulo 05

Servicios dentro de alcance relevantes para el Dominio 5. La columna final recoge cuándo **no** conviene usarlos, que es donde suelen estar los distractores. Referencias: las de [README.md](README.md#referencias). Disponibilidad comprobada el 16 de octubre de 2026.

## Proteger sistemas de IA

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| AWS IAM | Roles, políticas y permisos con mínimo privilegio: quién invoca qué modelo o gestiona qué recurso; roles de servicio de Bedrock | Para filtrar el contenido de los *prompts* (Guardrails) o cifrar datos (KMS) |
| AWS KMS | Claves de cifrado en reposo controladas por el cliente: modelos personalizados, agentes, ingesta de Knowledge Bases, evaluaciones, S3 | Para guardar contraseñas o claves de API de terceros (Secrets Manager) |
| Amazon Macie | Descubrir datos sensibles (PII, credenciales) y *buckets* expuestos en S3 antes de usarlos con IA | Para filtrar PII en tiempo real en las respuestas de un modelo (Guardrails) |
| AWS PrivateLink | Llegar a Bedrock desde una VPC por *endpoints* de interfaz, sin Internet | Para controlar qué usuario puede invocar qué modelo (IAM) |
| Amazon VPC | Aislar en red los recursos que usan la IA (subredes privadas, grupos de seguridad) | Para cifrar los datos almacenados (KMS) |
| Amazon Bedrock AgentCore | Identity: credenciales de agentes para actuar en nombre del usuario. Policy: límites deterministas de las herramientas. Observabilidad: trazas | Para filtrar contenido dañino en los *prompts* (Guardrails) |
| Amazon Bedrock Guardrails | Bloquear ataques de *prompt*, contenido dañino y datos personales en entradas y respuestas | Como sustituto de IAM, del cifrado o de la red privada |
| AWS Secrets Manager | Guardar y rotar claves de API y credenciales que usan las herramientas de un agente | Para claves de cifrado (KMS) o credenciales de AWS (IAM) |

## Datos y origen

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Bedrock Knowledge Bases | Respuestas con citas a los documentos de origen | Para registrar con qué datos se entrenó un modelo (linaje) |
| AWS Glue | Catálogo central de metadatos (Data Catalog) y calidad de datos (Glue Data Quality) | Para controlar permisos por columna o fila (Lake Formation) |
| AWS Glue DataBrew | Perfilar y limpiar datos de forma visual, sin código | Para catalogar los conjuntos de datos de la organización (Glue Data Catalog) |
| AWS Lake Formation | Permisos detallados (columna, fila, celda) sobre el lago de datos | Para descubrir PII en S3 (Macie) |
| Amazon SageMaker AI | Linaje de ML (ML Lineage Tracking, MLflow), Model Cards y Role Manager | Cuando el modelo se consume por API en Bedrock y no se entrena |

## Gobierno y cumplimiento

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| AWS Config | Inventario e historial de configuración de recursos y evaluación con reglas | Para saber quién llamó a una API (CloudTrail) |
| Amazon Inspector | Gestión de vulnerabilidades en EC2, imágenes de contenedores y Lambda | Para informes de cumplimiento de AWS (Artifact) |
| AWS Artifact | Descargar informes de cumplimiento de AWS (SOC, ISO, PCI) y gestionar acuerdos | Para demostrar la configuración de los recursos del cliente (Config) |
| AWS CloudTrail | Auditoría de la actividad de la API: quién hizo qué y cuándo | Para guardar el texto de los *prompts* y respuestas (registro de invocaciones de Bedrock) |
| AWS Trusted Advisor | Recomendaciones de coste, rendimiento, disponibilidad, seguridad y límites de servicio | Para escanear vulnerabilidades de *software* (Inspector) |
| Amazon CloudWatch | Métricas, registros (destino del registro de invocaciones) y alarmas; retención por grupo de registros | Para registrar cambios de configuración (Config) |
| AWS Well-Architected Tool | Revisar una carga de trabajo frente a las buenas prácticas y las lentes de AWS | Para escanear vulnerabilidades o recopilar evidencias automáticamente |
| Amazon S3 | Datos de entrenamiento y registros; S3 Lifecycle para transición y expiración | Para consultas de configuración o auditoría de API |
| Amazon S3 Glacier | Archivo de bajo coste de datos y registros que hay que conservar años | Datos que se consultan a menudo |
