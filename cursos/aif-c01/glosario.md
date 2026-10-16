# Glosario: AWS Certified AI Practitioner (AIF-C01)

Términos del curso en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo. Los servicios se ordenan sin los prefijos «Amazon» y «AWS» (Amazon S3 aparece en la S).

Total: 236 términos.

## A

- **A2A** (Agent-to-Agent, Agent2Agent). *Concepto.* Protocolo abierto para la comunicación entre agentes: cada agente publica una Agent Card con su identidad, capacidades y punto de acceso para que otros lo descubran, y se intercambian mensajes y tareas. AgentCore Runtime admite servidores A2A.
  - Usar cuando: Para que agentes de equipos o proveedores distintos se descubran y colaboren.
  - No usar cuando: Para conectar un agente con herramientas o datos: eso es MCP.
  - Referencia: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-a2a.html>
- **AgentCore Evaluations** (Amazon Bedrock AgentCore Evaluations). *Servicio.* Servicio de Amazon Bedrock AgentCore que evalúa agentes y herramientas a partir de sus trazas (por ejemplo, de Strands o LangGraph) con evaluadores integrados o propios basados en LLM-as-a-judge, antes y después del despliegue.
  - Usar cuando: Para medir de forma continua la calidad de un agente: utilidad, elección de herramientas, cumplimiento de la tarea.
  - No usar cuando: Para comparar modelos en tareas estándar: Amazon Bedrock Model Evaluation.
  - Referencia: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html>
- **AgentCore Identity** (Amazon Bedrock AgentCore Identity). *Servicio.* Servicio de Amazon Bedrock AgentCore de identidad y gestión de credenciales para agentes: autentica y autoriza a los agentes y sus herramientas para acceder a recursos de AWS y de terceros en nombre de los usuarios, con trazas de auditoría.
  - Usar cuando: Cuando un agente debe acceder a servicios externos o de AWS con la identidad y los permisos del usuario.
  - No usar cuando: Para limitar qué acciones puede hacer el agente con cada herramienta (Policy in AgentCore).
  - Referencia: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html>
- **agrupamiento** (clustering, análisis de agrupamiento). *Técnica.* Técnica no supervisada que busca grupos en los datos cuyos miembros se parecen entre sí lo más posible y se diferencian de los de otros grupos.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html>
- **AWS AI Service Cards** (AI Service Cards, AI Service Card). *Servicio.* Fichas que publica AWS sobre sus servicios y modelos de IA (por ejemplo, Amazon Nova o Bedrock Guardrails) con los casos de uso previstos, las limitaciones, las decisiones de diseño responsable y las buenas prácticas de rendimiento.
  - Usar cuando: Para conocer el uso previsto y las limitaciones de un servicio o modelo de AWS antes de adoptarlo.
  - No usar cuando: Para documentar un modelo propio: SageMaker Model Cards.
  - Referencia: <https://aws.amazon.com/ai/responsible-ai/resources/>
- **algoritmo** (algoritmos, algorithm). *Concepto.* La «receta» con la que se resuelve un tipo de problema de ML. Al aplicarlo a unos datos de entrenamiento se obtiene un modelo. La relación entre algoritmos y tipos de problema es de muchos a muchos.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html>
- **alucinación** (alucinaciones, hallucination, hallucinations). *Concepto.* Respuesta incorrecta o engañosa que genera un modelo fundacional. Causas habituales: datos de entrenamiento insuficientes o sesgados, sobreajuste y falta de contexto. Se mitiga con RAG, prompts precisos y verificación.
  - Referencia: <https://aws.amazon.com/what-is/ai-hallucinations/>
- **análisis por subgrupos** (subgroup analysis). *Técnica.* Calcular las mismas métricas (exactitud, precisión, recall, tasa de aprobación) para cada grupo de personas, incluidos los interseccionales, y compararlas con un umbral aceptable para detectar sesgo que la media oculta.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/rairc03-bp02.html>
- **API Converse** (Converse API, Converse). *Concepto.* API unificada de Amazon Bedrock para conversar con los modelos: abstrae sus diferencias, de modo que se puede cambiar de modelo modificando un solo parámetro.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html>
- **aprendizaje automático** (ML, machine learning). *Concepto.* Subconjunto de la IA que usa grandes cantidades de datos para crear y validar una lógica de decisión, llamada modelo. Casi todos los sistemas de IA actuales se crean con ML.
  - Referencia: <https://docs.aws.amazon.com/decision-guides/latest/machine-learning-on-aws-how-to-choose/guide.html>
- **aprendizaje autosupervisado** (self-supervised learning). *Técnica.* Variante en la que las etiquetas se generan a partir de los propios datos de entrada (por ejemplo, ocultar una palabra y predecirla). Es como se preentrenan los modelos fundacionales con enormes volúmenes de datos sin etiquetar.
  - Referencia: <https://aws.amazon.com/what-is/foundation-models/>
- **aprendizaje no supervisado** (no supervisado, unsupervised learning). *Técnica.* Los datos no tienen etiquetas ni valores objetivo: el modelo descubre patrones, como agrupaciones, anomalías o una representación con menos dimensiones.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html>
- **aprendizaje por refuerzo** (reinforcement learning). *Técnica.* Un agente aprende un comportamiento por ensayo y error interactuando con un entorno dinámico, con el objetivo de maximizar las recompensas a largo plazo.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html>
- **aprendizaje profundo** (deep learning). *Concepto.* Método de IA inspirado en el cerebro humano que procesa datos con redes neuronales de muchas capas. Reconoce patrones complejos en imágenes, texto, sonido y otros datos.
  - Referencia: <https://aws.amazon.com/what-is/deep-learning/>
- **aprendizaje supervisado** (supervisado, supervised learning). *Técnica.* Los datos incluyen entradas y los valores objetivo (salidas) correctos. Si el objetivo es categórico es un problema de clasificación; si es continuo, de regresión.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html>
- **ARPU** (ingreso medio por usuario, average revenue per user). *Métrica.* Ingreso medio por usuario: ingresos totales divididos entre el número de usuarios en un periodo.
  - Referencia: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain2.html>
- **AWS Artifact** (Artifact). *Servicio.* Portal de descarga bajo demanda de los informes de seguridad y cumplimiento de AWS (por ejemplo, SOC, ISO o PCI) y de gestión de los acuerdos con AWS.
  - Usar cuando: Para entregar a un auditor la evidencia de cumplimiento de la infraestructura de AWS.
  - No usar cuando: Para demostrar la configuración o el cumplimiento de los recursos del propio cliente (Config).
  - Referencia: <https://docs.aws.amazon.com/artifact/latest/ug/what-is-aws-artifact.html>
- **AUC** (área bajo la curva ROC). *Métrica.* Área bajo la curva ROC: resume el rendimiento de un clasificador en todos los umbrales. 1 es perfecto y 0,5 equivale a adivinar al azar.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-metrics-validation.html>
- **AWS Audit Manager** (Audit Manager). *Servicio.* Servicio que recopila automáticamente evidencias para auditorías con marcos predefinidos o propios. Ya no está abierto a clientes nuevos; los existentes pueden seguir usándolo.
  - No usar cuando: Como opción para un proyecto nuevo: ya no admite clientes nuevos.
  - Referencia: <https://docs.aws.amazon.com/audit-manager/latest/userguide/what-is.html>
- **auditoría humana** (human audit, auditorías humanas). *Técnica.* Revisión por personas, idealmente independientes del equipo y con sus propios datos de evaluación, de los aspectos críticos o subjetivos de un sistema de IA (seguridad, sesgo, experiencia de usuario) antes de lanzarlo y de forma periódica.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/raier01-bp02.html>
- **Amazon Augmented AI** (Amazon A2I, A2I). *Servicio.* Servicio para añadir revisión humana a predicciones de ML con baja confianza o a muestras aleatorias (Textract, Rekognition, modelos propios). Ya no está abierto a clientes nuevos; los existentes pueden seguir usándolo.
  - Usar cuando: Clientes actuales que necesitan revisión humana de predicciones de baja confianza.
  - No usar cuando: Como opción para un proyecto nuevo: ya no admite clientes nuevos.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html>
- **Amazon Aurora** (Aurora, Aurora PostgreSQL). *Servicio.* Base de datos relacional gestionada compatible con MySQL y PostgreSQL. Con la extensión pgvector de PostgreSQL almacena embeddings y combina consultas SQL con búsqueda por similitud; Bedrock Knowledge Bases la admite como almacén vectorial.
  - Usar cuando: Cuando la aplicación ya usa SQL relacional y quiere combinar filtros relacionales y búsqueda vectorial en la misma base de datos.
  - No usar cuando: Cuando el caso pide relaciones de grafo (Neptune) o búsqueda de texto completo a gran escala (OpenSearch).
  - Referencia: <https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html>
- **Automated Reasoning checks** (comprobaciones de razonamiento automatizado). *Técnica.* Salvaguarda de Bedrock Guardrails que valida con lógica formal si una respuesta es coherente con una política de reglas definida por el cliente, explica por qué y señala supuestos no declarados. Solo detecta (no bloquea): devuelve hallazgos y la aplicación decide. Solo inglés (EE. UU.), sin streaming y sin protección frente a la inyección de prompts.
  - Usar cuando: Sectores regulados o reglas complejas (elegibilidad, prestaciones, normativa interna) donde hay que demostrar que la respuesta cumple las reglas.
  - No usar cuando: Para detectar contenido dañino, temas fuera de alcance o ataques de prompt: filtros de contenido y temas denegados.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html>

## B

- **base de datos vectorial** (bases de datos vectoriales, vector database). *Concepto.* Base de datos que almacena e indexa vectores (embeddings) para encontrar rápidamente los más parecidos a uno dado. Es la pieza de búsqueda semántica de RAG.
  - Referencia: <https://aws.amazon.com/what-is/vector-databases/>
- **Amazon Bedrock** (Bedrock). *Servicio.* Servicio totalmente gestionado que da acceso seguro a modelos fundacionales de alto rendimiento de las principales compañías de IA para crear y escalar aplicaciones de IA generativa.
  - Usar cuando: Para usar modelos fundacionales de varios proveedores mediante API, sin gestionar la infraestructura.
  - No usar cuando: Cuando se necesita entrenar un modelo propio desde cero o controlar toda la infraestructura de entrenamiento.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>
- **Amazon Bedrock AgentCore** (AgentCore). *Servicio.* Plataforma agéntica para crear, desplegar y operar agentes de IA de forma segura y a escala, con cualquier framework y modelo fundacional.
  - Usar cuando: Cuando hay un caso de uso agéntico que necesita ejecución, memoria, identidad y observabilidad gestionadas.
  - No usar cuando: Cuando basta una consulta sencilla a un modelo: no hace falta un agente.
  - Referencia: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html>
- **Amazon Bedrock Agents** (Bedrock Agents, Amazon Bedrock Agents Classic). *Servicio.* Permite crear y configurar agentes autónomos en una aplicación: orquestan las interacciones entre modelos fundacionales, fuentes de datos, aplicaciones y usuarios, y llaman a APIs para ejecutar acciones. Ahora se llama Agents Classic y ya no está abierto a clientes nuevos.
  - No usar cuando: En proyectos nuevos: AWS remite a Amazon Bedrock AgentCore para capacidades similares.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html>
