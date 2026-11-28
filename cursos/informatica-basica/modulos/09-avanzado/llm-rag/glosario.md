# Glosario: LLM, RAG y agentes

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## A

- **Agente** (agent, flujo de trabajo agéntico). *Concepto.* Sistema en el que el modelo decide dinámicamente qué pasos y herramientas usar para completar una tarea; en un flujo de trabajo, en cambio, los pasos los fija el código.
  - Referencia: <https://www.anthropic.com/engineering/building-effective-agents>
- **Alucinación** (hallucination, confabulación). *Concepto.* Respuesta del modelo que suena plausible pero es falsa o inventada, porque genera texto probable, no comprobado.
  - Referencia: <https://genai.owasp.org/llm-top-10/>

## B

- **Búsqueda semántica** (semantic search, base de datos vectorial). *Técnica.* Búsqueda por significado: se compara el embedding de la pregunta con los de los documentos y se devuelven los más cercanos.
  - Referencia: <https://huggingface.co/nomic-ai/nomic-embed-text-v1.5>

## E

- **Embedding** (vector, embeddings, representación vectorial). *Concepto.* Vector de números que representa el significado de un texto, de modo que textos parecidos tienen vectores cercanos.
  - Referencia: <https://docs.ollama.com/capabilities/embeddings>

## F

- **Fragmentación** (chunking, chunks). *Técnica.* División de los documentos en trozos de tamaño adecuado antes de calcular sus embeddings, para recuperar solo las partes relevantes.
  - Referencia: <https://arxiv.org/abs/2005.11401>

## I

- **Inyección de instrucciones** (prompt injection). *Concepto.* Ataque en el que un texto (del usuario o de un documento, web o herramienta) contiene instrucciones que el modelo sigue como si fueran legítimas. Es el riesgo LLM01 del OWASP Top 10 para LLM.
  - Referencia: <https://genai.owasp.org/llmrisk/llm01-prompt-injection/>

## L

- **Llamada a herramientas** (tool calling, function calling). *Técnica.* Capacidad del modelo de pedir, con un nombre y unos argumentos estructurados, que la aplicación ejecute una función y le devuelva el resultado.
  - Referencia: <https://docs.ollama.com/capabilities/tool-calling>

## M

- **Model Context Protocol** (MCP). *Protocolo.* Protocolo abierto para conectar aplicaciones de IA con herramientas y fuentes de datos de forma estándar, mediante servidores que exponen herramientas, recursos y prompts.
  - Referencia: <https://modelcontextprotocol.io/docs/getting-started/intro>
- **Modelo de lenguaje grande** (LLM, large language model). *Concepto.* Red neuronal (normalmente un transformer) entrenada con enormes cantidades de texto para predecir el siguiente token; de esa predicción repetida surge la generación de texto.
  - Referencia: <https://arxiv.org/abs/1706.03762>

## R

- **RAG** (generación aumentada por recuperación, retrieval-augmented generation). *Patrón.* Patrón que recupera documentos relevantes y los incluye en el prompt para que el modelo responda basándose en ellos, con fuentes, en lugar de en su memoria.
  - Referencia: <https://arxiv.org/abs/2005.11401>

## S

- **Similitud del coseno** (cosine similarity). *Métrica.* Medida de lo parecidos que son dos vectores según el ángulo entre ellos: 1 si apuntan igual, 0 si no tienen relación.
  - Referencia: <https://docs.ollama.com/capabilities/embeddings>

## T

- **Temperatura** (temperature, seed). *Concepto.* Parámetro que controla la aleatoriedad al elegir el siguiente token: baja da respuestas más previsibles; alta, más variadas.
  - Referencia: <https://docs.ollama.com/api>
- **Token** (tokens, tokenizador). *Concepto.* Fragmento de texto (una palabra, parte de una palabra o un signo) que el modelo procesa como unidad. Los límites de contexto y los costes se miden en tokens.
  - Referencia: <https://huggingface.co/docs/tokenizers/index>

## V

- **Ventana de contexto** (context window, contexto). *Concepto.* Número máximo de tokens (instrucciones, conversación, documentos y respuesta) que el modelo puede tener en cuenta a la vez.
  - Referencia: <https://huggingface.co/Qwen/Qwen3-1.7B>
