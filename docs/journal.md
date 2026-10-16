# Journal del proyecto

Diario de trabajo del curso AIF-C01 y de su consola. Recoge **qué se hizo, qué se decidió y por qué** en cada etapa, con sus commits y cambios de OpenSpec. El detalle de los cambios está en [CHANGELOG.md](../CHANGELOG.md); los requisitos vigentes, en [openspec/specs/](../openspec/specs/).

## Cómo se trabaja

1. **Proponer** cada etapa como un cambio de OpenSpec (`/opsx:propose`): `proposal.md`, `design.md`, `specs/` y `tasks.md`.
2. **Revisar** la propuesta con el usuario antes de implementar.
3. **Implementar** (`/opsx:apply`) en una rama propia (`modulo/NN-…` o `feat/…`), marcando las tareas.
4. **Verificar**: `validar_preguntas.py`, `comprobar_cobertura.py --preguntas`, markdownlint, Mermaid (`tests/e2e`) y `pytest`.
5. **Revisión independiente** del contenido al cerrar cada módulo (ver `AGENTS.md`, «Calidad del contenido»).
6. **Cerrar la etapa**: archivar el cambio (`/opsx:archive`), actualizar `CHANGELOG.md` y este journal, commit con *Conventional Commits*, push y PR a `main`.

---

## 2026-10-14

### Iteración 0: fundación del curso

- Estructura del repositorio, `AGENTS.md`, licencia propuesta (MIT para el código y CC BY 4.0 para el contenido, pendiente de confirmar), esquema JSON del banco, `validar_preguntas.py`, `quiz.py` y CI (markdownlint, lychee, validación y aviso de pendientes).
- Transcripción literal de la guía oficial v1.1 (30 de abril de 2026): 69 objetivos en 14 tareas y listas de servicios dentro y fuera de alcance.
- Decisión: se llaman **objetivos** (`N.M.K`) a lo que `promt.md` llamaba habilidades, como hace la guía v1.1.
- OpenSpec: `2026-10-14-iteracion-0-fundacion-curso`.

### Consola web, soporte multicurso, glosario y diagramas

- Consola web (FastAPI) con roles `admin` y `estudiante`, lectura con seguimiento, cuestionarios, simulacro cronometrado y estadísticas.
- Multicurso: el contenido pasa a `cursos/<slug>/` con manifiesto `curso.yaml`; matrícula por curso.
- Glosario por curso con modal y diagramas Mermaid con estilo único validado, en los que cada caja abre información y enlaces.
- OpenSpec: `consola-web-curso`, `soporte-multicurso`, `glosario-y-diagramas-interactivos` e `info-en-cajas-de-diagramas` (archivados con fecha 2026-10-14).

### Iteración 1: módulos 00 y 01

- Módulo 00 (base de AWS) y módulo 01 (Dominio 1) con mapa de cobertura de los 17 objetivos, laboratorio demostrativo y 32 preguntas.
- Nueva herramienta `comprobar_cobertura.py`.
- OpenSpec: `2026-10-14-iteracion-1-modulos-00-01`.

### Revisión de calidad de la Iteración 1

- **Encargo:** revisión crítica independiente de los módulos 00 y 01 como experto en AIF-C01 y en didáctica para perfiles junior, sin modificar ficheros. Primera valoración: 6,5/10 de preparación para el Dominio 1.
- **Hallazgos verificados en la documentación oficial:**
  - D1-026 afirmaba que la mayoría de los servicios de IA no admiten *endpoints* de VPC. Es falso según la lista de PrivateLink; la frase venía de una guía de decisión de mayo de 2024.
  - SageMaker Experiments es ahora *Classic*; AWS recomienda MLflow.
  - Desde el 3 de diciembre de 2024, «Amazon SageMaker» es una plataforma unificada que incluye SageMaker AI.
  - La política IAM del laboratorio no servía para la consola.
  - La capa gratuita cambió en julio de 2025 (créditos y plan de seis meses).
  - Ground Truth tampoco admite clientes nuevos; se suma a Model Monitor, Clarify y Bedrock Agents Classic.
