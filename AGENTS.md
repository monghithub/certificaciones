# Reglas para agentes y colaboradores

Resumen operativo de las reglas del repositorio. Las reglas específicas del curso AIF-C01 están en `promt.md`: ante cualquier duda sobre ese curso prevalece `promt.md`, y ante cualquier discrepancia con AWS, prevalece la guía oficial.

## Rol y destinatarios

Curso en **español de España**, registro formal y técnico, para aprobar AIF-C01. Lector: perfil junior; revisor: arquitecto sénior. Nivel *foundational*: qué servicio o técnica aplicar y por qué, no cómo implementarlo. Los nombres de servicios y los términos que el examen usa en inglés se mantienen en inglés, con su traducción en la primera aparición.

## Fuente de verdad

- Primaria: la [guía oficial AIF-C01](https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html) y sus subpáginas (dominios 1–5, servicios in/out of scope, revisiones).
- Secundarias: documentación oficial de cada servicio en `docs.aws.amazon.com`, la página de certificación y AWS Skill Builder.
- Antes de redactar un módulo, relee `cursos/<curso>/fuentes/dominio-N.md` y redáctalo contra esa lista. Si la guía cambia, actualiza `fuentes/`, anota la diferencia en `CHANGELOG.md` y revisa los módulos y preguntas afectados.
- **Prohibido inventar** cuotas, precios, nombres de funcionalidades, regiones o fechas. Si no puedes verificar un dato, escribe `> ⚠️ PENDIENTE DE VERIFICAR:` seguido de la duda y continúa.
- **Prohibido** usar o reproducir preguntas reales del examen ("dumps") o material de terceros protegido.
- Lo que la guía declara fuera de alcance (desarrollar modelos, ingeniería de datos o *features*, ajuste de hiperparámetros, pipelines, análisis matemático, implantar protocolos de seguridad o marcos de gobierno) solo se menciona para reconocerlo.

## Estructura

```text
cursos/<curso>/curso.yaml  Manifiesto: dominios y pesos, simulacro, mínimos del banco
cursos/<curso>/fuentes/    dominio-N.md (objetivos oficiales literales, en inglés), servicios-alcance.md
cursos/<curso>/modulos/NN-*/  README.md, servicios.md, trampas.md, preguntas.yaml, laboratorio.md
schemas/pregunta.schema.json, schemas/curso.schema.json
scripts/validar_preguntas.py, scripts/quiz.py
tests/                     pytest de las herramientas
```

## Plantilla de módulo (`README.md`)

1. Objetivos de aprendizaje, con correspondencia a tareas oficiales ("Task 3.1").
2. Mapa de cobertura: objetivo oficial → sección que lo cubre. Sin filas sin cubrir. Formato comprobable con `scripts/comprobar_cobertura.py`: una tabla Markdown con una fila por objetivo de `fuentes/` cuya primera columna es su id (`1.2.3`, o `CP.1` en el módulo 00) y con un enlace `[texto](#ancla)` a un encabezado del mismo README:

   ```markdown
   | Objetivo | Descripción | Sección |
   |---|---|---|
   | 1.1.1 | Definir términos básicos de IA | [Términos básicos](#términos-básicos-de-ia) |
   ```

   Qué fuente cubre cada módulo se declara en el bloque `cobertura` de `curso.yaml`.
3. Teoría, con ejemplos de negocio y diagramas Mermaid donde aporten.
4. Puntos clave para el examen (5–10 viñetas).
5. Referencias oficiales.

Criterios de decisión que hay que reforzar: gestionado frente a medida; prompt engineering → RAG → fine-tuning → pre-entrenamiento continuado (coste y esfuerzo); on-demand frente a provisioned throughput; métrica de evaluación según el problema.

## Calidad del contenido (obligatorio en todos los módulos)

Reglas surgidas de la revisión técnica de la iteración 1. Se aplican a todo módulo nuevo o modificado:

