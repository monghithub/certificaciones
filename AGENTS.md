# Reglas para agentes y colaboradores

Este repositorio reúne **todos los cursos de preparación de certificaciones** que se vayan estudiando, de cualquier proveedor (AWS, Microsoft, Google Cloud, Kubernetes, etc.), junto con una consola web común para estudiarlos. Este fichero recoge las reglas **comunes a todos los cursos**.

Cada curso puede tener sus propias reglas en `cursos/<curso>/AGENTS.md` y su especificación en `cursos/<curso>/promt.md`. Orden de prevalencia:

1. La guía oficial del examen del proveedor.
2. `cursos/<curso>/promt.md` y `cursos/<curso>/AGENTS.md`, para ese curso.
3. Este fichero.

## Rol y destinatarios

Cursos en **español de España**, registro formal y técnico, pensados para un perfil junior y revisados por un arquitecto sénior. La profundidad la marca el nivel de cada certificación (por ejemplo, *foundational*: qué servicio o técnica aplicar y por qué, no cómo implementarlo). Los nombres de productos y los términos que el examen usa en inglés se mantienen en inglés, con su traducción en la primera aparición.

## Fuente de verdad

- **Primaria:** la guía oficial del examen y sus subpáginas, transcritas literalmente en `cursos/<curso>/fuentes/` con URL y fecha de consulta.
- **Secundarias:** la documentación oficial del proveedor y su plataforma oficial de formación. Las aceptadas para cada curso se declaran en `fuentes_oficiales` de `curso.yaml`, y el validador exige que la `referencia` de cada pregunta pertenezca a ellas.
- Antes de redactar un módulo, relee `cursos/<curso>/fuentes/dominio-N.md` y redáctalo contra esa lista. Si la guía cambia, actualiza `fuentes/`, anota la diferencia en `CHANGELOG.md` y revisa los módulos y preguntas afectados.
- **Prohibido inventar** cuotas, precios, nombres de funcionalidades, regiones o fechas. Si no puedes verificar un dato, escribe `> ⚠️ PENDIENTE DE VERIFICAR:` seguido de la duda y continúa. Si el marcador no se resuelve en la iteración, abre una issue con la etiqueta `verificar` (qué hay que verificar, qué dicen las fuentes, dónde está el marcador, impacto y criterio de cierre) y enlázala al final del marcador con «Seguimiento: issue #N».
- **Prohibido** usar o reproducir preguntas reales del examen (*dumps*) o material de terceros protegido.
- Lo que la guía declara fuera de alcance solo se menciona al nivel necesario para reconocerlo.

## Estructura

```text
cursos/<curso>/curso.yaml     Manifiesto: proveedor, fuentes oficiales, dominios y pesos, simulacro, mínimos del banco
cursos/<curso>/promt.md       Especificación del curso (opcional)
cursos/<curso>/AGENTS.md      Reglas propias del curso (opcional)
cursos/<curso>/fuentes/       dominio-N.md (objetivos oficiales literales) y otras fuentes transcritas
cursos/<curso>/modulos/NN-*/  README.md, servicios.md, trampas.md, preguntas.yaml, laboratorio.md
cursos/<curso>/glosario.yaml  Glosario del curso (modal de la consola)
schemas/                      pregunta, curso y glosario (JSON Schema)
scripts/                      validar_preguntas.py, comprobar_cobertura.py, quiz.py
app/, curso/                  Consola web y lógica compartida
docs/                         consola.md y journal.md
tests/                        pytest de las herramientas y de la consola
```

## Añadir un curso nuevo

1. Crea `cursos/<slug>/curso.yaml` (el `slug` coincide con la carpeta): `titulo`, `proveedor`, `fuentes_oficiales` (hosts de la documentación oficial), `idioma`, `dominios` con sus pesos, `cobertura`, `banco` y, si hay simulacro, `simulacro` y `examen`.
2. Transcribe la guía oficial en `cursos/<slug>/fuentes/dominio-N.md` (`## Task Statement N.M` y objetivos `**N.M.K**`), con URL y fecha.
3. Si el curso necesita reglas propias (servicios, criterios de decisión típicos del proveedor, laboratorios), crea `cursos/<slug>/AGENTS.md` y, si procede, `cursos/<slug>/promt.md`.
4. Propón el curso como un cambio de OpenSpec y sigue el flujo de trabajo de abajo.
5. Añádelo a la tabla de cursos del `README.md` raíz.