- **Lagunas:** servicios por etapa (datos), capacidades de SageMaker AI (Canvas, Pipelines, Model Registry), Amazon Nova, restricciones operativas, matriz de confusión y exactitud con clases desequilibradas.
- **El usuario pidió:**
  1. Mejorar todo lo posible.
  2. Que las mejoras de procedimiento valgan para todo el proyecto.
  3. Muchas más preguntas, al estilo de las típicas del examen.
  4. Enlazar AWS Skill Builder.
- **Hecho:**
  - Correcciones y ampliaciones en los módulos 00 y 01, el laboratorio y el glosario (18 entradas nuevas).
  - Banco de 32 a **82 preguntas**, al menos 3 por objetivo y la posición de la respuesta repartida (12–13 por letra).
  - Reglas permanentes en `AGENTS.md`: «Calidad del contenido» y «Calidad del banco de preguntas».
  - Mínimos más altos (60 por módulo, 15 por tarea, 3 por objetivo).
  - Controles nuevos en la CI (posición de la respuesta, opciones repetidas, mínimo por objetivo, avisos por absolutos y por enunciados cortos).
  - Enlace al conjunto oficial de práctica de Skill Builder.
- **Decisiones:**
  - Las preguntas son siempre originales. El conjunto oficial de Skill Builder (20 preguntas, requiere iniciar sesión) solo se recomienda como control final y no se copia. No se usan *dumps*.
  - La posición de la respuesta se reparte en el YAML, porque el quiz y la consola no barajan las opciones.
  - Las heurísticas con falsos positivos son avisos; los controles objetivos son errores.
- **Verificación:** validador sin avisos, cobertura, markdownlint, 5/5 diagramas Mermaid y 215 tests en verde.
- OpenSpec: `2026-10-14-revision-calidad-iteracion-1`, documentado a posteriori porque la revisión empezó como informe y el usuario pidió aplicar los cambios sobre la marcha.

### Cierre de etapas y primera subida al repositorio

- Primeros commits del repositorio, agrupados por bloque: fundación y herramientas, consola, módulos 00 y 01, y OpenSpec. Identidad de git local del repositorio: `monghithub <monghit@gmail.com>`.
- Archivados los 7 cambios completados de OpenSpec. Para poder archivarlos se corrigieron dos requisitos antiguos que no usaban la palabra normativa SHALL (`official-sources`, `glosario-conceptos`). Los 26 specs consolidados en `openspec/specs/` validan en modo estricto.
- Push inicial de `main` a `origin` (`github.com/monghithub/aw-saif-c01`). A partir de aquí, cada etapa en su rama y con PR.
- La primera CI en GitHub falló solo por la comprobación de enlaces: `docs/consola.md` cita `http://127.0.0.1:8000/`. Se excluyen los enlaces locales en `.lychee.toml` y la CI pasa a verde en `main`.

### Renombrado del repositorio

- A petición del usuario, el repositorio de GitHub pasa de `aw-saif-c01` a **`certificaciones`** (`github.com/monghithub/certificaciones`). GitHub redirige el nombre antiguo, y el remoto `origin` local ya apunta al nuevo. La carpeta local del clon conserva su nombre.

### Plataforma multicertificación

- **Visión del usuario:** el repositorio reunirá en la consola todos los cursos de certificación que vaya estudiando, de cualquier proveedor, no solo de AWS.
- **Hecho** (rama `feat/plataforma-multicertificacion`, cambio de OpenSpec `plataforma-multicertificacion`):
  - Campos `proveedor` y `fuentes_oficiales` en el manifiesto; las referencias de las preguntas se validan contra las fuentes oficiales de su curso.
  - `AGENTS.md` raíz genérico, con el procedimiento para añadir un curso, y reglas propias de AWS y AIF-C01 en `cursos/aif-c01/AGENTS.md`.
  - `promt.md` movido a `cursos/aif-c01/`.
  - Consola «Certificaciones», imagen `certificaciones-consola` y README raíz con tabla de cursos por proveedor.
- **Decisiones:**
  - Las fuentes oficiales se declaran como hosts (se aceptan los subdominios) y son opcionales, para no romper los cursos existentes.
  - Cada curso lleva su propio `AGENTS.md`, que complementa al raíz.
  - Ramas `<slug>/<etapa>` y etiquetas `<slug>-vX.Y.Z` por curso.
