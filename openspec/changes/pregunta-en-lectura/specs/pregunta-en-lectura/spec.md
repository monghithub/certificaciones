## ADDED Requirements

### Requirement: Botón de pregunta durante la lectura
Las páginas de lectura de los módulos con preguntas (de repaso o de examen), salvo el simulacro, SHALL mostrar un botón «Ponme a prueba» que abre un modal con una pregunta tipo test. El modal SHALL abrirse solo al pulsar el botón.

#### Scenario: Módulo con preguntas
- **WHEN** el estudiante abre la teoría del módulo 03
- **THEN** ve el botón «Ponme a prueba»

#### Scenario: Simulacro
- **WHEN** el estudiante abre el README del módulo 06 (simulacro)
- **THEN** no hay botón

### Requirement: Pregunta del apartado visible
La consola SHALL elegir la pregunta entre las de los objetivos cuyo mapa de cobertura apunta al encabezado visible más cercano o a sus encabezados padres. Dentro de un apartado, primero las de repaso y, agotadas, las de examen. Si ningún apartado tiene preguntas disponibles, SHALL elegirla del módulo e indicarlo. Nunca SHALL usar preguntas del simulacro ni repetir una pregunta ya mostrada mientras quedan otras.

#### Scenario: Apartado con preguntas de repaso
- **WHEN** el estudiante pulsa el botón con el apartado de RAG en el centro de la ventana
- **THEN** recibe una pregunta de repaso del objetivo 3.1.3

#### Scenario: Apartado sin objetivo
- **WHEN** el estudiante está leyendo `trampas.md` del módulo 02
- **THEN** recibe una pregunta del módulo 02 y el modal indica que es del módulo

### Requirement: Corrección inmediata sin registro
En el modal, el estudiante SHALL poder responder los cuatro tipos de pregunta, ver al momento si es correcta, la solución, la explicación, los motivos de las opciones incorrectas, la referencia oficial y el enlace a la teoría, y pedir otra pregunta o cerrar. Las respuestas del modal NO SHALL guardarse ni contar en estadísticas ni en «Repetir falladas».

#### Scenario: Encadenar preguntas
- **WHEN** el estudiante responde y pulsa «Otra pregunta»
- **THEN** el modal muestra otra pregunta del apartado visible

#### Scenario: Sin registro
- **WHEN** el estudiante responde mal en el modal
- **THEN** la pregunta no aparece en «Repetir falladas»

#### Scenario: Seguridad
- **WHEN** se pide corregir sin token CSRF, o una pregunta del simulacro o de otro módulo
- **THEN** la consola lo rechaza
