# user-admin Specification

## Purpose
TBD - created by archiving change consola-web-curso. Update Purpose after archive.
## Requirements
### Requirement: Gestión de usuarios por el admin
El admin SHALL poder crear usuarios con nombre, usuario, rol y contraseña temporal, editar su rol y datos, desactivarlos y reactivarlos, y restablecer su contraseña.

#### Scenario: Alta de estudiante
- **WHEN** el admin crea un usuario con rol estudiante
- **THEN** el usuario puede iniciar sesión y se le obliga a cambiar la contraseña temporal

#### Scenario: Usuario desactivado
- **WHEN** el admin desactiva un usuario
- **THEN** no puede iniciar sesión y sus sesiones activas dejan de ser válidas, conservando su historial

#### Scenario: Usuario duplicado
- **WHEN** el admin crea un usuario con un nombre de usuario existente
- **THEN** se rechaza con un mensaje de error

### Requirement: Primer administrador y protección del último admin
El sistema SHALL crear el primer admin mediante comando o variables de entorno, sin credenciales por defecto, y SHALL impedir desactivar o degradar al último admin activo.

#### Scenario: Degradar al último admin
- **WHEN** el admin intenta cambiar su propio rol siendo el único admin activo
- **THEN** la operación se rechaza

### Requirement: Cambio de contraseña propio
Cualquier usuario SHALL poder cambiar su contraseña indicando la actual.

#### Scenario: Contraseña actual incorrecta
- **WHEN** se envía una contraseña actual errónea
- **THEN** el cambio se rechaza

