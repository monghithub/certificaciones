## Why

El estilo de diagramas actual (emojis, colores semánticos, tema suave, animación) gusta y debe mantenerse en todo el proyecto, pero hoy solo depende de la disciplina de quien escribe. Además, solo las cajas cuyo texto coincide con un término del glosario abren el modal, y la coincidencia automática puede elegir un concepto equivocado (p. ej., «IA generativa… modelos fundacionales» abre «modelo fundacional»). El estudiante necesita que **cualquier caja** de **cualquier diagrama** le dé información y enlaces.

## What Changes

- **Información en todas las cajas.** Cada diagrama va acompañado de un bloque `nodos` (YAML) que asocia a **cada nodo y cada subgrupo** su información: `concepto` (reutiliza una entrada del glosario) y/o `titulo`, `texto`, `usar_cuando`, `no_usar_cuando`, `enlaces` y `seccion` (enlace interno al curso). Al pulsar una caja se abre el modal con esa información y sus enlaces.
- **Enlaces en el modal**: lista de enlaces (documentación oficial y otros) para conceptos y cajas; los externos abren en pestaña nueva y los internos (`seccion`) llevan al apartado del curso. Las entradas del glosario admiten `enlaces` adicionales a `referencia`.
- **Sin coincidencia automática en diagramas**: lo que abre cada caja lo decide el autor de forma explícita.
- **Estilo obligatorio y validado**: `validar_preguntas.py` comprueba, en todo Markdown de los cursos, que cada diagrama es un `flowchart`, que cada etiqueta empieza por un emoji, que cada nodo tiene una clase semántica válida, que no se usa `classDef` y que **cada caja tiene información** (`nodos`), con `concepto` existente, URL `https` y `seccion` válida. Un incumplimiento es un error de validación (y del CI).
- **Anclas en los encabezados** del contenido renderizado, para que los enlaces internos (`#ancla`, p. ej. el mapa de cobertura) y los de `seccion` funcionen en la consola.
- Se añaden los bloques `nodos` a los 5 diagramas actuales, con enlaces a la documentación oficial ya consultada.
- Fuera de alcance: diagramas que no sean `flowchart`, edición de la información desde la web.

## Capabilities

### New Capabilities
- `info-en-cajas`: información y enlaces en cualquier caja de un diagrama (formato `nodos`, resolución, modal con enlaces y anclas).
- `estilo-de-diagramas`: reglas de estilo de los diagramas y su validación automática.

### Modified Capabilities
<!-- Amplía las capacidades `conceptos-interactivos`, `diagramas-amigables` y `glosario-conceptos` del cambio anterior (aún sin archivar). -->

## Impact

- Código: `app/content.py` (fence `nodos`, anclas, datos), `curso/glosario.py` (enlaces), nuevo `curso/diagramas.py` y `curso/anclas.py`, `scripts/validar_preguntas.py` y `scripts/comprobar_cobertura.py` (anclas compartidas), `app/static/app.js`, `app.css`, `base.html`, `schemas/glosario.schema.json`.
- Contenido: bloques `nodos` en los diagramas de los módulos 00 y 01 y, si procede, `enlaces` en el glosario.
- Cambio de comportamiento: un diagrama sin información en alguna caja deja de validar.
