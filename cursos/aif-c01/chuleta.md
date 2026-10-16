# Chuleta AIF-C01

Resumen para repasar la víspera del examen. Cada línea remite a un módulo donde está explicada con su fuente oficial. Regla de oro: **busca en el enunciado la restricción que decide** (menor esfuerzo, menor coste, sin Internet, sin código, en milisegundos…) y descarta lo que no la cumple.

## Examen

65 preguntas (50 puntúan, 15 no y no se sabe cuáles), 90 minutos, escala 100–1.000, aprobado con 700. Opción múltiple, respuesta múltiple (acertar todas), ordenación y emparejamiento. No penaliza fallar: **no dejes nada en blanco**. Pesos: D1 20 %, D2 24 %, D3 28 %, D4 14 %, D5 14 %.

## D1. Fundamentos de IA y ML ([módulo 01](modulos/01-fundamentos-ia-ml/README.md))

- **IA ⊃ ML ⊃ aprendizaje profundo ⊃ IA generativa**; la IA agéntica actúa con herramientas para cumplir objetivos.
- **Aprendizaje:** supervisado (datos etiquetados: clasificación, regresión), no supervisado (agrupamiento, anomalías), por refuerzo (recompensas).
- **Inferencia en SageMaker AI:** tiempo real (baja latencia, endpoint siempre encendido), *serverless* (tráfico intermitente, sin GPU), asíncrona (cargas de hasta 1 GB y hasta 1 hora), transformación por lotes (conjuntos completos, sin endpoint).
- **No uses ML** si una regla exacta y auditable lo resuelve o si no hay datos. **ML clásico** para datos tabulares etiquetados; **modelo fundacional** para lenguaje, imagen y tareas abiertas.
- **Servicios de IA:** Textract (documentos), Comprehend (texto: sentimiento, entidades), Transcribe (voz→texto), Polly (texto→voz), Translate, Rekognition (imagen y vídeo), Lex (bots), Personalize (recomendaciones).
- **Pipeline:** datos → preparación (Glue, DataBrew, EMR) → entrenamiento (SageMaker AI, JumpStart, Canvas sin código) → evaluación → despliegue → monitorización. MLOps: Pipelines, Model Registry, MLflow.
- **Métricas:** precisión = VP/(VP+FP); exhaustividad (*recall*) = VP/(VP+FN); F1 = media armónica; AUC para clasificación; RMSE/MAE para regresión. Negocio: ROI, coste por usuario.
- **Trampas:** Clarify, Model Monitor, Ground Truth y A2I ya no admiten clientes nuevos (siguen siendo la respuesta si el enunciado no dice que el cliente es nuevo).

## D2. Fundamentos de IA generativa ([módulo 02](modulos/02-fundamentos-genai/README.md))

- **Tokens** (unidad de cómputo y precio), *embeddings* (significado como vector → búsqueda semántica), *chunking*, *transformers*, modelos multimodales y de difusión.
- **Coste por tokens:** entrada + salida (la salida suele costar más). Ejemplo: 100 000 peticiones × (1 000 entrada + 500 salida) a 0,60/2,40 USD por millón = 60 + 120 = 180 USD.
- **Ingeniería de contexto:** decidir qué llega al modelo en cada petición (resumir historial, recuperar solo lo relevante, memoria).
- **Agentes:** razonan, planifican y usan herramientas; **MCP** conecta agentes con herramientas y datos; **A2A** conecta agentes entre sí.
- **Desventajas:** alucinaciones, no determinismo, interpretabilidad, inexactitud. **Ventajas:** adaptabilidad, rapidez, simplicidad.
- **Servicios:** Bedrock (modelos por API), JumpStart (modelos para desplegar en SageMaker AI), AgentCore (operar agentes: Runtime, Memory, Identity, Gateway, Policy, Observability), Strands Agents (SDK), Quick (asistente para empleados), Kiro (desarrollo agéntico), Transform (modernización).
- **Infraestructura:** Trainium (entrenar), Inferentia (inferencia, mejor rendimiento por vatio).
- **Coste de Bedrock:** bajo demanda (tráfico variable); **lotes** y **Flex** (−50 %) si se puede esperar; **Priority** (+75 %) para la respuesta más rápida; **Provisioned Throughput** (capacidad garantizada, se paga aunque no se use); *prompt caching* para contextos repetidos.

## D3. Aplicaciones de modelos fundacionales ([módulo 03](modulos/03-modelos-fundacionales/README.md))