- **Disponibilidad y nombres vigentes.** Antes de citar un servicio o funcionalidad, abre su página en `docs.aws.amazon.com` y busca avisos del tipo *no longer open to new customers*, *Classic* o *maintenance mode* (hoy: SageMaker Model Monitor, Clarify y Ground Truth, Bedrock Agents Classic y SageMaker Experiments Classic). Indícalo en la teoría, en `servicios.md` y en el glosario, y no lo presentes como la opción para proyectos nuevos. Comprueba también los renombrados: SageMaker AI frente a la plataforma unificada Amazon SageMaker.
- **Fuentes con fecha.** Las guías de decisión de AWS indican su *Last updated*. Si una afirmación de una guía antigua choca con la documentación del servicio, prevalece la del servicio. Ejemplo: la guía de ML de 2024 dice que la mayoría de los servicios de IA no admiten *endpoints* de VPC, pero la lista de PrivateLink dice lo contrario.
- **Cada objetivo oficial, con cuatro piezas:** definición breve, criterio de decisión (tabla «escenario → servicio o técnica»), ejemplo de negocio y trampa típica en `trampas.md`. Los matices que separan opciones parecidas (límites, exclusiones, modelo de facturación) se citan con su fuente.
- **Ejemplos resueltos.** Las métricas y los cálculos se explican con un ejemplo numérico (matriz de confusión, coste), y los ciclos de vida con un caso de principio a fin.
- **Servicios dentro de alcance por etapa.** Cuando un objetivo pide servicios «por etapa» o «para un caso», revisa `fuentes/servicios-alcance.md` y menciona los servicios in scope relevantes, no solo los del ejemplo de la guía.
- **Diagramas jerárquicos.** Las relaciones de inclusión (IA ⊃ ML ⊃ aprendizaje profundo) se dibujan con `subgraph` anidados, no como una cadena de flechas que parezca un proceso.
- **Glosario.** Todo servicio o concepto nuevo lleva su entrada. No uses como alias palabras comunes que aparezcan con otro sentido («Pipelines», «Canvas», «modelo»): usa la forma completa («SageMaker Pipelines»).
- **Laboratorios.** Distingue los permisos de consola de los de CLI: la consola suele necesitar las políticas administradas de solo lectura del servicio, y la CLI admite una política de mínimo privilegio. Describe la capa gratuita vigente (desde julio de 2025, créditos y plan gratuito de seis meses para cuentas nuevas), recomienda AWS Budgets antes de empezar e incluye preguntas de reflexión con respuestas orientativas.
- **Revisión independiente al cerrar cada módulo.** Comprueba los errores factuales contra la documentación, la suficiencia de cada objetivo para el examen, la calidad del banco con la lista de abajo y la didáctica para un perfil junior. Registra los cambios en `CHANGELOG.md`.

## Banco de preguntas

- Mínimos (en `curso.yaml`, comprobados por la CI): **60 preguntas por módulo de dominio, 15 por tarea y 3 por objetivo oficial** (≈60 % `multiple_choice`, 20 % `multiple_response`, 10 % `ordering`, 10 % `matching`). Como orientación, de 4 a 5 preguntas por objetivo; más en los objetivos de servicios y de criterios de decisión. Simulacro: 65, según los pesos oficiales, inéditas respecto a los bancos.
- Escenarios de negocio realistas; distractores plausibles, cada uno explicado; sin "todas/ninguna de las anteriores".
- `id`: `D<dominio>-NNN`; en el simulacro, `S-NNN`. `objetivo` (opcional, recomendado: `N.M.K`) enlaza la pregunta con un objetivo oficial de su tarea y permite comprobar que todos tienen preguntas. `tarea` debe existir en `cursos/<curso>/fuentes/dominio-N.md` y `dominio` en el manifiesto `curso.yaml`. `referencia`: URL oficial de AWS.
- Formato por tipo (guía oficial v1.1):