- **Amazon Bedrock Flows** (Bedrock Flows). *Servicio.* Constructor visual de flujos de trabajo de IA generativa que enlaza prompts, modelos fundacionales, Knowledge Bases y otros servicios como AWS Lambda, y despliega flujos inmutables. Se paga por los recursos que usa.
  - Usar cuando: Procesos con pasos fijos y predecibles.
  - No usar cuando: Cuando los pasos dependen de lo que vaya pasando y el sistema debe decidir por sí mismo: eso es un agente (AgentCore).
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html>
- **Amazon Bedrock Guardrails** (Bedrock Guardrails, Guardrails). *Servicio.* Salvaguardas configurables para detectar y filtrar contenido no deseado y proteger información sensible en las entradas y respuestas de los modelos: filtros de contenido, temas denegados, filtros de palabras, filtros de información sensible, comprobación de grounding contextual y Automated Reasoning checks. Se aplica al invocar un modelo de Bedrock o con la API ApplyGuardrail, sin invocar un modelo.
  - Usar cuando: Para aplicar políticas de uso responsable y privacidad a una aplicación de IA generativa.
  - No usar cuando: Como sustituto de los permisos IAM o del cifrado de los datos.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html>
- **Amazon Bedrock Knowledge Bases** (Bedrock Knowledge Bases, Knowledge Bases). *Servicio.* Permite integrar información propia en aplicaciones de IA generativa mediante RAG: busca en tus datos la información relevante para una consulta y la usa para mejorar las respuestas del modelo. Hay dos tipos: Managed Knowledge Base (Bedrock gestiona ingesta, índice y almacén, con conectores y permisos por documento) y customer-managed (el cliente elige y gestiona el almacén vectorial).
  - Usar cuando: Cuando el modelo debe responder con información propia, específica o actualizada.
  - No usar cuando: Cuando el modelo no necesita datos propios ni actualizados.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html>
- **Amazon Bedrock Model Evaluation** (Bedrock Model Evaluation, Amazon Bedrock Evaluations, Bedrock Evaluations). *Servicio.* Evaluaciones de Amazon Bedrock: programáticas (conjuntos integrados o propios con métricas de exactitud, robustez y toxicidad), con trabajadores humanos, con un modelo juez (LLM-as-a-judge) y de fuentes RAG o Knowledge Bases.
  - Usar cuando: Para comparar modelos, prompts o Knowledge Bases con datos del caso antes de elegir o de pasar a producción.
  - No usar cuando: Para evaluar agentes a partir de sus trazas: AgentCore Evaluations.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html>
- **Amazon Bedrock Prompt Management** (Prompt Management, Bedrock Prompt Management). *Servicio.* Funcionalidad de Amazon Bedrock para crear, guardar, probar y versionar prompts reutilizables: variables, variantes comparables, borrador y versiones inmutables que la aplicación invoca por su ARN o desde Bedrock Flows.
  - Usar cuando: Para reutilizar prompts probados, compararlos y desplegarlos o revertirlos por versiones sin tocar el código.
  - No usar cuando: Como control de seguridad: los ataques de prompt se filtran con Guardrails.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html>
- **benchmark** (benchmarks, benchmark datasets, conjunto de referencia). *Concepto.* Conjunto de datos de referencia con preguntas y respuestas conocidas para medir y comparar modelos de forma repetible. Bedrock incluye conjuntos integrados (TREX, BOLD, RealToxicityPrompts, Gigaword, BoolQ…) y admite conjuntos propios.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-tasks.html>
- **BERTScore**. *Métrica.* Métrica que compara los embeddings de la respuesta y de la referencia para medir su similitud semántica: reconoce paráfrasis que ROUGE y BLEU penalizan. Bedrock la usa en las tareas de resumen.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-tasks.html>
- **BLEU** (Bilingual Evaluation Understudy). *Métrica.* Métrica que mide el solapamiento de n-gramas orientada a la precisión (cuánto de la respuesta aparece en la referencia) y penaliza respuestas demasiado cortas. Típica de traducción automática.
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/dev-experimenting-quality.html>
- **AWS Budgets** (Budgets). *Servicio.* Permite definir presupuestos de coste o de uso y recibir alertas cuando el gasto real o previsto los supera.
  - Usar cuando: Para avisar antes de que un laboratorio o un proyecto de IA supere un gasto previsto.
  - No usar cuando: Para analizar en detalle el gasto histórico (AWS Cost Explorer).
  - Referencia: <https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html>

## C

- **calidad de las etiquetas** (label quality). *Técnica.* Control de las etiquetas de un conjunto de datos: formación de los anotadores, acuerdo entre anotadores, ejemplos con respuesta conocida, búsqueda de sesgos de los anotadores y contraste de las etiquetas sintéticas con el juicio humano.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/raidp02-bp03.html>
- **catalogación de datos** (data cataloging, catálogo de datos). *Concepto.* Inventario de los conjuntos de datos con su ubicación, esquema y metadatos para que se puedan encontrar y gobernar. En AWS, el AWS Glue Data Catalog.
  - Referencia: <https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html>
- **chain-of-thought** (cadena de pensamiento). *Técnica.* Técnica de prompt que pide al modelo razonar paso a paso antes de dar la respuesta. Mejora los problemas de varios pasos (cálculos, lógica) a cambio de más tokens de salida y latencia.
  - Referencia: <https://aws.amazon.com/what-is/prompt-engineering/>
- **chunking** (chunks, fragmentación de documentos). *Técnica.* Dividir documentos largos en fragmentos (chunks) antes de convertirlos en embeddings. Bedrock Knowledge Bases ofrece fragmentación de tamaño fijo (tokens por fragmento y solapamiento), jerárquica, semántica o sin fragmentar.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html>
- **ciclo de vida de los datos** (data lifecycle). *Concepto.* Qué ocurre con los datos desde que se crean hasta que se borran: almacenamiento, uso, archivo y eliminación según políticas. En S3 se automatiza con S3 Lifecycle.
  - Referencia: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>
- **citación de fuentes** (source citation). *Técnica.* Indicar de qué documentos sale cada respuesta. Amazon Bedrock Knowledge Bases devuelve citas con los fragmentos y documentos de origen, lo que permite comprobar la respuesta.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-retrieve-generate.html>
- **clasificación** (classification, clasificación binaria, clasificación multiclase). *Técnica.* Problema supervisado cuyo valor objetivo es categórico: asignar un elemento a una clase. Es binaria si hay dos clases (spam o no spam) y multiclase si hay varias (el tema de un documento).
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html>
- **Amazon CloudFront** (CloudFront). *Servicio.* Red de distribución de contenido que acelera la entrega de contenido web estático y dinámico a los usuarios desde ubicaciones de borde de todo el mundo.
  - Usar cuando: Para servir con baja latencia la interfaz web de una aplicación que usa IA.
  - No usar cuando: Para invocar o alojar el modelo (Bedrock, SageMaker AI).
  - Referencia: <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html>
- **AWS CloudTrail** (CloudTrail). *Servicio.* Servicio que registra la actividad de la cuenta (llamadas a la API de AWS: quién, qué, cuándo y desde dónde) para auditoría, gobierno y cumplimiento.
  - Usar cuando: Para auditar el uso de los servicios, por ejemplo quién invocó un modelo o cambió un permiso.
  - No usar cuando: Para monitorizar métricas de rendimiento (Amazon CloudWatch).
  - Referencia: <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html>
- **Amazon CloudWatch** (CloudWatch). *Servicio.* Servicio de monitorización de recursos y aplicaciones de AWS: recoge métricas y registros (logs) y permite crear alarmas cuando una métrica supera un umbral.
  - Usar cuando: Para vigilar el rendimiento y el uso de un endpoint o una aplicación y recibir alarmas.
  - No usar cuando: Para auditar quién hizo qué llamada a la API (AWS CloudTrail).
  - Referencia: <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html>
- **CLV** (valor del ciclo de vida del cliente, customer lifetime value). *Métrica.* Valor del ciclo de vida del cliente: ingresos que se esperan de un cliente durante toda su relación con la empresa. Sube cuando mejora la retención.
  - Referencia: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain2.html>
- **Amazon Comprehend** (Comprehend). *Servicio.* Usa procesamiento del lenguaje natural (NLP) para extraer información del contenido de los documentos: reconoce entidades, frases clave, idioma, opiniones y otros elementos.
  - Usar cuando: Para analizar texto: opiniones de clientes, entidades o temas de un conjunto de documentos.
  - No usar cuando: Cuando el problema no es de lenguaje natural (imágenes, datos tabulares).
  - Referencia: <https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html>
- **AWS Config** (Config). *Servicio.* Servicio que registra la configuración de los recursos de AWS, cómo se relacionan y cómo ha cambiado con el tiempo, y la evalúa con reglas y paquetes de conformidad.
  - Usar cuando: Para comprobar que los recursos de un sistema de IA cumplen reglas (cifrado, acceso público) y ver su historial de configuración.
  - No usar cuando: Para saber quién hizo una llamada a la API (CloudTrail).
  - Referencia: <https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html>
- **conjunto de datos equilibrado** (balanced dataset, datos equilibrados). *Concepto.* Conjunto en el que cada grupo y cada clase tienen suficientes ejemplos para aprender y medir. Los huecos se cubren recogiendo más datos o con muestreo estratificado.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/raidp03-bp02.html>
- **contextual grounding check** (comprobación de grounding contextual, contextual grounding checks). *Técnica.* Salvaguarda de Bedrock Guardrails que detecta alucinaciones: puntúa si la respuesta se basa en la fuente de referencia (grounding) y si responde a la pregunta (relevancia), y bloquea las que quedan por debajo del umbral (0 a 0,99). Para resúmenes, paráfrasis y preguntas y respuestas; no para chat conversacional.
  - Usar cuando: En RAG o resúmenes, para bloquear respuestas que añaden datos que no están en la fuente.
  - No usar cuando: Para comprobar respuestas contra reglas lógicas de negocio: Automated Reasoning checks.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html>
- **controlabilidad** (controllability). *Concepto.* Dimensión de la IA responsable: disponer de mecanismos para supervisar y dirigir el comportamiento del sistema, por ejemplo supervisión humana, límites de actuación de un agente o la posibilidad de corregir o detener una acción.
  - Referencia: <https://aws.amazon.com/ai/responsible-ai/>
- **AWS Cost Explorer** (Cost Explorer). *Servicio.* Herramienta para visualizar, entender y analizar los costes y el uso de AWS a lo largo del tiempo, con previsiones.
  - Usar cuando: Para ver qué servicios generan el gasto (por ejemplo, la inferencia de un modelo) y su tendencia.
  - No usar cuando: Para recibir alertas automáticas al superar un umbral (AWS Budgets).
  - Referencia: <https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html>
- **coste por interacción** (cost per interaction). *Métrica.* Coste total de una aplicación de IA (inferencia, almacenamiento, otros servicios) dividido entre el número de interacciones en un periodo.
  - Referencia: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain3.html>
- **curación de datos** (data curation). *Concepto.* Seleccionar, limpiar, deduplicar y revisar los datos antes de entrenar o ajustar un modelo: quitar errores, contenido tóxico y datos personales innecesarios.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-prepare.html>

## D

- **AWS Data Exchange** (Data Exchange). *Servicio.* Servicio para compartir y gestionar a escala datos de otras organizaciones (concesiones de datos y suscripciones de AWS Marketplace) y usarlos con servicios de analítica y ML.
  - Usar cuando: Para obtener conjuntos de datos de terceros con los que entrenar o enriquecer un modelo.
  - No usar cuando: Para preparar o transformar los datos (AWS Glue, Amazon EMR).
  - Referencia: <https://docs.aws.amazon.com/data-exchange/latest/userguide/what-is.html>
- **datos estructurados** (datos no estructurados, estructurados, no estructurados). *Concepto.* Los datos estructurados siguen un formato predefinido, normalmente tabular con filas y columnas. Los no estructurados (audio, vídeo, imágenes, documentos largos) no siguen reglas ni un esquema predeterminado.
  - Referencia: <https://aws.amazon.com/compare/the-difference-between-structured-data-and-unstructured-data/>
