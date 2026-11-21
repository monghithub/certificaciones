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
- **Parámetro frente a hiperparámetro.** Los pesos los aprende el modelo al entrenar; la tasa de aprendizaje, las *epochs* o el tamaño de lote se fijan antes. «Ajustar hiperparámetros» no es preparar datos ni crear características.
- **Más datos no empeora el sobreajuste: lo combate.** Junto con parar antes, la regularización o quitar características poco útiles. Aumentar la complejidad del modelo lo agrava.
- **Más columnas no es más exactitud.** Con muchas características sube el coste y el riesgo de sobreajuste; por eso existe la reducción de dimensiones (PCA).
- **Aprendizaje profundo no implica etiquetas.** Puede aprender con datos etiquetados o sin ellos: los modelos fundacionales, que son aprendizaje profundo, se preentrenan de forma autosupervisada.
- **CNN, RNN y *transformer*.** Imágenes: CNN. Secuencias: RNN, hoy sustituidas en lenguaje por los *transformers*. Si el enunciado trata de píxeles, una CNN aprovecha la estructura de la imagen que un modelo pensado para tablas no ve.

## Tipos de aprendizaje y técnica

- **Clasificación frente a regresión.** Categoría (spam o no spam, tema de un documento) es clasificación; número continuo (precio, demanda) es regresión.
- **Agrupar no es clasificar.** El agrupamiento (*clustering*) no tiene etiquetas; la clasificación sí.
- **Detección de fraude.** Puede abordarse como clasificación (con ejemplos etiquetados) o como detección de anomalías (sin etiquetas): lee qué datos tiene el enunciado.
- **k-means frente a k-NN.** La «k» de los dos engaña: k-means agrupa sin etiquetas (no supervisado); k-NN clasifica o predice con ejemplos etiquetados (supervisado).
- **Regresión logística clasifica.** Pese a su nombre, responde «sí o no», no un número continuo.
- **Semisupervisado frente a no supervisado.** Si el enunciado dice que hay *algunas* etiquetas y muchos datos sin etiquetar, es semisupervisado; si no hay ninguna, no supervisado.
- **Regresión camuflada.** Aunque el enunciado hable de clientes, segmentos o recomendaciones, si lo que se predice es un importe o una cantidad, es regresión.

## Inferencia

- **Tiempo real, *serverless*, asíncrona y por lotes no son intercambiables.** Baja latencia interactiva: tiempo real. Ráfagas con inactividad: *serverless*. Cargas grandes (hasta 1 GB) o largas (hasta una hora) que se encolan: asíncrona. Conjunto de datos completo sin *endpoint* permanente: por lotes.
- ***Serverless* tiene límites.** No admite GPU ni configuración de VPC y tiene arranques en frío: si el caso pide GPU o red privada, no es la opción; mejor inferencia en tiempo real (o asíncrona, si puede esperar).
- **Un *endpoint* en tiempo real cuesta aunque no tenga tráfico.** Si el tráfico es esporádico, *serverless* o asíncrona (que escala a cero) son más baratas.
- **Entrenar no es inferir.** Entrenar crea el modelo; inferir lo usa para predecir.

## Cuándo (no) usar ML

- **«Siempre mejor con ML».** Falso: si unas reglas simples resuelven el problema, si faltan datos o si se exige un resultado exacto, ML no es lo apropiado.
- **«Modelo fundacional para todo».** Para una tarea concreta y medible, sobre todo con requisitos de explicabilidad o regulatorios, un modelo más simple puede ser la mejor opción.
- **RPA no es IA.** Para tareas repetitivas con reglas fijas sobre datos estructurados basta la automatización robótica de procesos o un *script*; la IA entra cuando hay texto libre, documentos escaneados o reglas que no se pueden escribir.
- **IDP no es «solo NLP».** El procesamiento inteligente de documentos combina extraer el texto (OCR, Textract) con entenderlo (NLP, Comprehend).

## Servicios

