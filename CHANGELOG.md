# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [Sin publicar]

### Añadido

- Iteración 0: estructura del repositorio, `README.md`, `AGENTS.md`, `LICENSE`.
- `fuentes/dominio-1..5.md`: objetivos oficiales transcritos de la guía AIF-C01 v1.1 (consulta del 2026-10-14): 17, 14, 19, 11 y 8 objetivos (69 en total) en 3, 3, 4, 2 y 2 tareas.
- `fuentes/servicios-alcance.md`: listas oficiales de servicios in scope y out of scope.
- `schemas/pregunta.schema.json`, `scripts/validar_preguntas.py`, `scripts/quiz.py` y tests en `tests/`.
- CI en `.github/workflows/ci.yml`.

- Consola web (`app/`, `curso/`, `migrations/`, `Dockerfile`, `compose.yaml`, `docs/consola.md`): autenticación con roles `admin` y `estudiante`, gestión de usuarios, navegación del curso con seguimiento de lectura, cuestionarios y simulacro cronometrado, y estadísticas por usuario. La corrección de respuestas se comparte con `scripts/quiz.py` mediante `curso/correccion.py`.

- Soporte multicurso: cada curso vive en `cursos/<slug>/` con su manifiesto `curso.yaml` (esquema `schemas/curso.schema.json`); `fuentes/` y `modulos/` del AIF-C01 se mueven a `cursos/aif-c01/`. El esquema de preguntas se generaliza (cualquier dominio declarado en el manifiesto), `validar_preguntas.py` y `quiz.py` aceptan `--curso`, y los mínimos, la distribución y el simulacro salen del manifiesto. La consola incorpora catálogo de cursos, matrícula por curso (roles globales `admin` y `estudiante`), rutas `/c/<curso>/…`, progreso e historial por curso, y la migración `0002`, que asigna los datos existentes a `aif-c01`. **Cambios incompatibles:** URLs de la consola, variable `COURSE_DIR` → `COURSES_DIR` y rutas de los ficheros de contenido.

- Iteración 1: módulo 00 (base de AWS: servicios centrales, responsabilidad compartida, IAM y modelos de precios; sin banco de preguntas) y módulo 01 (Dominio 1: teoría con mapa de cobertura de los 17 objetivos, `servicios.md`, `trampas.md`, laboratorio demostrativo y 32 preguntas: 19 de opción múltiple, 7 de respuesta múltiple, 3 de ordenación y 3 de emparejamiento). Nueva fuente `cursos/aif-c01/fuentes/conocimientos-previos.md`.
- `scripts/comprobar_cobertura.py`: comprueba que el mapa de cobertura de cada módulo cubre los objetivos de su fuente (bloque `cobertura` de `curso.yaml`) y, con `--preguntas`, que cada tarea y cada objetivo tienen preguntas. Se integra en el CI. Las preguntas admiten el campo opcional `objetivo`, que el validador comprueba.
- Hallazgos de la documentación oficial a tener en cuenta en iteraciones futuras: Amazon SageMaker Model Monitor y Amazon SageMaker Clarify ya no admiten clientes nuevos (la guía v1.1 todavía cita Clarify en la Tarea 4.2), y Amazon Bedrock Agents (ahora *Classic*) tampoco, con Amazon Bedrock AgentCore como alternativa.

- Glosario por curso (`cursos/<curso>/glosario.yaml`, `schemas/glosario.schema.json`, `curso/glosario.py`) con 68 entradas para el curso AIF-C01, validación en `validar_preguntas.py` (ids, términos y alias únicos, URL https y entrada obligatoria para todo servicio de un `servicios.md`) y página `/c/<curso>/glosario` con buscador.
- Consola: los términos del glosario son botones (primera aparición por apartado) que abren un modal accesible; los nodos de los diagramas también. Diagramas Mermaid con tema propio claro y oscuro, colores por tipo, aparición escalonada y flechas animadas, con respeto al movimiento reducido. Se reescriben los 5 diagramas existentes. Pruebas manuales de navegador en `tests/e2e`.