- **datos etiquetados** (etiquetado de datos, datos sin etiquetar, etiquetas). *Concepto.* Datos a los que se ha añadido una etiqueta informativa (por ejemplo, que una foto contiene un pájaro) para que un modelo supervisado pueda aprender de ellos.
  - Referencia: <https://aws.amazon.com/what-is/data-labeling/>
- **decisiones con consecuencias** (consequential decisions). *Concepto.* Decisiones que afectan a derechos, salud o seguridad de las personas (diagnóstico médico, crédito, empleo, vivienda, prestaciones, asesoramiento legal o financiero). Según la política de AWS, exigen evaluar riesgos e implantar supervisión humana y pruebas.
  - Referencia: <https://aws.amazon.com/ai/responsible-ai/policy/>
- **deriva** (deriva del modelo, deriva de datos, drift). *Concepto.* Cambio con el tiempo de los datos de producción (o de la relación entre entradas y resultados) respecto a los de entrenamiento, que degrada la calidad del modelo. Se detecta monitorizando y se corrige reentrenando.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/monitoring.html>
- **desequilibrio de clases** (class imbalance). *Métrica.* Métrica de sesgo previa al entrenamiento: CI = (na − nd) / (na + nd), con na y nd el número de miembros de cada grupo. Va de −1 a 1; cerca de 0 indica grupos equilibrados.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-bias-metric-class-imbalance.html>
- **destilación** (model distillation, distillation, Amazon Bedrock Model Distillation). *Técnica.* Transferir el conocimiento de un modelo grande (maestro) a uno más pequeño, rápido y barato (alumno) para un caso de uso. Bedrock genera respuestas del maestro con los prompts del cliente (o las toma de los registros de invocación) y ajusta al alumno.
  - Usar cuando: Cuando se quiere una calidad cercana a la del modelo grande con la latencia y el precio de uno pequeño.
  - No usar cuando: Cuando el problema es que faltan datos propios o actualizados: RAG.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-distillation.html>
- **detección de anomalías** (anomaly detection). *Técnica.* Identificación de elementos o eventos poco habituales que se desvían significativamente del resto de los datos; sirve, por ejemplo, para detectar fraude bancario o errores médicos.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html>
- **diferencia en las proporciones de etiquetas** (difference in proportions of labels, DPL). *Métrica.* Métrica de sesgo previa al entrenamiento: DPL = qa − qd, la diferencia entre la proporción de resultados positivos observados en un grupo y en otro. Un modelo entrenado con un DPL alto tiende a reproducirlo.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-data-bias-metric-true-label-imbalance.html>
- **diseño centrado en las personas** (human-centered design). *Concepto.* Diseñar el sistema de IA a partir de quién lo usa y qué necesita entender: transparencia de las decisiones, explicaciones adaptadas, supervisión humana donde hay consecuencias, feedback de los usuarios y accesibilidad.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/raigt01-bp04.html>
- **Amazon DocumentDB** (DocumentDB). *Servicio.* Base de datos de documentos compatible con MongoDB, con búsqueda vectorial nativa desde la versión 5.0.
  - Usar cuando: Aplicaciones que ya usan la API de MongoDB y quieren añadir búsqueda semántica.
  - No usar cuando: Cuando el caso no usa documentos JSON ni la API de MongoDB.
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-an-aws-vector-database-for-rag-use-cases/vector-db-options.html>
- **Amazon DynamoDB** (DynamoDB). *Servicio.* Base de datos NoSQL sin servidor y totalmente gestionada. Tiene índices vectoriales nativos que se consultan con la API SearchVectors para buscar por similitud junto a los datos operativos, sin otra base de datos ni réplicas.
  - Usar cuando: RAG o memoria de agentes cuando los datos operativos ya están en DynamoDB.
  - No usar cuando: Como almacén de una Bedrock Knowledge Base: no está admitido.
  - Referencia: <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/VectorSearch.html>

## E

- **Amazon EC2** (EC2, Amazon Elastic Compute Cloud). *Servicio.* Capacidad de cómputo escalable bajo demanda en la nube de AWS: servidores virtuales llamados instancias. El cliente elige el tipo de instancia, la red y el almacenamiento, y gestiona el sistema operativo invitado.
  - Usar cuando: Cuando se necesita control del sistema operativo, de la red y del almacenamiento (por ejemplo, para alojar un modelo propio).
  - No usar cuando: Cuando basta un servicio gestionado y no se quiere asumir parches, actualizaciones ni configuración del servidor.
  - Referencia: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html>
- **Amazon ECS** (ECS, Amazon Elastic Container Service). *Servicio.* Servicio totalmente gestionado de orquestación de contenedores para desplegar, gestionar y escalar aplicaciones en contenedores, integrado con Amazon ECR.
  - Usar cuando: Para desplegar en contenedores una aplicación o un modelo propio sin gestionar Kubernetes.
  - No usar cuando: Cuando la organización ya estandariza en Kubernetes (Amazon EKS) o basta un endpoint gestionado de SageMaker AI.
  - Referencia: <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html>
- **Amazon EKS** (EKS, Amazon Elastic Kubernetes Service). *Servicio.* Servicio gestionado de Kubernetes que elimina la complejidad de operar clústeres de Kubernetes para desplegar aplicaciones en contenedores.
  - Usar cuando: Para desplegar modelos o aplicaciones en Kubernetes cuando la organización ya usa ese estándar.
  - No usar cuando: Cuando basta un servicio de contenedores más sencillo (Amazon ECS) o un endpoint gestionado de SageMaker AI.
  - Referencia: <https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html>
- **Amazon ElastiCache** (ElastiCache, ElastiCache para Valkey). *Servicio.* Caché y almacén de datos en memoria totalmente gestionado (Valkey, Redis OSS, Memcached). Desde Valkey 8.2 ofrece búsqueda vectorial en memoria con latencias mínimas.
  - Usar cuando: Búsqueda semántica en tiempo real, caché semántica o memoria de agentes con latencias mínimas.
  - No usar cuando: Como almacén de una Bedrock Knowledge Base: no está admitido.
  - Referencia: <https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/vector-search-overview.html>
- **embedding** (embeddings, incrustaciones vectoriales). *Concepto.* Representación numérica (un vector) de un objeto del mundo real, como un texto o una imagen, que captura su significado. Objetos parecidos tienen embeddings cercanos, lo que permite buscar por similitud semántica.
  - Referencia: <https://aws.amazon.com/what-is/embeddings-in-machine-learning/>
- **Amazon EMR** (EMR, Amazon Elastic MapReduce). *Servicio.* Plataforma gestionada de clústeres para ejecutar marcos de big data como Apache Hadoop y Apache Spark y procesar y analizar grandes volúmenes de datos.
  - Usar cuando: Para preparar con Spark o Hadoop volúmenes de datos muy grandes antes de entrenar un modelo.
  - No usar cuando: Para una preparación visual y sin código (AWS Glue DataBrew).
  - Referencia: <https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html>
- **envenenamiento de datos** (poisoning, data poisoning). *Concepto.* Introducción intencionada de datos maliciosos o sesgados en los datos de entrenamiento, de ajuste fino o en las fuentes de RAG para alterar el comportamiento del modelo. Se mitiga con curación, gobierno y control de acceso a los datos.
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/llm-prompt-engineering-best-practices/common-attacks.html>
- **evaluación humana** (human-in-the-loop, human evaluation). *Técnica.* Evaluación en la que personas (empleados o expertos) puntúan o comparan respuestas del modelo. Capta criterios subjetivos y es la referencia final, pero es lenta y cara.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-human.html>
- **exactitud** (accuracy). *Métrica.* Proporción de elementos clasificados correctamente sobre el total de elementos clasificados. Va de 0 a 1. Engaña con clases desequilibradas: si solo el 1 % de las operaciones es fraude, un modelo que nunca detecta fraude tiene un 99 % de exactitud.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-metrics-validation.html>
- **exceso de autonomía** (excessive agency). *Concepto.* Riesgo de que un agente de IA tenga más permisos o capacidad de acción de la necesaria, lo que multiplica el daño de un error o de una inyección de prompts. Se limita con mínimo privilegio, Policy in AgentCore y aprobación humana.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/security.html>
- **exhaustividad** (recall, sensibilidad). *Métrica.* De todos los positivos reales, cuántos detecta el modelo: VP / (VP + FN). Se prioriza cuando un falso negativo es costoso, por ejemplo al detectar una enfermedad.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-metrics-validation.html>
- **explicabilidad** (explainability). *Concepto.* Dimensión de la IA responsable: entender y evaluar por qué el sistema da una salida concreta, aunque el modelo sea complejo. Se apoya en explicaciones locales y globales (por ejemplo, SHAP), citas de fuentes o trazas de agentes.
  - Referencia: <https://aws.amazon.com/ai/responsible-ai/>

## F

- **few-shot** (few-shot prompting, one-shot, single-shot). *Técnica.* Técnica de prompt que incluye ejemplos de entrada y salida: uno (one-shot o single-shot) o varios (few-shot). Enseña un formato o una clasificación propia sin entrenar, a cambio de más tokens de entrada.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering-guidelines.html>
- **ficha de datos** (datasheet, datasheets). *Concepto.* Documento vivo que describe un conjunto de datos: uso previsto y no previsto, fuentes, forma de recogida, etiquetado, distribución y sesgos o limitaciones conocidos.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/raidp04-bp05.html>
- **filtros de contenido** (content filters, filtro de contenido). *Técnica.* Salvaguarda de Bedrock Guardrails que detecta contenido dañino en texto o imágenes por categorías (odio, insultos, sexual, violencia, conducta indebida y ataque de prompt), con una intensidad configurable para cada una.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-content-filters.html>
- **filtros de información sensible** (sensitive information filters). *Técnica.* Salvaguarda de Bedrock Guardrails que detecta datos personales (PII) y patrones propios con expresiones regulares en las entradas y respuestas, y bloquea el mensaje o enmascara el dato.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html>
- **filtros de palabras** (word filters). *Técnica.* Salvaguarda de Bedrock Guardrails que bloquea palabras o frases exactas de hasta tres palabras, sin distinguir mayúsculas y por palabra completa: una lista predefinida de blasfemias o términos propios, como nombres de la competencia. No tiene coste.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-word-filters.html>
- **fine-tuning** (ajuste fino, supervised fine-tuning). *Técnica.* Personalización de un modelo preentrenado con datos etiquetados de una tarea o dominio, que ajusta los parámetros del modelo. En Amazon Bedrock existen también el reinforcement fine-tuning y la destilación.
  - Usar cuando: Cuando el prompt y el contexto no consiguen la calidad, el estilo o el formato necesarios.
  - No usar cuando: Cuando el problema es que faltan datos actualizados o propios: eso lo resuelve RAG.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html>
- **fmeval** (FMEval). *Servicio.* Biblioteca de código abierto de AWS para evaluar modelos de lenguaje (exactitud, robustez, toxicidad y otras dimensiones), la que usa la evaluación de modelos fundacionales de SageMaker Clarify. Para proyectos nuevos, AWS indica Amazon Bedrock Evaluations como vía gestionada.
  - Usar cuando: Para evaluar con control total, en código, modelos de lenguaje alojados dentro o fuera de AWS.
  - No usar cuando: Cuando basta una evaluación gestionada de modelos de Bedrock (Bedrock Evaluations).
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-foundation-model-evaluate.html>
- **fuga de prompt** (prompt leakage). *Concepto.* Riesgo de exposición: el usuario consigue que el modelo revele las instrucciones del sistema, la configuración o el historial de la conversación. Guardrails lo detecta en su modalidad Standard (no en la Classic).
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html>