## Plantilla de módulo (`README.md`)

1. Objetivos de aprendizaje, con correspondencia a tareas oficiales («Task 3.1»).
2. Mapa de cobertura: objetivo oficial → sección que lo cubre. Sin filas sin cubrir. Formato comprobable con `scripts/comprobar_cobertura.py`: una tabla Markdown con una fila por objetivo de `fuentes/` cuya primera columna es su id (`1.2.3`, o `CP.1` en un módulo de conocimientos previos) y con un enlace `[texto](#ancla)` a un encabezado del mismo README:

   ```markdown
   | Objetivo | Descripción | Sección |
   |---|---|---|
   | 1.1.1 | Definir términos básicos de IA | [Términos básicos](#términos-básicos-de-ia) |
   ```

   Qué fuente cubre cada módulo se declara en el bloque `cobertura` de `curso.yaml`.
3. Teoría, con ejemplos de negocio y diagramas Mermaid donde aporten.
4. Puntos clave para el examen (5–10 viñetas).
5. Referencias oficiales.

## Calidad del contenido (obligatorio en todos los cursos)

Reglas surgidas de la revisión técnica de la iteración 1 de AIF-C01. Se aplican a todo módulo nuevo o modificado de cualquier curso:

- **Disponibilidad y nombres vigentes.** Antes de citar un producto o funcionalidad, abre su documentación oficial y busca avisos de retirada, de cierre a clientes nuevos, de modo de mantenimiento o de renombrado. Indícalo en la teoría, en `servicios.md` y en el glosario, y no lo presentes como la opción para proyectos nuevos.
- **Fuentes con fecha.** Si una guía o un documento antiguo choca con la documentación vigente del producto, prevalece la vigente.
- **Cada objetivo oficial, con cuatro piezas:** definición breve, criterio de decisión (tabla «escenario → producto o técnica»), ejemplo de negocio y trampa típica en `trampas.md`. Los matices que separan opciones parecidas (límites, exclusiones, modelo de facturación) se citan con su fuente.
- **Ejemplos resueltos.** Las métricas y los cálculos se explican con un ejemplo numérico, y los ciclos de vida con un caso de principio a fin.
- **Productos dentro de alcance.** Cuando un objetivo pide productos «por etapa» o «para un caso», revisa la lista oficial de alcance del curso y menciona los relevantes, no solo los del ejemplo de la guía.
- **Diagramas jerárquicos.** Las relaciones de inclusión se dibujan con `subgraph` anidados, no como una cadena de flechas que parezca un proceso.
- **Glosario.** Todo producto o concepto nuevo lleva su entrada. No uses como alias palabras comunes que aparezcan con otro sentido: usa la forma completa del nombre.
- **Laboratorios.** Distingue los permisos de consola de los de CLI, describe las condiciones vigentes de la capa gratuita del proveedor, recomienda una alerta de presupuesto antes de empezar e incluye preguntas de reflexión con respuestas orientativas.
- **Revisión independiente al cerrar cada módulo.** Comprueba los errores factuales contra la documentación, la suficiencia de cada objetivo para el examen, la calidad del banco con la lista de abajo y la didáctica para un perfil junior. Registra los cambios en `CHANGELOG.md`.

## Banco de preguntas

- Mínimos y distribución por tipos en `banco` de `curso.yaml`, comprobados por la CI (`minimo_por_modulo`, `minimo_por_tarea`, `minimo_por_objetivo`, `distribucion`). Como orientación, de 4 a 5 preguntas por objetivo; más en los objetivos de productos y de criterios de decisión.
- `id`: `D<dominio>-NNN`; en el simulacro, `S-NNN`. `objetivo` (recomendado: `N.M.K`) enlaza la pregunta con un objetivo oficial de su tarea. `tarea` debe existir en `cursos/<curso>/fuentes/dominio-N.md` y `dominio` en el manifiesto. `referencia`: URL https de una de las `fuentes_oficiales` del curso.
- Formato por tipo:

| Tipo | Opciones | `correctas` |
|---|---|---|
| `multiple_choice` | ≥4 (1 correcta y 3 distractores) | 1 id |
| `multiple_response` | ≥5 | ≥2 ids (hay que acertarlas todas) |
| `ordering` | ≥ nº de elementos | 3–5 ids **en orden**; sin `distractores` |
| `matching` | columna derecha; `prompts` en columna izquierda (3–7) | 3–7 pares `[prompt_id, opcion_id]`; `distractores` para las opciones sin par |

