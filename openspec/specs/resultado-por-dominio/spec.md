# resultado-por-dominio Specification

## Purpose

Resultado de cada intento por dominio y por tarea, con el total cuadrado, enlaces a la teoría y los dominios por debajo de la media en el simulacro.

## Requirements

### Requirement: Resultado por dominio

La página de resultado de cualquier intento SHALL mostrar, antes de la lista de preguntas, una tabla con los aciertos, el total y el porcentaje de cada dominio (con su nombre del manifiesto) y una fila de total. El desglose SHALL calcularse con todas las preguntas del intento: las sin responder cuentan como falladas, y la suma de las filas SHALL coincidir con el total y los aciertos del intento.

#### Scenario: Test con una pregunta sin responder

- **WHEN** el estudiante finaliza un test de 4 preguntas del Dominio 3 con 2 acertadas, 1 fallada y 1 sin responder
- **THEN** la tabla muestra el Dominio 3 con 2/4, el total 2/4 y un aviso de que la sin responder cuenta como fallada

#### Scenario: Pregunta retirada

- **WHEN** un intento referencia ids que ya no existen en el contenido
- **THEN** cuentan en una fila «Preguntas retiradas del contenido», fuera del desglose por tarea, y la página no falla

#### Scenario: Preguntas sin dominio oficial

- **WHEN** un test de los libros incluye una pregunta sin dominio
- **THEN** cuenta en la fila «Sin dominio oficial»

#### Scenario: Conocimientos previos

- **WHEN** un repaso incluye preguntas del dominio 0
- **THEN** cuentan en la fila «Conocimientos previos»

### Requirement: Desglose por tarea

Debajo de la tabla por dominio, la página SHALL ofrecer plegado el desglose por tarea oficial (aciertos, total y porcentaje), en orden numérico.

#### Scenario: Tareas de un simulacro

- **WHEN** el estudiante abre el desglose por tarea de un simulacro de AIF-C01
- **THEN** ve las 14 tareas con sus aciertos

### Requirement: Enlaces a la teoría

Cada dominio SHALL enlazar con la teoría del módulo que lo cubre según el bloque `cobertura` del manifiesto, y cada tarea, con la sección del primer objetivo de la tarea que tenga sitio en el mapa de cobertura. Si no hay destino, la fila SHALL mostrarse sin enlace.

#### Scenario: Dominio con teoría

- **WHEN** el resultado incluye el Dominio 1 de AIF-C01
- **THEN** su nombre enlaza con la teoría del módulo 01

### Requirement: Dominios por debajo de la media en el simulacro

En el resultado de un simulacro, la página SHALL marcar los dominios oficiales cuyo porcentaje quede por debajo del porcentaje global del intento y SHALL explicar que es un criterio relativo y orientativo, porque AWS no publica cortes por sección (solo «Meets competencies» o «Needs improvement»). No SHALL usar umbrales presentados como oficiales. En los demás modos no SHALL marcar dominios.

#### Scenario: Simulacro con dominios débiles

- **WHEN** el estudiante acierta 3 de 5 preguntas y falla las de los dominios 1 y 5
- **THEN** los dominios 1 y 5 aparecen marcados «por debajo de tu media» y en «Para repasar primero»

#### Scenario: Todo acertado

- **WHEN** el estudiante acierta todas las preguntas del simulacro
- **THEN** no se marca ningún dominio
