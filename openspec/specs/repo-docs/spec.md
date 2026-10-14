# repo-docs Specification

## Purpose
TBD - created by archiving change iteracion-0-fundacion-curso. Update Purpose after archive.
## Requirements
### Requirement: Estructura del repositorio
El repositorio SHALL contener `README.md`, `AGENTS.md`, `CHANGELOG.md`, `LICENSE`, `docs/journal.md`, `schemas/`, `scripts/`, `.github/workflows/` y un directorio por curso en `cursos/<slug>/` con `curso.yaml`, `README.md`, `fuentes/` y `modulos/`, y opcionalmente `glosario.yaml`, `AGENTS.md` y `promt.md` del curso.

#### Scenario: Curso autocontenido
- **WHEN** se lista `cursos/aif-c01/`
- **THEN** contiene `curso.yaml`, `README.md`, `AGENTS.md`, `promt.md`, `glosario.yaml`, `fuentes/` y `modulos/`

### Requirement: README del curso
El `README.md` de cada curso SHALL incluir presentación, índice de módulos, instrucciones de estudio, plan de estudio, datos del examen revalidados y la recomendación de validar la preparación con el material oficial de práctica del proveedor, enlazado, antes de reservar el examen.

#### Scenario: Recomendación final presente
- **WHEN** se lee `cursos/aif-c01/README.md`
- **THEN** contiene el enlace al conjunto oficial de práctica de AWS Skill Builder

### Requirement: AGENTS.md
El `AGENTS.md` raíz SHALL recoger las reglas comunes a todos los cursos (fuente de verdad, prohibición de inventar datos y de usar *dumps*, marcador `PENDIENTE DE VERIFICAR`, calidad del contenido y del banco, esquema de preguntas, glosario y diagramas, cómo añadir un curso, flujo de OpenSpec, Git y journal) y su orden de prevalencia. Las reglas propias de un curso SHALL ir en `cursos/<slug>/AGENTS.md`.

#### Scenario: Reglas de verificación documentadas
- **WHEN** un agente lee `AGENTS.md`
- **THEN** encuentra la prohibición de inventar datos y el formato del marcador `> ⚠️ PENDIENTE DE VERIFICAR:`

#### Scenario: Reglas propias de AIF-C01
- **WHEN** un agente trabaja en `cursos/aif-c01/`
- **THEN** encuentra en `cursos/aif-c01/AGENTS.md` las fuentes oficiales de AWS, los avisos de disponibilidad de servicios y las reglas de sus laboratorios

### Requirement: Registro de cambios
`CHANGELOG.md` SHALL registrar la Iteración 0 y toda discrepancia entre los datos de referencia de `promt.md` y la guía oficial.

#### Scenario: Discrepancia documentada
- **WHEN** la guía oficial difiere de la sección 4 de `promt.md`
- **THEN** `CHANGELOG.md` describe la diferencia y `README.md` usa el valor oficial

