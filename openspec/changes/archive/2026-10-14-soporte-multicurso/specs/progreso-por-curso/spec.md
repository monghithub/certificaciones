## ADDED Requirements

### Requirement: Progreso e intentos ligados a un curso
El progreso de lectura y los intentos de test SHALL registrarse con el curso al que pertenecen, y las vistas de índice, tests y estadísticas SHALL mostrar únicamente los datos del curso activo.

#### Scenario: Progreso independiente por curso
- **WHEN** un estudiante completa una sección en el curso A
- **THEN** su progreso en el curso B no cambia

#### Scenario: Estadísticas por curso
- **WHEN** un estudiante tiene intentos en dos cursos y abre las estadísticas del curso A
- **THEN** solo ve los aciertos y el historial del curso A

### Requirement: Simulacro configurado por el curso
El simulacro SHALL usar el número de preguntas y los minutos del manifiesto del curso y SHALL ofrecerse solo si el curso lo define.

#### Scenario: Curso con otro simulacro
- **WHEN** un curso declara `examen: {preguntas: 40, minutos: 60}`
- **THEN** su simulacro se compone de 40 preguntas con límite de 60 minutos

### Requirement: Migración sin pérdida
La migración de base de datos SHALL asignar el curso `aif-c01` a todo el progreso e intentos existentes y SHALL matricular en `aif-c01` a los usuarios con rol `estudiante` existentes, sin perder ni modificar otros datos.

#### Scenario: Datos previos
- **WHEN** se migra una base con 2 estudiantes, 5 intentos y 8 secciones leídas
- **THEN** tras migrar, los 5 intentos y 8 secciones pertenecen a `aif-c01` y ambos estudiantes están matriculados

### Requirement: Vista de administración por curso
El detalle de un usuario en administración SHALL permitir elegir el curso para ver su progreso y estadísticas, y SHALL mostrar su posición actual en cada curso.

#### Scenario: Usuario en dos cursos
- **WHEN** el admin abre el detalle de un usuario con dos matrículas
- **THEN** puede alternar entre las estadísticas de ambos cursos
