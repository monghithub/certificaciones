## Why

La guía vigente del examen AIF-C01 (versión 1.2, 29 de octubre de 2026) dice en «Response types» que el examen tiene **dos tipos de pregunta: opción múltiple y respuesta múltiple**. El simulacro del curso reproducía cuatro tipos (también ordenación y emparejamiento), siguiendo el anuncio de AWS de 2024. Issue [#45](https://github.com/monghithub/certificaciones/issues/45).

## What Changes

- **Simulacro:** las 11 preguntas de ordenación y emparejamiento se sustituyen por 7 de opción múltiple y 4 de respuesta múltiple sobre los mismos objetivos, con el mismo reparto por dominio (13/16/18/9/9). Queda en 51 de opción múltiple y 14 de respuesta múltiple.
- **Manifiesto:** `examen.tipos` (tipos que enumera la guía oficial) y `examen.distribucion` (reparto orientativo del simulacro), opcionales, en `schemas/curso.schema.json` y `curso/manifiesto.py`. AIF-C01 declara `[multiple_choice, multiple_response]` y 80/20.
- **Validador:** error si el simulacro usa un tipo que no está en `examen.tipos` o si `examen.distribucion` usa un tipo no declarado; el aviso de reparto del simulacro usa `examen.distribucion` si existe.
- **Bancos de los módulos:** sin cambios; la ordenación y el emparejamiento siguen como práctica (`banco.distribucion`).
- Documentación: README del curso y del simulacro, chuleta, `AGENTS.md`, CHANGELOG y journal.

## Capabilities

### Modified Capabilities
- `simulacro-aif-c01`: el simulacro usa solo los tipos que enumera la guía oficial.
- `question-validation`: comprobación de los tipos del simulacro frente al manifiesto.

## Impact

- Código: `schemas/curso.schema.json`, `curso/manifiesto.py`, `scripts/validar_preguntas.py`, `tests/test_validar_preguntas.py` (5 pruebas nuevas) y `tests/app/test_app_quiz.py` (una prueba que quitaba el bloque `examen` con un reemplazo de texto pasa a hacerlo leyendo el YAML).
- Contenido: `cursos/aif-c01/curso.yaml`, `cursos/aif-c01/modulos/06-simulacro/`.
- La consola no cambia: ya admite los cuatro tipos y el simulacro solo deja de usar dos.
