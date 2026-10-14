## ADDED Requirements

### Requirement: Matrícula de usuarios en cursos
El sistema SHALL permitir al admin matricular a un usuario en uno o varios cursos del catálogo y retirar matrículas, en el alta del usuario y desde su detalle. Los roles `admin` y `estudiante` SHALL seguir siendo globales.

#### Scenario: Alta con matrícula
- **WHEN** el admin crea un estudiante y marca el curso `aif-c01`
- **THEN** el estudiante queda matriculado en ese curso

#### Scenario: Retirar matrícula conserva el historial
- **WHEN** el admin retira la matrícula de un estudiante que tiene intentos en el curso
- **THEN** el estudiante deja de acceder al curso y, al matricularlo de nuevo, recupera su historial

#### Scenario: Curso inexistente
- **WHEN** el admin intenta matricular en un slug que no está en el catálogo
- **THEN** la operación se rechaza

### Requirement: Control de acceso por curso
Todas las rutas bajo `/c/{curso}` SHALL requerir que el usuario sea admin o esté matriculado en el curso, y SHALL responder 404 si el curso no existe o el usuario no tiene acceso.

#### Scenario: Estudiante sin matrícula
- **WHEN** un estudiante no matriculado en `aif-c01` solicita `/c/aif-c01/`
- **THEN** recibe 404

#### Scenario: Admin sin matrícula
- **WHEN** un admin solicita `/c/aif-c01/`
- **THEN** accede al curso

#### Scenario: Intento de otro curso
- **WHEN** un estudiante matriculado en el curso A abre un intento de B por su identificador
- **THEN** recibe 404

### Requirement: Selector «Mis cursos»
La página de inicio SHALL listar los cursos accesibles del usuario con su progreso, y SHALL redirigir directamente al curso cuando solo hay uno accesible. Un estudiante sin cursos SHALL ver un aviso indicando que debe solicitar acceso al administrador.

#### Scenario: Estudiante con dos cursos
- **WHEN** un estudiante matriculado en dos cursos abre `/`
- **THEN** ve ambos cursos con su progreso

#### Scenario: Estudiante sin cursos
- **WHEN** un estudiante sin matrículas abre `/`
- **THEN** ve el aviso de que no tiene cursos asignados

### Requirement: Administración de cursos
El admin SHALL disponer de un listado de cursos con título, número de módulos, preguntas y matriculados, y el listado de usuarios SHALL mostrar los cursos de cada uno.

#### Scenario: Listado de cursos
- **WHEN** el admin abre `/admin/cursos`
- **THEN** ve cada curso del catálogo con su número de matriculados
