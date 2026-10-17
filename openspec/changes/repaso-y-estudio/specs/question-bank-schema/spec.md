## ADDED Requirements

### Requirement: Preguntas de repaso y conocimientos previos
El esquema SHALL admitir ids `R<n>-NNN`, dominio 0, tarea `CP` y objetivo `CP.<n>`, además de los formatos existentes.

#### Scenario: Pregunta de conocimientos previos
- **WHEN** una pregunta tiene id `R0-001`, dominio 0, tarea `CP` y objetivo `CP.2`
- **THEN** cumple el esquema
