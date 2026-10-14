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
