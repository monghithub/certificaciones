## 1. Esquema, manifiesto y validación

- [ ] 1.1 Esquema: ids `R…`, dominio 0, tarea `CP` y objetivo `CP.N`
- [ ] 1.2 `curso.yaml` y `curso.schema.json`: bloque `repaso`; `Manifiesto` lo lee
- [ ] 1.3 `curso/cobertura.py` con el mapa objetivo → anclas; `comprobar_cobertura.py` lo usa y comprueba la cobertura del repaso
- [ ] 1.4 `validar_preguntas.py` valida `repaso.yaml` (esquema, ids únicos, dominio 0, mínimos, sin copiar enunciados de examen)
- [ ] 1.5 `quiz.py --repaso`

## 2. Consola

- [ ] 2.1 `Contenido` carga los bancos de repaso y el mapa objetivo → teoría
- [ ] 2.2 Modos repaso y repetir falladas
- [ ] 2.3 Explicación plegable con enlace a la teoría tras cada respuesta en todos los modos
- [ ] 2.4 Simulacro con modo estudio
- [ ] 2.5 Página de tests como ruta de estudio; estadísticas con «Conocimientos previos»
- [ ] 2.6 Pruebas (pytest y e2e)

## 3. Contenido

- [ ] 3.1 `repaso.yaml` de los módulos 00 a 05
- [ ] 3.2 Revisión independiente de los bancos de repaso

## 4. Documentación y cierre

- [ ] 4.1 `AGENTS.md` (reglas del banco de repaso), README del curso, `docs/consola.md`, CHANGELOG y journal
- [ ] 4.2 Validador, cobertura, markdownlint, pytest y e2e en verde
- [ ] 4.3 Commit, push, PR y archivo del cambio
