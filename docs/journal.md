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

## 2026-10-17

### Repaso de conocimientos y estudio con los tests

- Peticiones: «base aws no tiene preguntas test???»; «la idea es revisar conocimientos y estudiar a base de los test, Puedes hacer mas test generales de conocimiento y deespues los propios de examenes? la idea es que ahciendo test se vayan quedando los conocimientos»; «quiero en cada test aunque sea de examen, que aprezca una opcion de explicacion de la pregunta una vez contestada, pregunta a pregunta».
- Rama `aif-c01/repaso`, cambio de OpenSpec `repaso-y-estudio`.
- **Hecho:**
  - Bancos `repaso.yaml` en los módulos 00 a 05 (210 preguntas, ≥ 2 por objetivo; el 00 con dominio 0 y tarea `CP`). Redactados a partir de la teoría ya verificada de cada módulo y revisados por un revisor independiente por módulo.
  - Consola: ruta de estudio en «Tests», «Repetir falladas», «Ver explicación» con enlace a la teoría en todos los tests, «Modo estudio» en el simulacro y «Conocimientos previos» en las estadísticas.
  - Validador, cobertura y `quiz.py` admiten los bancos de repaso; 17 pruebas nuevas (245 en total) y comprobaciones de navegador del repaso y del desplegable (50 en total).
- **Revisión independiente:** ningún hallazgo crítico. Importantes: tres distractores defendibles (R3-009, R3-011, R3-038), una explicación ambigua del ámbito de la Scoping Matrix (R5-029), respuestas que salían del enunciado (R5-030, R5-004), referencias poco pertinentes (R1-014, R1-015, R2-012, R2-013, R2-023, R3-017, R3-021, R3-027, R3-030, R4-013, R4-015, R4-030) y la opción correcta como la más larga en muchas preguntas (reequilibrado). Todo aplicado.
- **Decisiones:**
  - Fichero aparte (`repaso.yaml`) con el mismo esquema: los tests de examen y el simulacro no cambian.
  - Las respuestas de repaso cuentan en los aciertos por dominio y tarea; el dominio 0 aparece como «Conocimientos previos».
  - El modo estudio del simulacro se guarda en `filtro = "estudio"` para no migrar la base de datos.
  - La explicación va en un desplegable cerrado si se acierta y abierto si se falla.
  - R5-010 preguntaba por el RGPD, que no tiene fuente de AWS: se reformula sobre lo que consigue la seudonimización según el *Responsible AI Lens*.
  - Se añaden a las referencias de los módulos 02 y 03 las páginas de ingeniería de contexto y de *transfer learning* que citan las preguntas de repaso.
  - Se unifica el tuteo en los enunciados de examen de los módulos 01 a 03.

### Pendiente

- Lo que siguen las issues #9 a #12 y #14 a #16.

## 2026-11-18

### Despliegue en titan

- La consola se sirve en la red local desde `~/Sistema/aplicaciones/certificaciones` (clon de `main`, Docker Compose, Traefik: `cursos.titan`, `certificaciones.titan` y `:8093`). Detalle en el inventario de `Sistema`.

### Guía v1.2 y marcadores pendientes

- Petición: «que falta en el curso, puedes completarlo?».
- Rama `aif-c01/guia-1-2`. Al revisar las fuentes de las issues #9 a #12 apareció la **guía v1.2** (29 de octubre de 2026). Comparación automática objetivo a objetivo y servicio a servicio contra `fuentes/`: objetivos, conocimientos previos e *in scope* idénticos; solo cambia la lista *out of scope* (25 servicios fuera, uno renombrado). La página de revisiones solo menciona 6 de los 25.
- **Decisiones:**
  - #9 se da por resuelta: la contradicción era de la v1.1 y la lista v1.2 coincide con lo que anunciaba la página de revisiones.
  - #10 se resuelve con el blog oficial de AWS «Best Practices for Prompt Engineering with Amazon CodeWhisperer» (`aws.amazon.com`, fuente oficial del curso). La guía repite la misma pareja «specific and concise / multiple comments» de ese artículo.
  - #12 se cierra como «no verificable» (criterio de cierre de la issue): ninguna fuente de AWS usa el término.
  - #11 sigue abierta: la guía de Bedrock solo enumera tres métodos, mientras que la FAQ y la referencia de la API mantienen el preentrenamiento continuado.
- Este cambio no pasa por OpenSpec: es mantenimiento de fuentes y notas sin preguntas ni requisitos nuevos, como la issue #8.

### «Ponme a prueba» durante la lectura

- Petición: «me gustaría que en las pantallas de vez en cuando aparecieran un modal con alguna pregunta concreta tipo test de la página que estoy visitando. Pudiera cerrarla o si no la cierro me vaya haciendo cuestiones y vaya yo respondiendo hasta que me aburra y la cierre. Sobre todo de la página que esté en ese momento en la ventana del navegador».
- Rama `feat/pregunta-en-lectura`, cambio de OpenSpec `pregunta-en-lectura`, revisado y aprobado por el usuario antes de implementar.
- **Decisiones del usuario:** el modal solo se abre con el botón (sin temporizador); no se guarda nada; primero repaso y después examen del mismo apartado.
- **Decisiones de diseño:** el cliente calcula la cadena de anclas visibles y el servidor elige, sin estado (el cliente manda los ids ya vistos). Índice (módulo, ancla) → objetivos con todas las anclas del mapa de cobertura. Respuestas JSON pintadas con `textContent`, compatibles con la CSP. Las rutas exigen matrícula y CSRF y rechazan el simulacro.
- **Verificación:** 258 pruebas de pytest (13 nuevas). En navegador (Chromium headless contra la imagen de la rama): seis preguntas seguidas del apartado «Buenas prácticas de ingeniería de prompts» sin repetir (2 de repaso y 4 de examen), y luego del módulo; `Esc` y retorno del foco; «Repasar en la teoría» cierra y navega; sin botón en el simulacro; claro, oscuro y móvil; «Falladas (0)» tras fallar en el modal; sin errores de consola.

### Revisión de las dudas abiertas

- Petición: «revisa nuevamente los puntos donde hay dudas».
- **#11:** pruebas nuevas en la documentación de Bedrock: los modelos Titan Text no aparecen en la disponibilidad por regiones (solo los de *embeddings*), ni tienen ficha de modelo, ni están en la lista de *fine-tuning*. Sin aviso explícito de retirada. **Decisión del usuario:** dejarla abierta hasta que AWS lo diga de forma explícita. Se amplía el marcador.
- **#14:** el usuario confirma el formato de `ordering` y `matching`. Se quita de `AGENTS.md` la nota de pendiente y se cierra la issue.
- Hallazgo lateral: la página de ciclo de vida de Bedrock da Nova Canvas, Nova Reel y Nova Sonic v1 como retirados desde septiembre de 2026; el curso ya lo recoge en el módulo 02.

### Pendiente

- #11 (a la espera de AWS), #15 y publicación de la v1.0.0 (#16).

## 2026-11-19

### Acceso libre en red local (#15)

- Petición: «la 15 significa quitar el login de la consola. Dejarla libre para poder entrar ya que solo va a funcionar en el entorno local».
- Rama `feat/acceso-libre`, cambio de OpenSpec `acceso-libre`, aprobado por el usuario (usuario fijo: `admin`).
- **Decisiones:** opción por variable de entorno, desactivada por defecto, para no cambiar otros despliegues; usuario existente (no anónimo) para que el progreso y las matrículas sigan funcionando; la sesión se crea al vuelo y CSRF se mantiene; en titan solo es accesible por la LAN (Traefik `lan-only`).
- Riesgo aceptado por el usuario: cualquiera en la red local entra como `admin`.

