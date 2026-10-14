## Context

El Dominio 2 tiene 3 tareas y 14 objetivos (`fuentes/dominio-2.md`, guía v1.1). La v1.1 incorpora conceptos nuevos: ingeniería de contexto (2.1.5), agentes con MCP, memoria, herramientas y orquestación (2.1.6), y servicios como Amazon Quick, Kiro, Strands Agents y Amazon Bedrock AgentCore (2.3.1). Las reglas comunes de `AGENTS.md` («Calidad del contenido» y «Calidad del banco de preguntas»), las propias de `cursos/aif-c01/AGENTS.md` y los mínimos de `curso.yaml` (60, 15 y 3) se aplican desde la primera versión.

## Goals / Non-Goals

**Goals:**
- Cubrir los 14 objetivos con definición, criterio de decisión, ejemplo de negocio y trampa.
- Un banco de unas 65–75 preguntas originales, al estilo del examen, que pase todos los controles sin avisos.
- Un laboratorio de coste mínimo, sin recursos con coste por hora.

**Non-Goals:**
- Técnicas de los dominios 3 a 5 en profundidad (RAG, *fine-tuning*, evaluación, Guardrails, seguridad): solo se presentan para reconocerlas y se remite a sus módulos.
- Implementar agentes o MCP: el nivel es *foundational*.

## Decisions

- **Estructura de la teoría por tarea:**
  - 2.1: conceptos, con un diagrama del flujo texto → *tokens* → *embeddings* → modelo, el ciclo de vida del modelo fundacional, el coste por *tokens* con un ejemplo numérico, la ingeniería de contexto y los patrones agénticos.
  - 2.2: ventajas, limitaciones y selección de modelos (tabla de criterios), y métricas de negocio.
  - 2.3: servicios, con una tabla «necesidad → servicio» para Bedrock, SageMaker AI, JumpStart, Quick, Kiro, Strands Agents y AgentCore, ventajas de AWS e infraestructura, y compromisos de coste (*on-demand*, *batch*, Provisioned Throughput, modelos personalizados, Región e inferencia entre Regiones).
- **Verificación primero:** antes de redactar cada sección se consultan las páginas oficiales y se revisan los avisos de disponibilidad (*no longer open to new customers*, *Classic*), como exige `AGENTS.md`.
- **Laboratorio:** playground de Bedrock con un modelo de texto económico (por ejemplo, de la familia Amazon Nova). Se varían la temperatura, top-p y la longitud máxima, y se observan los *tokens* de entrada y de salida para estimar el coste. Equivalente opcional con `aws bedrock-runtime converse`. Sin recursos persistentes. Hay que verificar el procedimiento vigente de acceso a modelos en Bedrock.
- **Banco:** unas 70 preguntas (≈42 de opción múltiple, 14 de respuesta múltiple, 7 de ordenación y 7 de emparejamiento), de 4 a 6 por objetivo. Distractores vecinos: Bedrock/SageMaker AI/JumpStart, AgentCore/Strands Agents/Bedrock Agents Classic, Quick/Kiro, *embeddings*/*tokens*, temperatura/top-p, *on-demand*/Provisioned Throughput.

## Risks / Trade-offs

- [Servicios recientes con poca documentación (Kiro, Quick, Strands Agents)] → solo se afirma lo documentado; lo demás se marca `PENDIENTE DE VERIFICAR` y no se usa en preguntas.
- [Solapamiento con el Dominio 3] → el módulo 02 explica *qué* es cada técnica y remite al 03 para el *cómo* y el *cuándo*.
- [Coste del laboratorio] → modelo económico, prompts cortos, AWS Budgets recomendado y aviso de facturación.

## Open Questions

- ¿Se mantiene el plan de 4 semanas del README del curso con los mínimos de preguntas más altos? Se revisará al cerrar la iteración.
