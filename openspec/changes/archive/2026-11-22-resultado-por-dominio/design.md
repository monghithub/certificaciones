## Context

- `app/routes/quiz.py:resultado` arma `filas` (una por id de `i.preguntas`, con la pregunta o «retirada») y `ok` (respuestas correctas). `IntentoRespuesta` guarda `dominio` y `tarea` de cada respuesta, pero no hay fila para las preguntas sin responder.
- `app/stats.py:aciertos_por` y `_estadisticas.html` ya muestran aciertos por dominio y por tarea, acumulados de todos los intentos y solo de las respuestas dadas.
- `Contenido.url_teoria(objetivo)` lleva a la sección de un objetivo según los mapas de cobertura. `curso.yaml` asocia en `cobertura` cada módulo con su fuente (`dominio-N.md` o la de conocimientos previos).
- Preguntas de los libros (`libros.yaml`): `dominio` opcional (0 por defecto) y `tarea: libros`. Repaso: dominio 0 y tarea `CP` para los conocimientos previos.

## Goals / Non-Goals

**Goals:** ver en el resultado de cada intento cómo ha ido por dominio y por tarea, con el total cuadrado, y saber qué teoría repasar.

**Non-Goals:** simular la escala 100–1000 ni los cortes oficiales; cambiar las estadísticas acumuladas; guardar el desglose en la base de datos.

## Decisions

### D1. Calculado desde `i.preguntas`, no desde las respuestas

`stats.desglose_intento(i, contenido)` recorre `i.preguntas` y busca cada id en el contenido: así las sin responder cuentan como falladas y la suma de los grupos es exactamente `len(i.preguntas)` y los aciertos, `ok`. *Descartado:* agrupar `IntentoRespuesta` por dominio, como `aciertos_por` (no ve las sin responder y el total no cuadraría).

### D2. Grupos

- Dominio oficial del manifiesto: su fila, «Dominio N · nombre».
- Dominio 0 con tarea `CP` en un curso con `repaso.previos`: «Conocimientos previos».
- Cualquier otra (libros sin dominio oficial): «Sin dominio oficial». Las de los libros con un dominio oficial cuentan en ese dominio; su tarea `libros` no entra en el desglose por tarea.
- Ids que ya no existen: «Preguntas retiradas del contenido», con su acierto si se respondieron. Nunca se marcan como débiles ni tienen enlace.

El desglose por tarea solo incluye tareas oficiales (`N.M` del dominio o `CP`); es un detalle y no tiene que sumar el total.

### D3. Dominios débiles: criterio relativo, solo en el simulacro

AWS no publica el corte por sección: el examen se puntúa de 100 a 1000 con aprobado en 700, y el informe solo dice «Meets competencies» o «Needs improvement» por sección. No se inventa un umbral. Se marcan los dominios oficiales cuyo porcentaje queda **por debajo del porcentaje global del intento** (comparación exacta con enteros: `ok_d · total < ok · n_d`), y la página lo explica. Si todos los dominios están en la media o por encima, no se marca ninguno.

- Solo en el simulacro: en los tests cortos (10 preguntas de un dominio o mixtos) la marca sería ruido.
- Las tareas no se marcan: con 2 a 7 preguntas por tarea en un simulacro, la diferencia con la media no significa nada.

*Descartado:* umbral fijo del 70 % (parece oficial y no lo es; las estadísticas lo usan para «puntos débiles» acumulados, con otra finalidad). *Descartado:* «los N peores» (marca dominios aunque vayan bien).

### D4. Enlaces a la teoría

- Dominio: `Contenido.url_dominio(d)` busca en `cobertura` el módulo cuya fuente es `dominio-d.md` (o `repaso.previos` para el dominio 0) y enlaza con su sección `teoria`, si existe.
- Tarea: `Contenido.url_tarea(t)` toma el primer objetivo de la tarea (orden numérico: `1.2.2` antes que `1.2.10`) que tenga sección en el mapa de cobertura y usa `url_teoria`.
- Se muestran en todos los modos (no estorban y sirven igual), aunque el texto que invita a usarlos solo aparece en el simulacro.

### D5. Presentación

Tarjeta «Resultado por dominio» antes de la lista de preguntas, con las clases de `_estadisticas.html` (`tablawrap`, `barra`) y `details.explicacion` para el plegable, así que funciona en móvil (tabla con desplazamiento) y en los dos temas sin CSS nuevo. Pie de tabla con el total. Si hay preguntas sin responder, una línea lo recuerda.

## Risks / Trade-offs

- [Pocas preguntas por dominio] → el texto lo dice; el criterio es relativo y solo informativo.
- [Una tarea sin objetivo en el mapa de cobertura] → la fila sale sin enlace.

## Open Questions

Ninguna.