## G

- **Generative AI Security Scoping Matrix** (AI Security Scoping Matrix, Security Scoping Matrix). *Concepto.* Marco de AWS que clasifica los casos de IA generativa en cinco ámbitos según cuánto controla la organización el modelo y sus datos (aplicación de consumo, aplicación empresarial, modelo preentrenado, modelo ajustado, modelo propio) y los cruza con cinco disciplinas: gobierno y cumplimiento, legal y privacidad, gestión de riesgos, controles y resiliencia.
  - Referencia: <https://aws.amazon.com/ai/generative-ai/security/scoping-matrix/>
- **AWS Glue** (Glue). *Servicio.* Servicio serverless de integración de datos para descubrir, preparar, mover e integrar datos de varias fuentes (ETL), con un catálogo de datos centralizado (AWS Glue Data Catalog).
  - Usar cuando: Para preparar y transformar datos (ETL) antes de entrenar un modelo o analizarlos.
  - No usar cuando: Para entrenar o desplegar modelos: eso es SageMaker AI.
  - Referencia: <https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html>
- **AWS Glue Data Catalog** (Glue Data Catalog, Data Catalog). *Servicio.* Repositorio central de metadatos de los conjuntos de datos de la organización: ubicación, esquema y métricas. Se rellena con rastreadores (crawlers) o a mano y lo usan Athena, Lake Formation o EMR.
  - Usar cuando: Para saber qué conjuntos de datos existen, dónde están y con qué esquema.
  - No usar cuando: Para controlar permisos detallados sobre esos datos (Lake Formation).
  - Referencia: <https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html>
- **AWS Glue Data Quality** (Glue Data Quality). *Servicio.* Funcionalidad serverless de AWS Glue para medir y vigilar la calidad de los datos con reglas (recomendadas o propias), una puntuación de calidad y detección de anomalías con ML.
  - Usar cuando: Para comprobar la calidad de los datos antes de entrenar o ajustar un modelo.
  - No usar cuando: Para descubrir datos personales (Macie).
  - Referencia: <https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html>
- **AWS Glue DataBrew** (DataBrew, Glue DataBrew). *Servicio.* Herramienta visual de preparación de datos que permite limpiar y normalizar datos sin escribir código, con más de 250 transformaciones predefinidas. Es serverless.
  - Usar cuando: Cuando analistas sin experiencia en programación deben limpiar datos para analítica o ML.
  - No usar cuando: Cuando se necesita un pipeline ETL programado a medida (AWS Glue) o entrenar un modelo.
  - Referencia: <https://docs.aws.amazon.com/databrew/latest/dg/what-is.html>
- **GraphRAG**. *Técnica.* Variante de RAG que combina la búsqueda vectorial con un grafo de conocimiento, para recuperar también las relaciones entre entidades. En AWS, con Amazon Neptune Analytics y Bedrock Knowledge Bases.
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-an-aws-vector-database-for-rag-use-cases/vector-db-options.html>
- **Amazon GuardDuty** (GuardDuty). *Servicio.* Servicio de detección de amenazas que analiza de forma continua registros y datos de la cuenta con inteligencia de amenazas y ML para encontrar actividad sospechosa, como credenciales comprometidas o exfiltración de datos. Está fuera del alcance del examen AIF-C01: basta reconocerlo.
  - Referencia: <https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html>

## I

- **IA agéntica** (agentic AI). *Concepto.* Sistema de IA autónomo que puede actuar de forma independiente para alcanzar objetivos predefinidos, sin una supervisión humana constante. En AWS, un agente orquesta modelos, fuentes de datos y aplicaciones, y llama a APIs para ejecutar acciones.
  - Referencia: <https://aws.amazon.com/what-is/agentic-ai/>
- **IA generativa** (GenAI, generative AI). *Concepto.* Conjunto de sistemas y modelos de IA diseñados para generar contenido nuevo (texto, código, imágenes, música u otros datos) a partir de patrones aprendidos de datos existentes. Es un subconjunto del aprendizaje profundo.
  - Referencia: <https://docs.aws.amazon.com/decision-guides/latest/generative-ai-on-aws-how-to-choose/guide.html>
- **IA responsable** (responsible AI). *Concepto.* Disciplina de diseñar, desarrollar y usar la IA con el objetivo de maximizar los beneficios y minimizar los riesgos. AWS la concreta en dimensiones: equidad, explicabilidad, privacidad y seguridad, seguridad frente a daños, controlabilidad, veracidad y robustez, gobierno y transparencia.
  - Referencia: <https://aws.amazon.com/ai/responsible-ai/>
- **AWS Identity and Access Management (IAM)** (IAM, AWS IAM, AWS Identity and Access Management). *Servicio.* Servicio que controla de forma segura el acceso a los recursos de AWS: quién está autenticado (ha iniciado sesión) y quién está autorizado (tiene permisos) para usar qué recursos.
  - No usar cuando: No es un servicio de datos ni de cómputo: no sustituye al cifrado ni a las políticas de la propia aplicación.
  - Referencia: <https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html>
- **impacto dispar** (disparate impact). *Métrica.* Métrica de sesgo posterior al entrenamiento: DI = q'd / q'a, la proporción de predicciones positivas del grupo desfavorecido entre la del favorecido. 1 indica paridad; por debajo de 1, el grupo d recibe menos resultados positivos.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-post-training-bias-metric-di.html>
- **in-context learning** (aprendizaje en contexto). *Técnica.* Capacidad del modelo de adaptarse a una tarea a partir de las instrucciones y los ejemplos que recibe en el prompt, sin cambiar sus parámetros. Es la forma más barata de personalización.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering-guidelines.html>
- **inclusividad** (inclusivity, inclusión). *Concepto.* Que el sistema funcione bien para todos los grupos que lo van a usar, incluidos los minoritarios y las personas con necesidades de accesibilidad. Empieza por conjuntos de datos que los representen.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/raidp03-bp02.html>
- **indemnización de propiedad intelectual** (IP indemnity). *Concepto.* AWS ofrece una indemnización sin límite frente a reclamaciones de terceros por derechos de autor sobre la salida de los modelos de Amazon y de otros servicios de IA generativa enumerados en sus condiciones de servicio, siempre que el cliente use el servicio de forma responsable.
  - Referencia: <https://aws.amazon.com/bedrock/faqs/>
- **inferencia** (inferir, inference). *Concepto.* Uso de un modelo ya entrenado para obtener predicciones sobre datos nuevos. Se distingue del entrenamiento, que es el proceso de crear el modelo a partir de datos conocidos.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html>
- **inferencia asíncrona** (asynchronous inference). *Técnica.* Opción de SageMaker AI que encola las solicitudes y las procesa de forma asíncrona: ideal para cargas grandes o con tiempos de procesamiento largos. Puede escalar a cero cuando no hay solicitudes.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html>
- **inferencia en tiempo real** (real-time inference). *Técnica.* Opción de SageMaker AI para cargas interactivas con requisitos de baja latencia: un endpoint gestionado y permanente, con escalado automático.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html>
- **inferencia entre Regiones** (cross-Region inference, CRIS). *Concepto.* Enrutamiento automático de las peticiones de Amazon Bedrock a otras Regiones para ganar rendimiento. La geográfica se limita a una zona (EE. UU., UE, APAC) y sirve para residencia de datos; la global usa cualquier Región comercial y ahorra aproximadamente un 10 %. Sin coste adicional de enrutamiento.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html>
- **inferencia por lotes de Bedrock** (batch inference). *Concepto.* Modo de Amazon Bedrock que procesa de forma asíncrona muchos prompts de una vez: la entrada y la salida van a Amazon S3. En los modelos que lo admiten cuesta un 50 % menos que bajo demanda. No admite llamadas a herramientas.
  - Usar cuando: Para grandes volúmenes que no necesitan respuesta inmediata.
  - No usar cuando: En aplicaciones interactivas o conversaciones de varios turnos.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/batch-inference.html>
- **inferencia serverless** (Serverless Inference). *Técnica.* Opción de SageMaker AI que despliega y escala modelos sin gestionar la infraestructura. Es ideal para cargas con periodos de inactividad entre ráfagas de tráfico que toleran arranques en frío, y se paga por uso.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html>
- **AWS Inferentia** (Inferentia). *Servicio.* Chips diseñados por AWS específicamente para la inferencia de aprendizaje profundo e IA generativa, con alto rendimiento al menor coste en Amazon EC2. AWS indica que las instancias Inf2 ofrecen hasta un 50 % más de rendimiento por vatio que instancias EC2 comparables, lo que ayuda a los objetivos de sostenibilidad.
  - Usar cuando: Para servir en EC2 un modelo ya entrenado al menor coste por inferencia.
  - No usar cuando: Para entrenar modelos: para eso está AWS Trainium.
  - Referencia: <https://aws.amazon.com/ai/machine-learning/inferentia/>
- **ingeniería de contexto** (context engineering). *Técnica.* Decidir qué información llega al modelo en cada llamada, en qué orden y con qué tamaño: instrucciones del sistema, historial y memoria, conocimiento recuperado (RAG), herramientas y ejemplos. Busca respuestas correctas sin desperdiciar tokens.
  - Referencia: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html>
- **ingeniería de prompts** (prompt engineering). *Técnica.* Redactar y refinar el prompt (instrucciones, contexto, ejemplos y pregunta) para que el modelo dé la respuesta deseada sin modificar el modelo. Es la forma más barata de adaptar un modelo fundacional.
  - Referencia: <https://aws.amazon.com/what-is/prompt-engineering/>
- **Amazon Inspector** (Inspector). *Servicio.* Servicio de gestión de vulnerabilidades que descubre y escanea de forma continua instancias EC2, imágenes de contenedores en ECR y funciones Lambda en busca de vulnerabilidades de software y exposición de red no deseada.
  - Usar cuando: Para detectar bibliotecas vulnerables en el software que sirve o rodea a un modelo.
  - No usar cuando: Para obtener informes de cumplimiento de AWS (Artifact) o recomendaciones generales (Trusted Advisor).
  - Referencia: <https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html>
- **instrucciones del sistema** (system prompt, prompt del sistema). *Concepto.* Parte fija del prompt que define el papel, las reglas, el tono y el formato de todas las respuestas de una aplicación, separada del mensaje que escribe el usuario.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/design-a-prompt.html>
- **instruction tuning** (ajuste por instrucciones). *Técnica.* Ajuste fino con pares instrucción → respuesta para que el modelo siga mejor las instrucciones de un tipo de tarea.
  - Referencia: <https://aws.amazon.com/what-is/foundation-models/>
- **integridad de los datos** (data integrity). *Concepto.* Garantía de que los datos no se alteran sin control: versiones, registros de cambios y permisos de escritura mínimos, también como defensa frente al envenenamiento de los datos de entrenamiento.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/raidp04-bp03.html>
- **inteligencia artificial** (IA, AI). *Concepto.* Cualquier sistema capaz de replicar tareas que antes requerían inteligencia humana. La mayoría de los casos de uso buscan un resultado probabilístico: una predicción o decisión con un alto grado de certeza.
  - Referencia: <https://docs.aws.amazon.com/decision-guides/latest/machine-learning-on-aws-how-to-choose/guide.html>
- **Intelligent Prompt Routing** (enrutamiento inteligente de prompts). *Técnica.* Funcionalidad de Amazon Bedrock que envía cada petición, dentro de una familia de modelos, al que predice que dará la mejor calidad al menor coste: las preguntas sencillas a un modelo pequeño y las complejas a uno más capaz.
  - Referencia: <https://aws.amazon.com/bedrock/pricing/>
