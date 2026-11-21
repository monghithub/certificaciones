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

El desglose por tarea se muestra si hay al menos una tarea oficial (`N.M` de un dominio del manifiesto, o `CP`) y **también suma el total**: las preguntas sin tarea oficial van en «Sin tarea oficial» y las retiradas, en su fila. Una tarea cuenta en su propia fila aunque la pregunta declare otro dominio: `validar_preguntas.py` ya da error si la tarea no pertenece al dominio en los bancos de examen, repaso y simulacro, así que solo puede pasar con los libros, y la tarea pertenece a su dominio en las fuentes.

Tipos: `desglose_intento` solo acepta como dominio un entero (no un bool ni una lista) y como tarea una cadena; lo demás va a «Sin dominio oficial» o «Sin tarea oficial». Además, `_cargar_libros` convierte un dominio `1.0` en `1` y descarta, con aviso en el registro, las preguntas con un dominio o una tarea de otro tipo.

### D3. Dominios débiles: criterio relativo, solo en el simulacro

AWS no publica el corte por sección: el examen se puntúa de 100 a 1000 con aprobado en 700, y el informe solo dice «Meets competencies» o «Needs improvement» por sección. No se inventa un umbral. Se marcan los dominios oficiales cuyo porcentaje **mostrado** (redondeado) queda por debajo del porcentaje global mostrado, y la página lo explica. Se compara lo que se ve para no marcar «69 % frente a 69 %» (la primera versión comparaba fracciones exactas; corregido tras la revisión). El texto calcula el rango de preguntas por dominio del intento y usa `proveedor` del manifiesto (genérico si no lo hay); la frase de «Meets competencies» solo sale con AWS. Si todos los dominios están en la media o por encima, no se marca ninguno.

- Solo en el simulacro: en los tests cortos (10 preguntas de un dominio o mixtos) la marca sería ruido.
- Las tareas no se marcan: con 2 a 7 preguntas por tarea en un simulacro, la diferencia con la media no significa nada.

*Descartado:* umbral fijo del 70 % (parece oficial y no lo es; las estadísticas lo usan para «puntos débiles» acumulados, con otra finalidad). *Descartado:* «los N peores» (marca dominios aunque vayan bien).

### D4. Enlaces a la teoría

- Dominio: `Contenido.url_dominio(d)` busca en `cobertura` el módulo cuya fuente es `dominio-d.md` (o `repaso.previos` para el dominio 0) y enlaza con su sección `teoria`, si existe.
- Tarea: `Contenido.url_tarea(t)` toma el primer objetivo de la tarea (orden numérico: `1.2.2` antes que `1.2.10`) que tenga sección en el mapa de cobertura y usa `url_teoria`.
- Se muestran en todos los modos (no estorban y sirven igual), aunque el texto que invita a usarlos solo aparece en el simulacro.

### D5. Una sola fuente para el total

El total de la cabecera, el pie de la tabla y el texto salen del desglose (`desglose.ok`, `desglose.total`, `desglose.pct`), no de `i.respuestas`.

### D6. Presentación

Tarjeta «Resultado por dominio» antes de la lista de preguntas, con las clases de `_estadisticas.html` (`tablawrap`, `barra`) y `details.explicacion` para el plegable, así que funciona en móvil (tabla con desplazamiento) y en los dos temas sin CSS nuevo. Pie de tabla con el total (`th scope="row"` y celdas `td`), `caption` y cabecera de la barra solo para lectores de pantalla (`sr-only`) y barra con `aria-hidden`. Si hay preguntas sin responder, una línea lo recuerda; las retiradas se mencionan aparte y no cuentan como «sin responder».

## Risks / Trade-offs

- [Pocas preguntas por dominio] → el texto lo dice; el criterio es relativo y solo informativo.
- [Una tarea sin objetivo en el mapa de cobertura] → la fila sale sin enlace.

## Revisión independiente (2026-11-22)

Nada crítico; las 21 URLs de dominio y tarea dan 200 con anclas existentes. Correcciones menores aplicadas: tipos de `dominio` y `tarea` en los libros, marca con el porcentaje mostrado, texto con el rango real y el proveedor, retiradas fuera de «sin responder», tareas que suman, una sola fuente para el total, accesibilidad de las tablas y pruebas más estrictas (enlaces y anclas reales, reparto calculado con `simulacro.cuotas_dominio`, redondeo, tipos raros, tarea de otro dominio y orden «1.10» frente a «1.2»).

## Open Questions

Ninguna.