- **Textract frente a Rekognition.** Textract extrae texto y estructura de documentos; Rekognition analiza imágenes y vídeos (objetos, rostros, escenas).
- **Transcribe, Polly y Translate.** Transcribe: voz a texto. Polly: texto a voz. Translate: de un idioma a otro. Comprehend: entiende el contenido del texto.
- **Lex frente a Comprehend.** Lex construye conversaciones con usuarios; Comprehend analiza texto ya existente.
- **Canvas frente a SageMaker AI «completo».** Si el enunciado dice «analistas de negocio», «sin escribir código», la respuesta suele ser SageMaker Canvas; si dice «científicos de datos», «algoritmo propio», «control del entrenamiento», SageMaker AI.
- **Rekognition también lee texto en imágenes, pero no es para documentos.** Para formularios, tablas y facturas escaneadas, Textract.
- **Detectar texto frente a analizar documentos en Textract.** Si hacen falta los pares clave-valor de un formulario o las tablas, es el análisis de documentos; la detección devuelve solo el texto.
- **La funcionalidad decide.** Separar a los hablantes de una llamada: diarización de Transcribe. Que una marca no se traduzca: terminología personalizada de Translate. Comprobar que hay una persona real ante la cámara: Face Liveness de Rekognition. Qué quiere el usuario y qué datos faltan en un *chatbot*: intenciones y ranuras de Lex.
- **Clasificación, detección y segmentación de imágenes.** Una etiqueta para toda la imagen; dónde está cada objeto (recuadro); qué clase tiene cada píxel.
- **Servicios de los libros cerrados a clientes nuevos.** Amazon Forecast (usa SageMaker Canvas), Amazon Fraud Detector (SageMaker AI), Amazon Kendra (Amazon Bedrock Knowledge Bases), SageMaker Studio Lab (SageMaker Studio) y el modelado de temas de Comprehend (un modelo de Amazon Bedrock). Si aparecen como opción para un proyecto nuevo, desconfía.
- **Kendra recupera, no redacta.** Es un servicio de recuperación de información que puede actuar como recuperador dentro de un RAG, pero no genera la respuesta; además, está cerrado a clientes nuevos y AWS remite a Bedrock Knowledge Bases.
- **Comprehend frente a modelo fundacional.** Para extraer opiniones o entidades a escala con un servicio preentrenado, Comprehend; para redactar o resumir, un modelo fundacional en Bedrock.
- **«Servicio gestionado» no significa «sin red privada».** La mayoría de los servicios de IA de AWS y Bedrock admiten *endpoints* de VPC; lo que cambia con un modelo autoalojado es quién lo opera y qué modelo se puede usar.
- **Servicio gestionado frente a SageMaker AI.** Si un servicio preentrenado cubre el caso, es la opción de menor esfuerzo; SageMaker AI es para modelos propios y mayor control.
- **Servicios cerrados a nuevos clientes.** Model Monitor, Clarify, Ground Truth y Bedrock Agents Classic siguen funcionando para quien ya los usa, pero no son la opción para proyectos nuevos. Alternativas: CloudWatch para monitorizar, métricas de sesgo y SHAP con bibliotecas abiertas (o Bedrock Evaluations para modelos fundacionales) y Amazon Bedrock AgentCore para agentes; Ground Truth no tiene sustituto indicado por AWS. SageMaker Experiments es ahora *Classic*: para experimentos, MLflow en SageMaker AI.
- **Preentrenar desde cero casi nunca es la respuesta.** Es la opción de mayor coste y esfuerzo; antes se prueban un servicio preentrenado o un modelo fundacional adaptado.

## Ciclo de vida y métricas

- **El ciclo no termina en el despliegue.** La monitorización puede llevar a reentrenar.
- **EDA frente a preparación y frente a ingeniería de características.** Calcular estadísticas y gráficos para entender los datos es EDA; limpiar y corregir es preparación; crear o transformar variables para el modelo es ingeniería de características.
- **Feature Store no es un almacén de datos de negocio.** Sirve las mismas características al entrenar y al inferir; para informes y análisis, Amazon Redshift; para datos operativos de una aplicación, Amazon RDS.
- **Data Wrangler frente a Glue.** Preparar y analizar datos *para un modelo* con poco código: Data Wrangler (en Canvas). ETL genérico de datos: AWS Glue. Orquestar todo el flujo de ML: SageMaker Pipelines.
- **Deriva de datos frente a deriva de concepto.** Si cambian las entradas, deriva de datos; si las entradas son parecidas pero ya no predicen lo mismo, deriva de concepto (para verla hace falta el resultado real). Ninguna de las dos es sobreajuste: el sobreajuste se reconoce por la diferencia entre entrenamiento y validación, no por una caída tras un cambio en el mundo real.
- **Prueba en sombra frente a A/B y canario.** En sombra el modelo nuevo recibe una copia del tráfico y nadie ve sus respuestas; en A/B o canario, parte de los usuarios sí las recibe.
- **Vigilar el modelo frente a vigilar la cuenta.** La calidad y la deriva de un modelo en producción se vigilan con métricas y alarmas de CloudWatch (o Model Monitor, para clientes existentes); los registros de quién llamó a qué API son de CloudTrail y no dicen si el modelo acierta.
- **La exactitud engaña con clases desequilibradas.** Con un 1 % de fraude, «nunca hay fraude» da un 99 % de exactitud. Mira precisión, exhaustividad, F1 o AUC.
- **«Precisión» coloquial frente a *precision*.** En una pregunta de métricas, «precisión» es la métrica VP / (VP + FP), no «lo bien que funciona» el modelo.
- **Precisión frente a exhaustividad.** Precisión: de lo que predigo como positivo, ¿cuánto lo es? Se prioriza si el falso positivo es caro. Exhaustividad: de los positivos reales, ¿cuántos detecto? Se prioriza si el falso negativo es caro.
- **Métrica técnica frente a métrica de negocio.** Exactitud, F1 o AUC miden el modelo; ROI, coste por usuario u opiniones de clientes miden el valor de negocio.
- **Matriz de confusión frente a matriz de correlación.** Para ver qué clases confunde un clasificador (también multiclase), la matriz de confusión; la de correlación relaciona variables. MAE o RMSE son de regresión, no de clasificación.
- **Métricas de regresión.** MSE, RMSE y MAE: cuanto más bajas, mejor. R²: cuanto más cerca de 1, mejor. El MSE castiga más los errores grandes.
- **MLOps no es solo despliegue.** Incluye experimentación, procesos repetibles, escalabilidad, monitorización y reentrenamiento.