- **interpretabilidad** (interpretability). *Concepto.* Grado en que se entiende cómo funciona un modelo por dentro sin herramientas adicionales. Los modelos simples (regresión lineal, árbol de decisión) son más interpretables; los complejos suelen rendir más pero necesitan explicaciones a posteriori.
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/ml-model-interpretability/overview.html>

## J

- **jailbreaking** (jailbreak, jailbreaks). *Concepto.* Ataque con prompts diseñados para saltarse las protecciones de seguridad y moderación del propio modelo y obtener contenido dañino (por ejemplo, prompts tipo DAN o juegos de rol). Guardrails incluye un filtro de jailbreaks.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html>

## K

- **Kiro**. *Servicio.* Plataforma de desarrollo con IA de AWS, basada en especificaciones (spec-driven development), con un IDE y una CLI en los que agentes de IA ayudan a planificar, escribir y probar código.
  - Usar cuando: Para acelerar el desarrollo de software (incluidas aplicaciones de IA) con un asistente agéntico.
  - No usar cuando: Cuando la pregunta trata de entrenar o desplegar un modelo de ML.
  - Referencia: <https://aws.amazon.com/documentation-overview/kiro/>
- **AWS KMS** (AWS Key Management Service, KMS). *Servicio.* Servicio gestionado para crear y controlar las claves de cifrado y firma. Las claves se protegen en módulos de seguridad de hardware y no salen del servicio sin cifrar. En Bedrock cifra con claves del cliente modelos personalizados, agentes, ingesta de Knowledge Bases y evaluaciones.
  - Usar cuando: Para cifrar en reposo datos y modelos con claves que controla la empresa y auditar su uso.
  - No usar cuando: Para guardar contraseñas o claves de API de terceros (Secrets Manager).
  - Referencia: <https://docs.aws.amazon.com/kms/latest/developerguide/overview.html>

## L

- **AWS Lake Formation** (Lake Formation). *Servicio.* Servicio para gobernar, proteger y compartir los datos de un lago de datos con permisos detallados por columna, fila y celda sobre los datos de S3 y sus metadatos del AWS Glue Data Catalog.
  - Usar cuando: Para que cada equipo o modelo acceda solo a las columnas o filas que necesita.
  - No usar cuando: Para descubrir datos personales en S3 (Macie) o catalogar los conjuntos de datos (Glue Data Catalog).
  - Referencia: <https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html>
- **AWS Lambda** (Lambda). *Servicio.* Servicio de cómputo serverless: ejecuta código sin aprovisionar ni gestionar servidores. AWS se encarga del mantenimiento, la capacidad, el escalado y los parches.
  - Usar cuando: Para ejecutar código en respuesta a eventos o llamadas a una API sin gestionar servidores.
  - No usar cuando: Cuando se necesita control sobre el servidor o el sistema operativo.
  - Referencia: <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>
- **Amazon Lex** (Lex, Amazon Lex V2). *Servicio.* Servicio para crear interfaces conversacionales por voz y texto en las aplicaciones, con comprensión del lenguaje natural (NLU) y reconocimiento automático del habla (ASR).
  - Usar cuando: Para construir un chatbot o asistente de voz propio.
  - No usar cuando: Cuando solo se quiere analizar texto existente, sin diálogo con el usuario.
  - Referencia: <https://docs.aws.amazon.com/lexv2/latest/dg/what-is.html>
- **linaje de datos** (data lineage, linaje). *Concepto.* Recorrido de los datos y artefactos desde su origen hasta el modelo desplegado (conjunto de datos, versión, trabajo de entrenamiento, endpoint). SageMaker ML Lineage Tracking lo registra para reproducir el flujo y auditarlo.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html>
- **LLM** (modelo de lenguaje de gran tamaño, large language model, LLMs). *Concepto.* Modelo de aprendizaje profundo muy grande, preentrenado con enormes cantidades de datos y basado en la arquitectura transformer, capaz de comprender y generar lenguaje.
  - Referencia: <https://aws.amazon.com/what-is/large-language-model/>
- **LLM-as-a-judge** (modelo juez, LLM como juez). *Técnica.* Evaluación en la que un segundo modelo puntúa las respuestas de otro con una rúbrica (corrección, fidelidad, relevancia, tono…) y explica la nota. Escala bien, pero el juez debe validarse con personas y conviene que sea de otra familia de modelos.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-judge.html>

## M

- **Amazon Macie** (Macie). *Servicio.* Servicio de seguridad de datos que descubre datos sensibles en Amazon S3 con aprendizaje automático y coincidencia de patrones, mantiene un inventario de los buckets y avisa de riesgos, como un bucket que pasa a ser público.
  - Usar cuando: Antes de usar un bucket para ajustar un modelo o como fuente de una Knowledge Base, para saber si contiene datos personales.
  - No usar cuando: Para filtrar datos personales en tiempo real en las respuestas de un modelo (Bedrock Guardrails).
  - Referencia: <https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html>
- **matriz de confusión** (confusion matrix, falso positivo, falsos positivos, falso negativo, falsos negativos). *Métrica.* Tabla que cruza las clases reales con las predichas: verdaderos positivos (VP), falsos positivos (FP), verdaderos negativos (VN) y falsos negativos (FN). A partir de ella se calculan la exactitud, la precisión, la exhaustividad y F1.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality-metrics.html>
- **MCP** (Model Context Protocol). *Concepto.* Model Context Protocol: protocolo abierto que proporciona una capa de comunicación estándar para que los agentes de IA interactúen con datos, herramientas y servicios externos, y también con otros agentes.
  - Usar cuando: Para exponer una herramienta o fuente de datos una sola vez y que la use cualquier agente compatible.
  - No usar cuando: No es un modelo ni un servicio de AWS: no genera respuestas por sí mismo.
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/getting-started-with-mcp.html>
- **mecanismo de feedback** (user-feedback mechanism, feedback de los usuarios). *Técnica.* Forma de que los usuarios valoren o notifiquen respuestas incorrectas o inadecuadas, unida a un circuito de revisión periódica que convierte ese feedback en mejoras del sistema (guardrails, prompts, datos).
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/raimon02-bp01.html>
- **memoria del agente** (memoria a corto plazo, memoria a largo plazo). *Concepto.* Capacidad de un agente para recordar: la memoria a corto plazo guarda los turnos de la sesión; la de largo plazo extrae y conserva entre sesiones datos clave como las preferencias del usuario. Sin memoria, cada interacción empieza de cero.
  - Referencia: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html>
- **mínimo privilegio** (least privilege). *Concepto.* Práctica recomendada de IAM: conceder solo los permisos imprescindibles para cada tarea.
  - Referencia: <https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html>
- **MLflow en SageMaker AI** (MLflow, SageMaker Experiments). *Servicio.* MLflow totalmente gestionado en SageMaker AI para registrar, organizar y comparar experimentos y registrar los mejores modelos. Sustituye como opción recomendada a SageMaker Experiments, que ahora es Experiments Classic y solo funciona en Studio Classic.
  - Usar cuando: Para que los experimentos de ML sean reproducibles y comparables.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/mlflow.html>
- **MLOps** (ML Operations). *Concepto.* Metodología que aplica las prácticas de DevOps a las cargas de trabajo de ML: integra desarrollo de software, operaciones, ingeniería de datos y ciencia de datos para agilizar la entrega de modelos durante todo su ciclo de vida.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-why.html>
- **modelo de difusión** (modelos de difusión, diffusion model). *Concepto.* Modelo generativo de imagen (y vídeo) que aprende a eliminar ruido: al generar parte de ruido y lo va limpiando, guiado por el prompt, hasta obtener la imagen. Stable Diffusion es un ejemplo.
  - Referencia: <https://aws.amazon.com/what-is/stable-diffusion/>
- **modelo de responsabilidad compartida** (responsabilidad compartida, shared responsibility model). *Concepto.* La seguridad y el cumplimiento son una responsabilidad compartida: AWS protege la infraestructura (seguridad de la nube) y el cliente protege sus datos, accesos y configuración (seguridad en la nube). El reparto depende del servicio usado.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/security.html>
- **modelo fundacional** (modelos fundacionales, foundation model, foundation models, FM, FMs). *Concepto.* Modelo muy grande preentrenado con vastos conjuntos de datos que sirve de base de la IA generativa. Se desarrolla en los dominios 2 y 3 del examen.
  - Referencia: <https://docs.aws.amazon.com/decision-guides/latest/generative-ai-on-aws-how-to-choose/guide.html>
- **modelo multimodal** (modelos multimodales, multimodal). *Concepto.* Modelo que procesa y entiende varios tipos de entrada a la vez (texto, imágenes, vídeo, documentos, audio) en una misma petición, y puede generar uno o varios tipos de salida.
  - Referencia: <https://docs.aws.amazon.com/nova/latest/nova2-userguide/what-is-nova-2.html>

## N

- **Amazon Neptune** (Neptune, Neptune Analytics, Amazon Neptune Analytics). *Servicio.* Base de datos de grafos gestionada. Neptune Analytics añade búsqueda vectorial combinada con recorridos y algoritmos de grafos, la base de GraphRAG; Bedrock Knowledge Bases la admite.
  - Usar cuando: Cuando importan las relaciones entre entidades: GraphRAG, redes de fraude, vista 360 del cliente, respuestas explicables por relaciones.
  - No usar cuando: Para una búsqueda semántica sencilla sobre documentos sin relaciones relevantes.
  - Referencia: <https://docs.aws.amazon.com/neptune-analytics/latest/userguide/vector-similarity.html>
- **niveles de servicio de Bedrock** (service tiers, nivel Flex, nivel Priority, nivel Reserved, nivel Standard). *Concepto.* Niveles de inferencia de Amazon Bedrock: Standard (por defecto), Priority (respuesta más rápida con un recargo del 75 %), Flex (un 50 % de descuento para cargas que toleran más tiempo) y Reserved (capacidad reservada de tokens por minuto durante 1 o 3 meses, con objetivo de disponibilidad del 99,5 %; el exceso pasa a Standard).
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html>
- **no determinismo** (nondeterminism, no deterministas). *Concepto.* Propiedad de los modelos generativos por la que la misma petición puede dar respuestas distintas, porque el siguiente token se elige muestreando una distribución de probabilidad. Una temperatura baja la reduce.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/inference-parameters.html>
- **Amazon Nova** (Nova). *Servicio.* Familia de modelos fundacionales de Amazon que se usan mediante API a través de Amazon Bedrock: Micro (solo texto), Lite, Pro y Premier, y la generación Nova 2 (Lite, Sonic y Multimodal Embeddings). Nova Canvas (imagen), Nova Reel (vídeo) y Nova Sonic v1 están retirados desde septiembre de 2026.
  - Usar cuando: Cuando se busca un modelo fundacional propio de Amazon dentro de Bedrock, por ejemplo por precio-rendimiento.
  - No usar cuando: Cuando basta un servicio de IA especializado o un modelo de ML tradicional para una tarea acotada.
  - Referencia: <https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html>

## O

- **On-Demand** (bajo demanda). *Concepto.* Modelo de precios de pago por uso sin compromiso. En Amazon EC2 se paga por segundo por las instancias lanzadas; en Amazon Bedrock, por los tokens de entrada y de salida de cada petición (nivel Standard por defecto).
  - Referencia: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html>
