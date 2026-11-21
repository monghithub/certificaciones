# Servicios del módulo 01

Servicios dentro de alcance relevantes para el Dominio 1. La columna final recoge cuándo **no** conviene usarlos, que es donde suelen estar los distractores. Referencias: las de [README.md](README.md#referencias).

## Servicios de IA especializados (preentrenados)

Se integran por API **sin experiencia en ML**. Ofrecen una personalización limitada: normalmente los datos de entrada y algunos parámetros, y en algunos casos personalizaciones acotadas (clasificadores propios en Comprehend, Custom Labels en Rekognition). La mayoría admite *endpoints* privados de VPC (AWS PrivateLink).

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Transcribe | Reconocimiento automático del habla: convertir audio en texto | Cuando se necesita generar voz a partir de texto (es Amazon Polly) o traducir (es Amazon Translate) |
| Amazon Translate | Traducir texto, también documentos no estructurados, y crear aplicaciones multilingües | Cuando hay que transcribir audio (es Amazon Transcribe) o extraer información del documento (Amazon Textract o Amazon Comprehend) |
| Amazon Comprehend | NLP: extraer entidades, frases clave, idioma y opiniones de documentos | Cuando el problema no es de lenguaje natural: imágenes (Amazon Rekognition) o datos tabulares (Amazon SageMaker AI) |
| Amazon Lex | Construir interfaces conversacionales (voz y texto) con comprensión del lenguaje natural y reconocimiento del habla | Cuando solo se quiere analizar texto existente, sin diálogo con el usuario (es Amazon Comprehend) |
| Amazon Polly | Convertir texto en voz realista | Cuando se necesita el proceso inverso, de voz a texto (Amazon Transcribe) |
| Amazon Rekognition | Análisis de imágenes y vídeo (visión por computador) sin experiencia en ML | Cuando hay que extraer texto estructurado de documentos (es Amazon Textract) |
| Amazon Textract | Detectar y analizar texto mecanografiado y manuscrito en documentos, formularios y tablas | Cuando se trata de reconocer objetos o rostros en fotografías (es Amazon Rekognition) |
| Amazon Personalize | Recomendaciones de elementos para los usuarios y segmentos por afinidad, con ML totalmente gestionado | Cuando no se dispone de datos propios de usuarios y elementos con los que generar recomendaciones: hasta reunirlos, una regla sencilla (por ejemplo, los más vendidos) |

## Plataforma de ML y modelos

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon SageMaker AI | Construir, entrenar y desplegar modelos de ML propios, con la mayor flexibilidad sobre el algoritmo | Cuando un servicio preentrenado (Rekognition, Comprehend, Transcribe…) resuelve el caso con menos esfuerzo |
| Amazon SageMaker Canvas | Modelos predictivos y predicciones **sin escribir código**, para analistas de negocio | Cuando un equipo de ciencia de datos necesita controlar el algoritmo y el código (SageMaker AI con cuadernos o código propio) |
| Amazon SageMaker JumpStart | Partir de modelos preentrenados de código abierto, ajustarlos y desplegarlos | Cuando se necesita un modelo totalmente a medida con un algoritmo propio sin partir de uno preentrenado (SageMaker AI con código o contenedor propios) |
| Amazon Bedrock | Modelos fundacionales de varios proveedores, por API y totalmente gestionado | Cuando basta una tarea acotada de ML clásico que un servicio especializado ya cubre (Comprehend, Rekognition, Textract…) |
| Amazon Nova | Modelos fundacionales de Amazon (texto, imagen, vídeo, voz), usados a través de Amazon Bedrock | Cuando la tarea es de ML clásico acotada (SageMaker AI) o un servicio especializado ya la resuelve (Comprehend, Rekognition…) |
| Amazon Bedrock AgentCore | Plataforma para crear, desplegar y operar agentes de IA de forma segura a escala | Cuando no hay un caso de uso agéntico: una simple consulta a un modelo (Amazon Bedrock) no necesita agentes |
| Amazon Bedrock Knowledge Bases | Integrar información propia en aplicaciones de IA generativa con RAG | Cuando el modelo no necesita datos propios ni actualizados: basta invocar el modelo con un buen *prompt* |

## Datos y ciclo de vida

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| AWS Glue | Integrar, transformar y catalogar datos (ETL *serverless*) antes de entrenar o analizar | Para entrenar o desplegar modelos (es Amazon SageMaker AI) |
| AWS Glue DataBrew | Limpiar y normalizar datos de forma visual, sin código | Cuando se necesita un ETL programado a medida (AWS Glue) |
| Amazon SageMaker Data Wrangler | Importar, analizar (EDA) y preparar datos **para ML** con transformaciones integradas y poco código; hoy está dentro de SageMaker Canvas | Para un ETL genérico de datos que no van a un modelo (AWS Glue) o para orquestar todo el flujo de ML (SageMaker Pipelines) |
| Amazon SageMaker Feature Store | Guardar, compartir y reutilizar características, y servir las mismas al entrenar (almacén *offline*) y al inferir en milisegundos (almacén *online*) | Como almacén de datos de negocio o de informes: Amazon Redshift (análisis) o una base de datos operativa como Amazon RDS |
| Amazon SageMaker Pipelines | Automatizar y hacer repetibles los flujos de entrenamiento y despliegue (MLOps) | Para un experimento puntual que no se va a repetir: basta un trabajo de entrenamiento suelto o un cuaderno |
| SageMaker Model Registry | Versionar modelos, aprobarlos antes de producción y desplegarlos | Para registrar experimentos de entrenamiento (MLflow) |
| MLflow en SageMaker AI | Registrar y comparar experimentos para que sean reproducibles | Para orquestar el flujo completo (SageMaker Pipelines) |
| Amazon CloudWatch | Métricas, registros y alarmas de *endpoints* y aplicaciones | Para auditar quién hizo una llamada a la API (AWS CloudTrail) |

## Productividad y desarrollo con IA

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Quick | Servicio con IA para automatizar tareas, analizar datos, crear aplicaciones web e investigar mediante chat en lenguaje natural | Cuando se necesita un modelo propio con control sobre el entrenamiento (Amazon SageMaker AI) |
| Kiro | Plataforma de desarrollo (IDE y CLI) asistida por agentes de IA y basada en especificaciones | Cuando la pregunta trata de entrenar o desplegar un modelo de ML (es Amazon SageMaker AI) |

## Servicios de apoyo

Amazon S3 (almacenamiento de datos y artefactos), AWS Lambda (cómputo *serverless*), Amazon EC2 (servidores propios, por ejemplo para alojar un modelo) y Amazon VPC (red privada) aparecen como apoyo en las preguntas; se describen en el [módulo 00](../00-base-aws/servicios.md).

## Avisos de disponibilidad

- **Amazon SageMaker Model Monitor**, **Amazon SageMaker Clarify** y **Amazon SageMaker Ground Truth** ya no están abiertos a clientes nuevos; los existentes pueden seguir usándolos.
- **SageMaker Experiments** es ahora *Experiments Classic* (solo en Studio Classic); AWS recomienda MLflow en SageMaker AI.
- **Amazon Bedrock Agents** (ahora *Classic*) tampoco está abierto a clientes nuevos; AWS remite a Amazon Bedrock AgentCore para capacidades similares.
- **Amazon Forecast** (desde el 29 de julio de 2024), **Amazon Fraud Detector** (desde el 7 de noviembre de 2025), **Amazon Kendra** y **SageMaker Studio Lab** ya no admiten clientes nuevos. Alternativas que indica AWS: la previsión de series temporales de SageMaker Canvas; SageMaker AI, AutoGluon o AWS WAF Fraud Control; Amazon Bedrock Knowledge Bases; y SageMaker Studio. Ninguno figura en la lista de servicios dentro de alcance.
- **Amazon Comprehend:** el modelado de temas (*topic modeling*), la detección de eventos y la clasificación de seguridad de *prompts* ya no admiten clientes nuevos (AWS remite a modelos de Amazon Bedrock y a Amazon Bedrock Guardrails). El resto de funciones de Comprehend no cambia.
- **Amazon Q** figura como añadido en la página de revisiones de la guía, pero no está en la lista vigente de servicios dentro de alcance: no se trata como materia evaluable (ver [servicios-alcance](../../fuentes/servicios-alcance.md)).
- Los servicios fuera de alcance de la guía (por ejemplo, Amazon Cognito o Amazon GuardDuty) no son materia evaluable.