### Diagramas de refuerzo

- Petición: «aquí por ejemplo puedes poner un diagrama dinámico para reforzar la idea, por favor revisa en el curso todos los sitios donde aplicaría un diagrama dinámico e interactivo».
- Rama `aif-c01/diagramas`, cambio de OpenSpec `diagramas-refuerzo`, aprobado por el usuario (los 19 propuestos).
- Revisión de los 33 apartados de teoría sin diagrama; descartados los que una tabla explica mejor, los que ya tienen un diagrama equivalente y los parámetros de inferencia (el orden en que se aplican depende del modelo).
- **Decisiones:** mismo sistema que los 25 existentes (Mermaid + `nodos`: animación, modal por caja, claro, oscuro y móvil); sin datos nuevos, cada caja resume el texto del apartado; cadenas largas en vertical por el móvil; títulos de subgrupo cortos (Mermaid corta los largos).
- **Revisión independiente:** 0 críticos, 4 importantes (orden del árbol de pago, que mandaba a On-Demand una carga interrumpible; orden de los criterios de elección de modelo; alcance de Guardrails frente al envenenamiento; RAG frente a no meter datos personales en el modelo) y 11 menores. Todo aplicado.
- **Verificación:** validador, 44/44 diagramas Mermaid válidos y navegador (todas las cajas abren su modal, sin errores de consola, claro, oscuro y móvil).

## 2026-11-20

### Alternativas en cada «cuándo no usar» (#26)