- **Amazon OpenSearch Service** (OpenSearch Service, OpenSearch Serverless, Amazon OpenSearch Serverless). *Servicio.* Servicio gestionado de búsqueda y análisis con búsqueda vectorial (k-NN). Combina búsqueda de texto completo y vectorial con latencias muy bajas; OpenSearch Serverless es la opción de creación rápida más habitual para Bedrock Knowledge Bases y, junto con los clústeres gestionados, la única que admite vectores binarios.
  - Usar cuando: Búsqueda híbrida (texto completo + vectores), muchas consultas con baja latencia o el almacén vectorial de una Knowledge Base.
  - No usar cuando: Cuando la aplicación ya usa PostgreSQL y basta añadir pgvector, o cuando hay que guardar miles de millones de vectores al menor coste con consultas poco frecuentes (S3 Vectors).
  - Referencia: <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html>
- **orquestación de flujos** (workflow orchestration). *Concepto.* Coordinación de los pasos, herramientas y agentes de un proceso: orden, paralelismo, gestión de errores y puntos de aprobación humana.
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html>

## P

- **parámetros de inferencia** (inference parameters, temperatura de muestreo, top-p, Top-p, top-k, Top-k). *Concepto.* Ajustes de cada petición que cambian la generación. La temperatura baja favorece los tokens más probables (respuestas más deterministas) y la alta da más variedad; top-k limita a los k candidatos más probables; top-p, a los que suman una proporción de la probabilidad acumulada; la longitud máxima limita la respuesta.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/inference-parameters.html>
- **Amazon Personalize** (Personalize). *Servicio.* Servicio de aprendizaje automático totalmente gestionado que usa tus datos para generar recomendaciones de elementos para los usuarios y segmentos de usuarios por afinidad.
  - Usar cuando: Para personalizar recomendaciones (por ejemplo, en una aplicación de vídeo).
  - No usar cuando: Cuando no se dispone de datos propios de usuarios y elementos con los que generar recomendaciones.
  - Referencia: <https://docs.aws.amazon.com/personalize/latest/dg/what-is-personalize.html>
- **PII** (datos personales, personally identifiable information). *Concepto.* Información de identificación personal: datos que identifican a una persona, como nombre, dirección, correo, teléfono, número de documento o de tarjeta.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html>
- **plantilla de prompt** (prompt template, prompt templates, plantillas de prompt). *Técnica.* Prompt fijo con variables que se rellenan en cada petición. Permite reutilizar un prompt probado de forma coherente; en AWS se gestiona con Amazon Bedrock Prompt Management.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html>
- **Policy in AgentCore** (Policy in Amazon Bedrock AgentCore). *Servicio.* Políticas deterministas, en lenguaje Cedar o redactadas en lenguaje natural, que un motor de políticas evalúa en el AgentCore Gateway antes de permitir cada llamada de un agente a una herramienta: qué puede hacer y con qué límites.
  - Usar cuando: Para impedir que un agente actúe fuera de su autoridad, por ejemplo aprobar importes por encima de un límite.
  - No usar cuando: Para filtrar contenido dañino en los prompts (Guardrails) o gestionar las credenciales del agente (AgentCore Identity).
  - Referencia: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html>
- **política de IAM** (políticas de IAM, IAM policy). *Concepto.* Documento JSON que define permisos (qué acciones se permiten o deniegan sobre qué recursos). Las basadas en identidad se asocian a usuarios, grupos o roles; las basadas en recursos, a un recurso como un bucket de S3.
  - Referencia: <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html>
- **Amazon Polly** (Polly). *Servicio.* Servicio en la nube que convierte texto en voz realista, con varios idiomas y voces. Solo se paga por el texto sintetizado.
  - Usar cuando: Para dar voz a aplicaciones: lectura de artículos, asistentes, accesibilidad.
  - No usar cuando: Cuando se necesita el proceso inverso, de voz a texto (Amazon Transcribe).
  - Referencia: <https://docs.aws.amazon.com/polly/latest/dg/what-is.html>
- **precisión** (precision). *Métrica.* De todo lo que el modelo predice como positivo, qué parte lo es realmente: VP / (VP + FP). Se prioriza cuando un falso positivo es costoso.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-metrics-validation.html>
- **preentrenamiento** (pre-training, preentrenar). *Técnica.* Entrenamiento inicial de un modelo fundacional con datos masivos, de forma autosupervisada. Requiere enormes recursos y puede durar meses; lo hacen los proveedores de modelos, no las empresas que los usan.
  - Referencia: <https://aws.amazon.com/what-is/foundation-models/>
- **preentrenamiento continuado** (continued pre-training, continued pretraining). *Técnica.* Seguir preentrenando un modelo existente con grandes volúmenes de texto sin etiquetar de un dominio (médico, legal, financiero) para que aprenda su vocabulario, conservando la mayor parte de sus capacidades generales.
  - Usar cuando: Cuando el modelo no conoce la jerga de un dominio y hay mucho texto propio sin etiquetar.
  - No usar cuando: Cuando el problema es la información actualizada (RAG) o una tarea concreta con ejemplos etiquetados (fine-tuning).
  - Referencia: <https://aws.amazon.com/bedrock/faqs/>
- **AWS PrivateLink** (PrivateLink). *Servicio.* Conectividad privada entre una VPC y servicios de AWS (como Amazon Bedrock) mediante endpoints de interfaz, sin exponer el tráfico a internet.
  - Usar cuando: Cuando el tráfico hacia el servicio no debe pasar por internet.
  - No usar cuando: Como sustituto de los permisos IAM o del cifrado.
  - Referencia: <https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html>
- **procesamiento del lenguaje natural** (NLP, PLN). *Concepto.* Tecnología que permite a los ordenadores interpretar, manipular y comprender el lenguaje humano, en texto y en voz.
  - Referencia: <https://aws.amazon.com/what-is/nlp/>
- **prompt caching** (caché de prompts). *Técnica.* Funcionalidad de Amazon Bedrock que reutiliza prefijos de prompt repetidos (por ejemplo, un documento largo) para reducir la latencia y el coste de los tokens de entrada. Disponible en modelos compatibles.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html>
- **prompt injection** (inyección de prompts, hijacking, secuestro de objetivo). *Concepto.* Ataque con instrucciones (del usuario o escondidas en un documento o web que lee el modelo) que intentan ignorar y sustituir las del desarrollador para cambiar el objetivo del modelo. Prevenirlo en la aplicación es responsabilidad del cliente; Guardrails ayuda a detectarlo.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html>
- **prompt negativo** (negative prompt, negative prompts). *Concepto.* Indicación de lo que no debe aparecer en la respuesta. En modelos de imagen suele ser un campo aparte (sin texto, sin personas); en texto se expresa como restricción.
  - Referencia: <https://docs.aws.amazon.com/nova/latest/userguide/prompting-image-negative.html>
- **Provisioned Throughput** (rendimiento aprovisionado, unidades de modelo, unidad de modelo). *Concepto.* Opción de Amazon Bedrock para reservar un mayor nivel de rendimiento de un modelo a un coste fijo, facturado por horas según el modelo y el número de unidades de modelo (MU), sin compromiso o con compromiso de 1 o 6 meses. Se factura mientras exista, se use o no. Es una de las formas de usar un modelo personalizado; algunos modelos personalizados admiten también inferencia bajo demanda.
  - Usar cuando: Para un rendimiento alto y constante de un modelo concreto, o para servir un modelo personalizado con capacidad dedicada.
  - No usar cuando: Con tráfico bajo, variable o de prueba: bajo demanda es más barato porque solo se paga por uso.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html>
- **puntuación de confianza** (confidence scoring, confidence score). *Técnica.* Valor que indica cuánto se puede fiar de una salida. Se usa con un umbral para entregar, avisar, derivar a una persona o no responder. Guardrails da puntuaciones de grounding y relevancia; servicios como Textract o Comprehend devuelven una confianza por predicción.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html>
- **puntuación F1** (F1, F1 score). *Métrica.* Media armónica de la precisión y la exhaustividad: F1 = 2 × (precisión × exhaustividad) / (precisión + exhaustividad). Va de 0 a 1.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-metrics-validation.html>

## Q

- **Amazon Q** (Amazon Q Business, Amazon Q Developer). *Servicio.* Asistentes de IA generativa de AWS. Amazon Q Business ya no admite clientes nuevos (AWS remite a Amazon Quick) y los plugins de IDE de Amazon Q Developer dejan de tener soporte el 30 de abril de 2027 (AWS remite a Kiro).
  - No usar cuando: En proyectos nuevos: para asistentes empresariales, Amazon Quick; para desarrollo, Kiro.
  - Referencia: <https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/what-is.html>
- **Amazon Quick** (Quick). *Servicio.* Servicio con IA para automatizar tareas, analizar datos, crear aplicaciones web e investigar. Se usa mediante chat en lenguaje natural y emplea agentes de IA sobre los datos y aplicaciones conectados.
  - Usar cuando: Para dar a los empleados un asistente con agentes que consulte los datos de la empresa, automatice tareas, analice datos e investigue, sin desarrollar.
  - No usar cuando: Cuando se necesita un modelo propio con control sobre el entrenamiento, o una aplicación propia para clientes.
  - Referencia: <https://docs.aws.amazon.com/quick/latest/userguide/what-is.html>

## R

- **RAG** (Retrieval Augmented Generation, generación aumentada por recuperación). *Técnica.* Retrieval Augmented Generation: técnica que usa información de fuentes de datos para mejorar la relevancia y la exactitud de las respuestas generadas por un modelo fundacional.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html>
- **Amazon RDS** (RDS for PostgreSQL, Amazon RDS for PostgreSQL, Amazon Relational Database Service). *Servicio.* Servicio de bases de datos relacionales gestionadas. Amazon RDS for PostgreSQL con la extensión pgvector puede almacenar y consultar embeddings sin otra base de datos.
  - Usar cuando: Aplicaciones RAG propias de equipos que ya gestionan PostgreSQL en RDS.
  - No usar cuando: Como almacén de una Bedrock Knowledge Base: no está admitido (Aurora PostgreSQL sí).
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-an-aws-vector-database-for-rag-use-cases/vector-db-options.html>
- **red neuronal** (redes neuronales, neural network). *Concepto.* Método de IA que procesa datos con nodos (neuronas artificiales) interconectados y organizados en capas, de forma inspirada en el cerebro humano. Es la base del aprendizaje profundo.
  - Referencia: <https://aws.amazon.com/what-is/neural-network/>
- **Amazon Redshift** (Redshift). *Servicio.* Almacén de datos (data warehouse) totalmente gestionado a escala de petabytes; con Redshift Serverless se analizan datos sin configurar un almacén aprovisionado.
  - Usar cuando: Para analizar con SQL grandes volúmenes de datos estructurados que alimentan modelos o informes.
  - No usar cuando: Para guardar objetos y ficheros de entrenamiento sin estructura (Amazon S3).
  - Referencia: <https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html>
- **registro de invocaciones de modelos** (model invocation logging, registro de invocaciones). *Técnica.* Funcionalidad de Amazon Bedrock que guarda la petición, la respuesta y los metadatos de cada invocación (Converse, InvokeModel y sus variantes) en CloudWatch Logs o en S3 de la misma cuenta y Región. Está desactivada por defecto; cuánto se conservan los registros lo decide la retención del destino. El enmascarado de PII de Guardrails no se aplica a estos registros.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html>
- **regresión** (regression). *Técnica.* Problema supervisado cuyo valor objetivo es continuo: estima una variable dependiente a partir de otras, por ejemplo el precio de una vivienda.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html>
- **reinforcement fine-tuning** (ajuste fino por refuerzo). *Técnica.* Método de personalización de Amazon Bedrock en el que el modelo genera respuestas, una función de recompensa (código en Lambda o un modelo juez) las puntúa y el modelo aprende a maximizar la recompensa, sin pares etiquetados.
  - Usar cuando: Cuando el éxito se puede medir (código que pasa pruebas, respuestas verificables) pero es caro conseguir ejemplos etiquetados.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/reinforcement-fine-tuning.html>
