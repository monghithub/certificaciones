# repo-docs Specification

## Purpose
TBD - created by archiving change iteracion-0-fundacion-curso. Update Purpose after archive.
## Requirements
### Requirement: Estructura del repositorio
El repositorio SHALL contener `README.md`, `AGENTS.md`, `CHANGELOG.md`, `LICENSE`, y los directorios `fuentes/`, `modulos/00-base-aws` … `modulos/06-simulacro`, `schemas/`, `scripts/` y `.github/workflows/`, según la sección 5 de `promt.md`.

#### Scenario: Directorios de módulo presentes
- **WHEN** se lista `modulos/`
- **THEN** existen exactamente los siete directorios `00-base-aws`, `01-fundamentos-ia-ml`, `02-fundamentos-genai`, `03-modelos-fundacionales`, `04-ia-responsable`, `05-seguridad-gobierno` y `06-simulacro`

### Requirement: README del curso
`README.md` SHALL incluir presentación, índice de módulos, instrucciones de estudio, plan de 4 semanas, datos del examen revalidados y la recomendación de validar la preparación con el examen de práctica oficial de AWS Skill Builder antes de reservar el examen.

#### Scenario: Recomendación final presente
- **WHEN** se lee `README.md`
- **THEN** contiene la recomendación sobre el examen de práctica oficial de AWS Skill Builder

### Requirement: AGENTS.md
`AGENTS.md` SHALL resumir las reglas de `promt.md` para colaboradores: fuente de verdad, prohibición de inventar datos y de usar "dumps", marcador `PENDIENTE DE VERIFICAR`, criterios de redacción, esquema de preguntas (incluido el formato de `ordering` y `matching`), convenciones Git y flujo por iteraciones.

#### Scenario: Reglas de verificación documentadas
- **WHEN** un agente lee `AGENTS.md`
- **THEN** encuentra la prohibición de inventar datos y el formato del marcador `> ⚠️ PENDIENTE DE VERIFICAR:`

### Requirement: Registro de cambios
`CHANGELOG.md` SHALL registrar la Iteración 0 y toda discrepancia entre los datos de referencia de `promt.md` y la guía oficial.

#### Scenario: Discrepancia documentada
- **WHEN** la guía oficial difiere de la sección 4 de `promt.md`
- **THEN** `CHANGELOG.md` describe la diferencia y `README.md` usa el valor oficial

