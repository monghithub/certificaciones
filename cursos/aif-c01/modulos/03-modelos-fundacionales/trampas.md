# Trampas habituales del módulo 03

## Diseño de aplicaciones

- **El modelo más grande es la opción segura.** El examen premia el modelo **más pequeño y barato que cumple** los requisitos. Si el enunciado pide «el MENOR coste» o «la MENOR latencia», descarta los modelos grandes salvo que la tarea lo exija.
- **Temperatura 0 para que no invente.** Reduce la variabilidad, no las alucinaciones. Para respuestas basadas en datos propios: RAG.
- **Top-k frente a top-p.** Top-k limita a un **número** fijo de candidatos; top-p, a una **proporción** de la probabilidad acumulada.
- **Longitud máxima para respuestas concisas.** La longitud máxima **corta** la respuesta; para que sea breve y completa, se pide en el *prompt*.
- ***Prompt caching* frente a RAG.** El *prompt caching* abarata un contexto **que se repite**; no busca información. RAG **recupera** lo relevante en cada pregunta.
- **RAG reentrena el modelo.** RAG no cambia el modelo: añade fragmentos al *prompt* en cada petición. Por eso los datos se actualizan solo con volver a sincronizar.
- **Ajuste fino para información que cambia.** Si los documentos cambian cada semana, el ajuste fino habría que repetirlo cada semana: RAG.
- **RAG para cambiar el tono.** RAG aporta información; el estilo, el formato o la jerga se consiguen con *prompts* o *fine-tuning*.
- **Si tiene búsqueda vectorial, sirve para Knowledge Bases.** RDS for PostgreSQL, DynamoDB y ElastiCache tienen búsqueda vectorial, pero Bedrock Knowledge Bases no los admite como almacén. Con PostgreSQL en una Knowledge Base, la respuesta es **Aurora** PostgreSQL.
- **DynamoDB no guarda vectores.** Ya tiene índices vectoriales nativos: si los datos operativos están en DynamoDB, se puede buscar por similitud sin otra base de datos.
- **OpenSearch frente a Aurora.** «Ya usan PostgreSQL y quieren combinar SQL y vectores» → Aurora o RDS con `pgvector`. «Búsqueda de texto completo y vectorial, baja latencia» → OpenSearch.
- **Neptune para todo RAG.** Neptune Analytics es para **relaciones** (GraphRAG); sin relaciones relevantes es una complejidad innecesaria.
- **Preentrenar es la forma de «tener un modelo propio».** Casi nunca es la respuesta: es lo más caro y lento. La escalera es *prompts* → RAG → *fine-tuning* → preentrenamiento continuado → preentrenamiento.
- **El *fine-tuning* se paga una vez.** Se paga el entrenamiento (*tokens* × épocas), un **almacenamiento mensual** por modelo y su **inferencia**, y se repite si cambian los datos.
- **Destilación = compresión del mismo modelo.** La destilación entrena un modelo **alumno más pequeño** con las respuestas de un **maestro** más grande, para un caso de uso concreto.
- **La destilación es más barata que el *fine-tuning*.** Incluye un *fine-tuning* del alumno y, además, la inferencia del maestro. Lo que abarata es la **inferencia posterior**, y no exige datos etiquetados.
- **Agente para todo.** Si el proceso tiene siempre los mismos pasos, Bedrock Flows; si solo hay que responder con documentos, una Knowledge Base. El agente se justifica cuando hay que **actuar** y decidir los pasos.
- **Bedrock Agents para un proyecto nuevo.** *Agents Classic* ya no admite clientes nuevos: AgentCore.

## Ingeniería de prompts

