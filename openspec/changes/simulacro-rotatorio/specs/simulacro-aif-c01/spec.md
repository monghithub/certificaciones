## MODIFIED Requirements

### Requirement: Simulacro con los pesos oficiales

`cursos/aif-c01/modulos/06-simulacro/preguntas.yaml` SHALL ser un banco de al menos 80 preguntas `S-NNN` que cubra los 69 objetivos oficiales con al menos una pregunta cada uno, solo de los tipos que enumera la guía oficial del examen (`examen.tipos` del manifiesto: opción múltiple y respuesta múltiple en la versión 1.2), con dificultad repartida y suficientes preguntas por dominio y tipo para formar siempre un intento de 65 con 13/16/18/9/9 por dominio y 52 de opción múltiple y 13 de respuesta múltiple. Los ids existentes no SHALL renumerarse ni reutilizarse.

#### Scenario: Simulacro disponible en la consola

- **WHEN** un estudiante abre los tests del curso
- **THEN** puede iniciar el simulacro de 65 preguntas y 90 minutos

#### Scenario: Tipos del examen

- **WHEN** se valida el simulacro de AIF-C01
- **THEN** todas sus preguntas son de opción múltiple o de respuesta múltiple

#### Scenario: Cobertura de objetivos

- **WHEN** se ejecuta `comprobar_cobertura.py --preguntas`
- **THEN** el banco del simulacro cubre los 69 objetivos oficiales

### Requirement: Instrucciones del simulacro

`cursos/aif-c01/modulos/06-simulacro/README.md` SHALL explicar el formato, que cada intento saca 65 preguntas al azar de un banco mayor con el reparto oficial y prefiere las que no salieron en el intento anterior, cómo interpretar el resultado por dominio y la recomendación de hacer el conjunto oficial de práctica de AWS Skill Builder antes de reservar el examen.

#### Scenario: Estudiante que termina el simulacro

- **WHEN** el estudiante lee el README tras el simulacro
- **THEN** sabe qué módulos repasar según sus fallos por dominio

#### Scenario: Estudiante que quiere repetirlo

- **WHEN** el estudiante lee el README antes de un segundo intento
- **THEN** sabe que el segundo intento cambia parte de las preguntas (unas 15 de 65), que la mayoría se repiten y que conviene repasar antes de repetirlo
