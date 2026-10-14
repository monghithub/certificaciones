# modulo-00-base-aws Specification

## Purpose
TBD - created by archiving change iteracion-1-modulos-00-01. Update Purpose after archive.
## Requirements
### Requirement: Conocimientos previos de AWS transcritos
`cursos/aif-c01/fuentes/conocimientos-previos.md` SHALL transcribir literalmente, con URL y fecha de consulta, la sección «Recommended AWS knowledge» de la guía oficial.

#### Scenario: Fichero de fuente presente
- **WHEN** se abre `fuentes/conocimientos-previos.md`
- **THEN** contiene la URL de la guía, la fecha de consulta y los cuatro conocimientos recomendados en su redacción original

### Requirement: Contenido del módulo 00
El módulo 00 SHALL contener `README.md` (siguiendo la plantilla de módulo), `servicios.md` y `trampas.md`, redactados en español de España a nivel *foundational*, sin banco de preguntas ni laboratorio.

#### Scenario: Plantilla completa
- **WHEN** se lee `modulos/00-base-aws/README.md`
- **THEN** contiene objetivos de aprendizaje, mapa de cobertura, teoría, 5–10 puntos clave y referencias oficiales

### Requirement: Cobertura de los conocimientos recomendados
El mapa de cobertura del módulo 00 SHALL tener una fila por cada conocimiento recomendado (servicios centrales, modelo de responsabilidad compartida, IAM y modelos de precios), enlazada a la sección que lo cubre.

#### Scenario: Sin filas sin cubrir
- **WHEN** se revisa el mapa de cobertura
- **THEN** cada fila enlaza a una sección existente del README

### Requirement: Verificabilidad
Toda afirmación sobre servicios, límites, precios o regiones SHALL enlazar a documentación oficial de AWS o marcarse con `> ⚠️ PENDIENTE DE VERIFICAR:`.

#### Scenario: Dato no verificable
- **WHEN** no se encuentra fuente oficial para un dato
- **THEN** el texto incluye el marcador de pendiente y no afirma el dato

