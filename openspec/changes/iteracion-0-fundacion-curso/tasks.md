## 1. Verificación de la guía oficial

- [x] 1.1 Consultar la página principal de la guía AIF-C01 y contrastar los datos de la sección 4 de `promt.md` (duración, preguntas, puntuación, tipos, coste, validez, pesos)
- [x] 1.2 Consultar `aif-01-revisions.html` y registrar la versión/fecha vigente de la guía
- [x] 1.3 Registrar el resultado (coincidencias y discrepancias) para `CHANGELOG.md`

## 2. Transcripción de fuentes oficiales

- [x] 2.1 Crear `fuentes/dominio-1.md` con URL, fecha de consulta y Task Statements/habilidades literales (encabezados `## Task Statement 1.M`)
- [x] 2.2 Crear `fuentes/dominio-2.md` (mismo formato)
- [x] 2.3 Crear `fuentes/dominio-3.md` (mismo formato)
- [x] 2.4 Crear `fuentes/dominio-4.md` (mismo formato)
- [x] 2.5 Crear `fuentes/dominio-5.md` (mismo formato)
- [x] 2.6 Crear `fuentes/servicios-alcance.md` con servicios in scope y out of scope (URL y fecha)
- [x] 2.7 Marcar con `> ⚠️ PENDIENTE DE VERIFICAR:` cualquier dato no accesible o dudoso

## 3. Estructura y documentación base

- [x] 3.1 Crear directorios `modulos/00-base-aws` … `modulos/06-simulacro`, `schemas/`, `scripts/`, `.github/workflows/` (con `.gitkeep` donde proceda)
- [x] 3.2 Escribir `README.md` (presentación, índice, cómo estudiar, plan de 4 semanas, datos revalidados, recomendación de examen de práctica de Skill Builder)
- [x] 3.3 Escribir `AGENTS.md` (reglas de `promt.md`, formato de ordering/matching, convenciones Git, flujo por iteraciones)
- [x] 3.4 Escribir `CHANGELOG.md` con la Iteración 0 y las discrepancias detectadas en 1.3
- [x] 3.5 Añadir `LICENSE` (confirmar licencia con el revisor; por defecto MIT código / CC BY 4.0 contenido)
- [x] 3.6 Añadir `.markdownlint-cli2.yaml`, `.lychee.toml`, `.gitignore` y `requirements.txt` (pyyaml, jsonschema, pytest)

## 4. Esquema y validador

- [x] 4.1 Crear `schemas/pregunta.schema.json` cubriendo los cuatro tipos (incl. `prompts` para matching y rangos de ordering/matching)
- [x] 4.2 Crear fixtures en `tests/fixtures/` (válidos de los cuatro tipos e inválidos: id duplicado, correctas inexistentes, nº de correctas incoherente, tarea inexistente, distractor sin explicar, "todas las anteriores")
- [x] 4.3 Implementar `scripts/validar_preguntas.py` (esquema, unicidad, referencias, coherencia por tipo, tarea en fuentes, distractores, mínimos, distribución, `--sin-minimos`, código de salida)
- [x] 4.4 Escribir `tests/test_validar_preguntas.py` y ejecutarlos en local

## 5. Quiz interactivo

- [x] 5.1 Implementar `scripts/quiz.py` con carga, filtros (`--modulo`, `--dominio`, `--tipo`, `--n`, `--semilla`), presentación y corrección de los cuatro tipos
- [x] 5.2 Escribir `tests/test_quiz.py` para las funciones de corrección y filtrado
- [x] 5.3 Probar manualmente el quiz con un fixture válido

## 6. Integración continua

- [x] 6.1 Crear `.github/workflows/ci.yml` (markdownlint, lychee, tests + `validar_preguntas.py`, aviso de `PENDIENTE DE VERIFICAR`)
- [x] 6.2 Ejecutar en local markdownlint y el validador sobre el repositorio y corregir incidencias

## 7. Cierre de la iteración

- [x] 7.1 Generar el resumen de cierre (ficheros, cobertura de tareas transcritas, preguntas por tipo = 0, marcadores PENDIENTE abiertos, resultado de scripts en local)
- [x] 7.2 Detenerse para revisión humana antes de la Iteración 1
