## 1. Esquema, manifiesto y validación

- [x] 1.1 Esquema: ids `R…`, dominio 0, tarea `CP` y objetivo `CP.N`
- [x] 1.2 `curso.yaml` y `curso.schema.json`: bloque `repaso`; `Manifiesto` lo lee
- [x] 1.3 `curso/cobertura.py` con el mapa objetivo → anclas; `comprobar_cobertura.py` lo usa y comprueba la cobertura del repaso
- [x] 1.4 `validar_preguntas.py` valida `repaso.yaml` (esquema, ids únicos, dominio 0, mínimos, sin copiar enunciados de examen)
- [x] 1.5 `quiz.py --repaso`

## 2. Consola

- [x] 2.1 `Contenido` carga los bancos de repaso y el mapa objetivo → teoría
- [x] 2.2 Modos repaso y repetir falladas
- [x] 2.3 Explicación plegable con enlace a la teoría tras cada respuesta en todos los modos
- [x] 2.4 Simulacro con modo estudio
- [x] 2.5 Página de tests como ruta de estudio; estadísticas con «Conocimientos previos»
- [x] 2.6 Pruebas (pytest y e2e)

## 3. Contenido

- [x] 3.1 `repaso.yaml` de los módulos 00 a 05
- [x] 3.2 Revisión independiente de los bancos de repaso

## 4. Documentación y cierre

- [x] 4.1 `AGENTS.md` (reglas del banco de repaso), README del curso, `docs/consola.md`, CHANGELOG y journal
- [x] 4.2 Validador, cobertura, markdownlint, pytest y e2e en verde
- [x] 4.3 Commit, push, PR y archivo del cambio