- Consola: tema claro de tonos suaves por defecto (botones tonales, sombras discretas) con selector claro, oscuro o sistema; los conceptos del glosario son texto normal en reposo y se resaltan solo al pasar el ratón (pista tenue en pantallas táctiles). **Corrección:** los estáticos se servían con caché de una hora, de modo que tras actualizar la consola el navegador podía mostrar un CSS y un JavaScript antiguos (los conceptos aparecían como recuadros azules sin función); ahora se revalidan siempre y se enlazan con versión.

- Diagramas: estilo único obligatorio y validado (`curso/diagramas.py`, integrado en `validar_preguntas.py` y en el CI): solo `flowchart`, emoji en cada etiqueta, clases semánticas, sin `classDef`. **Cualquier caja** de un diagrama abre un modal con información y enlaces definidos en un bloque `nodos` tras el diagrama (`concepto`, `titulo`, `texto`, `usar_cuando`, `no_usar_cuando`, `enlaces`, `seccion`); el glosario admite `enlaces` además de `referencia`. Los encabezados renderizados llevan ancla (formato GitHub), con lo que funcionan los enlaces `#ancla` del mapa de cobertura. Se añaden los `nodos` a los 5 diagramas de los módulos 00 y 01.

- **Corrección (consola):** un formulario de acceso abierto antes de cerrar sesión en otra pestaña, o tras expirar la sesión, devolvía un 403 «No tienes permiso». Ahora cerrar sesión no invalida los formularios abiertos y, si un formulario ha caducado, se explica y se permite repetir (en el acceso se vuelve a mostrar el formulario; en el resto se vuelve a la página anterior sin ejecutar la acción).

- Revisión técnica de los módulos 00 y 01 (2026-10-14), contrastada con la documentación oficial:
  - **Correcciones:** D1-026 afirmaba que la mayoría de los servicios de IA especializados no admiten *endpoints* de VPC (falso: casi todos figuran en la lista de AWS PrivateLink); SageMaker Experiments pasa a ser *Experiments Classic* y se sustituye por MLflow en SageMaker AI; «SageMaker = SageMaker AI» se matiza (desde el 3 de diciembre de 2024, «Amazon SageMaker» es una plataforma unificada que incluye SageMaker AI) y se retira el alias `Amazon SageMaker` del glosario; la política IAM del laboratorio no bastaba para la consola (se usan las políticas administradas de solo lectura); se actualiza la capa gratuita (créditos y plan de seis meses para cuentas nuevas desde julio de 2025); se cierran los pendientes de Polly en `us-east-1` y de la documentación de Kiro.
  - **Contenido nuevo:** módulo 00 con políticas, grupos y roles de IAM, VPC, CloudWatch y CloudTrail, modelos de precios de los servicios de IA, AWS Budgets y AWS Cost Explorer. Módulo 01 con diagrama de conjuntos anidados que incluye la IA agéntica, pistas para distinguir ML, aprendizaje profundo, IA generativa e IA agéntica, aprendizaje autosupervisado y RLHF, matices de las opciones de inferencia (límites de la asíncrona y de *serverless*, inferencia por lotes de Bedrock), escenarios por servicio especializado, capacidades de SageMaker AI (Canvas, JumpStart, Pipelines, Model Registry, MLflow), restricciones operativas en ML tradicional frente a modelos fundacionales, Amazon Nova como fuente de modelos, regla de coste y esfuerzo, tabla de API gestionada frente a autoalojada, servicios de datos por etapa (S3, Glue, DataBrew, Ground Truth), ejemplo de ciclo de vida, matriz de confusión con ejemplo numérico, trampa de la exactitud con clases desequilibradas y métricas de negocio por pregunta de la dirección. Ground Truth se marca como cerrado a clientes nuevos.
  - **Banco de preguntas:** de 32 a 82 preguntas originales (50 de opción múltiple, 16 de respuesta múltiple, 8 de ordenación y 8 de emparejamiento), con al menos 3 por objetivo y las respuestas correctas repartidas entre las letras (12–13 por letra). Se reescriben enunciados o distractores de D1-001 a D1-031 para quitar pistas y distractores evidentes. D1-033 a D1-082 siguen el estilo de escenario del examen («MENOR esfuerzo operativo», «sin experiencia en ML», restricciones de latencia o de explicabilidad) con distractores de servicios vecinos. El conjunto oficial de Skill Builder (20 preguntas, requiere inicio de sesión) no se ha usado ni copiado; tampoco *dumps*.
  - **Reglas permanentes para todo el proyecto:** `AGENTS.md` incorpora «Calidad del contenido» y «Calidad del banco de preguntas», y `promt.md` sube los mínimos. `curso.yaml` exige 60 preguntas por módulo, 15 por tarea y el nuevo `minimo_por_objetivo` (3), que comprueba `comprobar_cobertura.py --preguntas`. `validar_preguntas.py` falla si la respuesta correcta de opción múltiple se concentra en una letra (más del 40 %) o si hay opciones repetidas, y avisa de distractores con términos absolutos y de enunciados demasiado cortos. Hay tests nuevos para cada control.
  - **Glosario:** 18 entradas nuevas (Amazon Nova, AWS Glue, Glue DataBrew, SageMaker Canvas, Ground Truth, Pipelines, Model Registry, MLflow, CloudWatch, CloudTrail, VPC, Budgets, Cost Explorer, política de IAM, aprendizaje autosupervisado, deriva, matriz de confusión y algoritmo).
  - `cursos/aif-c01/README.md`: enlaces al conjunto oficial de preguntas de práctica de AWS Skill Builder, a la página de la certificación y a la guía del examen (criterio de aceptación de `promt.md`); estado actualizado a 82 preguntas.
  - `fuentes/servicios-alcance.md`: se anota la contradicción de AWS entre la página de revisiones y la lista out of scope vigente.