- **Amazon Rekognition** (Rekognition). *Servicio.* Servicio de análisis de imágenes y vídeo basado en aprendizaje profundo que añade capacidades de visión por computador a las aplicaciones sin necesidad de experiencia en ML.
  - Usar cuando: Para analizar imágenes y vídeos: objetos, escenas, moderación de contenido.
  - No usar cuando: Cuando hay que extraer texto estructurado de documentos (Amazon Textract).
  - Referencia: <https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html>
- **rendimiento entre dominios** (cross-domain performance). *Métrica.* Capacidad de una aplicación de IA generativa de mantener la calidad en tareas o áreas distintas de aquellas para las que se probó o ajustó.
  - Referencia: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain2.html>
- **Reserved Instances** (instancias reservadas). *Concepto.* Modelo de precios que reduce el coste de Amazon EC2 a cambio de comprometerse con una configuración concreta de instancia (tipo y Región) durante 1 o 3 años.
  - Referencia: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html>
- **residencia de datos** (data residency). *Concepto.* Requisito de que los datos se almacenen y procesen en una Región o geografía concreta. En Bedrock se respeta eligiendo la Región y, con inferencia entre Regiones, un perfil geográfico en lugar del global.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html>
- **Responsible AI Lens** (AWS Well-Architected Responsible AI Lens). *Concepto.* Guía del AWS Well-Architected Framework (noviembre de 2025) con buenas prácticas para diseñar, desarrollar y operar de forma responsable sistemas de IA para casos de uso concretos, organizada en ocho áreas del ciclo de vida.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/responsible-ai-lens.html>
- **retención de datos** (data retention). *Concepto.* Cuánto tiempo se conservan los datos y los registros antes de borrarlos. En AWS se fija con la retención de los grupos de CloudWatch Logs (indefinida por defecto), la expiración de S3 Lifecycle y los modos de retención de datos de Bedrock.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html>
- **retorno de la inversión** (ROI, return on investment). *Métrica.* Métrica de negocio que compara el beneficio económico obtenido con lo invertido. Mide el valor que aporta una solución, no la calidad técnica del modelo.
- **RLHF** (Reinforcement Learning from Human Feedback, aprendizaje por refuerzo con retroalimentación humana). *Técnica.* Técnica en la que personas comparan o puntúan respuestas del modelo; con esas preferencias se entrena un modelo de recompensa y se ajusta el modelo para producir las respuestas que prefieren las personas (más útiles, seguras o alineadas).
  - Referencia: <https://aws.amazon.com/what-is/reinforcement-learning-from-human-feedback/>
- **robustez** (robustness). *Concepto.* Capacidad de un sistema de IA de dar salidas correctas ante entradas esperadas e inesperadas: erratas, sinónimos, otro idioma o ataques. Bedrock Evaluations la mide perturbando ligeramente los prompts y comparando las respuestas.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-report-programmatic.html>
- **rol de IAM** (roles de IAM, IAM role). *Concepto.* Identidad de IAM que concede credenciales temporales. AWS recomienda que las cargas de trabajo usen roles en lugar de claves de acceso permanentes.
  - Referencia: <https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html>
- **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation, ROUGE-N, ROUGE-L). *Métrica.* Métrica que mide el solapamiento de n-gramas entre la respuesta y un texto de referencia, orientada a la exhaustividad (cuánto de la referencia aparece en la respuesta). Típica de resúmenes.
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/dev-experimenting-quality.html>

## S

- **Amazon S3** (S3, Amazon Simple Storage Service). *Servicio.* Servicio de almacenamiento de objetos con gran escalabilidad, disponibilidad, seguridad y rendimiento. Se usa, entre otros, para lagos de datos, sitios web, copias de seguridad y analítica de big data.
  - No usar cuando: Como base de datos transaccional o como sistema de ficheros de baja latencia para un servidor.
  - Referencia: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>
- **Amazon S3 Glacier** (S3 Glacier). *Servicio.* Clases de almacenamiento de archivo de Amazon S3, de bajo coste, para datos que se consultan poco y deben conservarse mucho tiempo. (El servicio original de bóvedas, Amazon Glacier, es distinto.)
  - Usar cuando: Para conservar años datos de entrenamiento o registros que exige la normativa.
  - No usar cuando: Para datos que se consultan a menudo o con baja latencia.
  - Referencia: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>
- **S3 Lifecycle** (ciclo de vida de S3). *Técnica.* Reglas de Amazon S3 que mueven automáticamente los objetos a clases de almacenamiento más baratas (transición) o los borran al cumplirse un plazo (expiración).
  - Referencia: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>
- **Amazon S3 Vectors** (S3 Vectors). *Servicio.* Almacenamiento vectorial de Amazon S3 (buckets e índices vectoriales) optimizado en coste para volúmenes enormes, con latencias por debajo del segundo en consultas poco frecuentes y de unos 100 ms en las frecuentes. Se integra con Bedrock Knowledge Bases.
  - Usar cuando: Miles de millones de vectores al menor coste, con consultas poco frecuentes.
  - No usar cuando: Aplicaciones que necesitan latencias de pocos milisegundos o búsqueda de texto completo.
  - Referencia: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html>
- **Amazon SageMaker AI** (SageMaker AI, SageMaker). *Servicio.* Servicio totalmente gestionado de aprendizaje automático para construir, entrenar y desplegar modelos propios en un entorno de alojamiento listo para producción. Antes del 3 de diciembre de 2024 se llamaba Amazon SageMaker; desde esa fecha, «Amazon SageMaker» es el nombre de una plataforma unificada de datos, analítica e IA que incluye SageMaker AI.
  - Usar cuando: Cuando hace falta un modelo propio y la máxima flexibilidad y control sobre el algoritmo.
  - No usar cuando: Cuando un servicio de IA preentrenado resuelve el caso con menos esfuerzo.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html>
- **Amazon SageMaker Canvas** (SageMaker Canvas). *Servicio.* Funcionalidad de SageMaker AI para generar predicciones con ML sin escribir código: modelos listos para usar (basados en Rekognition, Textract y Comprehend) o modelos propios de regresión, clasificación, previsión de series temporales, imagen y texto.
  - Usar cuando: Cuando analistas de negocio sin experiencia en ML ni en programación necesitan un modelo predictivo con sus datos.
  - No usar cuando: Cuando un equipo de ciencia de datos necesita control total sobre el algoritmo y el código.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/canvas.html>
- **SageMaker Clarify** (Amazon SageMaker Clarify). *Servicio.* Herramienta de SageMaker AI para detectar sesgo en los datos (por ejemplo, CI y DPL) y en las predicciones (por ejemplo, DI) y explicarlas con SHAP. Ya no está abierta a clientes nuevos; los existentes pueden seguir usándola. AWS indica como sustituto calcular las mismas métricas con bibliotecas abiertas y SHAP, y Amazon Bedrock Evaluations para modelos fundacionales.
  - Usar cuando: Clientes actuales que necesitan métricas de sesgo y explicaciones de modelos de ML clásico.
  - No usar cuando: Como opción para un proyecto nuevo, o para evaluar modelos fundacionales: Amazon Bedrock Evaluations.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-availability-change.html>
- **Amazon SageMaker Ground Truth** (SageMaker Ground Truth, Ground Truth). *Servicio.* Servicio para crear conjuntos de datos de entrenamiento etiquetados con trabajadores humanos (propios, de un proveedor o de Amazon Mechanical Turk) y etiquetado automático. Ya no está abierto a clientes nuevos; los existentes pueden seguir usándolo.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html>
- **Amazon SageMaker JumpStart** (SageMaker JumpStart, JumpStart). *Servicio.* Ofrece modelos preentrenados de código abierto para muchos tipos de problemas, que se pueden entrenar de forma incremental y ajustar antes de desplegarlos, además de plantillas de solución y cuadernos de ejemplo.
  - Usar cuando: Para partir de un modelo preentrenado y ajustarlo con datos propios sin entrenar desde cero.
  - No usar cuando: Cuando se necesita un modelo totalmente a medida con un algoritmo propio, sin partir de uno preentrenado.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html>
- **Amazon SageMaker Model Cards** (SageMaker Model Cards, Model Cards, model card). *Servicio.* Documentación de un modelo de ML en un único sitio: uso previsto y no previsto, calificación de riesgo (desconocido, bajo, medio, alto), detalles de entrenamiento, métricas y resultados de evaluación. Cada cambio crea una versión inmutable; se exporta a PDF y se integra con el Model Registry.
  - Usar cuando: Para gobierno y auditoría: comunicar a riesgos, cumplimiento o reguladores para qué sirve un modelo y cómo se evaluó.
  - No usar cuando: Para detectar sesgo o explicar predicciones: documenta, no mide.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html>
- **SageMaker Model Monitor** (Model Monitor, Amazon SageMaker Model Monitor). *Servicio.* Vigila modelos de SageMaker AI en producción: deriva de la calidad de los datos y del modelo, deriva del sesgo y de la atribución de características, con alertas. Ya no está abierto a clientes nuevos; los existentes pueden seguir usándolo. AWS indica como sustituto sus soluciones abiertas de monitorización con CloudWatch.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality-metrics.html>
- **SageMaker Model Registry** (Model Registry, Amazon SageMaker Model Registry). *Servicio.* Catálogo de modelos de SageMaker AI: gestiona versiones, metadatos (como métricas de entrenamiento), linaje, estado de aprobación y despliegue a producción.
  - Usar cuando: Para versionar modelos, aprobarlos antes de producción y saber qué versión está desplegada.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html>
- **Amazon SageMaker Pipelines** (SageMaker Pipelines). *Servicio.* Servicio de orquestación de flujos de trabajo de SageMaker AI para automatizar el procesamiento de datos, el entrenamiento, la evaluación, el despliegue y la monitorización de modelos, con versionado y trazabilidad (lineage).
  - Usar cuando: Para que el entrenamiento y el despliegue sean repetibles y automatizados (MLOps).
  - No usar cuando: Para un experimento puntual que no se va a repetir.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html>
- **satisfacción del usuario** (user satisfaction, CSAT). *Métrica.* Valoración de los usuarios de una aplicación de IA: encuestas (CSAT), votos positivos o negativos y quejas.
  - Referencia: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain3.html>
- **Savings Plans** (Savings Plan). *Concepto.* Modelo de precios que reduce el coste de Amazon EC2 a cambio de comprometerse a un uso constante, en dólares por hora, durante 1 o 3 años.
  - Referencia: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html>
- **AWS Secrets Manager** (Secrets Manager). *Servicio.* Servicio para guardar, recuperar y rotar credenciales de bases de datos, claves de API, tokens OAuth y otros secretos, para no escribirlos en el código de las aplicaciones.
  - Usar cuando: Para las claves de API y credenciales que usan las herramientas de un agente o una aplicación de IA.
  - No usar cuando: Para claves de cifrado (KMS) o credenciales de AWS (IAM).
  - Referencia: <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>
- **series temporales** (time series, serie temporal). *Concepto.* Datos ordenados en el tiempo, como las lecturas continuas de sensores de IoT o los datos financieros.
  - Referencia: <https://aws.amazon.com/what-is/time-series-database/>
- **serverless** (sin servidores). *Concepto.* Modelo en el que el cliente ejecuta su código sin aprovisionar ni gestionar servidores: AWS se encarga de la infraestructura, la capacidad, el escalado y los parches. No significa que no haya servidores.
  - Referencia: <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>
