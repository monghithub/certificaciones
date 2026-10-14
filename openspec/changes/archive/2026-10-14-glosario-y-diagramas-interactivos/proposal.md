## Why

El material se estudia en la consola, pero hoy los conceptos y servicios son texto plano: un estudiante junior que se topa con «Amazon Bedrock», «RAG» o «F1» tiene que salir del módulo para entenderlos. Los diagramas Mermaid son correctos pero fríos y estáticos. Se quiere que estudiar sea más amable: pulsar cualquier concepto clave y ver su explicación al instante, y diagramas más vistosos y con movimiento suave. Debe valer para **todos los cursos**, siempre, sin tocar código cada vez.

## What Changes

- **Glosario por curso** (`cursos/<curso>/glosario.yaml`): conceptos y servicios con término, alias, categoría, definición breve, cuándo usarlo y cuándo no (opcional) y enlace a la documentación oficial. Con su JSON Schema y validación (ids únicos, alias sin colisiones, URL válida) y una comprobación de que todo servicio listado en un `servicios.md` tiene entrada.
- **Conceptos pulsables en el contenido**: al renderizar cualquier sección, la consola detecta los términos del glosario (en la primera aparición de cada apartado) y los convierte en botones que abren un **modal** accesible (teclado, `Esc`, foco, móvil, modo oscuro) con la definición y el enlace oficial.
- **Página de glosario** del curso (`/c/<curso>/glosario`) con buscador; cada entrada abre el mismo modal.
- **Diagramas más amables y animados**: tema propio de Mermaid (colores suaves, bordes redondeados, tipografía legible, modo claro y oscuro), clases semánticas para colorear por tipo de elemento, aparición escalonada de los nodos, flujo animado en las flechas y efecto al pasar el ratón. Respetan `prefers-reduced-motion`. Los nodos de los diagramas cuyo texto sea un concepto del glosario también abren el modal.
- Se **reescriben los 5 diagramas actuales** con las nuevas clases y etiquetas más claras, y se crea el glosario inicial del curso AIF-C01 para los módulos 00 y 01.
- Reglas para autores en `AGENTS.md` y `docs/consola.md`: todo servicio o concepto clave nuevo entra en el glosario, y cómo escribir diagramas con las clases semánticas.
- Fuera de alcance: glosario bilingüe generado para `glosario.md` (Iteración 6; la fuente será este YAML), modales en las preguntas de los tests, edición del glosario desde la web.

## Capabilities

### New Capabilities
- `glosario-conceptos`: formato, validación y contenido del glosario por curso, y la página de glosario.
- `conceptos-interactivos`: detección de conceptos en el contenido, modal accesible y nodos de diagrama pulsables.
- `diagramas-amigables`: tema, clases semánticas, animación y accesibilidad de los diagramas Mermaid.

### Modified Capabilities
<!-- Ninguna: las capacidades anteriores aún no están archivadas en openspec/specs/. -->

## Impact

- Código: `app/content.py` (transformación del Markdown y carga del glosario), `app/routes/course.py` (página de glosario), `app/static/app.js` y `app/static/app.css`, `app/templates/base.html`, `seccion.html` y una plantilla nueva; `scripts/validar_preguntas.py` (o un script hermano de validación del glosario), `schemas/glosario.schema.json`.
- Contenido: `cursos/aif-c01/glosario.yaml` nuevo y retoques en los 5 diagramas de los módulos 00 y 01.
- Pruebas: tests unitarios del renderizado y del validador, y una prueba de navegador (Chrome sin interfaz) con capturas.
- Sin cambios de base de datos ni de dependencias de producción. Las páginas que ya no cargan JavaScript siguen mostrando el texto y los diagramas como código/texto legible.
