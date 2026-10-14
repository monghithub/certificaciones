## ADDED Requirements

### Requirement: Índice del curso
El sistema SHALL mostrar un índice con los módulos 00 a 06 y sus secciones (teoría, servicios, trampas, laboratorio, preguntas), cargados desde el directorio del curso, indicando por cada módulo el progreso del usuario.

#### Scenario: Índice con contenido
- **WHEN** un usuario autenticado abre el índice
- **THEN** ve los módulos existentes, sus secciones y su estado (sin empezar, en curso, completado)

### Requirement: Lectura de módulos
El sistema SHALL renderizar los ficheros Markdown de cada módulo de forma sanitizada, incluidos los diagramas Mermaid y las tablas, sin depender de recursos externos.

#### Scenario: Diagrama Mermaid
- **WHEN** una sección contiene un bloque ```mermaid
- **THEN** se muestra renderizado como diagrama

### Requirement: Seguimiento de posición
El sistema SHALL registrar la última sección abierta por cada usuario y permitir marcarla como completada, y SHALL ofrecer "continuar donde lo dejaste".

#### Scenario: Reanudar
- **WHEN** un estudiante vuelve tras abandonar el módulo 03, sección trampas
- **THEN** el índice ofrece un enlace directo a esa sección
