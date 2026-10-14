# estilo-de-diagramas Specification

## Purpose
TBD - created by archiving change info-en-cajas-de-diagramas. Update Purpose after archive.
## Requirements
### Requirement: Estilo único de los diagramas
Todos los diagramas de los cursos SHALL ser `flowchart` de Mermaid con el estilo del proyecto: etiqueta de cada nodo y subgrupo que comience por un emoji, color por tipo mediante `class <ids> <tipo>` con tipos `ia`, `ml`, `dl`, `gen`, `dato`, `proceso`, `servicio`, `accion`, `aviso` o `decision`, y sin `classDef`.

#### Scenario: Diagrama conforme
- **WHEN** un `flowchart` cumple todas las reglas
- **THEN** el validador no informa de errores

#### Scenario: Etiqueta sin emoji
- **WHEN** un nodo tiene la etiqueta «Datos» sin emoji inicial
- **THEN** el validador informa de error indicando el fichero, el diagrama y el nodo

#### Scenario: Clase no permitida o `classDef`
- **WHEN** un diagrama usa `class A rojo` o una sentencia `classDef`
- **THEN** el validador informa de error

#### Scenario: Otro tipo de diagrama
- **WHEN** un bloque `mermaid` empieza por `sequenceDiagram`
- **THEN** el validador informa de error

### Requirement: Cobertura de información de las cajas
El validador SHALL comprobar que cada nodo y cada subgrupo de cada diagrama tiene una entrada en el bloque `nodos` siguiente, que no hay entradas de ids inexistentes, que `concepto` existe en el glosario del curso, que cada URL es `https` y que `seccion` apunta a un módulo, una sección y un ancla existentes.

#### Scenario: Caja sin información
- **WHEN** el nodo `C` no tiene entrada en `nodos`
- **THEN** el validador informa de que `C` no tiene información

#### Scenario: Entrada huérfana
- **WHEN** `nodos` contiene la clave `Z` y el diagrama no tiene ese nodo
- **THEN** el validador informa de error

#### Scenario: Concepto inexistente
- **WHEN** una caja declara `concepto: no-existe`
- **THEN** el validador informa de error

#### Scenario: Sección inexistente
- **WHEN** una caja declara una `seccion` cuyo ancla no existe
- **THEN** el validador informa de error

### Requirement: Validación en CI
La validación de diagramas SHALL ejecutarse como parte de `scripts/validar_preguntas.py`, de modo que el CI falle ante cualquier incumplimiento.

#### Scenario: CI
- **WHEN** un diagrama incumple el estilo
- **THEN** `validar_preguntas.py` termina con código distinto de cero

### Requirement: Reglas para autores
`AGENTS.md` SHALL documentar el estilo obligatorio, el formato del bloque `nodos` y que el estilo de diagramas actual se mantiene en todo el proyecto.

#### Scenario: Documentación
- **WHEN** un colaborador consulta `AGENTS.md`
- **THEN** encuentra las reglas y un ejemplo de diagrama con su bloque `nodos`