| Tipo | Opciones | `correctas` |
|---|---|---|
| `multiple_choice` | ≥4 (1 correcta y 3 distractores) | 1 id |
| `multiple_response` | ≥5 | ≥2 ids (hay que acertarlas todas) |
| `ordering` | ≥ nº de elementos | 3–5 ids **en orden**; sin `distractores` |
| `matching` | columna derecha; `prompts` en columna izquierda (3–7) | 3–7 pares `[prompt_id, opcion_id]`; `distractores` para las opciones sin par |

Los ids de `prompts` son números (`"1"`, `"2"`…, entre comillas en YAML) y los de `opciones` letras (`a`–`j`). Las opciones incorrectas de `multiple_*` y las no usadas en `matching` deben tener su explicación en `distractores`. El esquema `matching`/`ordering` concreto es una decisión de diseño de este repositorio; el ejemplo de `promt.md` solo cubre `multiple_choice`.

### Calidad del banco de preguntas

Todas las preguntas son de elaboración propia. El conjunto oficial de práctica de AWS Skill Builder sirve solo como referencia de estilo y de temas, nunca para copiar enunciados. Están prohibidos los *dumps* y las webs de terceros.

1. **Escenario de negocio con una restricción que decide:** «con el MENOR esfuerzo operativo», «de la forma MÁS rentable», «sin experiencia en ML», «en milisegundos», «sin entrenar modelos», «la decisión final es del perito». La restricción debe ser la que descarta las opciones plausibles.
2. **Distractores plausibles del mismo terreno:** servicios o técnicas vecinas que un candidato confundiría (Textract/Rekognition, Transcribe/Polly, Comprehend/Lex, Canvas/SageMaker AI, *serverless*/asíncrona/por lotes, precisión/exhaustividad, sobreajuste/deriva). Nada de opciones absurdas ni de categorías ajenas.
3. **Sin pistas:** el enunciado no copia la definición de la respuesta ni contiene su palabra clave («agente» → IA agéntica, «recompensa» → refuerzo). Los distractores no usan absolutos («siempre», «nunca», «cualquier», «garantiza»); el validador avisa.
4. **Posiciones repartidas:** la respuesta correcta de opción múltiple no puede estar en la misma letra en más del 40 % del banco; el validador falla. En respuesta múltiple, varía también las combinaciones.
5. **Explicaciones:** la correcta explica *por qué* encaja con la restricción del escenario; cada distractor explica por qué *en este escenario* no encaja.
6. **Dificultad real:** «alta» significa que dos opciones son plausibles y las separa un matiz del enunciado o de la documentación (límites, exclusiones, disponibilidad). Reparto orientativo: 20 % baja, 60 % media y 20 % alta.
7. **Datos verificados:** una pregunta no puede depender de un dato marcado como `PENDIENTE DE VERIFICAR`.
8. **Tras reordenar opciones**, comprueba que `correctas` y `distractores` siguen apuntando al texto correcto.

Antes de cada commit: `python scripts/validar_preguntas.py && python scripts/comprobar_cobertura.py --preguntas && python -m pytest`. Revisa también los `AVISO` del validador.

## Cursos

Un curso nuevo es una carpeta `cursos/<slug>/` con su `curso.yaml` (el `slug` coincide con la carpeta). Los usuarios se matriculan por curso desde la consola; los roles `admin` y `estudiante` son globales. Las herramientas (`validar_preguntas.py`, `quiz.py`) aceptan `--curso`.

## Glosario y diagramas (consola)

