## 0. Revisión

- [x] 0.1 Revisión humana de la propuesta y respuesta a las «Open Questions» de `design.md` (aprobada el 2026-11-21)

## 1. Manifiesto

- [x] 1.1 `banco.minimo_simulacro_por_objetivo` (entero ≥ 0, opcional) en `schemas/curso.schema.json` y en `Manifiesto` (`curso/manifiesto.py`)
- [x] 1.2 Pruebas del manifiesto con y sin el campo (las de cobertura del simulacro lo declaran y lo omiten)

## 2. Composición del simulacro (`curso/simulacro.py`)

- [x] 2.1 `cuotas`: reparto por dominio con restos mayores y matriz dominio × tipo con `examen.distribucion` (D2, D3)
- [x] 2.2 `rotatorio` y `comprobar_banco` (errores por celda insuficiente y líneas de resumen con el reparto y las repeticiones inevitables)
- [x] 2.3 `extraer` con prioridades cuotas → objetivos sin repetir → no vistas → azar, reinicios y barajado final (D4); camino compatible con `sorted(ids)` (D7)
- [x] 2.4 `tests/test_simulacro.py`: cuotas de AIF-C01, propiedades de `cuotas`, 500 semillas sobre banco sintético, `evitar`, banco del tamaño del examen, banco infactible y determinismo con semilla

## 3. Consola

- [x] 3.1 `iniciar` (modo `simulacro`): `extraer` con `evitar` = preguntas del último intento de simulacro del usuario en el curso; error con `flash` si el banco no permite formar el examen
- [x] 3.2 `inicio` y `tests_inicio.html`: disponibilidad según `comprobar_banco` y texto del banco rotatorio
- [x] 3.3 Pruebas en `tests/app/test_app_quiz.py`: intento con las cuotas, rotación en el segundo intento, reanudar y resultado de un intento con la lista antigua, banco infactible; las pruebas actuales del simulacro siguen pasando sin cambios (`tests/app/test_app_simulacro.py`)

## 4. Validación, cobertura y CLI

- [x] 4.1 `validar_preguntas.py`: factibilidad del banco rotatorio, ids `S-NNN` solo en el simulacro y resumen por intento (D9)
- [x] 4.2 `comprobar_cobertura.py --preguntas`: cobertura de objetivos del banco del simulacro con `banco.minimo_simulacro_por_objetivo`
- [x] 4.3 `scripts/quiz.py --simulacro` con `extraer` y `--semilla`
- [x] 4.4 Pruebas en `tests/test_validar_preguntas.py`, `tests/test_cobertura.py` y `tests/test_quiz.py`
- [x] 4.5 Documentación técnica: `docs/consola.md` (simulacro rotatorio y rotación), `AGENTS.md` (banco del simulacro, ids `S-NNN` estables y no reutilizables, `minimo_simulacro_por_objetivo`)

## 5. Contenido del banco (tras integrar `aif-c01/simulacro-cobertura`)

- [x] 5.1 Recalcular sobre el banco resultante los objetivos sin cubrir y las preguntas que faltan por dominio y tipo (objetivo: 18/19/22/12/11 por dominio, con al menos 3/4/5/3/3 de respuesta múltiple; unas 17 nuevas)
- [x] 5.2 Redactar las preguntas nuevas `S-070` a `S-087` (18; ver journal): primero una por cada objetivo sin cubrir y después las de holgura por dominio; inéditas respecto a los bancos de los módulos, con escenario de negocio, distractores explicados y referencia oficial
- [x] 5.3 `cursos/aif-c01/curso.yaml`: `banco.minimo_simulacro: 80` y `banco.minimo_simulacro_por_objetivo: 1`
- [x] 5.4 `06-simulacro/README.md` (banco, reparto por intento, rotación, cómo repetirlo; deja de decir que el banco es fijo) y `cursos/aif-c01/README.md` y `README.md` (cifras)
- [ ] 5.5 Revisión independiente del contenido nuevo

## 6. Cierre

- [ ] 6.1 Validador, cobertura con `--preguntas`, pytest, markdownlint y Mermaid
- [ ] 6.2 Prueba manual en la consola: dos simulacros seguidos con el mismo usuario (reparto, rotación, resultado e historial)
- [ ] 6.3 Archivo del cambio, `CHANGELOG.md` y `docs/journal.md`, PR a `main`
