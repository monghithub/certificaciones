> Guía de implementación en `design.md`. Aprobada por el responsable el 2026-11-21; el código está implementado y el contenido del banco (tarea 5) espera a la fusión del PR #52.

## Why

El simulacro de AIF-C01 son 65 preguntas fijas (`cursos/aif-c01/modulos/06-simulacro/preguntas.yaml`) que salen siempre en el mismo orden (`sorted(ids)[:65]` en `app/routes/quiz.py`). Tiene dos problemas:

- **No puede cubrir todos los objetivos oficiales.** La guía tiene 69 objetivos (17 en el Dominio 1, 14 en el 2, 19 en el 3, 11 en el 4 y 8 en el 5) y el reparto por pesos da 13/16/18/9/9 preguntas: el Dominio 1 tiene 4 objetivos más que preguntas, el 3 uno más y el 4 dos más. Con 65 preguntas fijas, el máximo alcanzable es 62 objetivos; hoy se cubren 58.
- **Repetirlo mide la memoria, no la preparación.** El propio README del simulacro lo advierte («el banco es fijo»).

## What Changes

- **Banco rotatorio.** El simulacro pasa a ser un banco mayor que el examen (82 preguntas previstas para AIF-C01) que cubre **todos** los objetivos oficiales. Cada intento extrae `examen.preguntas` (65) al azar.
- **Reparto en cada intento:** por dominio según los pesos de `dominios` (restos mayores: 13/16/18/9/9, calculado, no declarado) y por tipo según `examen.distribucion` (80/20: 52 de opción múltiple y 13 de respuesta múltiple), con un reparto por dominio y tipo determinista. Dentro de cada dominio, sin repetir objetivo salvo cuando el banco lo haga inevitable. Orden aleatorio.
- **Rotación entre intentos:** a igualdad de lo anterior, se prefieren las preguntas que no salieron en el intento de simulacro anterior del mismo usuario. Con 82 preguntas, dos intentos seguidos ven el banco completo.
- **Sin migración.** `Intento.preguntas` ya guarda los ids en orden; reanudar, resultado, historial, estadísticas, falladas y consultas siguen igual. Los intentos antiguos no cambian.
- **Compatibilidad:** si el banco tiene exactamente `examen.preguntas` preguntas, el simulacro se comporta como hoy (todas, en el orden de los ids, sin comprobar el reparto). Lo mismo vale para AIF-C01 hasta que se amplíe el banco.
- **Módulo compartido `curso/simulacro.py`** (cuotas, comprobación del banco y extracción), usado por la consola, el validador y `scripts/quiz.py --simulacro`.
- **Validador y CI:**
  - `validar_preguntas.py`: error si un banco mayor que el examen no permite formar un examen válido (preguntas insuficientes en algún dominio y tipo); error si un id del simulacro no es `S-NNN` o un `S-NNN` aparece fuera del simulacro; resumen con el reparto por intento y las repeticiones de objetivo inevitables.
  - `comprobar_cobertura.py --preguntas`: cobertura de los objetivos oficiales en el banco del simulacro con el mínimo `banco.minimo_simulacro_por_objetivo` (nuevo, opcional; AIF-C01 declara 1).
- **Manifiesto:** `banco.minimo_simulacro_por_objetivo` en `schemas/curso.schema.json` y `curso/manifiesto.py`. AIF-C01 sube `banco.minimo_simulacro` de 65 a 80.
- **Contenido (tarea posterior, tras integrar la rama `aif-c01/simulacro-cobertura`):** redactar unas 17 preguntas nuevas `S-070`… para llegar a 82 (18/19/22/12/11 por dominio, con al menos 3/4/5/3/3 de respuesta múltiple) y cubrir los objetivos que falten.
- **Documentación:** README del simulacro y del curso, `docs/consola.md`, `AGENTS.md`, página de tests de la consola, CHANGELOG y journal.

## Capabilities

### New Capabilities

- `simulacro-rotatorio`: composición de cada intento del simulacro a partir de un banco mayor que el examen (reparto, objetivos, rotación, compatibilidad y reproducibilidad).

### Modified Capabilities

- `simulacro-aif-c01`: el simulacro de AIF-C01 es un banco de al menos 80 preguntas que cubre los 69 objetivos.
- `quiz-engine`: el simulacro cronometrado usa la composición por intento y el número de preguntas del manifiesto.
- `question-validation`: banco del simulacro suficiente para formar un examen e ids `S-NNN`.
- `comprobacion-cobertura`: cobertura de objetivos del banco del simulacro.
- `catalogo-cursos`: `banco.minimo_simulacro_por_objetivo` en el manifiesto.
- `quiz-cli`: opción `--simulacro` con la misma composición que la consola.

## Impact

- Código: `curso/simulacro.py` (nuevo), `curso/manifiesto.py`, `schemas/curso.schema.json`, `app/routes/quiz.py` (`iniciar`, `inicio`), `app/templates/tests_inicio.html`, `scripts/validar_preguntas.py`, `scripts/comprobar_cobertura.py`, `scripts/quiz.py`.
- Pruebas: `tests/test_simulacro.py` (nuevo), `tests/test_validar_preguntas.py`, `tests/test_cobertura.py`, `tests/test_quiz.py`, `tests/app/test_app_quiz.py`; `tests/conftest.py` mantiene su simulacro de 3 preguntas con examen de 3 (camino compatible) y se añade un banco mayor.
- Base de datos: sin cambios ni migración.
- Contenido: `cursos/aif-c01/curso.yaml`, `cursos/aif-c01/modulos/06-simulacro/preguntas.yaml` (+17 aprox.) y su `README.md`, `cursos/aif-c01/README.md`.
- Dependencia: el contenido parte del resultado de la rama `aif-c01/simulacro-cobertura`; el código no depende de ella.