- **Verificación:** validador, cobertura y 219 tests en verde (4 nuevos).
- Integrado en `main` con la PR #2 (CI en verde; el primer intento falló por un error temporal de la API de GitHub) y cambio archivado como `2026-10-14-plataforma-multicertificacion`.

### Iteración 2: propuesta del módulo 02 (Dominio 2)

- Rama `modulo/02-fundamentos-genai`. Cambio de OpenSpec `iteracion-2-modulo-02-genai` con propuesta, diseño, tres specs (`modulo-02-fundamentos-genai`, `banco-preguntas-dominio-2`, `laboratorio-modulo-02`) y tareas. Valida en modo estricto.
- Decisiones de diseño:
  - Unas 70 preguntas, de 4 a 6 por objetivo.
  - El laboratorio usa el playground de Bedrock con un modelo económico y sin recursos con coste por hora.
  - El módulo 02 explica *qué* es cada técnica y remite al 03 para el *cómo*.
  - Antes de redactar se verifica cada servicio reciente (Quick, Kiro, Strands Agents, AgentCore).
- Estado: el usuario la aprobó («hazlo todo») y se implementó en la misma rama.

### Iteración 2: módulo 02 (Dominio 2) implementado

- **Petición del usuario:** «hazlo todo», que cubría reconstruir la consola con la imagen `certificaciones-consola` (la antigua `aif-c01-consola` se borró) e implementar la iteración 2.
- **Verificación primero:** antes de redactar se descargaron y contrastaron unas 60 páginas oficiales (Bedrock, niveles de servicio, lotes, Provisioned Throughput, inferencia entre Regiones, personalización, AgentCore, Quick, Kiro, Strands Agents, MCP, Nova, Amazon Q, Trainium e Inferentia). Hallazgos: Amazon Q Business ya no admite clientes nuevos (→ Amazon Quick), los *plugins* de IDE de Q Developer pierden soporte el 30/04/2027 (→ Kiro), los modelos personalizados pueden usarse también bajo demanda y Nova Canvas y Nova Reel están retirados.
- **Hecho:** teoría con los 14 objetivos y 5 diagramas, `servicios.md`, `trampas.md`, laboratorio del *playground* de Bedrock con Nova Micro, 75 preguntas y 38 entradas de glosario. La prueba de navegador cubre también las cajas del módulo 02.
- **Decisiones:**
  - El ejemplo de coste por *tokens* usa precios reales y fechados de un modelo cuya tabla es pública (DeepSeek v3.2 en us-east-1), porque la tabla de Nova se carga con JavaScript y no se pudo verificar.
  - El laboratorio no da el precio de Nova Micro: remite a la página de precios y acota el coste con una cota superior explícita.
  - El glosario no usa «temperatura» como alias, porque en el módulo 01 aparece con otro sentido (la temperatura de una máquina).
  - Las preguntas se escriben con la correcta primero y un generador fuera del repositorio reparte las letras; la fuente de verdad es `preguntas.yaml`.
- **Revisión independiente:** encontró 3 errores críticos (cálculo de un distractor, Nova Canvas y Nova Reel retirados y Trainium también para inferencia), 11 importantes (AWS Transform y A2A ausentes, cifras de Priority y Flex, pistas en enunciados, distractores débiles, la correcta como opción más larga en el 54 % de los casos) y varios menores. Se aplicaron todos antes del cierre, salvo dos: las referencias de las métricas de negocio siguen citando la guía del examen, porque AWS no tiene páginas oficiales que las definan, y la dificultad baja queda en el 13 %.
- **Verificación:** validador, cobertura (14/14, de 4 a 8 preguntas por objetivo), markdownlint, 10/10 diagramas, 219 tests y 36/36 comprobaciones de navegador.
- **Queda abierto:** el marcador sobre Amazon Q en `servicios-alcance.md` y en `servicios.md`. En la consola, la solución de las preguntas de emparejamiento se muestra en formato técnico (`[['1','e'], …]`); es un defecto anterior a esta iteración.

## 2026-10-15

### Integración de la iteración 2 y arreglo de la consola

- **Petición del usuario:** «¿Puedes continuar con todo?», tras la lista de lo que faltaba.
- PR #1 (módulo 02) integrada en `main`.
- PR #3 (`fix/consola-solucion-legible`) integrada: la solución y la respuesta de las preguntas de ordenación y emparejamiento se muestran como lista con el texto de cada opción en lugar de `[['1', 'e'], …]`. Una prueba nueva (220 en total).