- **Glosario.** Cada curso tiene `cursos/<curso>/glosario.yaml`. **Todo servicio o concepto clave que se introduzca en un módulo debe tener su entrada** (término, alias, categoría, definición breve, y para servicios «cuándo usarlo» y «cuándo no», y una `referencia` oficial). La consola convierte sus apariciones (la primera de cada apartado) en botones que abren un modal. `scripts/validar_preguntas.py` falla si un servicio de la primera columna de un `servicios.md` no tiene entrada, o si hay ids, términos o alias duplicados. Define como alias las variantes que aparecen en el texto (plural, siglas, nombre corto); las siglas y los términos de 5 o menos caracteres distinguen mayúsculas.
- **Diagramas: estilo único en todo el proyecto.** El estilo actual (emojis, colores pastel por tipo, tema suave, animación) es **obligatorio** en todos los cursos y se comprueba en `scripts/validar_preguntas.py` (y por tanto en el CI). Reglas:
  - Solo `flowchart` de Mermaid; sin `classDef`.
  - La etiqueta de **cada nodo y de cada subgrupo** empieza por un emoji; usa `<b>…</b>` para el título y `<br/>` para una segunda línea de explicación. Etiquetas cortas y siempre entre comillas.
  - Cada nodo lleva una clase semántica con `class A,B tipo`: `ia`, `ml`, `dl`, `gen` (familia de IA), `dato`, `proceso`, `servicio` (servicios de AWS), `accion`, `aviso` o `decision`.
  - **Cualquier caja debe dar información y enlaces al pulsarla.** Justo después del diagrama (solo líneas en blanco entre ambos) va un bloque ```` ```nodos ```` con un mapa YAML `id → información` que cubre **todos** los nodos y subgrupos. Cada entrada usa `concepto` (id de una entrada del glosario) y/o `titulo` + `texto`, y opcionalmente `usar_cuando`, `no_usar_cuando`, `enlaces` (`texto` y `url` https) y `seccion` (`modulo/seccion#ancla`, que se muestra como «Ver en el curso»). Los campos de la caja sustituyen a los del concepto y sus enlaces se suman a los del glosario. No hay coincidencia automática: lo que abre cada caja lo decides tú.
  - Valida también la sintaxis Mermaid con `tests/e2e` (`npm run mermaid`).

  ````text
  ```mermaid
  flowchart LR
      A["🧩 <b>RAG</b><br/>recupera datos propios"] --> B["✨ <b>Amazon Bedrock</b><br/>genera la respuesta"]
      class A proceso
      class B servicio
  ```

  ```nodos
  A:
    concepto: rag
    seccion: 03-modelos-fundacionales/teoria#rag
  B:
    concepto: amazon-bedrock
    enlaces: [{texto: "Guía de Bedrock", url: "https://docs.aws.amazon.com/bedrock/"}]
  ```
  ````

## Laboratorios

Objetivo y relación con tareas; requisitos (cuenta, región con Bedrock y acceso a modelos); pasos por consola y, si procede, CLI o boto3; **estimación de coste** con aviso de facturación; **limpieza de recursos obligatoria** (Knowledge Bases, colecciones de OpenSearch Serverless, endpoints de SageMaker…).

## Git

- *Conventional Commits*: `feat(modulo-03): ...`, `docs: ...`, `fix(preguntas): ...`, `ci: ...`.
- Una rama por módulo (`modulo/03-modelos-fundacionales`) integrada en `main` con PR.
- `CHANGELOG.md` actualizado al completar cada módulo. Etiqueta `v1.0.0` solo con los siete módulos completos y CI en verde, sin marcadores `PENDIENTE DE VERIFICAR`.

## Journal

`docs/journal.md` es el diario de trabajo: al cerrar cada etapa se añade una entrada con fecha que recoja qué se hizo, qué se decidió y por qué, los cambios de OpenSpec y los commits, y lo que queda pendiente. El journal no sustituye a `CHANGELOG.md`, que solo dice qué cambia.

## Flujo por iteraciones (detenerse para revisión humana al final de cada una)

- Iteración 0: cimientos.
- Iteración 1: módulos 00 y 01.
- Iteraciones 2 a 5: un módulo de dominio por iteración (02 a 05).
- Iteración 6: simulacro, `glosario.md`, `chuleta.md` y revisión cruzada de cobertura.

Cada cierre incluye: ficheros creados o modificados; cobertura de tareas (cubiertas/totales); preguntas por tipo; marcadores pendientes abiertos; resultado de CI o scripts en local.
