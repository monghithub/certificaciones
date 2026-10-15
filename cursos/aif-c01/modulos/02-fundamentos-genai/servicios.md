# Servicios del módulo 02

Servicios dentro de alcance relevantes para el Dominio 2. La columna final recoge cuándo **no** conviene usarlos, que es donde suelen estar los distractores. Referencias: las de [README.md](README.md#referencias). Disponibilidad comprobada el 14 de octubre de 2026.

## Modelos fundacionales y plataforma de ML

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Bedrock | Usar modelos fundacionales de varios proveedores por API, totalmente gestionado y *serverless*, pagando por uso; incluye Knowledge Bases, Guardrails, evaluaciones, personalización y AgentCore | Cuando hay que entrenar un modelo desde cero o controlar la infraestructura de entrenamiento e inferencia |
| Amazon Nova | Familia de modelos fundacionales de Amazon, en Bedrock: Micro (solo texto, mínima latencia), Lite (multimodal muy barato), Pro (equilibrio), Premier (el más capaz); Nova 2 (Lite, Sonic y Multimodal Embeddings). Nova Canvas, Nova Reel y Nova Sonic v1 están retirados | Cuando un servicio de IA especializado (Translate, Transcribe, Textract) resuelve una tarea acotada con menos esfuerzo |
| Amazon SageMaker AI | Entrenar, ajustar a fondo y desplegar modelos abiertos, propietarios o propios, con control sobre coste, rendimiento y latencia | Cuando basta consumir un modelo existente por API sin gestionar infraestructura (Bedrock) |
| Amazon SageMaker JumpStart | Partir de modelos fundacionales preentrenados (públicos o propietarios), probarlos, ajustarlos y desplegarlos en SageMaker AI | Cuando no se quiere gestionar *endpoints* ni instancias: Bedrock es *serverless* |
| AWS Trainium | Chips de AWS para entrenar y servir (inferencia) modelos de IA a escala con la mejor relación coste-rendimiento | Cuando no se entrena ni se aloja un modelo propio: con Bedrock no se eligen chips |
| AWS Inferentia | Chips de AWS específicos para inferencia de aprendizaje profundo e IA generativa al menor coste en EC2 | Para entrenar (Trainium) o cuando se consume un modelo por API |

## Agentes y aplicaciones

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Bedrock AgentCore | Desplegar y operar agentes en producción de forma segura y a escala, con cualquier *framework* y modelo: entre otros, Runtime (MCP y A2A), Memory, Gateway (herramientas MCP), Identity, Policy, Evaluations, Code Interpreter, Browser, Observability, Harness | Cuando basta una consulta sencilla a un modelo, sin acciones ni herramientas |
| Strands Agents | SDK de código abierto para programar agentes con un enfoque centrado en el modelo, con herramientas, MCP y patrones multiagente | Cuando no se quiere programar ni operar un agente propio (Amazon Quick para empleados) |
| Amazon Quick | Asistente con agentes para empleados: chat sobre los datos de la empresa, automatización (Flows, Automate), análisis (Quick Sight), investigación (Research) y aplicaciones (Apps), sin desarrollar | Cuando hay que construir una aplicación propia de IA generativa para clientes con control del modelo y del código |
| Kiro | Desarrollo de software agéntico: de *prompts* a especificaciones, código, documentación y pruebas; *hooks* de agente y ficheros de *steering* | Cuando la pregunta trata de entrenar o desplegar un modelo de ML, de un asistente de negocio o de migrar sistemas heredados (AWS Transform) |
| AWS Transform | Modernizar y migrar aplicaciones, código e infraestructura existentes (mainframes, servidores VMware) con IA agéntica | Para desarrollar funcionalidades nuevas (Kiro) o crear una aplicación de IA generativa propia (Bedrock) |
| Amazon Bedrock Guardrails | Filtrar contenido dañino, bloquear temas denegados, enmascarar datos sensibles y detectar respuestas no fundamentadas | Como sustituto de los permisos IAM o del cifrado de los datos |
| Amazon Bedrock Knowledge Bases | Conectar datos propios mediante RAG (fragmentación, *embeddings* y búsqueda vectorial gestionadas) | Cuando el modelo no necesita información propia ni actualizada |

## Servicios con avisos de disponibilidad

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Bedrock Agents | Agentes en Bedrock; ahora *Agents Classic* | En proyectos nuevos: ya no admite clientes nuevos; AWS remite a Amazon Bedrock AgentCore |
| Amazon Q | Amazon Q Business (asistente empresarial) y Amazon Q Developer (asistente de desarrollo) | En proyectos nuevos: Q Business ya no admite clientes nuevos (AWS remite a Amazon Quick) y los *plugins* de IDE de Q Developer dejan de tener soporte el 30 de abril de 2027 (AWS remite a Kiro) |

> ⚠️ PENDIENTE DE VERIFICAR: la página de revisiones de la guía v1.1 dice que Amazon Q se añadió a la lista de servicios evaluables, pero la lista actual no lo incluye (ver [fuentes/servicios-alcance.md](../../fuentes/servicios-alcance.md)). Ninguna pregunta del banco depende de ello.

## Opciones de inferencia y coste de Amazon Bedrock

| Opción | Caso de uso | Cuándo NO usarla |
|---|---|---|
| On-Demand | Tráfico variable o impredecible; pago por *token* sin compromiso | Volúmenes grandes que pueden esperar (lotes es más barato) |
| Nivel Priority | Respuestas más rápidas en aplicaciones críticas, sin reservar capacidad (75 % más caro que Standard) | Cargas internas o no urgentes: paga un recargo innecesario |
| Nivel Flex | Cargas que toleran más tiempo de proceso, con un 50 % de descuento y las mismas llamadas a la API | Aplicaciones interactivas con requisitos de latencia |
| Inferencia por lotes | Grandes volúmenes asíncronos, con entrada y salida en S3; un 50 % menos en los modelos que la admiten | Conversaciones o aplicaciones que necesitan respuesta inmediata o llamadas a herramientas |
| Nivel Reserved | Capacidad reservada de *tokens* por minuto (1 o 3 meses) para aplicaciones críticas | Pilotos o tráfico bajo: hay capacidad mínima y compromiso |
| Provisioned Throughput | Capacidad dedicada por horas y unidades de modelo; servir modelos personalizados | Tráfico bajo o variable: se paga aunque no se use |
| Prompt caching | Contextos largos repetidos en muchas peticiones | Prompts que cambian siempre: no hay prefijo que reutilizar |
| Inferencia entre Regiones | Más rendimiento ante picos; la geográfica respeta la residencia de datos y la global ahorra aproximadamente un 10 % | Global, cuando los datos deben quedarse en una zona geográfica |