### Iteración 3: módulo 03 (Dominio 3)

- Rama `aif-c01/modulo-03`, cambio de OpenSpec `iteracion-3-modulo-03-fm` (propuesta, diseño, tres specs y tareas). La petición «continuar con todo» se tomó como aprobación de la propuesta.
- **Verificación primero:** unas 50 páginas oficiales (Knowledge Bases, almacenes vectoriales, personalización, destilación, *reinforcement fine-tuning*, evaluaciones, Prompt Management, ataques de *prompt*, AgentCore Evaluations, Flows, guías prescriptivas de bases vectoriales y de evaluación). Hallazgos: Bedrock solo enumera hoy tres métodos de personalización y la página de modelos con preentrenamiento continuado ya no existe; la fuga de *prompt* de Guardrails solo está en su modalidad Standard; Bedrock mide la exactitud de los resúmenes con BERTScore; DynamoDB y ElastiCache tienen búsqueda vectorial, pero Knowledge Bases no los admite.
- **Hecho:** teoría con 19/19 objetivos y 6 diagramas, `servicios.md`, `trampas.md`, laboratorio de técnicas de *prompt* y Prompt Management, 94 preguntas y 41 entradas de glosario.
- **Decisiones:**
  - La destilación se presenta aparte de la escalera de coste, porque incluye un *fine-tuning*.
  - Los ejemplos de coste de la personalización usan cifras supuestas y lo dicen; el coste de RAG reutiliza el precio real y fechado del módulo 02.
  - «using multiple comments» y «task engineering» se interpretan y se marcan como pendientes, sin preguntas que dependan de ellos.
  - El generador de D3 vive fuera del repositorio, como el de D2; la fuente de verdad es `preguntas.yaml`.
- **Banco D2:** 6 preguntas fáciles añadidas al final sin regenerar el banco, para no cambiar las opciones de preguntas ya respondidas por estudiantes.
- **Revisión independiente:** 2 hallazgos críticos (DynamoDB y ElastiCache; la destilación como peldaño más barato), 8 importantes (paso de Save as draft, la correcta como opción más larga en 27 preguntas, D3-057, «nivel Standard» ambiguo, RDS y Knowledge Bases, BERTScore en Bedrock, objetivos 3.2.3 y 3.4.3, dificultades) y varios menores. Se aplicaron todos.
- **Verificación:** validador sin avisos, cobertura 19/19 (de 4 a 7 preguntas por objetivo), markdownlint, 16/16 diagramas, 220 tests y 37/37 comprobaciones de navegador.

### Pendiente

- Iteraciones 4 y 5: módulos 04 (IA responsable) y 05 (seguridad, cumplimiento y gobierno), con al menos 60 preguntas cada uno y laboratorio.
- Iteración 6: simulacro de 65 preguntas inéditas, `chuleta.md`, decidir sobre `glosario.md` (hoy existe `glosario.yaml`) y revisión cruzada.
- Marcadores `PENDIENTE DE VERIFICAR`: Amazon Q (`fuentes/servicios-alcance.md`, módulo 02), preentrenamiento continuado en Bedrock y «using multiple comments» / «task engineering» (módulo 03).
- Decisiones del usuario: licencia y formato de `ordering`/`matching`.
- Borrar los usuarios de prueba `test` y `admintest` de la consola local al terminar los desarrollos.
- Etiqueta `aif-c01-v1.0.0` con todo completo, la CI en verde y sin pendientes.

## 2026-10-16

### Cierre de la sesión

- **Petición del usuario:** «guarda el journal y haz push».
- PR #4 (iteración 3, módulo 03) abierta con la CI en verde y pendiente de la revisión del usuario antes de integrarla en `main`.
- No se ha abierto ningún túnel público hacia la consola: queda a la espera de confirmación y, antes, de desactivar los usuarios de prueba `test` y `admintest`.
- Sigue vigente la lista de pendientes del 2026-10-15.

### Iteración 4: módulo 04 (Dominio 4)

