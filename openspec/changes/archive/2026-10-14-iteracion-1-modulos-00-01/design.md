## Context

Existen `cursos/aif-c01/fuentes/dominio-1.md` (3 tareas, 17 objetivos numerados `1.M.K`), el manifiesto `cursos/aif-c01/curso.yaml`, el esquema y validador de preguntas (por curso), el quiz y la consola multicurso. Los módulos están vacíos. Todas las rutas de este cambio son relativas a `cursos/aif-c01/` salvo los scripts y las pruebas. El destinatario es un perfil junior (poca experiencia en AWS) y el revisor un arquitecto sénior, así que el texto debe ser formal, preciso y verificable, a nivel *foundational*: qué servicio o técnica y por qué, no cómo implementarlo.

La guía v1.1 cita ejemplos nuevos (agentic AI, inferencia asíncrona y serverless, Amazon Quick, Kiro, modelos tradicionales frente a FMs) y retira otros (Data Wrangler, Feature Store, Model Monitor). Amazon Q figura como añadido en la página de revisiones pero no en la lista vigente de servicios (marcador abierto en `cursos/aif-c01/fuentes/servicios-alcance.md`).

## Goals / Non-Goals

**Goals:**
- Cobertura del 100 % de los 17 objetivos del Dominio 1, con trazabilidad en el mapa de cobertura.
- Banco de ≥ 30 preguntas originales, realistas y con todos los distractores explicados.
- Cada afirmación factual sobre AWS respaldada por una URL oficial.
- Comprobación automática de cobertura reutilizable en las iteraciones 2–5.

**Non-Goals:**
- Enseñar a programar o entrenar modelos, ingeniería de datos o de *features*, ajuste de hiperparámetros, pipelines, matemáticas o estadística (fuera de alcance según la guía): solo se nombran para reconocerlos.
- Contenido de GenAI más allá de lo que pide el Dominio 1 (el D2 y el D3 desarrollan FMs, RAG, prompts y evaluación).
- Banco de preguntas del módulo 00.

## Decisions

1. **Módulo 00 sin preguntas.** El esquema exige `dominio` 1–5 y `tarea` existente en `fuentes/`; el módulo 00 no corresponde a ninguna. Su mapa de cobertura se hace contra los cuatro conocimientos de AWS recomendados en la guía (servicios centrales, responsabilidad compartida, IAM, precios), que se transcriben en `cursos/aif-c01/fuentes/conocimientos-previos.md` con URL y fecha. Alternativa: crear un "dominio 0" en el esquema; descartada por romper el contrato con el validador y la consola.

2. **Un fichero por finalidad, según la plantilla de `promt.md`.** `README.md` sigue las cinco secciones obligatorias; `servicios.md` es una tabla `servicio → caso de uso → cuándo NO usarlo`; `trampas.md` recoge confusiones típicas (p. ej. IA vs ML vs deep learning vs GenAI; precisión vs recall; clasificación vs regresión; cuándo no usar ML).

3. **Mapa de cobertura con formato máquina-legible.** Tabla Markdown con una fila por objetivo, cuya primera columna es el id `N.M.K` (p. ej. `1.2.3`), seguida del texto abreviado y del enlace a la sección que lo cubre. Esto permite `comprobar_cobertura.py` sin ambigüedad.

4. **`scripts/comprobar_cobertura.py --curso <slug>`** (sin él, recorre todos los cursos). Lee `cursos/<curso>/fuentes/dominio-N.md`, extrae los ids `N.M.K` y comprueba, para el módulo indicado (o todos los que tengan README con mapa), que: cada id aparece en una fila del mapa con un enlace a un ancla existente en el mismo README; y, con `--preguntas`, que cada tarea (`N.M`) tiene al menos una pregunta. Sale con código 1 ante huecos. Los módulos sin contenido se omiten salvo `--modulo`. Se prueba con fixtures y entra en CI.

