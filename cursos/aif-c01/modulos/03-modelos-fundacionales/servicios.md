# Servicios del módulo 03

Servicios dentro de alcance relevantes para el Dominio 3. La columna final recoge cuándo **no** conviene usarlos, que es donde suelen estar los distractores. Referencias: las de [README.md](README.md#referencias). Disponibilidad comprobada el 15 de octubre de 2026.

## Modelos, personalización y gestión de prompts

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Bedrock | Modelos fundacionales por API, con personalización (*supervised fine-tuning*, *reinforcement fine-tuning*, destilación), *prompt caching*, Intelligent Prompt Routing y evaluaciones | Cuando hay que controlar todo el entrenamiento o usar técnicas que Bedrock no ofrece (SageMaker AI) |
| Amazon SageMaker AI | Entrenar, preentrenar o ajustar a fondo cualquier modelo con control de la infraestructura | Cuando basta personalizar un modelo de Bedrock sin gestionar infraestructura |
| Amazon SageMaker JumpStart | Partir de modelos preentrenados, ajustarlos y desplegarlos en SageMaker AI | Cuando no se quiere gestionar *endpoints* ni instancias (Bedrock) |
| Amazon Bedrock Prompt Management | Crear, probar, comparar y versionar *prompts* con variables; desplegar una versión y revertir | Como control de seguridad frente a ataques de *prompt* (Guardrails) |
| Amazon Bedrock Flows | Flujos con pasos fijos que enlazan *prompts*, modelos, Knowledge Bases y Lambda en un editor visual | Cuando el sistema debe decidir los pasos por sí mismo (agente con AgentCore) |
| Amazon Bedrock Guardrails | Filtrar ataques de *prompt* (*jailbreaks*, *prompt injection*, fuga de *prompt*), contenido dañino, temas denegados y datos sensibles | Como sustituto de validar la entrada en la aplicación, de los permisos IAM o de la curación de los datos de entrenamiento |

## RAG y bases de datos vectoriales

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Bedrock Knowledge Bases | RAG gestionado: ingesta, *embeddings*, almacén vectorial, recuperación y respuestas con citas | Cuando el problema no es la información sino el estilo o el formato (*prompts* o *fine-tuning*) |
| Amazon OpenSearch Service | Búsqueda vectorial y de texto completo (híbrida) con baja latencia; almacén habitual de Knowledge Bases (OpenSearch Serverless) | Cuando ya se usa PostgreSQL y basta `pgvector`, o para guardar miles de millones de vectores al menor coste (S3 Vectors) |
| Amazon Aurora | PostgreSQL con `pgvector`: combinar consultas SQL y búsqueda vectorial en la misma base de datos | Para relaciones de grafo (Neptune) o búsqueda de texto completo a gran escala (OpenSearch) |
| Amazon RDS | RDS for PostgreSQL con `pgvector`, para aplicaciones RAG propias de equipos que ya usan PostgreSQL en RDS | Como almacén de una Bedrock Knowledge Base (no está admitido: Aurora PostgreSQL sí) |
| Amazon Neptune | Neptune Analytics: búsqueda vectorial combinada con grafos (GraphRAG), fraude, vista 360 del cliente | Para una búsqueda semántica sencilla sin relaciones relevantes entre entidades |
| Amazon DocumentDB | Búsqueda vectorial en aplicaciones que ya usan la API de MongoDB | Cuando el caso no usa documentos JSON ni MongoDB |
| Amazon S3 Vectors | Miles de millones de vectores al menor coste, consultas poco frecuentes | Aplicaciones que necesitan latencias de pocos milisegundos |
| Amazon DynamoDB | Índices vectoriales nativos para buscar por similitud junto a los datos operativos (RAG, memoria de agentes) | Como almacén de una Bedrock Knowledge Base: no está admitido |
| Amazon ElastiCache | Búsqueda vectorial en memoria (Valkey 8.2 o posterior) con latencias mínimas, caché semántica | Como almacén de una Bedrock Knowledge Base: no está admitido |

## Agentes y evaluación

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Bedrock AgentCore | Desplegar y operar agentes en producción; AgentCore Evaluations evalúa agentes a partir de sus trazas | Cuando una consulta a una Knowledge Base o un flujo fijo resuelve el caso |
| Strands Agents | SDK de código abierto para programar agentes | Cuando no se quiere programar un agente propio |
| Amazon Bedrock Model Evaluation | Evaluaciones programáticas, humanas, con modelo juez y de RAG para comparar modelos, *prompts* y Knowledge Bases | Para evaluar agentes a partir de sus trazas (AgentCore Evaluations) |

## Servicios con avisos de disponibilidad

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Bedrock Agents | Agentes en Bedrock; ahora *Agents Classic* | En proyectos nuevos: ya no admite clientes nuevos; AWS remite a Amazon Bedrock AgentCore |
| SageMaker Clarify | Sesgo, explicabilidad y evaluación de modelos fundacionales (FMEval) | En proyectos nuevos: ya no admite clientes nuevos; para evaluar modelos fundacionales, Amazon Bedrock Model Evaluation |
| SageMaker Ground Truth | Etiquetado de datos con personas | En proyectos nuevos: ya no admite clientes nuevos |