- **Petición del usuario:** «continua con todo hasta el final y haz push». Se integró la PR #4 (iteración 3) y se encadenan las iteraciones 4, 5 y 6, cada una con su PR. La petición se toma como aprobación de las propuestas y de la integración de cada PR con la CI en verde.
- Rama `aif-c01/modulo-04`, cambio de OpenSpec `iteracion-4-modulo-04-rai` (propuesta, diseño, tres specs y tareas).
- **Verificación primero:** unas 60 páginas oficiales (IA responsable y política de AWS, AI Service Cards, Responsible AI Lens y Generative AI Lens, todas las salvaguardas de Guardrails con sus niveles, idiomas, permisos y precios, Bedrock Evaluations, Clarify y sus métricas, Model Monitor, A2I, Ground Truth, Model Cards, FAQ de Bedrock, guía prescriptiva de interpretabilidad, sobreajuste, Inferentia). Hallazgos: A2I también está cerrado a clientes nuevos; AWS publica cómo sustituir Clarify (bibliotecas abiertas, SHAP y Bedrock Evaluations) y Model Monitor (soluciones abiertas de monitorización); la *Responsible AI Lens* (noviembre de 2025) enumera diez dimensiones frente a las ocho de la página de AWS; Automated Reasoning checks solo detecta.
- **Hecho:** teoría con 11/11 objetivos y 5 diagramas, `servicios.md`, `trampas.md`, laboratorio de Guardrails, 75 preguntas y 34 entradas de glosario.
- **Decisiones:**
  - Los servicios cerrados a clientes nuevos se explican porque el examen los nombra, con una regla de lectura: si la pregunta no dice que el cliente sea nuevo, siguen siendo la respuesta esperada; si es un cliente nuevo o un modelo fundacional, Bedrock Evaluations y Guardrails.
  - Las cifras de marketing (por ejemplo, el porcentaje de contenido dañino que bloquea Guardrails) no se usan; la de rendimiento por vatio de Inferentia2 se cita con su fuente.
  - El banco reparte la longitud de las opciones: la correcta es la más larga en 15 de 52 preguntas de opción múltiple.
  - El generador del banco pasa a ser genérico (`genbanco.py`, fuera del repositorio); la fuente de verdad sigue siendo `preguntas.yaml`.
- **Revisión independiente:** sin errores críticos; 9 hallazgos importantes (Automated Reasoning solo detecta, lectura de Clarify/A2I en el examen, fechas no verificadas en dos preguntas, alertas de deriva, pasos del laboratorio, distractores de otra categoría, fmeval y gobierno de ML, dos dificultades) y varios menores. Se aplicaron todos; se añadieron tres preguntas con Clarify o A2I como respuesta correcta.
- **Verificación:** validador sin avisos, cobertura 11/11 (de 6 a 9 preguntas por objetivo), markdownlint, 21/21 diagramas, 220 tests y 38/38 comprobaciones de navegador.

### Iteración 5: módulo 05 (Dominio 5)

- Rama `aif-c01/modulo-05`, cambio de OpenSpec `iteracion-5-modulo-05-seguridad` (propuesta, diseño, tres specs y tareas), integrada la PR #5 de la iteración 4.
- **Verificación primero:** unas 60 páginas oficiales (protección de datos, cifrado, PrivateLink, retención de datos, detección de abusos, registro de invocaciones y CloudTrail de Bedrock; AgentCore Identity y Policy; Macie, KMS, Secrets Manager; linaje, Glue Data Catalog y Data Quality, Lake Formation; Config, Inspector, Artifact, CloudTrail, Trusted Advisor, Audit Manager, Well-Architected Tool; S3 Lifecycle, CloudWatch Logs; inferencia entre Regiones; AI Security Scoping Matrix; Generative AI Lens y Responsible AI Lens; CAF for AI). Hallazgos: Audit Manager y SageMaker Role Manager ya no admiten clientes nuevos; Bedrock tiene ahora modos de retención de datos por Región y algunos modelos retienen tráfico hasta 30 días para detección de abusos; la Scoping Matrix se publica como *AI Security Scoping Matrix*; el CAF for AI es ya solo de referencia histórica (no se cita).
- **Hecho:** teoría con 8/8 objetivos y 4 diagramas, `servicios.md`, `trampas.md`, laboratorio de mínimo privilegio, registro y auditoría, 69 preguntas y 30 entradas de glosario.
- **Decisiones:**
  - GuardDuty, IAM Identity Center y otros servicios de seguridad fuera de alcance solo se mencionan para reconocerlos; ninguna pregunta los tiene como respuesta correcta.
  - La retención cero de Bedrock se explica en una frase (es reciente y se configura por API) y tiene una sola pregunta de dificultad alta.
  - Los enunciados con la comprobación de *grounding* hablan de servicios de preguntas y respuestas o de resumen, no de chatbots, también en el módulo 04 (sin cambiar opciones ni ids).