- **sesgo y equidad** (equidad, fairness). *Concepto.* Un sistema se considera sesgado si discrimina a determinadas personas o grupos; los datos pueden reflejar desigualdades, por ejemplo por representación insuficiente de grupos o etiquetas sesgadas. La equidad es la ausencia de ese trato desigual. No confundir con el «sesgo» como error del modelo (bias frente a varianza).
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-detect-data-bias.html>
- **SHAP** (SHapley Additive exPlanations, valores de Shapley). *Técnica.* Método de explicación a posteriori, independiente del modelo, basado en los valores de Shapley de la teoría de juegos cooperativos: asigna a cada variable su contribución a una predicción concreta (explicación local) o al modelo en general (global).
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-explainability.html>
- **sistema multiagente** (sistemas multiagente, multi-agent). *Concepto.* Varios agentes con roles o especialidades distintos que colaboran en una tarea compleja, bien con un coordinador que delega (flujo centralizado), bien como iguales que negocian y comparten información.
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/multi-agent-collaboration.html>
- **sobreajuste** (overfitting). *Concepto.* El modelo acierta con los datos de entrenamiento pero no con datos reales porque se ajusta demasiado a ellos y no generaliza. Es un modelo de alta varianza.
  - Referencia: <https://aws.amazon.com/what-is/overfitting/>
- **sostenibilidad de la IA** (sostenibilidad). *Concepto.* Reducir el impacto ambiental de una carga de IA: comprobar si la IA generativa hace falta, elegir el modelo del tamaño justo, personalizar de forma eficiente y usar recursos que se ajustan a la demanda (serverless, autoescalado, chips eficientes).
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/sustainability.html>
- **Spot Instances** (instancias Spot, Spot). *Concepto.* Instancias de EC2 sin usar solicitadas a un coste significativamente menor. Son una opción rentable si la aplicación es flexible en cuándo se ejecuta y admite interrupciones.
  - Referencia: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html>
- **Strands Agents** (Strands). *Servicio.* SDK de código abierto publicado inicialmente por AWS para crear agentes de IA con un enfoque centrado en el modelo. Admite MCP, patrones multiagente (Swarm, Graph, Workflow) y varios proveedores de modelos, incluido Amazon Bedrock.
  - Usar cuando: Para programar agentes en código con herramientas y MCP, sobre Bedrock u otros proveedores.
  - No usar cuando: Cuando no se quiere programar: para un asistente listo para empleados, Amazon Quick.
  - Referencia: <https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/strands-agents.html>
- **subajuste** (underfitting). *Concepto.* El modelo no encuentra una relación significativa entre las entradas y las salidas y falla incluso con los datos de entrenamiento. Es un modelo de alto sesgo.
  - Referencia: <https://aws.amazon.com/what-is/overfitting/>
- **supervisión humana** (human oversight). *Técnica.* Revisión o decisión de una persona en los puntos donde un error tiene consecuencias graves o donde su experiencia aporta más. La política de IA responsable de AWS la exige en las decisiones con consecuencias para las personas.
  - Referencia: <https://aws.amazon.com/ai/responsible-ai/policy/>

## T

- **tasa de conversión** (conversion rate). *Métrica.* Porcentaje de usuarios que completan la acción deseada (comprar, registrarse) respecto al total. Métrica de negocio habitual para asistentes de venta.
  - Referencia: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain2.html>
- **tasa de tareas completadas** (task completion rate). *Métrica.* Proporción de solicitudes que una aplicación de IA resuelve sin intervención humana. Por ejemplo, 42 000 de 60 000 consultas = 70 %.
  - Referencia: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01-domain3.html>
- **tecnologías de mejora de la privacidad** (privacy-enhancing technologies, PET). *Técnica.* Técnicas para usar datos protegiendo a las personas: minimización, anonimización, seudonimización o tokenización, enmascarado, privacidad diferencial y datos sintéticos.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/raisp02-bp02.html>
- **temas denegados** (denied topics). *Técnica.* Salvaguarda de Bedrock Guardrails que bloquea los temas que el cliente define en lenguaje natural como no deseados para su aplicación, en las preguntas y en las respuestas.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-denied-topics.html>
- **Amazon Textract** (Textract). *Servicio.* Detecta y analiza texto mecanografiado y manuscrito en documentos, y extrae texto, formularios y tablas de documentos con datos estructurados.
  - Usar cuando: Para digitalizar formularios, facturas y documentos escaneados.
  - No usar cuando: Cuando se trata de reconocer objetos o rostros en fotografías (Amazon Rekognition).
  - Referencia: <https://docs.aws.amazon.com/textract/latest/dg/what-is.html>
- **token** (tokens). *Concepto.* Unidad mínima de texto (u otro dato) que procesa un modelo: una palabra, parte de una palabra o un signo. El modelo recibe tokens de entrada y genera tokens de salida uno a uno. Cada modelo tokeniza a su manera. Es la unidad de facturación y de las cuotas de los modelos fundacionales.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/count-tokens.html>
- **AWS Trainium** (Trainium). *Servicio.* Chips diseñados por AWS para entrenar y servir (inferencia) modelos de IA a escala con la mejor relación coste-rendimiento, disponibles en instancias de Amazon EC2.
  - Usar cuando: Para entrenar modelos grandes propios (o servirlos) en EC2 optimizando el coste.
  - No usar cuando: Cuando se consume un modelo por API en Bedrock: ahí no se eligen chips.
  - Referencia: <https://aws.amazon.com/ai/machine-learning/trainium/>
- **Amazon Transcribe** (Transcribe). *Servicio.* Servicio de reconocimiento automático del habla que usa modelos de aprendizaje automático para convertir audio en texto.
  - Usar cuando: Para transcribir audio (reuniones, llamadas) a texto.
  - No usar cuando: Cuando se necesita generar voz a partir de texto (Amazon Polly) o traducir (Amazon Translate).
  - Referencia: <https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html>
- **transfer learning** (aprendizaje por transferencia). *Técnica.* Reutilizar lo que un modelo aprendió en una tarea general para otra concreta, con pocos datos o entrenando solo una parte. Es la idea en la que se basa el ajuste fino de los modelos fundacionales.
  - Referencia: <https://aws.amazon.com/what-is/transfer-learning/>
- **AWS Transform** (Transform). *Servicio.* Servicio con IA agéntica para acelerar la transformación de infraestructura, aplicaciones y código: modernizar y migrar cargas existentes, por ejemplo mainframes o servidores VMware, a AWS.
  - Usar cuando: Para modernizar o migrar sistemas y código heredados con ayuda de agentes.
  - No usar cuando: Para desarrollar software nuevo (Kiro) o crear una aplicación de IA generativa propia (Amazon Bedrock).
  - Referencia: <https://docs.aws.amazon.com/transform/latest/userguide/what-is-service.html>
- **transformación por lotes** (batch transform, inferencia por lotes). *Técnica.* Opción de SageMaker AI para obtener inferencias de conjuntos de datos grandes sin necesitar un endpoint persistente y asociando cada registro de entrada con su predicción.
  - Referencia: <https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html>
- **transformer** (transformers, arquitectura transformer). *Concepto.* Arquitectura de red neuronal en la que se basan los LLM. Su mecanismo de autoatención (self-attention) analiza a la vez todas las partes de la secuencia y decide cuáles son más importantes, en lugar de procesarla palabra a palabra.
  - Referencia: <https://aws.amazon.com/what-is/transformers-in-artificial-intelligence/>
- **Amazon Translate** (Translate). *Servicio.* Servicio de traducción de texto bajo demanda que usa aprendizaje automático. Sirve para traducir documentos de texto no estructurado y para crear aplicaciones multilingües.
  - No usar cuando: Cuando hay que transcribir audio o extraer información del contenido de un documento.
  - Referencia: <https://docs.aws.amazon.com/translate/latest/dg/what-is.html>
- **transparencia** (transparency). *Concepto.* Dimensión de la IA responsable: permitir que las personas decidan con información sobre su relación con un sistema de IA (que se usa IA, uso previsto, limitaciones, datos). Se documenta con Model Cards, AI Service Cards o fichas de datos.
  - Referencia: <https://aws.amazon.com/ai/responsible-ai/>
- **AWS Trusted Advisor** (Trusted Advisor). *Servicio.* Servicio que inspecciona el entorno de AWS y recomienda mejoras para ahorrar costes, mejorar la disponibilidad y el rendimiento y cerrar brechas de seguridad. Con el plan Basic se accede a los límites de servicio y a algunas comprobaciones de seguridad y tolerancia a fallos.
  - Usar cuando: Para revisar buenas prácticas de la cuenta (permisos abiertos, cuotas, costes).
  - No usar cuando: Para escanear vulnerabilidades de software (Inspector).
  - Referencia: <https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html>

## U

- **uso de herramientas** (tool use, llamadas a herramientas, function calling). *Concepto.* Capacidad de un modelo para decidir qué herramienta (API, función, base de datos) llamar y con qué parámetros. La aplicación o la plataforma la ejecuta y devuelve el resultado al modelo.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html>
- **usuario raíz** (root user). *Concepto.* Identidad de inicio de sesión con la que empieza toda cuenta de AWS, con acceso completo a todos los servicios y recursos. AWS recomienda no usarla en las tareas diarias.
  - Referencia: <https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html>

## V

- **validación de la salida** (output validation). *Técnica.* Comprobar la respuesta de un modelo antes de usarla: contra la fuente (grounding), contra reglas lógicas (Automated Reasoning), contra un formato o esquema esperado, o con revisión humana.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/security.html>
- **vector** (vectores). *Concepto.* Lista de valores numéricos que representa información en un espacio de muchas dimensiones. Es la forma de un embedding; la distancia entre vectores mide la similitud.
  - Referencia: <https://aws.amazon.com/what-is/embeddings-in-machine-learning/>
- **ventana de contexto** (context window). *Concepto.* Cantidad máxima de tokens (entrada e historial) que un modelo puede tener en cuenta en una petición. Es un límite técnico y un factor de coste: más contexto implica pagar más tokens.
  - Referencia: <https://docs.aws.amazon.com/nova/latest/nova2-userguide/what-is-nova-2.html>
- **veracidad** (veracity, veracidad y robustez). *Concepto.* Dimensión de la IA responsable: que las salidas sean factualmente correctas, también ante entradas inesperadas o maliciosas (robustez). En IA generativa se protege con RAG y citas, comprobaciones de grounding y Automated Reasoning checks.
  - Referencia: <https://aws.amazon.com/ai/responsible-ai/>
- **visión por computador** (computer vision). *Concepto.* Campo de la IA que permite a los ordenadores obtener información útil de imágenes, vídeos y otras entradas visuales.
  - Referencia: <https://aws.amazon.com/what-is/computer-vision/>
- **Amazon VPC** (VPC, Amazon Virtual Private Cloud). *Servicio.* Red virtual aislada lógicamente dentro de AWS en la que el cliente lanza sus recursos y controla direcciones IP, subredes, tablas de rutas y acceso.
  - Usar cuando: Cuando los recursos (por ejemplo, un endpoint de modelo) deben quedar en una red privada controlada por el cliente.
  - Referencia: <https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html>

## W

- **AWS Well-Architected Tool** (Well-Architected Tool, AWS WA Tool). *Servicio.* Herramienta para revisar una carga de trabajo frente a las buenas prácticas del AWS Well-Architected Framework y a lentes adicionales del catálogo oficial o propias, con un plan de mejora.
  - Usar cuando: Para revisar de forma estructurada la arquitectura de un sistema de IA.
  - No usar cuando: Para escanear vulnerabilidades o recopilar evidencias de auditoría automáticamente.
  - Referencia: <https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses.html>

## Z

- **zero-shot** (zero-shot prompting). *Técnica.* Técnica de prompt que pide la tarea sin incluir ejemplos. Sirve para tareas que el modelo ya hace bien.
  - Referencia: <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering-guidelines.html>