- ***Few-shot* entrena el modelo.** Los ejemplos van en el *prompt*: es *in-context learning*, sin cambiar los parámetros.
- ***Zero-shot* frente a *one-shot* frente a *few-shot*.** Cero, uno o varios ejemplos en el *prompt*. Si el enunciado dice «sin ejemplos», es *zero-shot*.
- ***Chain-of-thought* es gratis.** Mejora los problemas de varios pasos, pero genera **más *tokens* de salida** y más latencia.
- **Plantilla de *prompt* = versión.** La plantilla tiene **variables**; la versión de Prompt Management es una **instantánea inmutable** de un *prompt* para desplegarlo y revertir.
- **Variante frente a versión.** Las variantes se **comparan** durante las pruebas (otro texto, modelo o parámetros); la versión se **despliega**.
- **Un modelo mejor arregla un *prompt* vago.** Un *prompt* sin tarea, público ni formato da respuestas genéricas también en un modelo mayor, y cuesta más: primero, especificidad.
- ***Discovery* = evaluación final.** Explorar con *prompts* sencillos qué sabe el modelo es el **primer** paso, antes de diseñar el *prompt* definitivo; no sustituye a la evaluación.
- **«No hagas X» como única instrucción.** Las restricciones negativas ayudan, pero suele funcionar mejor decir lo que se quiere. Y una instrucción en el *prompt* no es un control de seguridad: Guardrails.
- ***Prompt injection* frente a *jailbreaking*.** La inyección intenta **sustituir las instrucciones del desarrollador** (cambiar el objetivo); el *jailbreak* intenta **saltarse las protecciones de seguridad del modelo** para obtener contenido dañino.
- **Exposición frente a envenenamiento.** La exposición **revela** información (el *system prompt*, el historial, datos sensibles); el envenenamiento **mete** datos maliciosos en el entrenamiento o en las fuentes de RAG.
- **AWS evita el *prompt injection*.** Por la responsabilidad compartida, prevenirlo en la aplicación es responsabilidad **del cliente**; Guardrails ayuda a detectarlo.

## Entrenamiento y datos

- **Preentrenamiento continuado con datos etiquetados.** Usa **texto sin etiquetar** del dominio. Los pares etiquetados son para *fine-tuning*.
- ***Instruction tuning* frente a preentrenamiento continuado.** El primero enseña a **seguir instrucciones** con pares instrucción → respuesta; el segundo enseña **vocabulario de un dominio** con texto sin etiquetar.
- **RLHF = etiquetar datos.** En RLHF las personas **comparan o puntúan respuestas** del modelo para entrenar un modelo de recompensa; no etiquetan el conjunto original.
- ***Reinforcement fine-tuning* necesita respuestas de referencia.** Usa **funciones de recompensa** que puntúan las respuestas, no pares etiquetados.
- **Más datos siempre es mejor.** Importan la **calidad**, la **representatividad** y el **gobierno**; muchos datos malos empeoran el modelo y pueden introducir sesgos o datos envenenados.

## Evaluación

- **ROUGE frente a BLEU.** ROUGE → **resúmenes** (*recall*: cuánto de la referencia está en la respuesta). BLEU → **traducción** (precisión, penaliza respuestas cortas).
- **Bedrock evalúa los resúmenes con ROUGE.** En las evaluaciones programáticas de Bedrock, la exactitud de la tarea de resumen se calcula con **BERTScore**; ROUGE es la métrica clásica de resúmenes, pero no la que usa Bedrock en esa tarea.
- **ROUGE y BLEU miden el significado.** Miden **palabras coincidentes**; una paráfrasis correcta puntúa bajo. Para similitud semántica, BERTScore.
- ***LLM-as-a-judge* sustituye a las personas.** Escala y es barato, pero puede equivocarse o favorecer respuestas parecidas a las suyas: se valida con evaluación humana y conviene un juez de otra familia.
- **Evaluación humana para comparar miles de respuestas cada día.** Es lenta y cara: para volumen, métricas automáticas o juez LLM; las personas, para criterios subjetivos y decisiones críticas.
- **Un *benchmark* público basta.** Mide capacidades generales; para tu caso hace falta un conjunto propio representativo.
- **Exactitud alta = objetivo de negocio cumplido.** Hay que medir productividad, satisfacción, tasa de tareas completadas o coste por interacción frente a una línea base.
- **Medir el valor sin línea base.** «El 80 % de los usuarios usa el asistente» no demuestra nada si no se compara con cómo se trabajaba antes o con un grupo de control.
- **Coste por interacción = coste por consulta resuelta.** Si la tasa de tareas completadas es baja, el coste por consulta **resuelta** es mucho mayor que el coste por interacción.
- **Evaluar un RAG solo por la respuesta final.** Hay que separar **recuperación** (¿trae los fragmentos correctos?) y **generación** (¿es fiel al contexto?) para saber qué falla.
- **SageMaker Clarify para evaluar un modelo fundacional en un proyecto nuevo.** Ya no admite clientes nuevos: Amazon Bedrock Model Evaluation.