- **Revisión independiente:** 1 hallazgo crítico (Role Manager cerrado a clientes nuevos, que era la respuesta correcta de una pregunta), 7 importantes (GuardDuty fuera de alcance, límites del *grounding*, eventos de datos de CloudTrail, una pregunta de respuesta múltiple con correcta débil, una ordenación ambigua, preguntas de definición con distractores débiles, retención de datos) y varios menores. Se aplicaron todos.
- **Verificación:** validador sin avisos, cobertura 8/8 (de 7 a 10 preguntas por objetivo), markdownlint, 25/25 diagramas, 220 tests y 39/39 comprobaciones de navegador.

### Iteración 6: simulacro, chuleta, glosario y revisión cruzada

- Rama `aif-c01/simulacro`, cambio de OpenSpec `iteracion-6-simulacro-cierre` (propuesta, diseño, specs `simulacro-aif-c01`, `chuleta-y-glosario` y delta de `question-validation`), integrada la PR #6 de la iteración 5.
- **Hecho:**
  - Simulacro de 65 preguntas inéditas (13/16/18/9/9 por dominio, las 14 tareas, 44 de opción múltiple, 10 de respuesta múltiple, 5 de ordenación y 6 de emparejamiento; 13 baja, 39 media y 13 alta), con los dominios intercalados, e instrucciones en `06-simulacro/README.md`. Probado en la consola local: el botón aparece, arranca con 1/65 y cronómetro de 90 minutos.
  - `validar_preguntas.py` falla si un enunciado del simulacro repite, normalizado, uno de los bancos o del propio simulacro, y avisa de las preguntas muy parecidas (Jaccard ≥ 0,5).
  - `glosario.md` generado desde `glosario.yaml` con `scripts/generar_glosario.py`; la CI comprueba que está al día.
  - `chuleta.md` por dominio.
- **Revisión cruzada:**
  - Cobertura: 69/69 objetivos con mapa y preguntas (más el módulo 00 de conocimientos previos).
  - Servicios dentro de alcance: los 51 de la lista oficial aparecen en algún módulo; se añadieron al módulo 01 y al glosario AWS Data Exchange, Amazon EMR, Amazon Redshift, Amazon ECS, Amazon EKS y Amazon CloudFront, que faltaban.
  - Servicios fuera de alcance: ninguno de los 117 es respuesta correcta en los 466 enunciados.
  - Marcadores `PENDIENTE DE VERIFICAR`: se revalidaron el 2026-10-16 las páginas oficiales (servicios dentro de alcance, revisiones, Dominio 3, personalización de Bedrock) y siguen las mismas contradicciones; los cinco marcadores se mantienen y ninguna pregunta depende de ellos.
- **Decisiones:**
  - `glosario.yaml` sigue siendo la fuente de verdad (lo usa la consola); `glosario.md` es un derivado para leer en GitHub.
  - La comprobación de servicios dentro de alcance se hizo de forma puntual y queda documentada aquí; no se añade como control permanente.
  - No se crea la etiqueta `aif-c01-v1.0.0`: `promt.md` y `AGENTS.md` la condicionan a no tener marcadores pendientes.
