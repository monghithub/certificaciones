# Trampas habituales del módulo 04

## Rasgos y herramientas

- **«Sesgo» siempre es discriminación.** En el examen hay dos sentidos: el ético (trato desigual a grupos) y el estadístico (*bias* frente a varianza, subajuste). Lee el contexto: «falla con los datos de entrenamiento y con los nuevos» es **alto sesgo** estadístico.
- **Transparencia, explicabilidad e interpretabilidad son lo mismo.** Transparencia: información para decidir (que hay IA, uso previsto, límites). Explicabilidad: por qué salió **esta** respuesta. Interpretabilidad: entender el modelo por dentro sin herramientas.
- **Robustez frente a veracidad.** Veracidad: la respuesta es correcta. Robustez: sigue siendo correcta cuando la entrada cambia un poco o es maliciosa.
- **Temas denegados frente a filtros de palabras.** Los temas denegados bloquean un **tema** descrito en lenguaje natural (consejos de inversión); los filtros de palabras bloquean **palabras o frases exactas** (nombres de la competencia).
- **Filtros de contenido para datos personales.** Los filtros de contenido detectan odio, insultos, sexual, violencia, conducta indebida y ataques de *prompt*. Los datos personales se tratan con el **filtro de información sensible**, que puede **enmascarar** en lugar de bloquear.
- ***Contextual grounding check* frente a Automated Reasoning checks.** Grounding: ¿la respuesta se basa en **la fuente** y responde a la pregunta? Automated Reasoning: ¿la respuesta es coherente con **reglas lógicas** definidas por la empresa? Automated Reasoning no protege contra la inyección de *prompts* y solo admite inglés.
- **Grounding para un chatbot conversacional.** La comprobación de *grounding* está pensada para resúmenes, paráfrasis y preguntas y respuestas sobre una fuente; el chat conversacional no está admitido.
- **Guardrails solo funciona con modelos de Bedrock.** La API `ApplyGuardrail` evalúa texto sin invocar un modelo, así que las mismas políticas se aplican a modelos externos o propios.
- **Guardrails sustituye a IAM o al cifrado.** Filtra contenido; no controla quién accede a qué ni protege los datos almacenados (módulo 05).
- **Descartar Clarify, Model Monitor, A2I o Ground Truth por sistema.** Ya no admiten clientes nuevos, pero la guía del examen los mantiene en alcance. Si la pregunta pide detectar sesgo o explicar predicciones de un modelo de ML clásico, vigilar su deriva o añadir revisión humana, y no dice que el cliente sea nuevo, siguen siendo la respuesta esperada. Si el enunciado deja claro que es un cliente nuevo, o habla de evaluar o proteger un **modelo fundacional**, piensa en Bedrock Evaluations y Guardrails.
- **Automated Reasoning checks bloquea respuestas.** Solo detecta: devuelve hallazgos y explicaciones, y la aplicación decide si entrega, reescribe o pide aclaraciones.

## Modelos, datos y riesgos

- **El modelo más capaz es el más responsable.** La opción responsable y sostenible es el **más pequeño que cumple** los requisitos, y antes, comprobar si hace falta IA generativa.
- **AWS indemniza por cualquier salida de cualquier modelo.** La indemnización sin límite cubre reclamaciones por **derechos de autor** sobre la salida de los modelos de Amazon y de los servicios enumerados en las condiciones, con uso responsable (sin introducir material que infrinja derechos ni desactivar filtros).
- **El cliente puede delegar en AWS la responsabilidad de las decisiones.** Según la política de IA responsable de AWS, el cliente responde de las decisiones tomadas con la IA y, si son **decisiones con consecuencias**, debe implantar supervisión humana.
- **Más datos arreglan el sesgo.** Más datos del mismo grupo mayoritario no ayudan: hacen falta datos **representativos** del grupo infrarrepresentado (o muestreo estratificado) y medir por subgrupos.
- **Una exactitud global alta descarta el sesgo.** La media puede ocultar que un grupo pequeño tiene mucho más error: hay que hacer **análisis por subgrupos**.
- **Sobreajuste frente a subajuste.** Bien en entrenamiento y mal en prueba = **sobreajuste** (alta varianza). Mal en los dos = **subajuste** (alto sesgo).
- **El sesgo se mide una vez, antes de lanzar.** Puede aparecer **después** del despliegue si cambian los datos reales: hay que monitorizar.
- **Etiquetas fiables por definición.** Las etiquetas humanas también tienen sesgos y errores: acuerdo entre anotadores, ejemplos de control y revisión de las sintéticas.

## Transparencia y diseño

- **Model Cards frente a AI Service Cards.** Model Cards: **tú** documentas **tu** modelo en SageMaker AI. AI Service Cards: **AWS** documenta **sus** servicios y modelos.
- **Model Cards detecta sesgo.** Documenta el uso previsto, el riesgo y los resultados de evaluación; no calcula métricas.
- **Más transparencia siempre es mejor.** Publicar las instrucciones del sistema o las reglas exactas de los filtros facilita saltárselos: se publica lo que el usuario necesita para decidir.
- **Elegir siempre el modelo de mayor rendimiento.** Si un regulador exige explicar cada decisión y el modelo interpretable cumple el mínimo de rendimiento, suele ser la opción adecuada.
- **SHAP da la verdad sobre el modelo.** Es una explicación a posteriori y aproximada; AWS recomienda validarla con expertos del negocio.
- **Diseño centrado en las personas = interfaz bonita.** Se trata de *feedback* de los usuarios, transparencia de las decisiones (factores, confianza, fuentes), supervisión humana donde hay consecuencias y explicaciones adaptadas a cada usuario.
