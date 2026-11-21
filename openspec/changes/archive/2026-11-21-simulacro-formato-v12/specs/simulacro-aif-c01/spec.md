## MODIFIED Requirements

### Requirement: Simulacro con los pesos oficiales
`cursos/aif-c01/modulos/06-simulacro/preguntas.yaml` SHALL contener 65 preguntas `S-NNN`: 13 del Dominio 1, 16 del 2, 18 del 3, 9 del 4 y 9 del 5, solo de los tipos que enumera la guía oficial del examen (`examen.tipos` del manifiesto: opción múltiple y respuesta múltiple en la versión 1.2), con dificultad repartida y dominios intercalados.

#### Scenario: Simulacro disponible en la consola
- **WHEN** un estudiante abre los tests del curso
- **THEN** puede iniciar el simulacro de 65 preguntas y 90 minutos

#### Scenario: Tipos del examen
- **WHEN** se valida el simulacro de AIF-C01
- **THEN** todas sus preguntas son de opción múltiple o de respuesta múltiple
