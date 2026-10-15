## Why

Los módulos 00 a 02 están completos e integrados en `main`. El Dominio 3 (Aplicaciones de modelos fundacionales) es el de **más peso del examen (28 %)** y el que más criterios de decisión exige: selección de modelos, RAG y bases de datos vectoriales, coste de las formas de personalización, agentes, *prompt engineering*, *fine-tuning* y evaluación. Es la Iteración 3 de `cursos/aif-c01/promt.md`.

## What Changes

- **Módulo 03 (`cursos/aif-c01/modulos/03-modelos-fundacionales/`):**
  - `README.md` con objetivos, mapa de cobertura de los 19 objetivos de las tareas 3.1 a 3.4, teoría con diagramas Mermaid y ejemplos de negocio, puntos clave y referencias oficiales.
  - `servicios.md` y `trampas.md`.
  - `laboratorio.md`: técnicas de *prompt engineering* y Prompt Management en Amazon Bedrock (zero-shot, few-shot, chain-of-thought, plantillas con variables y versiones), sin recursos con coste por hora.
- **Banco del Dominio 3:** al menos 60 preguntas originales (mínimo 15 por tarea y 3 por objetivo); objetivo orientativo de 85 a 95, con el reparto de tipos, de posiciones y de dificultad (≈20/60/20) que piden las reglas.
- **Glosario:** entradas para cada concepto y servicio nuevo (por ejemplo, *chain-of-thought*, *few-shot*, *negative prompt*, *prompt injection*, *jailbreaking*, destilación, *instruction tuning*, RLHF, ROUGE, BLEU, BERTScore, *LLM-as-a-judge*, Bedrock Model Evaluation, Prompt Management, OpenSearch Service, Aurora, Neptune, RDS for PostgreSQL).
- **Revisión independiente** del módulo al cerrarlo, según «Calidad del contenido» de `AGENTS.md`.
- Actualización de `CHANGELOG.md`, `docs/journal.md`, el estado del README del curso y la comprobación e2e de las cajas de los diagramas del módulo 03.
- Fuera de alcance: los módulos 04 a 06 y cambios funcionales de la consola o de las herramientas.

## Capabilities

### New Capabilities
- `modulo-03-modelos-fundacionales`: teoría, servicios, trampas y cobertura completa del Dominio 3.
- `banco-preguntas-dominio-3`: banco de al menos 60 preguntas del Dominio 3 con reparto por tareas, objetivos, tipos, posiciones y dificultad.
- `laboratorio-modulo-03`: laboratorio guiado de *prompt engineering* y Prompt Management en Amazon Bedrock con coste y limpieza.

### Modified Capabilities
<!-- Ninguna. -->

## Impact

- Ficheros nuevos en `cursos/aif-c01/modulos/03-modelos-fundacionales/` y entradas nuevas en `cursos/aif-c01/glosario.yaml`.
- La consola muestra el módulo y sus preguntas sin cambios de código.
- Requiere verificar en `docs.aws.amazon.com` los datos de Bedrock Knowledge Bases, almacenes vectoriales admitidos, personalización de modelos (*fine-tuning*, preentrenamiento continuado, destilación, refuerzo), Model Evaluation, Prompt Management, AgentCore y los avisos de disponibilidad (SageMaker Clarify, Ground Truth, Bedrock Agents Classic).
- Git: rama `aif-c01/modulo-03` con PR a `main`.