- Iteración 2: módulo 02 (Dominio 2, fundamentos de IA generativa), verificado contra la documentación oficial el 2026-10-14:
  - **Teoría** con mapa de cobertura de los 14 objetivos y 5 diagramas: *tokens*, *chunking*, *embeddings*, vectores, *transformers*, modelos multimodales y de difusión; casos de uso; ciclo de vida del modelo fundacional con un caso de principio a fin; precios por *tokens* con ejemplo resuelto; ingeniería de contexto; IA agéntica (uso de herramientas, MCP, memoria, orquestación, patrones multiagente); ventajas, limitaciones y parámetros de inferencia; criterios para elegir un modelo; métricas de negocio con ejemplo de ROI; servicios (Bedrock, SageMaker AI, JumpStart, Quick, Kiro, Strands Agents, AgentCore), ventajas de AWS, infraestructura (privacidad de Bedrock, cumplimiento, Trainium e Inferentia) y compromisos de coste (niveles Standard, Priority, Flex y Reserved, lotes, Provisioned Throughput, modelos personalizados, *prompt caching* e inferencia entre Regiones).
  - `servicios.md`, `trampas.md` y laboratorio del *playground* de Bedrock con Amazon Nova Micro (temperatura, top-p, longitud máxima y *tokens*), con permisos de consola y CLI, coste y limpieza.
  - **Banco:** 75 preguntas originales (46 de opción múltiple, 15 de respuesta múltiple, 6 de ordenación y 8 de emparejamiento; 31, 20 y 24 por tarea; de 4 a 8 por objetivo; dificultad 10 baja, 46 media y 19 alta).
  - **Glosario:** 38 entradas nuevas (124 en total), entre ellas A2A, AWS Transform, AWS PrivateLink y la API Converse.
  - **Disponibilidad:** Amazon Q Business ya no admite clientes nuevos (AWS remite a Amazon Quick) y los *plugins* de IDE de Amazon Q Developer pierden soporte el 30 de abril de 2027 (AWS remite a Kiro). Amazon Quick sustituye a QuickSight, que sigue como Quick Sight.
  - **Correcciones:** la entrada del glosario de *Provisioned Throughput* decía que es obligatorio para usar un modelo personalizado; ahora algunos modelos personalizados admiten también inferencia bajo demanda. La referencia de Kiro apunta a su página de documentación en AWS.
  - `tests/e2e/consola.mjs` comprueba también las cajas de los diagramas del módulo 02.
  - **Revisión independiente** (2026-10-14), contrastada con la documentación oficial y aplicada antes del cierre:
    - Nova Canvas, Nova Reel y Nova Sonic v1 están retirados (fin de vida en septiembre de 2026): se retiran como distractores y se anota en el glosario.
    - AWS Trainium sirve para entrenar **y** para inferencia; Inferentia es específico de inferencia (se reescribe D2-066).
    - Cifras de los niveles de servicio: Priority +75 % y Flex −50 % sobre Standard (igual que lotes); Reserved desborda a Standard.
    - Se añaden AWS Transform (servicio in scope que faltaba) y el protocolo A2A frente a MCP, y la lista de módulos de AgentCore se completa con Policy y Evaluations.
    - Trampas nuevas para los objetivos 2.1.2, 2.2.1 y 2.3.2, y un ejemplo de negocio para 2.3.3.
    - Banco: corregida la explicación de un distractor de cálculo (D2-017); distractores más plausibles y sin pistas en D2-003, 009, 012, 016, 022, 023, 026, 028, 033, 038, 040, 044, 046, 053, 056, 060 y 061; la respuesta correcta ya no es la opción más larga en la mayoría de las preguntas (de 25 a 13 de 46).
    - Precisiones: ventana de contexto (incluye a menudo la salida), *chunking* por defecto de unos 300 *tokens*, `CountTokens` solo en modelos compatibles, *Provisioned Throughput* no se combina con la inferencia entre Regiones, y el plan gratuito de AWS no da acceso a todos los servicios.

