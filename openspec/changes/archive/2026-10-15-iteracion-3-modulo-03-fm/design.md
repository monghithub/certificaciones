## Context

El Dominio 3 tiene 4 tareas y 19 objetivos (`fuentes/dominio-3.md`, guía v1.1) y pesa el 28 %. La v1.1 añade *prompt caching* como criterio de selección (3.1.1), los agentes (3.1.6), Prompt Management (3.2.5), la destilación (3.1.5 y 3.3.1), *LLM-as-a-judge* (3.4.2) y la evaluación de aplicaciones RAG, agentes y flujos (3.4.4, 3.4.5). El módulo 02 ya presentó *tokens*, *embeddings*, parámetros de inferencia, RAG y agentes a nivel de concepto: el 03 profundiza en el **cuándo** y el **coste** de cada técnica.

## Goals / Non-Goals

**Goals:**
- Cubrir los 19 objetivos con definición, criterio de decisión, ejemplo de negocio y trampa.
- Un banco de unas 85–95 preguntas originales que pase todos los controles sin avisos, con al menos un 18 % de dificultad baja.
- Un laboratorio de coste mínimo, sin recursos con coste por hora.

**Non-Goals:**
- IA responsable (sesgo, Guardrails como control ético) y seguridad o gobierno: se presentan para reconocerlos y se remite a los módulos 04 y 05.
- Implementar RAG, *fine-tuning* o agentes con código: el nivel es *foundational*.

## Decisions

- **Estructura de la teoría por tarea:**
  - 3.1: tabla de criterios de selección de modelos (coste, modalidad, latencia, idiomas, tamaño, complejidad, personalización, longitud, *prompt caching*); parámetros de inferencia con efecto en la respuesta; RAG de principio a fin con Knowledge Bases (diagrama); almacenes vectoriales en AWS con tabla «escenario → servicio»; escalera de personalización (*prompt* → RAG → *fine-tuning* → preentrenamiento continuado → preentrenamiento) con coste, esfuerzo y datos, más destilación; agentes y casos de negocio.
  - 3.2: anatomía de un *prompt* (instrucción, contexto, datos de entrada, indicador de salida, *negative prompt*); técnicas con ejemplos; buenas prácticas; riesgos (*prompt injection*/secuestro, *jailbreaking*, envenenamiento, exposición) y mitigaciones; Prompt Management (plantillas, variables, versiones, comparación).
  - 3.3: elementos del entrenamiento (preentrenamiento, *fine-tuning*, preentrenamiento continuado, destilación); métodos (*instruction tuning*, adaptación a dominio, *transfer learning*); preparación de datos (curación, gobierno, tamaño, etiquetado, representatividad, RLHF).
  - 3.4: enfoques de evaluación (humana, *benchmarks*, Bedrock Model Evaluation y sus modos), métricas con ejemplo numérico (ROUGE, BLEU, BERTScore, *LLM-as-a-judge*), objetivos de negocio, evaluación de RAG, agentes y flujos, y métricas de alineamiento con el negocio con ejemplo de coste por interacción.
- **Verificación primero:** antes de redactar cada sección se consultan las páginas oficiales y se revisan los avisos de disponibilidad.
- **Laboratorio:** Prompt Management de Bedrock con un modelo económico de Amazon Nova: crear un *prompt* con variables, probar zero-shot, few-shot y chain-of-thought, crear versiones y compararlas. El único recurso persistente (el *prompt*) no tiene coste por hora y se borra en la limpieza. Equivalente opcional con la AWS CLI.
- **Banco:** unas 90 preguntas (≈54 de opción múltiple, 18 de respuesta múltiple, 9 de ordenación y 9 de emparejamiento), de 4 a 6 por objetivo. Distractores vecinos: RAG/*fine-tuning*/preentrenamiento continuado, OpenSearch/Aurora/Neptune/DynamoDB, ROUGE/BLEU/BERTScore, zero-shot/few-shot/chain-of-thought, *prompt injection*/*jailbreaking*/envenenamiento, Model Evaluation automática/humana/*LLM-as-a-judge*, AgentCore/Bedrock Agents Classic.

## Risks / Trade-offs

- [Funcionalidades de Bedrock que cambian a menudo (modos de evaluación, métodos de personalización por modelo, almacenes vectoriales admitidos)] → se cita la página vigente; lo no verificable se marca `PENDIENTE DE VERIFICAR` y no se usa en preguntas.
- [Solapamiento con los módulos 02 y 04] → el 03 remite al 02 para los conceptos básicos y al 04 para sesgo y Guardrails como control responsable.
- [Coste del laboratorio] → modelo económico, *prompts* cortos, AWS Budgets recomendado y limpieza del *prompt* creado.

## Open Questions

- Ninguna bloqueante. El plan de 4 semanas del README del curso se revisará al cerrar la iteración.
