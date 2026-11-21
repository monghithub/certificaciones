## Context

Guía de implementación autocontenida. Las decisiones marcadas como **pendientes de revisión** se confirman con el responsable antes de implementar.

### Estado de partida (2026-11-21, `main` en `b7ffcfa`)

- **Manifiesto** (`cursos/aif-c01/curso.yaml`): `dominios` con pesos 20/24/28/14/14, `simulacro: 06-simulacro`, `examen: {preguntas: 65, minutos: 90, tipos: [multiple_choice, multiple_response], distribucion: {multiple_choice: 80, multiple_response: 20}}`, `banco.minimo_simulacro: 65`. Lo lee `curso/manifiesto.py` (`Manifiesto.examen_preguntas`, `examen_tipos`, `examen_distribucion`, `minimo_simulacro`) y lo valida `schemas/curso.schema.json`.
- **Carga** (`app/content.py`): el módulo del simulacro (`Modulo.es_simulacro`) carga `preguntas.yaml` en `mod.preguntas` (lista de ids en el orden del fichero) y cada pregunta en `Contenido.preguntas[pid]` con `dominio`, `tarea`, `objetivo`, `tipo`, `modulo` y `banco = "examen"`.
- **Inicio del simulacro** (`app/routes/quiz.py:iniciar`, modo `simulacro`): `ids = sorted(banco.preguntas)[: m.examen_preguntas]`, error si hay menos; `limite_segundos = examen.minutos * 60`; `filtro = "estudio"` en modo estudio. La página de tests (`inicio`) ofrece el simulacro si `n_sim >= examen_preguntas`.
- **Almacenamiento** (`app/models.py`): `Intento.preguntas` es una columna JSON con **los ids en el orden en que se presentan**; `IntentoRespuesta` guarda por respuesta `pregunta_id`, `dominio`, `tarea`, `tipo`, `respuesta` y `correcta`. Reanudar (`continuar`), ver y responder (`/p/{n}` usa `i.preguntas[n - 1]`), resultado (filas en el orden de `i.preguntas`, «retirada» si el id ya no existe), historial (`stats.resumen_intento`: `len(i.preguntas)`), estadísticas por dominio y tarea (`stats.aciertos_por`, desde `IntentoRespuesta`), «Repetir falladas» (excluye el módulo del simulacro) y consultas a Claude (por `pregunta_id`) **no dependen de cómo se eligieron los ids**.
- **Banco actual:** 65 preguntas `S-001`…`S-065`; 13/16/18/9/9 por dominio; 51 de opción múltiple y 14 de respuesta múltiple (por dominio, respuesta múltiple 2/2/5/1/4); cubren 58 de los 69 objetivos, con 7 objetivos repetidos.
- **Objetivos oficiales** (`fuentes/dominio-N.md`, `**N.M.K**`): 17/14/19/11/8 por dominio.
- **Validador** (`scripts/validar_preguntas.py`): exige `banco.minimo_simulacro`, tipos de `examen.tipos`, avisa del reparto de tipos frente a `examen.distribucion`, simulacro inédito. **Cobertura** (`scripts/comprobar_cobertura.py --preguntas`): solo los módulos del bloque `cobertura`; el simulacro no se comprueba.
- **CLI** (`scripts/quiz.py`): `--modulo 06 --n 65` hace un muestreo simple con `--semilla`.
- **En paralelo:** la rama `aif-c01/simulacro-cobertura` sustituye preguntas que repiten objetivo por otras de objetivos sin cubrir, manteniendo el banco en 65. Con 13/16/18/9/9 fijo, el máximo posible es 62 objetivos (13 + 14 + 18 + 9 + 8).

## Goals / Non-Goals

**Goals:**

- Banco del simulacro mayor que el examen que cubra todos los objetivos oficiales.
- Cada intento con el reparto oficial por dominio y el de tipos de `examen.distribucion`, sin repetir objetivo cuando sea posible.
- Variedad real entre intentos consecutivos del mismo usuario.
- Cero cambios en base de datos y en las vistas de intento, resultado, historial y estadísticas; compatibilidad con los intentos antiguos y con los cursos cuyo banco tiene el tamaño del examen.
- Que la CI garantice que cualquier intento se puede formar.

**Non-Goals:**

- Equiparar la dificultad entre intentos (ver «Open Questions»).
- Puntuación escalada ni preguntas que no puntúan.
- Cambiar los bancos de los módulos, el repaso o «Repetir falladas».
- Redactar ahora las preguntas nuevas (tarea 5 de `tasks.md`).

