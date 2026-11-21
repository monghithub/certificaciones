## ADDED Requirements

### Requirement: Banco rotatorio del simulacro

Si el banco del simulacro de un curso tiene más preguntas que `examen.preguntas`, cada intento SHALL extraer `examen.preguntas` preguntas distintas de ese banco y presentarlas en orden aleatorio. El módulo `curso/simulacro.py` SHALL ser la única implementación de la composición y SHALL usarlo la consola, el validador y `scripts/quiz.py`.

#### Scenario: Intento de un banco mayor que el examen

- **WHEN** el banco tiene 82 preguntas, `examen.preguntas` es 65 y el estudiante inicia el simulacro
- **THEN** el intento contiene 65 preguntas distintas del banco, en orden aleatorio

### Requirement: Reparto por dominio y tipo en cada intento

La cuota de cada dominio SHALL calcularse con el método de restos mayores sobre `examen.preguntas` y los pesos de `dominios` (desempate: mayor peso y, después, menor id). Si el manifiesto declara `examen.distribucion`, la cuota global de cada tipo SHALL calcularse igual y repartirse entre dominios con una matriz dominio × tipo determinista (restos mayores, desempate por mayor cuota de dominio y menor id). Cada intento SHALL cumplir exactamente esas cuotas.

#### Scenario: Cuotas de AIF-C01

- **WHEN** `examen.preguntas` es 65, los pesos son 20/24/28/14/14 y `examen.distribucion` es 80/20
- **THEN** cada intento tiene 13/16/18/9/9 preguntas por dominio, 52 de opción múltiple y 13 de respuesta múltiple, y 2/3/4/2/2 de respuesta múltiple por dominio

#### Scenario: Curso sin distribución de tipos

- **WHEN** el manifiesto no declara `examen.distribucion`
- **THEN** el intento cumple las cuotas por dominio y los tipos salen al azar

### Requirement: Objetivos sin repetir en un intento

Dentro de un intento, un objetivo SHALL repetirse solo cuando el banco no permita evitarlo. El número de repeticiones de cada dominio SHALL ser la cuota del dominio menos el máximo de objetivos distintos que permiten las cuotas por dominio y tipo (emparejamiento máximo entre los huecos de cada celda y los objetivos presentes en ella), y la preferencia por las preguntas no vistas no SHALL aumentarlo.

#### Scenario: Dominio con más objetivos que cuota

- **WHEN** el Dominio 1 tiene cuota 13 y el banco cubre sus 17 objetivos
- **THEN** las 13 preguntas del Dominio 1 del intento son de 13 objetivos distintos

#### Scenario: Dominio con menos objetivos que cuota

- **WHEN** el Dominio 5 tiene cuota 9 y 8 objetivos
- **THEN** el intento repite un solo objetivo del Dominio 5

#### Scenario: Objetivos compartidos entre tipos

- **WHEN** la opción múltiple del dominio (cuota 2) solo tiene preguntas del objetivo A y la respuesta múltiple (cuota 1) tiene B y C
- **THEN** el mínimo de repeticiones del dominio es 1 y el intento repite A una sola vez

#### Scenario: Preferir las no vistas sin repetir objetivo

- **WHEN** la respuesta múltiple (cuota 2) tiene o5, o4 y o1, solo o4 sin ver, y la opción múltiple (cuota 3) tiene o6, o4, o4, o6 y o2
- **THEN** el intento no repite ningún objetivo

### Requirement: Rotación entre intentos

Al iniciar un simulacro rotatorio, la consola SHALL preferir las preguntas que no estaban en el intento de simulacro anterior del mismo usuario y curso, sin incumplir las cuotas ni la regla de objetivos sin repetir.

#### Scenario: Dos intentos seguidos

- **WHEN** el banco tiene 82 preguntas sin objetivos repetidos que impidan la rotación y el estudiante inicia su segundo simulacro
- **THEN** el segundo intento incluye las 17 preguntas que no salieron en el primero

### Requirement: Preguntas y orden guardados en el intento

El intento SHALL guardar los ids de las preguntas extraídas en el orden de presentación, y reanudar, revisar el resultado, el historial y las estadísticas SHALL usar esa lista, sin volver a extraer. No SHALL hacer falta ninguna migración de base de datos.

#### Scenario: Reanudar un intento

- **WHEN** el estudiante abandona un simulacro en la pregunta 20 y vuelve más tarde
- **THEN** continúa con las mismas preguntas y en el mismo orden

#### Scenario: Intento anterior al cambio

- **WHEN** un estudiante revisa un simulacro hecho con el banco fijo
- **THEN** ve sus 65 preguntas y su resultado como antes

### Requirement: Compatibilidad con bancos del tamaño del examen

Si el banco del simulacro tiene exactamente `examen.preguntas` preguntas, cada intento SHALL contenerlas todas, ordenadas por id, sin exigir las cuotas por tipo, como antes del cambio. Si tiene menos, el simulacro no SHALL ofrecerse.

#### Scenario: Banco de 65 preguntas

- **WHEN** el banco tiene 65 preguntas y `examen.preguntas` es 65
- **THEN** el intento contiene `S-001` a `S-065` en ese orden

### Requirement: Banco que no permite formar el examen

Si un banco rotatorio no tiene suficientes preguntas para alguna cuota de dominio y tipo, la consola no SHALL ofrecer el simulacro e iniciar uno SHALL devolver a la página de tests con un mensaje de error.

#### Scenario: Faltan preguntas de respuesta múltiple

- **WHEN** el banco tiene 82 preguntas pero solo una de respuesta múltiple del Dominio 4, con cuota 2
- **THEN** la página de tests indica que el simulacro no está disponible

### Requirement: Reproducibilidad

La extracción SHALL recibir el generador aleatorio, de modo que con la misma semilla y el mismo banco el resultado sea idéntico. La consola SHALL usar un generador sin semilla fija y no SHALL guardar la semilla.

#### Scenario: Misma semilla

- **WHEN** se extrae dos veces con la semilla 7 del mismo banco
- **THEN** ambas listas de ids son iguales
