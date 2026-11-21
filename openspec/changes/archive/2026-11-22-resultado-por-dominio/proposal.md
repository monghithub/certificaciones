> Aprobado de antemano por el responsable («haz lo que creas que va a mejorar», 2026-11-22). Guía en `design.md`.

## Why

La página de resultado de un intento solo muestra el total y la lista de preguntas. El informe del examen real de AWS da el rendimiento por sección, y es lo que dice al estudiante qué repasar. Las estadísticas ya tienen tablas por dominio y tarea, pero acumulan todos los intentos: tras un simulacro no se ve cómo ha ido ese intento por dominio.

## What Changes

- **Resultado por dominio** en la página de resultado de cualquier intento, antes de la lista de preguntas: aciertos/total, porcentaje y nombre del dominio (de `curso.yaml`), con una fila de total que cuadra con el resultado del intento.
- **Desglose por tarea**, plegable, debajo de la tabla.
- **Enlaces a la teoría:** cada dominio enlaza con la teoría de su módulo (bloque `cobertura` de `curso.yaml`) y cada tarea, con la sección de su primer objetivo en el mapa de cobertura.
- **En el simulacro:** se marcan los dominios por debajo del porcentaje global del intento (criterio relativo; AWS no publica cortes por sección), con un texto que lo explica y un «Para repasar primero».
- **Casos:** las sin responder cuentan como falladas; las preguntas retiradas van en una fila propia; las de los libros sin dominio oficial, en «Sin dominio oficial»; el dominio 0 (conocimientos previos) del repaso, con su nombre.
- Documentación: `docs/consola.md`, CHANGELOG y journal.

## Capabilities

### New Capabilities

- `resultado-por-dominio`: desglose del resultado de un intento por dominio y por tarea, con enlaces a la teoría y dominios débiles en el simulacro.

### Modified Capabilities

- Ninguna.

## Impact

- Código: `app/stats.py` (`desglose_intento`), `app/content.py` (`url_dominio`, `url_tarea`), `app/routes/quiz.py` (`resultado`), `app/templates/resultado.html`. Sin CSS nuevo: reutiliza `tablawrap`, `barra`, `mal-t`, `suave` y `details.explicacion`.
- Pruebas: `tests/app/test_app_resultado.py` (nuevo).
- Base de datos: sin cambios.