- **Plataforma multicertificación.** El repositorio pasa a llamarse `certificaciones` y reúne cursos de cualquier proveedor:
  - El manifiesto admite `proveedor` y `fuentes_oficiales`, y `validar_preguntas.py` exige que la `referencia` de cada pregunta pertenezca a las fuentes oficiales de su curso. El esquema de pregunta ya no está atado a AWS.
  - `AGENTS.md` raíz con las reglas comunes; las propias de AWS y AIF-C01 pasan a `cursos/aif-c01/AGENTS.md`, y `promt.md` a `cursos/aif-c01/promt.md`.
  - La consola se presenta como «Certificaciones». **Cambio incompatible:** la imagen Docker pasa a llamarse `certificaciones-consola` (`docker compose up -d --build` la crea; la antigua `aif-c01-consola` puede borrarse; los datos no cambian).
  - CI: se excluyen de lychee los enlaces locales de `docs/consola.md`.

### Corregido

- Consola: la solución y la respuesta del estudiante de las preguntas de ordenación y emparejamiento se mostraban en formato técnico (`[['1', 'e'], …]`). Ahora se muestran como lista con el texto de cada opción (posición, o elemento → opción), también en opción y respuesta múltiple y en la página de resultados (2026-10-15).

### Revalidación de los datos de referencia (2026-10-14)

Contrastados con la [guía oficial](https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html) (v1.1, 30 de abril de 2026) y la [página de la certificación](https://aws.amazon.com/certification/certified-ai-practitioner/).

Coinciden con `promt.md`: duración (90 min), preguntas (65; 50 puntuables y 15 no puntuables), puntuación (100–1.000, aprobado 700, compensatorio), sin penalización, coste (100 USD), validez (3 años) y pesos (20/24/28/14/14 %).

Matices y diferencias:

- La guía llama **objetivos** (*Objectives*) a lo que `promt.md` llama habilidades. Se numeran `N.M.K` por orden de aparición, convención confirmada por la página de revisiones.
- Respuesta múltiple: dos o más correctas entre **cinco o más** opciones; hay que acertar todas. Opción múltiple: 1 correcta y 3 distractores. Reflejado en el esquema.
- Emparejamiento: lista de respuestas que se asocia con 3–7 *prompts*.
- La guía v1.1 incorpora agentic AI, MCP, context engineering, AgentCore, Kiro y Strands Agents, entre otros (ver `aif-01-revisions.html`). Amazon SageMaker Data Wrangler, Feature Store y Model Monitor ya no se citan como ejemplos.
- Servicios añadidos a in scope en v1.1: Amazon Aurora, Amazon Bedrock AgentCore, Kiro, Strands Agents, Amazon Q, Amazon SageMaker JumpStart y AWS Transform. Eliminado: Amazon MemoryDB.
- **Pendiente de verificar:** la página de revisiones dice que Amazon Q se añadió a in scope, pero no figura en la lista actual (sí Amazon Quick). Ver `fuentes/servicios-alcance.md`.

### Decisiones pendientes de revisión

- Licencia propuesta: MIT (código) y CC BY 4.0 (contenido); titular provisional "Contribuidores del curso AIF-C01".
- Formato de `ordering` y `matching` en el banco de preguntas (ver `AGENTS.md`).