5. **Reparto de preguntas (32) proporcional al número de objetivos.** Tarea 1.1 (5 objetivos): 10; 1.2 (6): 12; 1.3 (6): 10. Tipos: 19 `multiple_choice`, 7 `multiple_response`, 3 `ordering`, 3 `matching` (≈59/22/9/9 %). Dificultad repartida (baja/media/alta ≈ 25/50/25). Ids `D1-001…D1-032`. Cada pregunta incluye `referencia` oficial.

6. **Proceso de redacción por objetivo.** Para cada objetivo: (a) consultar la documentación oficial de los servicios y conceptos implicados; (b) redactar la teoría; (c) anotar las URL en Referencias; (d) escribir las preguntas apoyadas en esa misma fuente. Lo no verificado se marca con `> ⚠️ PENDIENTE DE VERIFICAR:` y no se afirma. Los precios, cuotas y regiones no se citan sin fuente.

7. **Alcance de servicios.** Se tratan los servicios in scope relevantes para D1 (SageMaker AI, Transcribe, Translate, Comprehend, Lex, Polly, Rekognition, Textract, Personalize, Bedrock, Amazon Quick, Kiro, y de apoyo S3, Lambda, EC2). Los servicios out of scope no se tratan como evaluables. Amazon Q no se trata como evaluable mientras siga el marcador pendiente.

8. **Laboratorio del módulo 01 demostrativo y sin recursos persistentes.** Usar la consola con servicios de IA preentrenados (p. ej. Comprehend, Translate, Polly) para ver "qué hace un servicio gestionado" frente a entrenar un modelo propio. Incluye prerrequisitos, pasos, estimación de coste sacada de la página oficial de precios (o marcador pendiente), advertencia de facturación y sección de limpieza obligatoria (aunque sea "no hay recursos que eliminar", más cierre de sesión y revisión de la factura). Es opcional según `promt.md` §8.

9. **Verificación automática en cada entrega.** `validar_preguntas.py`, `comprobar_cobertura.py`, `pytest`, `markdownlint` y una comprobación de que todas las URL de `referencia` y de las secciones Referencias devuelven 200 (con `curl`, en local; en CI lo hace `lychee` para los `.md`).

10. **Git.** Rama `modulo/aif-c01/01-fundamentos-ia-ml` (y `modulo/aif-c01/00-base-aws`; con varios cursos el nombre de rama incluye el curso) con *Conventional Commits*, según `promt.md` §10. No se hace commit ni push sin que el usuario lo pida.

## Risks / Trade-offs

- [Datos de servicios que cambian (nombres, funcionalidades)] → Redactar contra la documentación oficial consultada en la fecha, registrar la fecha de consulta en Referencias y marcar lo dudoso.
- [Preguntas demasiado fáciles o con distractores débiles] → Escenarios de negocio; cada distractor plausible y explicado; revisión cruzada del validador y lectura final.
- [Riesgo de reproducir preguntas reales o material protegido] → Todo es de elaboración propia a partir de la documentación oficial; no se consultan "dumps".
- [Texto demasiado profundo para el nivel *foundational*] → Criterio: si requiere código o matemáticas, se reduce a un ejemplo y se señala como fuera de alcance.
- [Ejemplos de la guía poco claros (p. ej. "agentic AI" en D1)] → Tratar solo a nivel de definición y diferencia con IA/ML/GenAI; el desarrollo va al módulo 02 y 03.
- [Coste del laboratorio] → Servicios sin recursos persistentes, estimación basada en precios oficiales y aviso explícito.

## Open Questions

- El repositorio aún no tiene commits. ¿Quieres que, al cerrar la iteración, prepare el commit inicial en `main` (Iteración 0 y consola) y una rama por módulo, o prefieres hacerlo tú?
- ¿Incluir el laboratorio del módulo 01? `promt.md` lo marca como opcional; se propone sí, de bajo coste y sin recursos persistentes.
- Resolución de Amazon Q: se mantiene el marcador hasta confirmar con la guía.
