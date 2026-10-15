# Trampas habituales del módulo 02

## Conceptos

- ***Token* = palabra.** Un *token* puede ser una palabra, parte de ella o un signo, y cada modelo tokeniza a su manera: el mismo texto da recuentos distintos en modelos distintos.
- ***Embedding* = *token*.** El *token* es un trozo de texto; el *embedding* es el vector numérico que representa su significado. Se busca por similitud con *embeddings*, no con *tokens*.
- ***Chunking* frente a tokenización.** *Chunking* es partir **documentos** en fragmentos para indexarlos (RAG); tokenizar es partir **texto** en las unidades que procesa el modelo.
- **Base de datos vectorial frente a relacional.** Si el enunciado pide buscar «por significado» o «documentos parecidos», es búsqueda vectorial, no una consulta SQL por palabras exactas.
- **Multimodal frente a difusión.** Multimodal describe las **modalidades** de entrada y salida; difusión es una **técnica** para generar imágenes quitando ruido. Un modelo puede ser multimodal sin ser de difusión.
- **IA generativa para todo.** Para predecir un número o una categoría con datos tabulares (demanda, fraude), el ML tradicional es más barato, determinista y explicable.
- **Modelo fundacional frente a servicio especializado.** Si solo hay que traducir, Amazon Translate; si solo hay que recomendar productos con historial de usuarios, Amazon Personalize. Un modelo fundacional se justifica cuando la tarea combina varias capacidades o es abierta.
- **Más grande no es mejor.** Un modelo más grande cuesta más por *token* y suele ser más lento; si la tarea es sencilla, un modelo pequeño cumple.

## Ciclo de vida y costes

- **Preentrenar desde cero.** Casi nunca es la respuesta para una empresa: es lo más caro y lento. Lo habitual es partir de un modelo existente.
- **Ajuste fino para datos actualizados.** Si el problema es que el modelo no conoce información reciente o propia, la respuesta es RAG, no *fine-tuning*. El ajuste fino cambia el comportamiento, el estilo o el formato.
- **Solo se pagan los *tokens* de salida.** Se pagan entrada **y** salida. Enviar el manual entero en cada petición dispara el coste de entrada.
- **La salida cuesta lo mismo que la entrada.** Normalmente cuesta varias veces más: limitar la longitud de la respuesta ahorra.
- **Provisioned Throughput para ahorrar en un piloto.** Es capacidad dedicada que se paga por horas aunque no se use. Para tráfico bajo o variable, bajo demanda.
- **Lotes para un chat.** La inferencia por lotes es asíncrona (S3) y no admite llamadas a herramientas: no sirve para conversaciones.
- **Inferencia entre Regiones global con residencia de datos.** La global puede procesar en cualquier Región comercial; si los datos no pueden salir de la UE, la geográfica de la UE.
- **La inferencia entre Regiones cuesta más.** No hay coste adicional de enrutamiento; la global incluso ahorra aproximadamente un 10 %.

## Ventajas y limitaciones

- **Adaptabilidad = ajuste fino.** La adaptabilidad es usar el **mismo** modelo para muchas tareas cambiando el *prompt*; el ajuste fino modifica el modelo.
- **Capacidad de respuesta = respuestas fiables.** *Responsiveness* es responder rápido y a cualquier hora; no dice nada de la exactitud ni del determinismo.

- **Temperatura 0 elimina las alucinaciones.** Una temperatura baja hace las respuestas más **repetibles**, no más **ciertas**. Contra las alucinaciones: RAG, *prompts* precisos, verificación y Guardrails.
- **Temperatura frente a top-p y top-k.** Top-k limita a un **número** fijo de candidatos; top-p, a una **proporción** de la probabilidad acumulada; la temperatura cambia la **forma** de la distribución.
- **No determinismo = error del modelo.** Es una propiedad del muestreo: la misma pregunta puede dar respuestas distintas.
- **Interpretabilidad.** Si el enunciado exige explicar cada decisión (por ejemplo, la denegación de un crédito), un modelo generativo es difícil de justificar; un modelo de ML tradicional más simple puede ser mejor.

## Agentes y contexto

