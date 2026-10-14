# glosario-conceptos Specification

## Purpose
TBD - created by archiving change glosario-y-diagramas-interactivos. Update Purpose after archive.
## Requirements
### Requirement: Glosario por curso
Un curso MAY incluir `cursos/<curso>/glosario.yaml`, una lista de entradas con `id`, `termino`, `categoria` y `definicion` obligatorios y `alias`, `usar_cuando`, `no_usar_cuando` y `referencia` opcionales; cuando exista, SHALL validarse con `schemas/glosario.schema.json`.

#### Scenario: Entrada válida
- **WHEN** una entrada tiene id en minúsculas con guiones, término, categoría `servicio` y una definición
- **THEN** valida contra el esquema

#### Scenario: Categoría desconocida
- **WHEN** una entrada declara `categoria: otra`
- **THEN** el validador informa de error

### Requirement: Unicidad y coherencia
El validador SHALL comprobar que los ids son únicos y que ningún término ni alias se repite entre entradas (sin distinguir mayúsculas), y que `referencia`, si existe, es una URL `https`.

#### Scenario: Alias duplicado
- **WHEN** dos entradas comparten el alias «Bedrock»
- **THEN** el validador informa de error indicando ambas entradas

### Requirement: Todo servicio listado tiene entrada
Si el curso tiene glosario, el validador SHALL comprobar que cada servicio de la primera columna de las tablas de los `servicios.md` de sus módulos coincide con el término o un alias de alguna entrada.

#### Scenario: Servicio sin entrada
- **WHEN** `servicios.md` lista «Amazon Rekognition» y el glosario no la contiene
- **THEN** el validador informa de error con el módulo y el servicio

#### Scenario: Curso sin glosario
- **WHEN** el curso no tiene `glosario.yaml`
- **THEN** no se realizan estas comprobaciones y no hay error

### Requirement: Página de glosario
La consola SHALL ofrecer `/c/<curso>/glosario` con todas las entradas ordenadas alfabéticamente, un filtro instantáneo por texto y, para cada entrada, la apertura del modal de concepto. Solo SHALL ser accesible a quienes tengan acceso al curso.

#### Scenario: Filtrar
- **WHEN** el estudiante escribe «recall» en el filtro
- **THEN** solo permanecen visibles las entradas cuyo término, alias o definición contienen ese texto

#### Scenario: Curso sin glosario
- **WHEN** se solicita el glosario de un curso que no lo tiene
- **THEN** se muestra un aviso de que el curso no tiene glosario