## Decisions

### D1. Módulo compartido `curso/simulacro.py`

Funciones puras, sin dependencias de la consola, usadas por la consola, el validador y la CLI:

```python
def cuotas(m: Manifiesto) -> dict[tuple[int, str | None], int]
    # (dominio, tipo) -> nº de preguntas por intento; tipo None si no hay examen.distribucion
def rotatorio(m: Manifiesto, banco: list[dict]) -> bool
    # True si len(banco) > m.examen_preguntas
def comprobar_banco(m: Manifiesto, banco: list[dict]) -> tuple[list[str], list[str]]
    # (errores, líneas de resumen); sin errores si no es rotatorio
def extraer(m: Manifiesto, banco: list[dict], rnd: random.Random, evitar: set[str] = frozenset()) -> list[str]
    # ids en el orden de presentación; ValueError si el banco no permite formar el examen
```

`banco` es la lista de preguntas del simulacro (dicts con `id`, `dominio`, `tipo`, `objetivo`) en el orden del fichero. *Descartado:* meter la lógica en `app/routes/quiz.py` (el validador y la CLI la duplicarían).

### D2. Reparto por dominio: calculado con restos mayores

`cuota_d = examen.preguntas × peso_d / 100`, parte entera y las unidades que faltan a los mayores restos (desempate: mayor peso y, después, menor id de dominio). Para AIF-C01: 13 / 15,6 / 18,2 / 9,1 / 9,1 → 13/16/18/9/9, el reparto actual.

*Descartado:* declararlo en `curso.yaml` (p. ej. `examen.reparto: {1: 13, …}`): duplica los pesos y puede desincronizarse; si un curso lo necesitara, se añadiría como opción sin romper nada. **Pendiente de revisión.**

### D3. Reparto por tipo: cuotas globales y matriz dominio × tipo determinista

- Si `examen.distribucion` existe: cuota global por tipo con restos mayores sobre `examen.preguntas` (porcentajes normalizados). AIF-C01: 52 de opción múltiple y 13 de respuesta múltiple.
- Matriz dominio × tipo por redondeo controlado: los tipos se procesan de menor a mayor cuota global; la cuota de cada tipo se reparte entre dominios con restos mayores sobre `cuota_d × cuota_t / N`, sin superar lo que le queda a cada dominio; el tipo mayoritario completa cada dominio. Desempate: mayor cuota de dominio y, después, menor id.
- AIF-C01: respuesta múltiple 2,6 / 3,2 / 3,6 / 1,8 / 1,8 → **2/3/4/2/2**; opción múltiple **11/13/14/7/7**.
- Sin `examen.distribucion`: solo cuotas por dominio (`tipo = None`).

*Descartado:* exigir solo los totales globales de tipo y dejar libre el reparto por dominio (necesita un flujo o backtracking en cada intento y el validador no podría comprobar la factibilidad con un simple recuento). *Descartado:* tipos «orientativos» como hasta ahora: el usuario pide respetar el 80/20 en cada intento.

### D4. Algoritmo de extracción

1. Si el banco no es rotatorio (`len(banco) == examen.preguntas`): devolver `sorted(ids)`, como hoy (D7).
2. Si `comprobar_banco` da errores: `ValueError` con el primero.
3. Por cada dominio, rellenar sus celdas (dominio, tipo) empezando por la más escasa (menor holgura `candidatos − cuota`). En cada celda se elige una pregunta cada vez, la mínima según la clave `(objetivo ya usado en el dominio, id en evitar, rnd.random())`. Así, por prioridad: (a) las cuotas se cumplen siempre; (b) no se repite objetivo si hay alternativa; (c) se prefieren preguntas no vistas en el intento anterior; (d) el resto, al azar.
4. Se repite el paso 3 hasta 20 veces con el mismo `rnd` y se queda la selección con menos objetivos repetidos y, a igualdad, menos preguntas de `evitar` (corta antes si alcanza el mínimo inevitable).
5. `rnd.shuffle` de los 65 ids: los dominios quedan intercalados, como en el examen.

Mínimo inevitable de repeticiones por dominio: `max(0, cuota_d − objetivos distintos del dominio en el banco)`; en AIF-C01, 2 en el Dominio 2 (16 preguntas, 14 objetivos) y 1 en el 5 (9 preguntas, 8 objetivos). Las pruebas comprueban que el voraz lo alcanza con el banco real en todas las semillas probadas.

