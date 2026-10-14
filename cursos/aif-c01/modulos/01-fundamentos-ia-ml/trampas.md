# Trampas habituales del módulo 01

## Terminología

- **IA = ML.** No son sinónimos: la IA es el término más amplio y casi toda la IA actual se crea con ML.
- **IA generativa = clasificación.** La generativa **crea** contenido; clasificar o predecir es IA «clásica».
- **«Sesgo» con dos sentidos.** En equidad es un trato injusto a grupos; en el ajuste del modelo es el error sistemático (*bias*), opuesto a la varianza. Mira el contexto.
- **Sobreajuste frente a subajuste.** Sobreajuste: muy bien con los datos de entrenamiento y mal con datos nuevos (alta varianza). Subajuste: mal con ambos (alto sesgo).
- **Aprendizaje por refuerzo.** No usa etiquetas: usa recompensas por interactuar con un entorno. No lo confundas con el supervisado.
- **Autosupervisado no es no supervisado.** Los modelos fundacionales se preentrenan generando las etiquetas a partir de los propios datos (autosupervisado); el no supervisado busca grupos o anomalías.
- **IA agéntica frente a IA generativa.** La generativa *produce* contenido cuando se le pide; la agéntica *decide y ejecuta* pasos (usa herramientas, llama a APIs) para cumplir un objetivo, normalmente apoyándose en un modelo generativo.
- **«Agente» en dos sentidos.** En aprendizaje por refuerzo, el agente es lo que aprende con recompensas; en IA agéntica, es el sistema que actúa con herramientas.
- **Modelo frente a algoritmo.** El algoritmo es la receta; el modelo es el resultado de aplicarla a los datos.

## Tipos de aprendizaje y técnica

- **Clasificación frente a regresión.** Categoría (spam o no spam, tema de un documento) es clasificación; número continuo (precio, demanda) es regresión.
- **Agrupar no es clasificar.** El agrupamiento (*clustering*) no tiene etiquetas; la clasificación sí.
- **Detección de fraude.** Puede abordarse como clasificación (con ejemplos etiquetados) o como detección de anomalías (sin etiquetas): lee qué datos tiene el enunciado.

## Inferencia

- **Tiempo real, *serverless*, asíncrona y por lotes no son intercambiables.** Baja latencia interactiva: tiempo real. Ráfagas con inactividad: *serverless*. Cargas grandes (hasta 1 GB) o largas (hasta una hora) que se encolan: asíncrona. Conjunto de datos completo sin *endpoint* permanente: por lotes.
- ***Serverless* tiene límites.** No admite GPU ni configuración de VPC y tiene arranques en frío: si el caso pide GPU o red privada, no es la opción.
- **Un *endpoint* en tiempo real cuesta aunque no tenga tráfico.** Si el tráfico es esporádico, *serverless* o asíncrona (que escala a cero) son más baratas.
- **Entrenar no es inferir.** Entrenar crea el modelo; inferir lo usa para predecir.

## Cuándo (no) usar ML

- **«Siempre mejor con ML».** Falso: si unas reglas simples resuelven el problema, si faltan datos o si se exige un resultado exacto, ML no es lo apropiado.
- **«Modelo fundacional para todo».** Para una tarea concreta y medible, sobre todo con requisitos de explicabilidad o regulatorios, un modelo más simple puede ser la mejor opción.

## Servicios

- **Textract frente a Rekognition.** Textract extrae texto y estructura de documentos; Rekognition analiza imágenes y vídeos (objetos, rostros, escenas).
- **Transcribe, Polly y Translate.** Transcribe: voz a texto. Polly: texto a voz. Translate: de un idioma a otro. Comprehend: entiende el contenido del texto.
- **Lex frente a Comprehend.** Lex construye conversaciones con usuarios; Comprehend analiza texto ya existente.
- **Canvas frente a SageMaker AI «completo».** Si el enunciado dice «analistas de negocio», «sin escribir código», la respuesta suele ser SageMaker Canvas; si dice «científicos de datos», «algoritmo propio», «control del entrenamiento», SageMaker AI.
- **Rekognition también lee texto en imágenes, pero no es para documentos.** Para formularios, tablas y facturas escaneadas, Textract.
- **Comprehend frente a modelo fundacional.** Para extraer opiniones o entidades a escala con un servicio preentrenado, Comprehend; para redactar o resumir, un modelo fundacional en Bedrock.
- **«Servicio gestionado» no significa «sin red privada».** La mayoría de los servicios de IA de AWS y Bedrock admiten *endpoints* de VPC; lo que cambia con un modelo autoalojado es quién lo opera y qué modelo se puede usar.
- **Servicio gestionado frente a SageMaker AI.** Si un servicio preentrenado cubre el caso, es la opción de menor esfuerzo; SageMaker AI es para modelos propios y mayor control.
- **Servicios cerrados a nuevos clientes.** Model Monitor, Clarify, Ground Truth y Bedrock Agents Classic siguen funcionando para quien ya los usa, pero no son la opción para proyectos nuevos. SageMaker Experiments es ahora *Classic*: para experimentos, MLflow en SageMaker AI.
- **Preentrenar desde cero casi nunca es la respuesta.** Es la opción de mayor coste y esfuerzo; antes se prueban un servicio preentrenado o un modelo fundacional adaptado.

## Ciclo de vida y métricas

- **El ciclo no termina en el despliegue.** La monitorización puede llevar a reentrenar.
- **La exactitud engaña con clases desequilibradas.** Con un 1 % de fraude, «nunca hay fraude» da un 99 % de exactitud. Mira precisión, exhaustividad, F1 o AUC.
- **«Precisión» coloquial frente a *precision*.** En una pregunta de métricas, «precisión» es la métrica VP / (VP + FP), no «lo bien que funciona» el modelo.
- **Precisión frente a exhaustividad.** Precisión: de lo que predigo como positivo, ¿cuánto lo es? Se prioriza si el falso positivo es caro. Exhaustividad: de los positivos reales, ¿cuántos detecto? Se prioriza si el falso negativo es caro.
- **Métrica técnica frente a métrica de negocio.** Exactitud, F1 o AUC miden el modelo; ROI, coste por usuario u opiniones de clientes miden el valor de negocio.
- **MLOps no es solo despliegue.** Incluye experimentación, procesos repetibles, escalabilidad, monitorización y reentrenamiento.
