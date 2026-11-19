## Why

El usuario pide reforzar con diagramas dinámicos e interactivos los conceptos que se explican mejor de forma gráfica: «aquí por ejemplo puedes poner un diagrama dinámico para reforzar la idea, por favor revisa en el curso todos los sitios donde aplicaría…» (a propósito de las Regiones, en el módulo 00). Hoy el curso tiene 25 diagramas, pero hay apartados con procesos, decisiones, ciclos o jerarquías que solo se explican con texto y tablas.

## What Changes

Diagramas nuevos con el estilo y la interactividad que ya tiene la consola (aparición escalonada, flechas animadas, cada caja abre un modal con información, enlaces y «Ver en el curso»), en los apartados que lo piden. Revisados los 6 módulos de teoría, se proponen 19:

| # | Módulo · apartado | Qué dibuja | Forma |
|---|---|---|---|
| 1 | 00 · Servicios centrales (Regiones) | Cómo se elige la Región: servicios disponibles, cercanía a los usuarios (latencia) y requisitos legales; la disponibilidad varía por Región (Bedrock) | Decisión |
| 2 | 00 · IAM | Autenticación → autorización: *principal* (usuario, rol, federado, aplicación) → políticas de identidad y de recurso → permitido o denegado; ejemplo de la Lambda con rol | Flujo |
| 3 | 00 · Modelos de precios | Qué opción de pago según el patrón de uso (variable, estable, interrumpible, reservado) | Decisión |
| 4 | 01 · Tipos de inferencia | Tiempo real, *serverless*, asíncrona o por lotes según latencia, tamaño y tráfico | Decisión |
| 5 | 01 · Cuándo no usar ML + Elegir la técnica | ¿Reglas sencillas? ¿Datos? ¿Hay etiqueta? → regresión, clasificación, agrupamiento o anomalías | Decisión |
| 6 | 01 · De dónde salen los modelos | Escalera de coste y esfuerzo: usar tal cual < adaptar < entrenar uno propio | Escalera |
| 7 | 01 · MLOps | Ciclo: experimentar → *pipeline* → registro → despliegue → monitorización → reentrenamiento | Ciclo |
| 8 | 01 · Métricas | Matriz de confusión del ejemplo (VP, FP, FN, VN) → exactitud, precisión y exhaustividad | Flujo con cifras |
| 9 | 02 · Precios por *tokens* | Entrada + salida → coste, y las palancas (contexto, longitud, modelo, lotes, *caching*) | Flujo |
| 10 | 02 · Ingeniería de contexto | Las piezas que entran en la ventana de contexto (sistema, memoria, RAG, herramientas, ejemplos) | Jerarquía |
| 11 | 02 · Cómo elegir un modelo | Embudo: modalidad → capacidades → restricciones y Región → cumplimiento → coste y latencia → el más pequeño que cumpla | Embudo |
| 12 | 03 · Riesgos de los *prompts* | Por dónde entra cada ataque (usuario, documento, datos de entrenamiento) y qué lo mitiga | Flujo |
| 13 | 03 · Prompt Management | Variable → variantes → comparación → borrador → versión → la aplicación invoca por ARN | Ciclo |
| 14 | 03 · Evaluación de aplicaciones | Dónde se evalúa una aplicación RAG: recuperación y generación (fidelidad) | Flujo |
| 15 | 04 · Sesgo y varianza | Subajuste ↔ equilibrio ↔ sobreajuste, con el ejemplo de los tres modelos y cómo se corrige cada uno | Espectro |
| 16 | 05 · Citación y origen de los datos | Linaje: conjunto de datos → entrenamiento → versión del modelo → *endpoint*, con catálogo y Model Cards | Cadena |
| 17 | 05 · Ingeniería de datos segura | Datos en bruto → calidad → privacidad → control de acceso → integridad → modelo | Flujo |
| 18 | 05 · Estrategias de gobierno de datos | El ejemplo del ciclo de vida: 90 días en S3 Standard → Glacier → expiración | Línea temporal |
| 19 | 05 · Consideraciones de seguridad y privacidad | Recorrido de una petición con sus controles: aplicación → filtro de entrada (inyección) → control de acceso antes del contexto → modelo → filtrado de la salida (fugas, toxicidad), con registro y auditoría | Flujo |

Descartados: los apartados cuya tabla ya es la mejor forma (tipos de datos, casos de uso, criterios de selección de modelos del módulo 03, métricas ROUGE/BLEU), los que ya tienen un diagrama equivalente (agentes, compromisos de transparencia) y los parámetros de inferencia (el orden en que se aplican depende del modelo y no está documentado de forma general).

## Capabilities

### New Capabilities
- `diagramas-refuerzo`: diagramas de refuerzo en los apartados con procesos, decisiones, ciclos o jerarquías.

### Modified Capabilities
- Ninguna. Se aplican las reglas vigentes de estilo de diagramas (`AGENTS.md`).

## Impact

- Contenido: README de los módulos 00 a 05 (diagrama + bloque `nodos`); glosario si una caja necesita un concepto nuevo.
- Sin cambios de código. Validación con `validar_preguntas.py` (estilo y bloques `nodos`), `validar-mermaid.mjs` y prueba en navegador.
- Git: rama `aif-c01/diagramas` con PR a `main`.