*Descartado:* programación lineal entera o flujo de coste mínimo (exacto, pero desproporcionado para 5 dominios y unas 20 preguntas por dominio, y añade una dependencia). *Descartado:* muestreo simple con rechazo hasta cumplir las cuotas (sin garantía de terminar y lento con objetivos sin repetir). *Descartado:* conservar el orden del fichero en la selección (con muestreo, el orden del fichero ya no aporta un intercalado pensado).

### D5. Rotación: preferir las no vistas en el intento anterior (recomendado)

Al iniciar un simulacro, `iniciar` lee el último `Intento` del mismo usuario y curso con `modo == "simulacro"` (terminado o no, en modo estudio o no) y pasa sus `preguntas` como `evitar`. Es una preferencia, no una exclusión.

- Con 82 preguntas y 65 por intento, dos intentos seguidos comparten al menos 48 preguntas haga lo que haga el algoritmo; la preferencia garantiza que las 17 que no salieron entran en el siguiente (salvo que lo impidan las cuotas por celda o la regla de no repetir objetivo, que tienen prioridad), de modo que **dos intentos consecutivos recorren el banco entero y todos los objetivos**.
- Coste: una consulta, sin columnas nuevas.

*Descartado:* exclusión estricta (imposible: 82 < 2 × 65). *Descartado:* ponderar por todo el historial o por «menos vistas» (más consultas y poca ganancia frente al último intento). *Descartado:* no hacer nada (el azar puro deja fuera las mismas preguntas varias veces seguidas con probabilidad apreciable).

### D6. Almacenamiento y migración: ninguna

`Intento.preguntas` ya guarda qué preguntas y en qué orden le tocaron a cada intento; todas las vistas leen de ahí. No se guarda la semilla.

*Descartado:* tabla `intento_pregunta` (normaliza algo que hoy no se consulta por SQL). *Descartado:* columna `semilla` para regenerar el intento (se rompe en cuanto cambia el banco; la lista de ids ya es la fuente de verdad). *Descartado:* marcar el intento como «rotatorio» (no cambia ninguna vista).

### D7. Compatibilidad

- **Intentos antiguos:** su lista de ids (los 65 primeros por orden) sigue siendo válida; reanudar y revisar no cambian. Regla nueva en `AGENTS.md`: los ids `S-NNN` no se renumeran ni se reutilizan; las preguntas nuevas toman el siguiente número libre (`S-066`…). Si se retira una, los intentos antiguos la muestran como «pregunta retirada», como hoy.
- **Banco del tamaño del examen:** mismo comportamiento que hoy (todas, ordenadas por id), sin exigir la matriz de D3; el validador mantiene el aviso de reparto de tipos actual. Así, el código puede desplegarse antes que el contenido: AIF-C01 sigue igual hasta que su banco pase de 65.
- **Banco menor que el examen:** el simulacro no se ofrece, como hoy.
- **Intentos en curso durante el despliegue:** conservan su lista.

### D8. Reproducibilidad y semilla

`extraer` recibe un `random.Random`. La consola usa uno nuevo por intento sin semilla fija; las pruebas y `scripts/quiz.py --simulacro --semilla N` usan semillas fijas y son deterministas. La reproducibilidad de un intento concreto la da `Intento.preguntas`, no la semilla.

### D9. Validación y CI

- `validar_preguntas.py` (si el banco es rotatorio): error por cada celda con menos preguntas que su cuota («el simulacro necesita 4 preguntas de respuesta múltiple del dominio 3 por intento y el banco tiene 3»); error si una pregunta del simulacro no tiene id `S-NNN` o un `S-NNN` aparece en otro banco; línea de resumen con el reparto por intento y las repeticiones inevitables. El aviso de reparto de tipos se calcula sobre el banco, como hoy. Como la matriz es determinista, la factibilidad es un recuento exacto, sin simulación.
- `comprobar_cobertura.py --preguntas`: si el manifiesto declara `banco.minimo_simulacro_por_objetivo`, error por cada objetivo oficial (`fuentes/dominio-N.md` de los dominios del manifiesto) con menos preguntas en el banco del simulacro, y línea de resumen «simulacro: 69/69 objetivos».
- `banco.minimo_simulacro` sigue siendo el tamaño mínimo del banco; AIF-C01 lo sube a 80 en el mismo commit que amplía el banco.

*Descartado:* comprobar la factibilidad simulando muchos intentos en la CI (lento y no demuestra nada que el recuento no demuestre).

### D10. Consola

