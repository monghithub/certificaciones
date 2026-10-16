## Why

Los módulos 00 a 03 están completos e integrados en `main`. El Dominio 4 (Directrices para una IA responsable) pesa el 14 % del examen y exige reconocer las dimensiones de la IA responsable, las herramientas de AWS que ayudan a aplicarlas (Amazon Bedrock Guardrails, Model Evaluation, SageMaker Model Cards y Clarify), los riesgos legales de la IA generativa, el sesgo y la varianza, y la transparencia y explicabilidad de los modelos. Es la Iteración 4 de `cursos/aif-c01/promt.md`. El usuario pidió continuar «con todo hasta el final».

## What Changes

- **Módulo 04 (`cursos/aif-c01/modulos/04-ia-responsable/`):**
  - `README.md` con objetivos, mapa de cobertura de los 11 objetivos de las tareas 4.1 y 4.2, teoría con diagramas Mermaid y ejemplos de negocio, puntos clave y referencias oficiales.
  - `servicios.md` y `trampas.md`.
  - `laboratorio.md`: Amazon Bedrock Guardrails (filtros de contenido, temas denegados, filtro de datos sensibles y comprobación de *grounding*) probado en la ventana de prueba de la consola, sin recursos con coste por hora.
- **Banco del Dominio 4:** al menos 60 preguntas originales (mínimo 15 por tarea y 3 por objetivo); objetivo orientativo de 66 a 72, con el reparto de tipos, de posiciones y de dificultad (≈20/60/20) que piden las reglas.
- **Glosario:** entradas para cada concepto y servicio nuevo (dimensiones de la IA responsable, explicabilidad, transparencia, interpretabilidad, SHAP, Model Cards, AI Service Cards, Responsible AI Lens, A2I, filtros de Guardrails, Automated Reasoning checks, *contextual grounding check*, métricas de sesgo, análisis por subgrupos, sesgo y varianza, propiedad intelectual).
- **Revisión independiente** del módulo al cerrarlo, según «Calidad del contenido» de `AGENTS.md`.
- Actualización de `CHANGELOG.md`, `docs/journal.md`, el estado del README del curso y la comprobación e2e de las cajas de los diagramas del módulo 04.
- Fuera de alcance: los módulos 05 y 06 y cambios funcionales de la consola o de las herramientas.

## Capabilities

### New Capabilities
- `modulo-04-ia-responsable`: teoría, servicios, trampas y cobertura completa del Dominio 4.
- `banco-preguntas-dominio-4`: banco de al menos 60 preguntas del Dominio 4 con reparto por tareas, objetivos, tipos, posiciones y dificultad.
- `laboratorio-modulo-04`: laboratorio guiado de Amazon Bedrock Guardrails con coste y limpieza.

### Modified Capabilities
<!-- Ninguna. -->

## Impact

- Ficheros nuevos en `cursos/aif-c01/modulos/04-ia-responsable/` y entradas nuevas o actualizadas en `cursos/aif-c01/glosario.yaml`.
- La consola muestra el módulo y sus preguntas sin cambios de código.
- Requiere verificar en `docs.aws.amazon.com` y `aws.amazon.com` las dimensiones de la IA responsable de AWS, los componentes y niveles de Guardrails, Model Evaluation, Model Cards, los avisos de cierre a clientes nuevos (Clarify, Model Monitor, Ground Truth, A2I) y su sustitución recomendada, la indemnización de propiedad intelectual y las prácticas de sostenibilidad.
- Git: rama `aif-c01/modulo-04` con PR a `main`.