Los ids de `prompts` son números (`"1"`, `"2"`…, entre comillas en YAML) y los de `opciones` letras (`a`–`j`). Las opciones incorrectas de `multiple_*` y las no usadas en `matching` deben tener su explicación en `distractores`. El formato concreto de `matching` y `ordering` es una decisión de diseño de este repositorio, pendiente de confirmar ([issue #14](https://github.com/monghithub/certificaciones/issues/14)).

### Calidad del banco de preguntas

Todas las preguntas son de elaboración propia. Los conjuntos oficiales de práctica de cada proveedor sirven solo como referencia de estilo y de temas, nunca para copiar enunciados. Están prohibidos los *dumps* y las webs de terceros.

1. **Escenario de negocio con una restricción que decide:** «con el MENOR esfuerzo operativo», «de la forma MÁS rentable», «sin experiencia previa», «en milisegundos». La restricción debe ser la que descarta las opciones plausibles.
2. **Distractores plausibles del mismo terreno:** productos o técnicas vecinas que un candidato confundiría. Nada de opciones absurdas ni de categorías ajenas.
3. **Sin pistas:** el enunciado no copia la definición de la respuesta ni contiene su palabra clave. Los distractores no usan absolutos («siempre», «nunca», «cualquier», «garantiza»); el validador avisa.
4. **Posiciones repartidas:** la respuesta correcta de opción múltiple no puede estar en la misma letra en más del 40 % del banco; el validador falla. En respuesta múltiple, varía también las combinaciones.
5. **Explicaciones:** la correcta explica *por qué* encaja con la restricción del escenario; cada distractor explica por qué *en este escenario* no encaja.
6. **Dificultad real:** «alta» significa que dos opciones son plausibles y las separa un matiz del enunciado o de la documentación. Reparto orientativo: 20 % baja, 60 % media y 20 % alta.
7. **Datos verificados:** una pregunta no puede depender de un dato marcado como `PENDIENTE DE VERIFICAR`.
8. **Tras reordenar opciones**, comprueba que `correctas` y `distractores` siguen apuntando al texto correcto.

### Banco de repaso de conocimientos

Además del banco de examen, cada módulo de teoría tiene `repaso.yaml`: preguntas **directas** para fijar lo leído antes de pasar a los escenarios. La consola las ofrece como primer paso de la ruta de estudio y nunca las mezcla con los tests de examen ni con el simulacro.

- Mismo esquema y formato por tipo que el banco de examen. `id`: `R<módulo>-NNN`. Mínimos en el bloque `repaso` de `curso.yaml` (`minimo_por_modulo`, `minimo_por_objetivo`), comprobados por `comprobar_cobertura.py --preguntas`.
- **Conocimientos previos:** si `curso.yaml` declara `repaso.previos` (fuente con objetivos `CP.N`), el banco de repaso del módulo de base usa `dominio: 0`, `tarea: CP` y `objetivo: CP.N`. El dominio 0 solo se admite en bancos de repaso.
- **Una idea por pregunta**: un concepto, servicio, métrica o criterio. Se admiten enunciados cortos (no se aplica el aviso de «enunciado muy corto»).
- **Solo lo que dice la teoría del módulo:** cada pregunta se apoya en una afirmación ya verificada del módulo y cita la misma fuente oficial; no introduce datos nuevos.
- **Explicaciones que enseñan:** 2–4 frases con el concepto y una pista para recordarlo; cada distractor explica por qué no es la respuesta y qué es en realidad.
- Se mantienen las reglas 2, 3, 4, 7 y 8 de la calidad del banco de examen. El validador falla si un enunciado de repaso repite el de una pregunta de examen.

Antes de cada commit: `python scripts/validar_preguntas.py && python scripts/comprobar_cobertura.py --preguntas && python -m pytest`. Revisa también los `AVISO` del validador.

## Consola, glosario y diagramas

- **Consola.** Los usuarios se matriculan por curso; los roles `admin` y `estudiante` son globales. Las herramientas (`validar_preguntas.py`, `comprobar_cobertura.py`, `quiz.py`) aceptan `--curso`.
- **Glosario.** Cada curso tiene `cursos/<curso>/glosario.yaml`. **Todo producto o concepto clave que se introduzca en un módulo debe tener su entrada** (término, alias, categoría, definición breve, para productos «cuándo usarlo» y «cuándo no», y una `referencia` oficial). La consola convierte sus apariciones (la primera de cada apartado) en botones que abren un modal. `scripts/validar_preguntas.py` falla si un producto de la primera columna de un `servicios.md` no tiene entrada, o si hay ids, términos o alias duplicados. Define como alias las variantes que aparecen en el texto (plural, siglas, nombre corto); las siglas y los términos de 5 o menos caracteres distinguen mayúsculas.
- **Diagramas: estilo único en todo el proyecto.** El estilo (emojis, colores pastel por tipo, tema suave, animación) es **obligatorio** en todos los cursos y se comprueba en `scripts/validar_preguntas.py` y en la CI. Reglas:
  - Solo `flowchart` de Mermaid; sin `classDef`.
  - La etiqueta de **cada nodo y de cada subgrupo** empieza por un emoji; usa `<b>…</b>` para el título y `<br/>` para una segunda línea de explicación. Etiquetas cortas y siempre entre comillas.
  - Cada nodo lleva una clase semántica con `class A,B tipo`: `ia`, `ml`, `dl`, `gen` (familia de IA), `dato`, `proceso`, `servicio` (productos del proveedor), `accion`, `aviso` o `decision`.
  - **Cualquier caja debe dar información y enlaces al pulsarla.** Justo después del diagrama (solo líneas en blanco entre ambos) va un bloque ```` ```nodos ```` con un mapa YAML `id → información` que cubre **todos** los nodos y subgrupos. Cada entrada usa `concepto` (id de una entrada del glosario) y/o `titulo` + `texto`, y opcionalmente `usar_cuando`, `no_usar_cuando`, `enlaces` (`texto` y `url` https) y `seccion` (`modulo/seccion#ancla`, que se muestra como «Ver en el curso»). Los campos de la caja sustituyen a los del concepto y sus enlaces se suman a los del glosario.
  - Valida también la sintaxis Mermaid con `tests/e2e` (`node validar-mermaid.mjs ../../cursos/*/modulos/*/README.md`).

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

Objetivo y relación con tareas; requisitos (cuenta, región, accesos); pasos por consola y, si procede, CLI o SDK; **estimación de coste** con fuente oficial y aviso de facturación; **limpieza de recursos obligatoria**, con especial atención a los recursos que cobran por hora.

## Flujo de trabajo (OpenSpec)

1. **Proponer** cada etapa como un cambio de OpenSpec (`/opsx:propose`).
2. **Revisión humana** de la propuesta antes de implementar.
3. **Implementar** (`/opsx:apply`) en una rama propia, marcando las tareas.
4. **Verificar** con el validador, la cobertura, markdownlint, Mermaid y pytest.
5. **Revisión independiente** del contenido.
6. **Cerrar la etapa**: archivar el cambio (`/opsx:archive`), actualizar `CHANGELOG.md` y `docs/journal.md`, commit, push y PR a `main`.

Cada cierre incluye: ficheros creados o modificados, cobertura de tareas (cubiertas/totales), preguntas por tipo, marcadores pendientes abiertos y resultado de la CI.

## Git

- *Conventional Commits* con el ámbito del curso o del componente: `feat(aif-c01): ...`, `fix(preguntas): ...`, `feat(consola): ...`, `ci: ...`, `docs: ...`.
- Una rama por etapa, integrada en `main` con PR. Ramas nuevas: `<slug>/<etapa>` (por ejemplo, `aif-c01/modulo-03`) o `feat/<tema>` para lo común. Las ramas anteriores conservan su nombre.
- Versiones por curso con etiquetas `<slug>-vX.Y.Z` (por ejemplo, `aif-c01-v1.0.0`), solo con el curso completo, la CI en verde y sin marcadores `PENDIENTE DE VERIFICAR`.

## Journal

`docs/journal.md` es el diario de trabajo de todo el repositorio: al cerrar cada etapa se añade una entrada con fecha que recoja qué se hizo, qué se decidió y por qué, los cambios de OpenSpec y los commits, y lo que queda pendiente. El journal no sustituye a `CHANGELOG.md`, que solo dice qué cambia.