- `inicio`: `sim_ok` pasa a ser «banco ≥ examen y sin errores de `comprobar_banco`». Si el banco es rotatorio, la tarjeta dice «Banco de 82 preguntas: cada intento saca 65 al azar con el reparto oficial».
- `iniciar`: `extraer(...)`; si lanza `ValueError`, el mismo `flash` de error y redirección que hoy.
- Sin cambios en `pregunta.html`, `resultado.html`, historial ni estadísticas.

### D11. Pruebas

- `tests/test_simulacro.py` (nuevo): cuotas de AIF-C01 (13/16/18/9/9; 52/13; 2/3/4/2/2 y 11/13/14/7/7); propiedades de `cuotas` con pesos y tamaños aleatorios (sumas por fila y columna, sin negativos); `extraer` sobre un banco sintético de 82 y sobre el banco real (cuando exista), con 500 semillas: 65 ids distintos del banco, cuotas por celda exactas, repeticiones de objetivo iguales al mínimo inevitable; con `evitar` = intento anterior en un banco sin objetivos repetidos, entran todas las no vistas; banco del tamaño del examen → `sorted(ids)`; banco infactible → `ValueError`; misma semilla → mismo resultado.
- `tests/test_validar_preguntas.py`: celda insuficiente → error; banco del tamaño del examen con el reparto desviado → solo aviso; id que no es `S-NNN` → error.
- `tests/test_cobertura.py`: objetivo sin pregunta en el simulacro → error; sin `minimo_simulacro_por_objetivo` → sin comprobación.
- `tests/app/test_app_quiz.py`: banco rotatorio → intento de N preguntas con las cuotas; el segundo intento incluye las no vistas; reanudar y resultado de un intento creado con la lista antigua; banco infactible → no se ofrece y `iniciar` avisa. El simulacro de 3 preguntas de `tests/conftest.py` cubre el camino compatible (las pruebas actuales no cambian).
- `tests/test_quiz.py`: `--simulacro --semilla` determinista y con las cuotas.

## Risks / Trade-offs

- [Intentos de dificultad desigual] → la dificultad no entra en el muestreo; el validador informa del reparto de dificultad del banco. Si se ve necesario, se añadiría como criterio de desempate.
- [Solapamiento alto entre intentos seguidos, 48 de 65 como mínimo] → límite del tamaño del banco; el README sigue recomendando repetir el simulacro solo después de repasar. Un banco mayor lo reduce.
- [Renumerar ids rompe la revisión de intentos antiguos] → regla en `AGENTS.md` y revisión; el resultado ya tolera ids retirados.
- [El voraz no alcanza el mínimo de repeticiones en algún banco] → reinicios (D4, paso 4) y pruebas con el banco real; nunca incumple las cuotas, solo repetiría un objetivo de más.
- [Dependencia de la rama `aif-c01/simulacro-cobertura`] → el código no depende de ella; el contenido (tarea 5) espera a su integración y recalcula qué objetivos faltan.
- [El banco crece y no todas las preguntas tienen la misma calidad] → las nuevas pasan la misma revisión independiente que el resto.

## Migration Plan

1. Código, pruebas y documentación técnica (tareas 1–4). AIF-C01 mantiene 65 preguntas: comportamiento idéntico al actual.
2. Tras integrar `aif-c01/simulacro-cobertura`: redactar el banco, `minimo_simulacro: 80` y `minimo_simulacro_por_objetivo: 1` en `curso.yaml` (tarea 5). Desde ese despliegue, los intentos nuevos son rotatorios.
3. Marcha atrás: revertir el commit de contenido devuelve el banco a 65 y el comportamiento anterior; no hay datos que deshacer.

## Open Questions

1. **Reparto por dominio** calculado (recomendado) o declarado en `curso.yaml`.
2. **Desempate de la respuesta múltiple:** 2/3/4/2/2 (recomendado: el resto va al dominio con más preguntas) o 3/3/3/2/2 (menor id).
3. **Tamaño del banco:** 82 (mínimo para cubrir los 69 objetivos con algo de holgura en cada dominio) o hasta 90 (más rotación, unas 8 preguntas más que redactar).
4. **Rotación:** recomendada (D5). ¿Cuenta el intento anterior aunque se abandonara sin responder? Propuesta: sí, por sencillez.
5. **Dificultad:** ¿basta con informar o se quiere estratificar? Propuesta: informar.
6. **Rama paralela:** confirmar con qué cobertura queda; con 13/16/18/9/9 no puede pasar de 62 objetivos, así que el número exacto de preguntas nuevas por objetivo se fija al empezar la tarea 5.