- **Revisión independiente:** la primera versión del simulacro reformulaba con otras palabras el escenario de unas 35 preguntas de los bancos (por ejemplo, el mismo cálculo de 180 USD por tokens). Se reescribió entero eligiendo decisiones que los bancos no evalúan y los objetivos que no tenían pregunta en el simulacro (1.1.1, 1.1.4, 1.2.1, 1.2.4, 1.3.3, 3.2.1, 3.2.3, 3.4.3, 4.1.1, 4.2.3). La similitud máxima con los bancos bajó de 0,85 a 0,37. Lección: la comparación literal de enunciados no basta para garantizar preguntas inéditas; hay que comparar la decisión que se evalúa.
- **Segunda verificación del simulacro reescrito:** un distractor defendible (los modelos personalizados de Bedrock sí pagan un almacenamiento mensual), seis preguntas que aún repetían la decisión de un banco (sustituidas), una referencia que no respaldaba la respuesta (SHAP), dos ordenaciones ambiguas y varios distractores absolutos. Se aplicó todo; los datos verificados (F1 en Bedrock, 0,21 USD por tarea humana, lotes −50 %, Priority +75 %, eventos de datos de CloudTrail, componentes de AgentCore, A2A, Transform) eran correctos.
- **Verificación:** validador sin avisos, cobertura 69/69, markdownlint, 25/25 diagramas, 228 tests y 39/39 comprobaciones de navegador; simulacro probado en la consola local.

### Seguimiento en issues

- Petición: «corrige todo lo que puedas, y deja issues por las cosas que hay que verificar para hacer el estudio por separado».
- Comprobado antes de abrir las issues: validador sin avisos, cobertura 69/69 y glosario sincronizado; no había nada más que corregir en el contenido.
- **Issues de verificación** (etiquetas `verificar` y `aif-c01`), una por tema, con qué verificar, qué dice cada fuente, dónde está el marcador, impacto y criterio de cierre (incluido cerrar como «no verificable» si AWS no lo aclara):
  - [#8](https://github.com/monghithub/certificaciones/issues/8) Amazon Q en la lista de servicios evaluables.
  - [#9](https://github.com/monghithub/certificaciones/issues/9) Lista *out of scope* (DeepComposer, IAM Identity Center, Marketplace, Organizations).
  - [#10](https://github.com/monghithub/certificaciones/issues/10) «using multiple comments».
  - [#11](https://github.com/monghithub/certificaciones/issues/11) Preentrenamiento continuado en Bedrock.
  - [#12](https://github.com/monghithub/certificaciones/issues/12) «task engineering».
- **Issues de decisión** (etiqueta `decision`): [#13](https://github.com/monghithub/certificaciones/issues/13) licencia, [#14](https://github.com/monghithub/certificaciones/issues/14) formato de `ordering`/`matching`, [#15](https://github.com/monghithub/certificaciones/issues/15) retirar los usuarios de prueba.
- [#16](https://github.com/monghithub/certificaciones/issues/16) publicar `aif-c01-v1.0.0`, con la lista de issues que la bloquean.
- Cada marcador enlaza su issue; `AGENTS.md` lo exige para los marcadores que no se resuelvan en la iteración.
- **Decisiones:** no se resuelven los marcadores por cuenta propia ni se cambia `LICENSE` (son decisiones del usuario); los usuarios de prueba no se borran sin su confirmación y las pruebas de navegador los usan.

### Licencia confirmada

- El usuario confirma MIT para el código y CC BY 4.0 para el contenido. `LICENSE` deja de estar pendiente de confirmación y su lista de directorios incluye ahora la consola (`app/`, `curso/`, `migrations/`, `Dockerfile`) y `docs/`. Se cierra la [issue #13](https://github.com/monghithub/certificaciones/issues/13).
- El titular sigue siendo «Contribuidores del curso AIF-C01», que se fijó como provisional en la iteración 0.

### Issue #8: Amazon Q

- Petición: «empezamos por la 8».
- Fuentes consultadas el 2026-10-16: lista de servicios *in scope* y *out of scope*, páginas de los dominios 1 y 2, página de revisiones y PDF completo de la guía v1.1 (publicada el 30 de abril de 2026).
- **Hallazgo nuevo:** la página de revisiones transcribe el objetivo 1.3.4 nuevo como «Amazon Bedrock, Amazon Q, Amazon Quick, Kiro, SageMaker AI», pero el objetivo vigente (HTML y PDF) dice «Amazon Bedrock, Amazon Quick, Kiro, SageMaker AI». La página de revisiones no coincide con la guía en ningún punto donde cita Amazon Q.
- **Decisión:** se sigue la parte normativa de la guía: Amazon Q no es evaluable. Se quita el marcador en `fuentes/servicios-alcance.md` y en `02/servicios.md` (queda una nota con la explicación) y se ajusta la nota del módulo 01. No cambia ninguna pregunta.

### Pendiente

- Lo que siguen las issues #9 a #12 y #14 a #16.
