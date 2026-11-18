## Context

Cada pregunta tiene `objetivo` y el mapa de cobertura de cada README asocia cada objetivo a un ancla de `teoria` (`Contenido.teoria`: objetivo → (módulo, ancla); lo usa ya «Repasar en la teoría»). Los encabezados de las secciones tienen `id`. La CSP solo permite scripts propios (`script-src 'self'`), y la interacción está en `app/static/app.js`, sin dependencias. Las peticiones que modifican llevan el token CSRF en `X-CSRF-Token` (`hx-headers` del `<body>`).

## Goals / Non-Goals

**Goals:**
- Preguntarle al estudiante por lo que está leyendo, con un solo clic, y encadenar preguntas hasta que cierre.
- Reutilizar los bancos, la corrección (`curso/correccion.py`) y la presentación de la solución (`legible`) de los tests.

**Non-Goals:**
- Aparición automática por tiempo (el usuario prefiere abrirlo él).
- Guardar respuestas, estadísticas o falladas.
- Preguntas nuevas: se usan los bancos existentes.

## Decisions

- **Apartado visible en el cliente, elección en el servidor.** `app.js` busca en el `<article>` el último encabezado (`h2`–`h4` con `id`) cuya parte superior queda por encima del centro de la ventana y sube por sus padres (encabezados de nivel menor anteriores). Envía esa cadena de anclas, de la más concreta a la más general. El servidor recorre las anclas y usa la primera que tenga preguntas disponibles; si ninguna tiene, el módulo. Así un subapartado `h4` sin objetivo propio hereda el del `h3` que lo contiene.
- **Índice inverso en `Contenido`:** (módulo, ancla) → objetivos, construido con el mapa de cobertura completo (todas las anclas de cada objetivo, no solo la primera).
- **Sin estado en el servidor.** El cliente guarda en memoria los ids ya vistos mientras la página está abierta y los manda en `excluir`. Si se agotan todas las del módulo, se vuelve a empezar y el modal lo avisa. No hay tablas ni migración.
- **Dos rutas JSON** bajo `/c/{curso}/lectura/`: `GET pregunta?modulo=&anclas=&excluir=` devuelve la pregunta sin solución (como `_vista_pregunta`) y `POST corregir` recibe el id y la respuesta con los mismos campos que el formulario de los tests (`r`, `o1…`, `m_<id>`), la valida con `_leer_respuesta` y devuelve la corrección. Ambas exigen matrícula (`requiere_curso`) y rechazan el simulacro y los ids que no pertenecen al módulo pedido. El POST pasa por la comprobación CSRF.
- **Pintado con `textContent`** en `app.js`: el texto de las preguntas nunca se inserta como HTML.
- **Modal `<dialog>` propio** (`#modal-pregunta`), con el mismo estilo que el del glosario, foco en el enunciado al abrir y devuelto al botón al cerrar. Botón fijo abajo a la derecha, visible en móvil.

## Risks / Trade-offs

- [El mapa de cobertura no cubre todas las anclas] → se sube por los encabezados padres y, si nada coincide, se pregunta del módulo indicándolo.
- [Una pregunta de examen puede adelantar contenido de apartados posteriores] → se prioriza el repaso del apartado; las de examen solo cuando se agotan las de repaso de ese apartado.
- [Responder sin registro no deja rastro del progreso] → decisión del usuario; los tests siguen registrando.

## Open Questions

- Ninguna bloqueante.
