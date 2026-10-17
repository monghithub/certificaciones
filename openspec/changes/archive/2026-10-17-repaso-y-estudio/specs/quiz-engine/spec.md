## ADDED Requirements

### Requirement: Modo repaso
La consola SHALL ofrecer tests de repaso de conocimientos por módulo o de todos los módulos, con corrección tras cada respuesta, separados de los tests de examen (módulo, dominio, mixto), que no incluyen preguntas de repaso.

#### Scenario: Repaso del módulo 00
- **WHEN** el estudiante inicia un repaso del módulo 00
- **THEN** el test contiene solo preguntas de `00-base-aws/repaso.yaml`

### Requirement: Repetir falladas
La consola SHALL ofrecer un modo con las preguntas de repaso y de examen (no del simulacro) cuya última respuesta del estudiante fue incorrecta.

#### Scenario: Pregunta corregida
- **WHEN** el estudiante falla una pregunta y en un intento posterior la acierta
- **THEN** deja de aparecer en «repetir falladas»

### Requirement: Explicación tras cada respuesta
En todos los modos con corrección inmediata, tras responder una pregunta la consola SHALL mostrar si es correcta, la solución y un desplegable «Ver explicación» con la explicación, los motivos de las opciones incorrectas, la referencia oficial y, si el objetivo está en un mapa de cobertura, el enlace a la sección de teoría.

#### Scenario: Enlace a la teoría
- **WHEN** el estudiante responde una pregunta del objetivo 1.1.1
- **THEN** la explicación enlaza a la sección del módulo 01 que el mapa de cobertura asocia a 1.1.1

### Requirement: Modo estudio del simulacro
Al iniciar el simulacro, el estudiante SHALL poder marcar «Modo estudio»: con él, cada respuesta muestra la corrección y la explicación; sin él, el simulacro no muestra correcciones hasta el final.

#### Scenario: Simulacro normal
- **WHEN** el estudiante inicia el simulacro sin modo estudio y responde una pregunta
- **THEN** no ve la corrección hasta el resultado final
