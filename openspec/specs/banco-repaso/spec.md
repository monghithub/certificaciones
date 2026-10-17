# banco-repaso Specification

## Purpose
TBD - created by archiving change repaso-y-estudio. Update Purpose after archive.
## Requirements
### Requirement: Banco de repaso por módulo
Cada módulo de teoría (00 a 05) SHALL tener `repaso.yaml` con preguntas directas de conocimiento, ids `RN-NNN` (N = número de módulo), al menos `repaso.minimo_por_modulo` preguntas y al menos `repaso.minimo_por_objetivo` por objetivo de la fuente de cobertura del módulo. Cada pregunta SHALL apoyarse en una afirmación de la teoría del módulo, tener una explicación que enseñe el concepto, explicar cada opción incorrecta y citar una fuente oficial.

#### Scenario: Módulo 00
- **WHEN** se valida `00-base-aws/repaso.yaml`
- **THEN** sus preguntas usan dominio 0, tarea `CP` y objetivos `CP.1`–`CP.4`, todos cubiertos

#### Scenario: Objetivo sin repaso
- **WHEN** un objetivo del módulo 02 no tiene preguntas de repaso suficientes
- **THEN** `comprobar_cobertura.py --preguntas` informa del error y termina con código 1