- **Elegir modelo:** el **más pequeño y barato que cumple** (coste, modalidad, latencia, idiomas, ventana de contexto, personalización, *prompt caching*, Región).
- **Parámetros:** temperatura (↑ variedad), top-p (proporción de probabilidad), top-k (número de candidatos), longitud máxima (corta), secuencias de parada.
- **Personalización, de menos a más coste:** *prompt* (aprendizaje en contexto) → **RAG** → *fine-tuning* → preentrenamiento. Destilación: modelo pequeño que imita a uno grande (abarata la inferencia).
- **RAG = datos propios y cambiantes con citas** (Knowledge Bases); *fine-tuning* = tono, formato o tarea fija. Almacenes de Knowledge Bases: OpenSearch Serverless, **Aurora** PostgreSQL, Neptune Analytics, S3 Vectors… (DynamoDB, ElastiCache y RDS for PostgreSQL tienen búsqueda vectorial pero **no** son almacén de Knowledge Bases).
- **Prompts:** zero-shot, few-shot (ejemplos del formato), chain-of-thought (pasos), plantillas, *prompt* negativo. Riesgos: inyección, *jailbreak*, fuga de *prompt*, envenenamiento. **Prompt Management:** plantillas con variables y versiones.
- **Evaluación:** humana (subjetivo), *benchmarks*, métricas automáticas (**ROUGE** resúmenes, **BLEU** traducción, **BERTScore** semántica), *LLM-as-a-judge*. **Bedrock Evaluations:** programática, humana, juez y RAG. Negocio: coste por interacción, tareas completadas, satisfacción.

## D4. IA responsable ([módulo 04](modulos/04-ia-responsable/README.md))

- **Dimensiones de AWS:** equidad, explicabilidad, privacidad y seguridad, seguridad frente a daños, controlabilidad, veracidad y robustez, gobierno, transparencia.
- **Guardrails:** filtros de contenido (incluye ataques de *prompt*), **temas denegados** (un tema), **filtros de palabras** (términos exactos), **información sensible** (bloquear o enmascarar PII), ***grounding* contextual** (alucinaciones frente a la fuente; no chat), **Automated Reasoning** (reglas lógicas; solo detecta). `ApplyGuardrail` = sin invocar modelo.
- **Sesgo alto** = subajuste (falla en todo); **varianza alta** = sobreajuste (bien en entrenamiento, mal en prueba). Grupos con pocos datos se aprenden peor.
- **Detectar sesgo:** calidad de etiquetas, auditorías humanas independientes, análisis por subgrupos. CI = (na−nd)/(na+nd); DI = q'd/q'a (1 = paridad).
- **Riesgos legales:** propiedad intelectual (AWS indemniza por derechos de autor en sus modelos y servicios cubiertos), sesgo, pérdida de confianza, riesgo para el usuario, alucinaciones. **Decisiones con consecuencias → supervisión humana.**
- **Transparencia:** **Model Cards** (tu modelo: uso previsto, riesgo, evaluación) frente a **AI Service Cards** (servicios de AWS). Interpretable (árbol, regresión) frente a opaco con SHAP. Sostenible: modelo del tamaño justo.

## D5. Seguridad, cumplimiento y gobierno ([módulo 05](modulos/05-seguridad-gobierno/README.md))

- **Responsabilidad compartida:** AWS protege la nube; tú, tus datos, permisos y configuración. Bedrock **no comparte** tus datos con los proveedores **ni los usa para entrenar**.
- **Proteger:** IAM (mínimo privilegio), KMS (claves de cifrado), TLS (tránsito), **PrivateLink** (sin Internet), **Macie** (PII en S3), Secrets Manager (claves de API), **AgentCore Identity** (credenciales del agente) y **Policy in AgentCore** (límites deterministas de herramientas).
- **Origen:** citas (respuesta), **linaje** (modelo), **Glue Data Catalog** (qué datos hay), **Lake Formation** (quién accede por columna o fila).
- **Registro:** **CloudTrail** = quién llamó a la API (90 días en el historial); **registro de invocaciones** de Bedrock = texto de *prompts* y respuestas (desactivado por defecto; el enmascarado de Guardrails no le afecta).
- **Gobierno:** **Config** (configuración y reglas), **Inspector** (vulnerabilidades), **Artifact** (informes de AWS), **Trusted Advisor** (recomendaciones), Well-Architected Tool (revisión con lentes). Audit Manager y Role Manager no admiten clientes nuevos.
- **Datos:** S3 Lifecycle (transición y expiración), CloudWatch Logs (retención indefinida por defecto), residencia con perfiles geográficos de inferencia (el global puede salir de la geografía).
- **Security Scoping Matrix:** 1 app de consumo, 2 app empresarial, 3 modelo preentrenado por API, 4 modelo ajustado, 5 modelo propio. Más ámbito, más responsabilidad.

## Antes de reservar

Haz el [simulacro](modulos/06-simulacro/README.md) y después el conjunto oficial de práctica de AWS Skill Builder (enlace en el [README del curso](README.md#antes-de-reservar-el-examen)). Repasa las trampas del dominio en el que más falles.