- Petición: «se debe dar más explicaciones; por ejemplo, en 00-base-aws/teoria, cuando se habla de Amazon S3 se dice que no debe usarse para bases de datos transaccionales: hay que indicar qué se debe usar en ese caso». El usuario pidió primero dejarlo anotado (issues #26 y #27) y después «dale».
- Rama `aif-c01/alternativas`. Mantenimiento de contenido sin requisitos nuevos de la consola, sin cambio de OpenSpec (como la guía v1.2); la regla queda en `AGENTS.md`.
- **Decisiones:** la alternativa, dentro del alcance si existe (EBS y EFS, que el examen no evalúa, solo se nombran); para productos cerrados, el sustituto oficial o la constancia de que AWS no lo indica, comprobado en sus avisos de disponibilidad (Audit Manager, A2I, Ground Truth); Clarify se mantiene como respuesta clásica del examen para sesgo y SHAP.
- **Revisión independiente:** 0 críticos; 5 importantes (lista incompleta de almacenes de Knowledge Bases, Bedrock Evaluations presentado como sustituto de Clarify en ML clásico, Trainium, filas de `05/servicios.md` sin trasladar, filas que seguían sin alternativa) y 7 menores. Todo aplicado.

### Mapa de servicios (#27)

- Petición: «necesito cuadro resumen de los servicios que hay en AWS con su logo, como apartado de revisión global para hacernos una idea de la foto global, y un diagrama de dónde se usa o se relaciona cada uno».
- Rama `feat/mapa-servicios`, cambio de OpenSpec `mapa-servicios`.
- **Decisiones del usuario:** subir los iconos al repositorio (excluidos de MIT y CC BY con una nota en `LICENSE`) y una página aparte del curso, no un módulo.
- **Iconos:** las condiciones de AWS permiten usar sus *Architecture Icons* en diagramas y materiales como presentaciones, pero no dan permiso explícito para redistribuir los ficheros; el paquete no trae licencia. Se usan sin modificar (paquete de julio de 2026, 54 ficheros de 48 px, 304 KB). Las funcionalidades llevan el icono de su servicio; Kiro, Strands Agents, Trainium, Inferentia, fmeval y AI Service Cards no tienen icono propio.
- **Diseño:** el cuadro se genera del glosario para que no se desactualice; la categoría y el alcance salen de `fuentes/servicios-alcance.md`, y los módulos, de los `servicios.md`. Los 51 servicios *in scope* ya tenían entrada en el glosario.
- **Lección de Mermaid:** dentro de un subgrupo, `direction TB` pone en fila las cajas sin enlaces y `direction LR` las apila; las flechas que cruzan subgrupos desordenan el diagrama: mejor enlazar subgrupos enteros y usar `~~~` para colocar un bloque.
- **Verificación:** 270 pruebas de pytest (6 nuevas), validador, 4/4 diagramas válidos y navegador (enlace en el menú, 80 filas en 13 grupos, iconos, filtro, modal, claro, oscuro y móvil, sin errores de consola).

### Revisión con las guías de estudio: módulo 00 (#31)

- Petición: «revisar tema por tema y confrontarlo con la información de los libros .md […] haz una issue por apartado del curso para ir capítulo a capítulo de la certificación en la web validando». Issues #31 a #37 (módulos 00 a 05 y, al final, simulacro, chuleta, glosario y mapa). Se empieza por el 00.
- Material: las dos guías de estudio de 2025 en Markdown y sus 201 preguntas de práctica, en titan y fuera del repositorio (`CLAUDE.local.md`). No se copia nada; cada dato se comprueba y se cita en `docs.aws.amazon.com` o `aws.amazon.com`.
- Rama `aif-c01/revision-libros-00`. Mantenimiento de contenido sin requisitos nuevos de la consola: sin cambio de OpenSpec (como #26).
- **Hallazgos para el 00** (Taulli, cap. 1 y 2; preguntas TAU-C2 y TAU-PE-1 a 6):

  | Tema | Estado antes | Qué se hizo |
  |---|---|---|
  | Qué es la nube y sus ventajas | Faltaba | Definición de AWS y las seis ventajas |
  | Modelos de despliegue (nube, híbrido, local) | Faltaba | Tabla con cuándo encaja cada uno |
  | IaaS, PaaS y SaaS | Faltaba (lo preguntan dos cuestionarios) | Tabla, diagrama anidado y relación con la responsabilidad compartida |
  | Zonas de disponibilidad, Local Zones y ubicaciones de borde | Solo había Regiones | Apartado «Infraestructura global» con diagrama |
  | Responsabilidad compartida | Faltaban el cifrado, los servicios abstraídos y los controles compartidos | Añadidos |
  | IAM | Faltaba Access Analyzer | Añadido |
  | Precios | Faltaban el aviso de Spot, Dedicated Hosts, los tipos de Savings Plans y Pricing Calculator | Añadidos; el glosario decía que Savings Plans era solo para EC2 |
  | Responsabilidad compartida básica, IAM, EC2, S3, Lambda | Ya cubierto | Sin cambios |

- **Discrepancias de los libros con la documentación vigente** (prevalece la documentación):
  - Uno de los libros dice que Amazon VPC permite lanzar recursos en las instalaciones del cliente: es AWS Outposts; VPC es una red virtual dentro de AWS.
  - Una zona de disponibilidad no es «varios» centros de datos, sino **uno o varios**.
  - Capa gratuita: los libros describen la de 12 meses; desde julio de 2025 son créditos y un plan gratuito de hasta seis meses (el curso ya lo recogía).
  - Ejemplos de SaaS de AWS que ya no sirven: Amazon Chime dejó de tener soporte el 20 de febrero de 2026 y la página de Amazon WorkDocs ya no existe. AWS no clasifica sus servicios como PaaS o SaaS: el curso usa la distinción oficial entre servicios de infraestructura y servicios abstraídos.
  - Los libros dan 36 Regiones o similares; la documentación consultada da 34 y la portada de AWS, 39. El curso no cita la cifra.
- **Verificación:** validador sin avisos, cobertura (CP 4/4, 33 de repaso), 270 pruebas de pytest y 7/7 diagramas Mermaid válidos.

### Banco local de preguntas de los libros

- Petición: «incluir más test en cada apartado en base a los test en español que existan en los documentos que he subido […] no revises si están repetidas sino añade las que hay en las revisiones de cada capítulo y aparte un test nuevo final con todas las preguntas que haya en los libros».
- **Decisión del usuario:** las preguntas de los libros tienen copyright y este repositorio es público, así que **solo viven en titan**, fuera de git, hasta que se resuelva la privacidad del repositorio. Aquí solo entra el soporte genérico de la consola.
- **Diseño:** `cursos/<curso>/modulos/<NN>/libros.yaml`, opcional e ignorado por git. Banco aparte (`banco: libros`), con validación mínima (no pasa por el esquema de las preguntas propias, que exige referencia oficial y explicación de cada distractor) y fuera del repaso, el examen, el mixto, el dominio y el simulacro. Sí entra en «Repetir falladas». En «Tests», apartado «Preguntas de los libros»: por módulo, con un número de preguntas o todas, y un test final con todas, sin el tope de 100.
- Los ficheros los genera un script que vive junto a los libros, fuera del repositorio. El preparado de las preguntas, su reparto por módulo y la clasificación por dominio del test inicial y del examen de práctica están en su propio journal.
- **Verificación:** 274 pruebas de pytest (4 nuevas), validador, cobertura y glosario sin cambios.

## 2026-11-21

### Revisión con las guías de estudio: módulo 01 (#32)

- Petición: «comienza con las revisiones». Segunda issue de la serie #31 a #37, con el mismo método que el módulo 00. Rama `aif-c01/revision-libros-01`, sin cambio de OpenSpec.
- Material: Elango, capítulos 1, 3, 4 (parte de IA y ML), 7 (métricas) y 8 (MLOps); Taulli, capítulos 3 y 5; y sus preguntas ELA-C1, C3, C4, C8, TAU-C3, C5 y las de ELA-AT y TAU-PE del dominio 1. No se copia nada; cada dato se comprueba y se cita en `docs.aws.amazon.com` o `aws.amazon.com`.
- **Hallazgos por objetivo** (teoría):

  | Objetivo | Tema | Estado antes | Qué se hizo |
  |---|---|---|---|
  | 1.1.1 | Característica y etiqueta; parámetro frente a hiperparámetro | Faltaba | Definiciones y ajuste automático de modelos |
  | 1.1.1 | Cómo se corrige el sobreajuste o el subajuste; generalización | Solo se detectaba | Técnicas (más datos, *early stopping*, regularización, *pruning*, *ensembling*) |
  | 1.1.1 | No toda la IA es ML | Implícito | Una frase (sistemas de reglas) |
  | 1.1.2 | ML clásico frente a aprendizaje profundo (datos, características, cómputo, interpretabilidad) | Faltaba | Tabla |
  | 1.1.2 | CNN, RNN y *transformer* | Faltaba | Tabla para reconocerlas |
  | 1.1.4 | Datos semiestructurados; entrenamiento, validación y prueba; alta dimensionalidad | Faltaba | Añadidos |
  | 1.1.5 | Semisupervisado y aprendizaje por transferencia | Faltaba | Añadidos, con trampa frente a no supervisado |
  | 1.1.5 / 1.2.3 | Algoritmos integrados (k-means, k-NN, XGBoost, Linear Learner, Random Cut Forest, PCA) | Faltaba | Tabla y trampa «la k engaña» |
  | 1.2.2 | Objetivo no medible, datos malos o sin derecho de uso, explicabilidad obligatoria; RPA frente a IA | Parcial | Tres viñetas y nota sobre RPA |
  | 1.2.4 | IDP; clasificación, detección y segmentación de imágenes | Faltaba | Fila de IDP y tabla de tareas de visión |
  | 1.2.5 | Funcionalidades que deciden (diarización, vocabulario y PII de Transcribe, terminología de Translate, análisis de documentos de Textract, Face Liveness, motores de Polly, intenciones y ranuras de Lex) | Faltaba | Tabla |
  | 1.2.5 | SageMaker Studio, Data Wrangler, Feature Store, ajuste automático | Faltaba | Filas en capacidades de SageMaker AI |
  | 1.3.1 | KPI; pasos del procesamiento de datos (recogida, preparación, EDA, ingeniería de características) | Parcial | Desglose |
  | 1.3.1 / 1.3.5 | Deriva de datos frente a deriva de concepto | Solo «deriva» | Tabla con ejemplo y cómo se detecta |
  | 1.3.4 | Feature Store, Data Wrangler, Cost Explorer, Budgets y Quick por etapa | Faltaba | Filas nuevas |
  | 1.3.5 | Despliegue seguro: azul/verde (todo a la vez, canario, lineal), *rolling*, prueba en sombra; CI/CD e IaC; MLflow y Model Registry | Faltaba | Tabla, diagrama nuevo y trampa «sombra no es A/B» |
  | 1.3.6 | Errores de tipo I y II; matriz de confusión multiclase; MSE, RMSE, MAE y R² con ejemplo; implicación de usuarios y desglose del ROI | Parcial | Añadidos |
  | 1.1.3, 1.2.1, 1.2.6, 1.3.2, 1.3.3 | Inferencia, valor de la IA, ML frente a FM, origen de los modelos, API gestionada o autoalojada | Ya cubierto | Sin cambios |

- **Preguntas de los libros:** de 68 revisadas, 30 ya estaban cubiertas en concepto y trampa, 18 tenían el concepto pero no la trampa y 20 no estaban cubiertas (4 de ellas son de los dominios 2 o 3 y se dejan para su módulo). Los huecos se cubren con 16 preguntas de repaso (R1-043 a R1-058) y 17 de examen (D1-083 a D1-099), todas propias. Quedan fuera, por prioridad baja o fuera del alcance: lematización y *stopwords*, *endpoints* multimodelo y MLOps frente a LLMOps.
- **Discrepancias de los libros con la documentación vigente** (prevalece la documentación):
  - Presentan como vigentes servicios que ya no admiten clientes nuevos: Amazon Forecast (desde el 29 de julio de 2024; AWS remite a SageMaker Canvas), Amazon Fraud Detector (desde el 7 de noviembre de 2025), Amazon Kendra (AWS remite a Bedrock Knowledge Bases), SageMaker Studio Lab y el modelado de temas y la detección de eventos de Comprehend. También Model Monitor, Clarify, Ground Truth y Experiments, ya avisados en el curso. Clarify y Ground Truth constan además como servicios en mantenimiento desde el 30 de junio de 2026.
  - Data Wrangler está hoy dentro de SageMaker Canvas, y QuickSight forma parte de Amazon Quick.
  - Uno de los libros asocia la inferencia asíncrona a las series temporales: la asíncrona se define por el tamaño de la carga y la duración, no por el tipo de dato.
  - Uno de los libros dice que Model Monitor detecta la deriva «en tiempo real»: funciona con trabajos programados.
  - Un ejemplo de MSE de un libro tiene un error aritmético; el curso usa un ejemplo propio.
  - Para el fraude, un libro prioriza la precisión y el otro F1; el curso mantiene su criterio (F1 si pesan los dos errores, la métrica según el error más caro).
  - Algunas tablas de un libro presentan k-NN como agrupamiento: es supervisado. Se aprovecha como trampa.
- **Revisión independiente:** 3 hallazgos críticos (tres preguntas de examen demasiado próximas a preguntas de los libros: se reescribieron con otro escenario, otra restricción y otros distractores), 11 importantes (otras preguntas y tres trampas derivadas de distractores de los libros, fuentes que no respaldaban la deriva de concepto, la cifra de transformaciones de Data Wrangler o los errores de tipo I y II, repaso que adelantaba escenarios del examen, una pista en un enunciado, dificultades mal calibradas y matices sobre Kendra y el sobreajuste) y 4 menores. Todos aplicados; la deriva de concepto se cita ahora en AWS Prescriptive Guidance, la matriz de confusión en SageMaker Canvas, y se añaden AnalyzeExpense y AnalyzeID de Textract.
- **Verificación:** validador sin avisos, cobertura (1.1: 25 preguntas y 20 de repaso; 1.2: 38 y 18; 1.3: 36 y 20), 274 pruebas de pytest, 47/47 diagramas Mermaid válidos y glosario regenerado (271 términos, 23 nuevos).

### Revisión con las guías de estudio: módulo 02 (#33)

- Petición: «cuando termine abre el PR y sigue con la 33». PR #41 abierto para el módulo 01. Rama `aif-c01/revision-libros-02`, creada a partir de la del 01 para no chocar en el glosario, el journal y el CHANGELOG mientras #41 no se fusione.
- Material: Elango, capítulos 2, 3 y 4 (parte de IA generativa), 5 (selección de modelos) y 8 (ciclo de vida del modelo fundacional); Taulli, capítulos 4 y 6; y sus preguntas ELA-C2, ELA-C4 (IA generativa), TAU-C4, TAU-C6 y las de ELA-AT y TAU-PE del dominio 2 (estas están en el banco local del simulacro).
- El módulo ya cubría casi todo y estaba más al día que los libros (niveles Priority, Flex y Reserved, AgentCore, Quick, Kiro, MCP y A2A). **Hallazgos por objetivo:**

  | Objetivo | Tema | Estado antes | Qué se hizo |
  |---|---|---|---|
  | 2.1.1 | Familias generativas: GAN y VAE, además de *transformer* y difusión | Faltaba | Tabla y trampa (texto a imagen hoy es difusión) |
  | 2.1.3 | Ciclo de vida de los modelos de Bedrock (activo, *legacy*, fin de vida) | Solo el caso Nova | Párrafo y trampa |
  | 2.1.4 | Razonamiento (más *tokens* de salida), imagen por imagen y vídeo por segundo, «abierto no es gratis» | Faltaba | Tres viñetas |
  | 2.2.2 | Causa de las alucinaciones; riesgo de reputación | Parcial | Frase y fila nueva |
  | 2.2.3 | Tiempo hasta el primer *token* frente a tiempo total; ficha del modelo; *benchmarks* frente a datos propios | Faltaba | Párrafo y reglas |
  | 2.2.4 | Eficiencia de negocio frente a técnica; satisfacción del cliente | Parcial | Aclaración |
  | 2.3.1 | Bedrock Marketplace, Custom Model Import, Bedrock Data Automation; JumpStart sin coste adicional y con evaluación | Faltaba | Filas en la tabla y en `servicios.md` |
  | 2.3.3 | Sostenibilidad: silicio eficiente (Trainium) | Faltaba | Frase con la referencia del Machine Learning Lens |
  | 2.3.4 | Modelos personalizados e importados bajo demanda; Marketplace por instancia; Guardrails y Knowledge Bases aparte; «producción no implica *Provisioned Throughput*» | Faltaba | Viñetas y nota |
  | 2.1.2, 2.1.5, 2.1.6, 2.2.1, 2.3.2 | Casos de uso, ingeniería de contexto, IA agéntica, ventajas | Ya cubierto | Sin cambios |

- **Preguntas de los libros:** de 42 revisadas, 18 ya estaban cubiertas, 11 tenían el concepto pero no la trampa, 3 no estaban cubiertas y 10 son del dominio 3 (cubiertas en el módulo 03). Se añaden 10 preguntas de repaso (R2-037 a R2-046) y 10 de examen (D2-082 a D2-091), propias. Se descartan, por no encontrar fuente oficial de AWS que las respalde, la codificación posicional y el codificador y decodificador del *transformer*.
- **Discrepancias de los libros con la documentación vigente** (prevalece la documentación):
  - Uno de los libros define *chunking* como agrupar *tokens* en frases; en AWS es partir documentos antes de generar sus *embeddings*.
  - Generar imágenes a partir de texto: un libro da GAN; la familia que se usa hoy es la difusión.
  - Un libro dice que los modelos fundacionales se preentrenan de forma «semisupervisada»; AWS dice autosupervisada.
  - Ambos libros asocian modelo personalizado con *Provisioned Throughput* obligatorio y producción con *Provisioned Throughput*; hoy hay inferencia bajo demanda en modelos compatibles y Custom Model Import, y los niveles Priority, Flex y Reserved.
  - Precios por cada 1 000 *tokens*: AWS publica hoy por millón.
  - Amazon Q Business y Q Developer, Agents for Amazon Bedrock y QuickSight aparecen como vigentes (el curso ya lo trataba). El acceso a modelos ya no requiere solicitarlo modelo a modelo.
  - Un libro propone ajuste fino o bajar la temperatura contra las alucinaciones; el curso mantiene RAG, anclaje con Guardrails y verificación.
- **Revisión independiente:** 2 hallazgos críticos (una pregunta de examen cuya respuesta no respaldaba la fuente citada y una de repaso demasiado próxima a una de los libros: se reescribieron), 10 importantes (el ciclo de vida de Bedrock tiene dos políticas según la fecha de lanzamiento del modelo, con acceso ampliado más caro en los anteriores; el 25 % de Trainium es un ejemplo concreto de AWS; Marketplace cobra además el software del proveedor; la facturación de vídeo por segundo no se pudo verificar y se retiró; ejemplos y escenarios demasiado próximos a los libros; repaso que adelantaba el examen; distractores débiles y respuestas que destacaban por su forma) y 4 menores. Todos aplicados.
- **Verificación:** validador sin avisos, cobertura (2.1: 36 preguntas y 20 de repaso; 2.2: 25 y 12; 2.3: 30 y 14), 274 pruebas, 47/47 diagramas, markdownlint sin errores y glosario regenerado (278 términos, 7 nuevos).

### Revisión con las guías de estudio: módulo 03 (#34)

- Petición: «continúa tú solo de forma autónoma todo lo que puedas hacer sin preguntar nada». Se siguen las issues #34 a #37 con el mismo método, un PR por issue. Rama `aif-c01/revision-libros-03`, creada a partir de la del 02.
- Material: Elango, capítulos 5, 6 y 7; Taulli, capítulos 6 y 7; y sus preguntas ELA-C5, ELA-C6, ELA-C7, TAU-C6, TAU-C7 y las de ELA-AT y TAU-PE del dominio 3.
- El módulo ya cubría los 19 objetivos con más detalle y más al día que los libros. **Hallazgos:**

  | Objetivo | Tema | Estado antes | Qué se hizo |
  |---|---|---|---|
  | 3.1.2 | Semilla (*seed*) de los modelos de imagen | Faltaba | Párrafo |
  | 3.1.3 | `Retrieve` frente a `RetrieveAndGenerate`; filtros por metadatos | Solo la idea | Párrafo con las dos operaciones |
  | 3.1.3 | Análisis de documentos: inteligente y automático en la Managed Knowledge Base; por defecto, Bedrock Data Automation o modelo fundacional en la *customer-managed* | Faltaba | Párrafo, tabla y diagnóstico típico (tablas ignoradas) |
  | 3.1.6 | Piezas de Bedrock Agents *Classic* (grupos de acciones, Knowledge Base, versión y alias, traza) y colaboración multiagente con supervisor | Faltaba | Tabla y trampa de papeles (la Knowledge Base guarda, el agente actúa) |
  | 3.2.3 | Modalidades de Guardrails: Classic (inglés, francés y español) frente a Standard (más idiomas, inferencia entre Regiones) | Faltaba | Párrafo, trampa y preguntas |
  | 3.2.4 | Exposición frente a inyección | Parcial | Trampa |
  | 3.4.5 | Medir la satisfacción con el análisis de sentimiento de Amazon Comprehend | Faltaba | Párrafo |
  | 3.3.1 | Preentrenamiento continuado en Bedrock (#11) | Marcador | Nueva consulta sin cambios; comentario en #11 |
  | Resto | Selección, parámetros, RAG, bases vectoriales, *prompts*, ajuste fino, evaluación | Ya cubierto | Sin cambios |

- **Preguntas de los libros:** de 50 revisadas, 24 ya estaban cubiertas, 18 tenían el concepto pero no la trampa y 8 no estaban cubiertas. Se añaden 7 preguntas de repaso (R3-045 a R3-051) y 7 de examen (D3-095 a D3-101), propias. Se descartan, por no encontrar fuente oficial de AWS: el coste total de propiedad como criterio de selección, el olvido catastrófico, el *red teaming*, las preguntas tendenciosas como mala práctica y la recomendación de no ajustar a la vez temperatura y top-p.
- **Discrepancias de los libros con la documentación vigente** (prevalece la documentación):
  - Presentan el preentrenamiento continuado como disponible en Bedrock (ver #11) y Agents for Amazon Bedrock como opción para proyectos nuevos (hoy *Classic*, sin clientes nuevos).
  - Un libro llama «máximo de *tokens*» a la ventana de contexto.
  - Un libro sitúa la temperatura hasta 2,0 y da rangos «recomendados» de top-p; los rangos dependen del modelo.
  - Un libro recomienda bajar la temperatura contra las alucinaciones y SageMaker Clarify y Model Monitor para evaluar (cerrados a clientes nuevos).
  - Un libro presenta el modelo destilado como apto para dispositivos en el borde; el de Bedrock se sirve en Bedrock.
  - Una pregunta de un libro tiene la clave contradictoria con su explicación (parámetros de muestreo y tamaño del modelo); otra da preentrenamiento continuado donde el enunciado describe aprendizaje por transferencia.
  - El acceso a los modelos ya no se solicita modelo a modelo.
- **Revisión independiente:** 1 hallazgo crítico (la tabla de analizadores solo vale para la *customer-managed* Knowledge Base; la gestionada usa siempre su análisis inteligente: corregidos teoría, glosario y dos preguntas), 7 importantes (la ampliación de «exposición» a los datos de entrenamiento no tenía fuente oficial y se retiró; una pregunta de modos de inferencia en un objetivo de coste de personalización, sustituida por una de destilación; las modalidades de Guardrails no estaban en la teoría; pistas de forma en dos preguntas; un alias del glosario que chocaba con la evaluación de RAG; y una mención a los libros en la nota de #11, retirada) y 6 menores. Aplicados todos salvo el de no titular secciones «Revisión con las guías de estudio» en las referencias de los módulos 01 y 02, que se deja como en el módulo 00 (el journal ya documenta la revisión).
- **Verificación:** validador sin avisos, cobertura (3.1: 37 preguntas y 21 de repaso; 3.2: 24 y 12; 3.3: 16 y 7; 3.4: 24 y 11), 274 pruebas, 47/47 diagramas, markdownlint sin errores y glosario regenerado (281 términos, 3 nuevos).

### Revisión con las guías de estudio: módulo 04 (#35)

- Rama `aif-c01/revision-libros-04`, a partir de la del 03. Material: Elango, capítulo 9; Taulli, capítulo 8; preguntas ELA-C9, TAU-C8 y las de ELA-AT y TAU-PE del dominio 4. Desde esta issue se trabaja en paralelo: el análisis de los módulos 04 y 05 y de la #37 se lanzó a la vez.
- El módulo ya cubría los 11 objetivos y estaba más al día que los libros. **Hallazgos:**

  | Objetivo | Tema | Estado antes | Qué se hizo |
  |---|---|---|---|
  | 4.1.5 | Reequilibrar un conjunto (sobremuestreo, submuestreo, SMOTE con *Balance data* de Canvas) | Faltaba | Párrafo |
  | 4.1.6 | Parada temprana y regularización contra el sobreajuste | Parcial | Ampliado |
  | 4.1.7 | Los cuatro tipos de Model Monitor (calidad de datos y del modelo, deriva del sesgo y de la atribución) | Parcial | Párrafo con el sustituto para proyectos nuevos |
  | 4.1.7 | A2I: flujos integrados para Textract y Rekognition (umbral de confianza o muestreo aleatorio) frente a Ground Truth | Una fila | Párrafo y trampa |
  | 4.2.2 | Model Registry frente a Model Cards | De pasada | Fila en la tabla y trampa |
  | 4.2.4 | RLHF como alineamiento con valoraciones humanas | Faltaba | Frase con remisión al módulo 03 |
  | Resto | Rasgos, Guardrails, riesgos legales, sesgo, transparencia, compromisos, diseño centrado en las personas | Ya cubierto | Sin cambios |

- **Preguntas de los libros:** de 20 revisadas, 11 ya estaban cubiertas, 8 tenían el concepto pero no la trampa y 1 era de otro dominio (RLHF, cubierta en el 03). Se añaden 5 preguntas de repaso (R4-035 a R4-039) y 5 de examen (D4-076 a D4-080). Se descartan, sin fuente oficial de AWS: los principios de diseño centrado en las personas de un curso de formación, las explicaciones contrafactuales y la elección de Región por su huella de carbono (la página del pilar de sostenibilidad se marca como solo de referencia histórica).
- **Discrepancias de los libros con la documentación vigente:** presentan Clarify, Model Monitor, A2I y Ground Truth como vigentes para cualquier cliente; uno atribuye a Clarify la deriva de la calidad de los datos (es Model Monitor); uno da a entender que Automated Reasoning checks evita errores (solo detecta y solo admite inglés de EE. UU.); y una pregunta tiene opciones que no encajan con el enunciado.
- **Revisión independiente:** 0 críticos, 12 importantes (una pregunta de examen casi igual a otra existente y otra de repaso que repetía una anterior, rehechas; pistas en enunciados y respuestas que destacaban por su forma; repaso que adelantaba el examen; la lista de integraciones de A2I exageraba lo que dice AWS; RLHF colocado como principio de la guía; trampas sin el sustituto de los servicios cerrados) y 5 menores. Todos aplicados.
- **Verificación:** validador sin avisos, cobertura (4.1: 53 preguntas y 29 de repaso; 4.2: 27 y 10), 274 pruebas, markdownlint sin errores y glosario regenerado (284 términos, 3 nuevos).

### Revisión con las guías de estudio: módulo 05 (#36)

- Rama `aif-c01/revision-libros-05`, a partir de la del 04. Material: Elango, capítulo 10; Taulli, capítulo 9; preguntas ELA-C10, TAU-C9, ELA-AT-18 y TAU-PE-47 a 54.
- El módulo ya cubría los 8 objetivos con más detalle que los libros. **Hallazgos:**

  | Objetivo | Tema | Estado antes | Qué se hizo |
  |---|---|---|---|
  | 5.1.1 | *Endpoints* FIPS de Bedrock | Faltaba | Fila y entrada de glosario |
  | 5.1.1 / 5.1.3 | Dónde detectar datos personales: Macie (S3), Comprehend (texto de la aplicación), Guardrails (entradas y salidas del modelo) | Parcial | Filas en la tabla de decisión y trampa |
  | 5.1.4 | Defensa en profundidad (enfoque por capas del pilar de seguridad) | Faltaba | Párrafo |
  | 5.2.1 | Normativas (HIPAA, PCI DSS, RGPD, SOC e ISO) y qué hace el cliente en cada una; BAA y documentos de ISV en Artifact | Faltaba | Tabla y trampas |
  | 5.2.2 | Soberanía frente a residencia de los datos | Faltaba | Fila en la tabla de gobierno de datos |
  | 5.2.3 | Qué controla el cliente en cada ámbito de la AI Security Scoping Matrix | Parcial | Párrafo con las descripciones de la matriz |
  | Resto | Servicios de protección, citación, ingeniería de datos segura, alucinaciones, servicios de gobierno, procesos | Ya cubierto | Sin cambios |

- **Preguntas de los libros:** de 21 revisadas, 8 ya estaban cubiertas, 4 tenían el concepto pero no la trampa y 9 no estaban cubiertas (4 de ellas sobre servicios fuera de alcance o con un enunciado ambiguo). Se añaden 5 preguntas de repaso (R5-031 a R5-035) y 5 de examen (D5-070 a D5-074). Se descartan, sin fuente oficial de AWS: MITRE ATLAS, los ataques adversarios de evasión o de extracción del modelo y la definición de «carga de trabajo regulada».
- **Discrepancias de los libros con la documentación vigente:** presentan Audit Manager como vigente; uno da Shield, WAF, Cognito, GuardDuty y Security Hub como herramientas centrales (fuera de alcance); uno atribuye a Cognito los límites de peticiones; uno afirma que Bedrock no guarda nada de los *prompts* (depende del registro de invocaciones que active el cliente y de la detección de abusos de cada modelo); y una pregunta tiene dos opciones casi equivalentes.
- **Revisión independiente:** 2 críticos (una pregunta de repaso demasiado próxima a una de un libro y una de examen que duplicaba otra y afirmaba algo sobre soberanía que su referencia no respalda: reescritas, la segunda sobre *endpoints* FIPS), 9 importantes (otra pregunta de repaso con las opciones de un libro, afirmaciones sobre la matriz y sobre la soberanía sin respaldo, una definición de «carga regulada» retirada, una respuesta discutible, pistas y repaso que adelantaba el examen, y la entrada de glosario de FIPS que faltaba) y 4 menores. Todos aplicados.
- **Verificación:** validador sin avisos, cobertura (5.1: 45 preguntas y 21 de repaso; 5.2: 29 y 14), 274 pruebas, markdownlint sin errores y glosario regenerado (291 términos, 7 nuevos).

### Revisión con las guías de estudio: simulacro, chuleta, glosario y mapa (#37)

- Rama `aif-c01/revision-libros-06`, a partir de la del 05 y en un *worktree* aparte (`~/Cursos/certificaciones-06`) para trabajar en paralelo mientras se revisaba el módulo 05. La issue pedía hacerla cuando estuvieran cerradas las de los módulos; se hace al final de la cadena de PR, que depende de todas ellas.
- **Formato del examen:** la guía vigente (v1.2, 29 de octubre de 2026) solo enumera preguntas de **opción múltiple** y de **respuesta múltiple**; el anuncio de AWS de 2024 y algunas copias de la guía incluyen también ordenación y emparejamiento. Abierta la [issue #45](https://github.com/monghithub/certificaciones/issues/45) (`verificar`) para que el responsable decida si el simulacro y `curso.yaml` se adaptan; mientras tanto, la chuleta, el README del curso y el del simulacro citan la guía vigente y presentan la ordenación y el emparejamiento como práctica del curso. Verificados también: 65 preguntas (50 puntúan), 90 minutos, 100–1.000 con aprobado en 700, sin penalización, puntuación compensatoria, 100 USD, Pearson VUE presencial o en línea, español de España entre los idiomas y validez de 3 años.
- **Simulacro:** el reparto por dominio coincide con los pesos oficiales (13/16/18/9/9) y las 14 tareas tienen preguntas. Por tipos sobra opción múltiple y faltan unas 3 de respuesta múltiple respecto a `curso.yaml`, y 11 objetivos no tienen ninguna pregunta (1.1.3, 1.2.2, 1.2.3, 1.3.2, 1.3.4, 2.1.3, 2.3.3, 3.2.5, 3.4.5, 4.1.7 y 4.2.2). No se cambia hasta resolver #45, porque el reparto por tipos depende de esa decisión. Los conceptos que preguntan los tests de los libros y no estaban en ningún módulo eran dos: el preprocesamiento de texto (añadido al módulo 01) y la «carga de trabajo regulada» (sin fuente oficial).
- **Chuleta:** formato del examen corregido y ampliado (tipos según la guía vigente, puntuación compensatoria, precio, modalidades, idiomas y validez), una línea de estrategia basada en el propio curso (ritmo y restricción que decide) y recordatorios de lo añadido en esta revisión (D1 a D5). La posibilidad de marcar preguntas para revisarlas no aparece en la guía y no se incluye.
- **Glosario:** 6 términos nuevos con fuente oficial (gobierno de datos, regularización, codificador y decodificador, PCA, preprocesamiento de texto y SageMaker Model Dashboard) y alias nuevos («alta varianza», «alto sesgo», «ajuste de hiperparámetros»). Se descartan, sin fuente oficial de AWS: capacidades emergentes, modelos de lenguaje pequeños (SLM) y *red teaming*. El codificador, el decodificador y la codificación posicional, que en la revisión del módulo 02 se descartaron por falta de fuente, se añaden ahora al módulo 02 con la página «What are transformers» de AWS.
- **Revisión independiente:** 0 críticos, 3 importantes (el README del curso y el del simulacro contradecían a la chuleta sobre los tipos de pregunta; el párrafo de estrategia seguía de cerca el orden y los ejemplos de una de las guías de estudio y se rehízo con el material propio del curso; y un alias de PCA, «reducción de dimensiones», tenía un sentido más amplio en el módulo 01) y 6 menores. Todos aplicados.
- **Mapa de servicios:** su cuadro resumen se genera desde el glosario, así que ya incluye los servicios nuevos de la serie (Feature Store, Data Wrangler, Studio, Model Dashboard, Bedrock Marketplace, Custom Model Import, Data Automation y los cerrados a clientes nuevos, en «otros»). Los diagramas no necesitan cambios.

### Fusión de la serie y simulacro con los tipos de la guía v1.2 (#45)

- Petición: «hazlo todo» (fusionar los PR, resolver #45, desplegar y #40).
- **Fusión:** PR #41, #42, #43, #44, #46 y #47 fusionados en orden en `main` con la CI en verde; issues #32 a #37 cerradas. Al borrar la rama de #41, GitHub cerró #42 en lugar de cambiar su base: se restauró la rama, se reabrió #42 y, para el resto, se cambió la base a `main` con la API antes de fusionar (`gh pr edit` falla por la retirada de Projects classic). Ramas borradas al final.
- **Despliegue en titan:** `./desplegar.sh --solo-cursos` y reinicio del contenedor; versión `bc22e29`, consola sana y glosario con los términos nuevos.
- **Decisión sobre #45** (tomada al pedir el usuario que se hiciera todo): prevalece la guía oficial, así que el **simulacro** usa solo opción múltiple y respuesta múltiple, mientras que los **bancos de los módulos** mantienen la ordenación y el emparejamiento como práctica. Cambio de OpenSpec `simulacro-formato-v12`: `examen.tipos` y `examen.distribucion` en el manifiesto, error del validador si el simulacro usa otro tipo, 11 preguntas del simulacro sustituidas sobre los mismos objetivos (queda en 51 de opción múltiple y 14 de respuesta múltiple, con el mismo reparto por dominio y dificultad) y textos actualizados. Una prueba de la consola que quitaba el bloque `examen` con un reemplazo de texto pasa a hacerlo leyendo el YAML.
- El PR se deja **sin fusionar** para la revisión humana que pide el flujo de OpenSpec; al aprobarlo se archiva el cambio y se cierra #45.
- **Sigue pendiente:** los 11 objetivos sin pregunta en el simulacro (ver la entrada de #37).

### Propuesta: «Preguntar a Claude» en los tests (OpenSpec `consultas-claude`)

- Petición: «que en los exámenes se pudieran hacer preguntas a la IA que resolviera en background o cuando pudiera usando una sesión en segundo plano de Claude Code con esta cuenta […] en el propio navegador en modo conversación».
- **Decisiones del usuario:** en todos los tests y siempre (también antes de responder y en el simulacro cronometrado); modelo Sonnet; solo `admin`; fuentes: teoría del curso, documentación oficial de AWS y libros en Markdown.
- **Diseño:** cola en la base de datos de la consola, API interna con token y un trabajador en el anfitrión que llama a `claude -p` (con `--resume` para seguir la conversación) y solo usa herramientas de lectura y búsqueda. Comprobado en titan: la salida JSON trae `result` y `session_id`, y `--resume` solo encuentra la sesión si se lanza desde el mismo directorio de trabajo.
- No se implementa en esta sesión: el usuario pidió dejarlo «perfectamente indicado» para que lo desarrolle otra IA. Todo está en `openspec/changes/consultas-claude/` (guía de implementación en `design.md`, tareas en `tasks.md`) y en la issue de seguimiento.

### Implementación: «Preguntar a Claude» en los tests (#40)

- Rama `feat/consultas-claude` (en el *worktree* `~/Cursos/certificaciones-40`), tareas 1 y 2 de `openspec/changes/consultas-claude/tasks.md`. Lo hace otra IA a partir de la guía de `design.md`; el despliegue en titan (tarea 3.4) y el inventario de `~/Sistema` (3.5) quedan para quien lo encargó.
- **Consola:** `CONSULTAS_TOKEN` en `Settings` (mínimo 32 caracteres; sin él no se registran las rutas), modelos `Consulta` y `ConsultaMensaje` con la migración `0003`, `app/routes/consultas.py` (panel htmx, envío, «Reintentar», «Mis dudas» y conversación; solo `admin`, con CSRF) y la API interna con `Authorization: Bearer` (404 sin el token correcto). Panel en `pregunta.html` (todos los modos, antes y después de responder) y plegado en `resultado.html`; enlace «Mis dudas» en la cabecera.
- **Trabajador:** `scripts/consultas_trabajador.py` (biblioteca estándar) y la unidad `scripts/consultas-claude.service`. Prueba real única en titan de `claude -p … --model sonnet --output-format json --tools … --allowedTools … --add-dir …`: `permission_denials` vacío, sin pedir permisos, con `result`, `session_id`, `total_cost_usd` e `is_error`. Las pruebas usan un `claude` simulado.
- **Ajustes sobre el diseño:**
  - `consulta_mensaje` lleva además `actualizado`, porque la recuperación de los «procesando» de más de 15 minutos necesita la hora del último cambio de estado.
  - El sondeo cada 5 s se hace sobre un fragmento aparte con solo la conversación (`GET …/consultas/<pid>/mensajes`), no sobre el panel entero, para no borrar lo que se esté escribiendo en el formulario.
  - `reintentar` acepta `"contar": false`: la cuota agotada no gasta intentos (si no, tras tres esperas la duda acabaría en error). La respuesta de `siguiente` incluye `intentos`.
  - Se pasa también `--allowedTools` con las mismas herramientas, para que `WebFetch` y `WebSearch` no se denieguen en `-p`.
  - Los mensajes siguientes (`--resume`) añaden una nota con la respuesta del estudiante y la solución si ya ha respondido, para que Claude pueda comentarla aunque la primera duda fuera antes de responder.
  - La solución se incluye en el primer *prompt* sin haber respondido solo si la duda la pide de forma explícita («solución», «respuesta correcta», «cuál es la respuesta»…); un «¿cuál es la diferencia…?» no cuenta.
  - Las instrucciones fijas añaden «Escribe en Markdown, con los enlaces en formato [texto](URL)», porque la consola no convierte en enlaces las URL sueltas.
  - En `app.js`, los fragmentos del panel no relanzan la inicialización de la página (el sondeo reiniciaba el cronómetro del simulacro).
- **Verificación:** 304 pruebas de pytest (30 nuevas), validador, cobertura y glosario sin cambios, markdownlint sin errores e imagen Docker construida.
- **Revisión de seguridad independiente del PR #49** (2 críticos, 3 importantes y 8 menores), todo aplicado:
  - Críticos: `--allowedTools Read,Grep,Glob` sin rutas dejaba leer cualquier fichero del usuario (`~/.ssh`, `~/.claude`, el `.env` de la consola, la base de datos). Ahora `claude` va con `--restricted` (sin ajustes, permisos ni *plugins* del usuario y con las herramientas de ficheros confinadas a los directorios de trabajo), `--strict-mcp-config`, `--permission-mode dontAsk`, reglas con ruta absoluta (`Read(//…/cursos/<curso>/**)`, libros), `WebFetch(domain:docs.aws.amazon.com)` y `aws.amazon.com`, y `--disallowedTools` para `~/.ssh`, `~/.claude`, `~/.config`, `.env` y `data/`. Comprobado en `claude --help` qué opciones existen (no hay que inventar ninguna) y con una llamada real: lee `curso.yaml` y la lectura de `~/.ssh/known_hosts` queda en `permission_denials`. La unidad ya no carga el `.env` de la consola (con `SECRET_KEY`): usa `~/.config/consultas-claude.env` (600) solo con el token, y `claude` recibe un entorno mínimo (`HOME`, `PATH`, `LANG`, `USER`, `XDG_RUNTIME_DIR`).
  - Importantes: las imágenes Markdown se desactivan (quedan como enlace; la CSP ya era `img-src 'self' data:`); topes de 3 dudas en espera y 30 al día por usuario, y de gasto diario en el trabajador (`CONSULTAS_COSTE_DIARIO`, 5 USD, persistido en `gasto.json`) que pausa hasta el día siguiente; patrón de cuota preciso (*usage limit*, *rate limit*, *limit reached*, *overloaded*, 429, 529) con tope de repartos (`CONSULTAS_MAX_CUOTA`).
  - Menores: reparto atómico (`UPDATE … WHERE` y reintento si no cambia ninguna fila); `consulta_mensaje.repartos` y número de reparto obligatorio en `respuesta`, `reintentar` y `error` (solo en «procesando»); conversación creada a la vez en dos peticiones (`IntegrityError`) y `hx-disabled-elt`; tras un reintento normal se espera `CONSULTAS_ESPERA`; petición de la solución solo explícita; unidad sin `After=network-online.target`, con `NoNewPrivileges` y `TimeoutStopSec`. `InaccessiblePaths=` no se usa: en un servicio de usuario necesita espacios de nombres de usuario y titan los restringe (`kernel.apparmor_restrict_unprivileged_userns=1`). La API rechaza lo que llega con `X-Forwarded-For` o `Forwarded` (viene por Traefik). Documentado que en titan basta con el `.env` (su `compose.yaml` usa `env_file`) y que tras desplegar hay que volver a copiar la unidad si cambió.
  - La migración `0003` se modifica en el sitio (columna `repartos`) porque aún no se ha desplegado.
  - Verificación: 325 pruebas (51 nuevas con este cambio), validadores, markdownlint e imagen Docker.

### «Preguntar a Claude» desplegado en titan (#40)

- Implementación en el PR #49 (agente en paralelo en un *worktree*), con revisión independiente de seguridad: 2 críticos (Claude podía leer cualquier fichero del usuario, como `~/.ssh` o el `.env` de la consola, y heredaba sus secretos por el entorno), 3 importantes (imágenes en el Markdown como canal de salida, sin límite de gasto, patrón de cuota demasiado amplio) y 8 menores. Corregidos: `claude` con `--restricted --strict-mcp-config --permission-mode dontAsk`, lectura solo de los cursos y los libros, web solo de AWS, entorno mínimo, fichero de entorno propio del trabajador, sin imágenes, topes por usuario (3 en espera, 30 al día) y de 5 USD diarios, reparto atómico y API cerrada a peticiones que llegan por Traefik. Prueba real: la lectura de `~/.ssh` queda denegada.
- La propuesta de OpenSpec se dio por aprobada con el «hazlo todo» del usuario; cambio archivado y especificación `consultas-claude` creada.
- **Despliegue (2026-11-21):** `CONSULTAS_TOKEN` en el `.env` del despliegue, `./desplegar.sh` (migración `0003`), servicio de usuario `consultas-claude` habilitado. La copia de la base de datos previa a la migración falló porque titan no tiene el binario `sqlite3`; se hizo después con el módulo de Python y se comprobó que los datos siguen (la `0003` solo añade tablas). Inventario de `~/Sistema` actualizado.
- **Prueba de extremo a extremo:** duda antes de responder (orienta sin dar la solución y cita la documentación de AWS), segunda duda en la misma conversación, duda con el servicio parado («En cola» y resuelta al arrancarlo) y «Mis dudas»; unas 0,02–0,03 USD por duda.

### Repaso ampliado

- Petición: «crea más preguntas de repaso».
- Rama `aif-c01/repaso-ampliado`. Criterio: llevar cada objetivo oficial a un mínimo de 4 preguntas de repaso (muchos tenían 2). El módulo 00 ya tenía 5 o más por objetivo y no cambia.
- 93 preguntas nuevas: R1-059 a R1-084, R2-047 a R2-066, R3-052 a R3-083, R4-040 a R4-050 y R5-036 a R5-039. Total: 355.
- **Integración con `main` (2026-11-21):** el PR #28 quedó en conflicto porque las revisiones con las guías de estudio (#31 a #37) añadieron preguntas de repaso con los mismos ids. Se fusionó `main` en la rama (sin reescribir la historia): se conservan intactas las preguntas de `main` y las 93 del PR se renumeran a continuación de las existentes y se colocan junto a las de su objetivo. Ningún enunciado coincide con los de `main`. Antes de la fusión, `main` incumplía el mínimo de 4 en 44 objetivos.
- **Decisiones:** cada pregunta se apoya en una afirmación de la teoría del módulo y cita una fuente ya usada para ese objetivo; ninguna depende de los marcadores pendientes (preentrenamiento continuado en Bedrock, *task engineering*). Se mezclan los cuatro tipos y se reparten las letras correctas. `repaso.minimo_por_objetivo` pasa de 2 a 4 para que la CI mantenga el mínimo.
- El trabajo se pausó a petición del usuario tras el módulo 03 (2026-11-19) y se retomó el 2026-11-20.
- **Verificación:** validador sin errores ni avisos, cobertura con `--preguntas` y pytest.

### Simulacro rotatorio (OpenSpec `simulacro-rotatorio`)

- **Problema:** el simulacro de AIF-C01 eran 65 preguntas fijas que cubrían 58 de los 69 objetivos. Con 13/16/18/9/9 por dominio el máximo posible es 62 (el Dominio 1 tiene 17 objetivos para 13 preguntas, el 3 tiene 19 para 18 y el 4 tiene 11 para 9), y repetir el simulacro medía la memoria.
- **Propuesta** (rama `feat/simulacro-rotatorio`): un banco de 82 preguntas que cubra los 69 objetivos, del que cada intento extrae 65. **Aprobada por el responsable el 2026-11-21** con las recomendaciones: reparto por dominio calculado con restos mayores, respuesta múltiple 2/3/4/2/2, banco de 82, el intento abandonado cuenta para la rotación y la dificultad solo se informa.
- **Respuesta múltiple: 13 por intento.** El banco tiene 51/14, pero `examen.distribucion` es 80/20 y el 20 % de 65 son exactamente 13; 2/3/4/2/2 suma 13, así que se mantiene. Los 51/14 son la composición del banco fijo, no la de un intento.
- **Algoritmo:** voraz por dominio, empezando por la combinación de dominio y tipo con menos holgura, con la clave (objetivo ya usado, vista en el intento anterior, azar) y hasta 20 reintentos. Se descartaron la programación lineal entera (desproporcionada) y el muestreo con rechazo (puede no terminar). Con el banco previsto, en 500 semillas se cumplen siempre las cuotas y las únicas repeticiones de objetivo son las inevitables (2 en el Dominio 2 y 1 en el 5); dos intentos seguidos recorren el banco entero.
- **Sin migración:** `Intento.preguntas` ya guardaba los ids en orden. Los intentos antiguos, reanudar, el resultado, el historial y las estadísticas no cambian.
- **Compatibilidad:** un banco del tamaño del examen funciona como antes (todas, ordenadas por id). Por eso el código puede fusionarse antes que el contenido. `minimo_simulacro: 80` y `minimo_simulacro_por_objetivo: 1` se declararán en `curso.yaml` junto con el banco.
- **Pendiente:** redactar `S-070` a `S-086` cuando se fusione el PR #52 (que deja 62/69 objetivos con `S-066` a `S-069`).
- **Verificación:** 608 pruebas de pytest (278 nuevas), validador, cobertura con `--preguntas`, glosario, markdownlint, Mermaid e imagen Docker.
