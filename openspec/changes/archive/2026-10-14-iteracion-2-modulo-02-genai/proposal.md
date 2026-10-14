## Why

Los módulos 00 y 01 están completos y revisados. El Dominio 2 (Fundamentos de IA generativa) pesa el 24 % del examen y es la base de los dominios 3 a 5: sin él, el estudiante no puede razonar sobre *tokens*, *embeddings*, agentes ni costes de Bedrock. Es la Iteración 2 de `cursos/aif-c01/promt.md`.

## What Changes

- **Módulo 02 (`cursos/aif-c01/modulos/02-fundamentos-genai/`):**
  - `README.md` con objetivos, mapa de cobertura de los 14 objetivos de las tareas 2.1, 2.2 y 2.3, teoría con diagramas Mermaid y ejemplos de negocio, puntos clave y referencias oficiales.
  - `servicios.md` y `trampas.md`.
  - `laboratorio.md`: playground de Amazon Bedrock con parámetros de inferencia (temperatura, top-p, longitud máxima) y observación de *tokens* y coste, con estimación de coste y limpieza.
- **Banco del Dominio 2:** al menos 60 preguntas originales (mínimo 15 por tarea y 3 por objetivo) al estilo del examen, con el reparto de tipos y de posiciones que exige la CI.
- **Glosario:** entradas para cada concepto y servicio nuevo (por ejemplo, *token*, *chunking*, *embedding*, vector, modelo multimodal, modelo de difusión, ingeniería de contexto, MCP, Strands Agents).
- **Revisión independiente** del módulo al cerrarlo, según «Calidad del contenido» de `AGENTS.md`.
- Actualización de `CHANGELOG.md`, `docs/journal.md` y el estado del README del curso.
- Fuera de alcance: los módulos 03 a 06 y los cambios en la consola o en las herramientas.

## Capabilities

### New Capabilities
- `modulo-02-fundamentos-genai`: teoría, servicios, trampas y cobertura completa del Dominio 2.
- `banco-preguntas-dominio-2`: banco de al menos 60 preguntas del Dominio 2 con reparto por tareas, objetivos, tipos y posiciones.
- `laboratorio-modulo-02`: laboratorio guiado del playground de Amazon Bedrock con coste y limpieza.

### Modified Capabilities
<!-- Ninguna: las herramientas, el esquema y la consola no cambian de requisitos. -->

## Impact

- Ficheros nuevos en `cursos/aif-c01/modulos/02-fundamentos-genai/` y entradas nuevas en `cursos/aif-c01/glosario.yaml`.
- La consola muestra el módulo y sus preguntas sin cambios de código.
- Requiere verificar en `docs.aws.amazon.com` los datos de Bedrock, AgentCore, Strands Agents, Quick, Kiro, JumpStart y los precios por *tokens*.
- Git: rama `modulo/02-fundamentos-genai` con PR a `main`.
