## ADDED Requirements

### Requirement: Validación de los bancos de repaso
`scripts/validar_preguntas.py` SHALL validar cada `modulos/*/repaso.yaml` con el esquema y las comprobaciones de coherencia de los bancos, exigir ids únicos en todo el curso, admitir dominio 0 solo en bancos de repaso de cursos con `repaso.previos`, exigir el mínimo `repaso.minimo_por_modulo` y dar error si un enunciado repite el de una pregunta de examen.

#### Scenario: Dominio 0 en un banco de examen
- **WHEN** una pregunta de `preguntas.yaml` usa dominio 0
- **THEN** el validador informa del error y termina con código 1