- **Ingeniería de contexto = ingeniería de *prompts*.** La de *prompts* se centra en cómo se pide; la de contexto, en qué información acompaña a la petición (memoria, RAG, herramientas, historial).
- **El modelo recuerda la conversación.** El modelo no guarda estado entre llamadas: la memoria la aporta la aplicación o la plataforma (por ejemplo, AgentCore Memory).
- **MCP es un servicio de AWS o un modelo.** Es un **protocolo abierto** para conectar agentes con herramientas y datos.
- **MCP frente a A2A.** MCP conecta un agente con herramientas y datos; A2A, agentes entre sí (con *Agent Cards* para descubrirse).
- **El modelo ejecuta las herramientas.** El modelo decide qué herramienta llamar; la aplicación o la plataforma la ejecuta y le devuelve el resultado.
- **Un agente para todo.** Si una consulta sencilla resuelve el caso, un agente añade coste, latencia y complejidad.
- **Coordinador frente a colaboración.** Un coordinador central que delega y sigue los pasos es un flujo centralizado; agentes iguales que negocian y comparten información son colaboración multiagente.

## Servicios

- **Bedrock frente a SageMaker AI.** «Sin gestionar infraestructura», «por API», «varios proveedores» → Bedrock. «Entrenar», «control de la infraestructura», «modelo propio» → SageMaker AI.
- **JumpStart frente a Bedrock.** Ambos ofrecen modelos preentrenados, pero JumpStart los despliega en SageMaker AI (*endpoints* que gestiona el cliente); Bedrock es *serverless*.
- **Strands Agents frente a AgentCore.** Strands Agents es un SDK para **programar** agentes; AgentCore es la plataforma para **desplegarlos y operarlos** (y admite otros *frameworks*). Se combinan.
- **AgentCore frente a Bedrock Agents.** Bedrock Agents (*Classic*) ya no admite clientes nuevos: para proyectos nuevos, AgentCore.
- **Amazon Quick frente a Kiro.** Quick es para **empleados de negocio** (datos, automatización, investigación); Kiro, para **desarrolladores** (código, especificaciones, pruebas).
- **Amazon Q en proyectos nuevos.** Q Business ya no admite clientes nuevos (Amazon Quick) y los *plugins* de IDE de Q Developer pierden soporte el 30 de abril de 2027 (Kiro).
- **Quick = QuickSight.** QuickSight es ahora una funcionalidad (Quick Sight) dentro de Amazon Quick, que añade agentes, automatización e investigación.
- **Trainium frente a Inferentia.** Trainium sirve para entrenar **y** para inferencia; Inferentia es específico de inferencia: **no** es la opción para entrenar.
- **Kiro frente a AWS Transform.** Kiro, para desarrollar software nuevo con agentes; Transform, para modernizar o migrar lo existente (mainframes, VMware, código heredado).
- **Servicio gestionado = no hay que evaluar.** El servicio gestiona la infraestructura, pero evaluar la calidad, revisar las respuestas y configurar permisos sigue siendo trabajo del cliente.
- **Flex frente a lotes.** Ambos cuestan un 50 % menos que Standard, pero Flex mantiene las llamadas normales a la API (con herramientas) y lotes trabaja con ficheros en S3 de forma asíncrona. Priority, en cambio, cuesta un 75 % más.
- **Nova Canvas o Nova Reel en un proyecto nuevo.** Están retirados (fin de vida en septiembre de 2026).
- **Privacidad en Bedrock.** Los datos del cliente no se usan para mejorar los modelos base ni se comparten con los proveedores de modelos. Un distractor típico afirma lo contrario.

## Métricas de negocio

- **Exactitud como única métrica.** Un modelo muy exacto puede no aportar valor de negocio; se miden también ROI, eficiencia, conversión, ARPU o CLV según el objetivo.
- **ARPU frente a CLV.** ARPU es ingreso medio por usuario en un periodo; CLV es el valor de toda la relación con el cliente (sube con la retención).
- **Rendimiento entre dominios.** Mide si la calidad se mantiene en áreas distintas de las probadas; no es una métrica de latencia.
