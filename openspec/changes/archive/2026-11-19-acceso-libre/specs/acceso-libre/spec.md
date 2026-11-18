## ADDED Requirements

### Requirement: Acceso libre en red local
Si `ACCESO_LIBRE_USUARIO` nombra un usuario activo, una petición sin sesión SHALL quedar identificada como ese usuario sin pedir credenciales. Si la variable no está definida, o el usuario no existe o está desactivado, la consola SHALL exigir login como hasta ahora.

#### Scenario: Entrar sin login
- **WHEN** `ACCESO_LIBRE_USUARIO=admin` y alguien abre `/` sin sesión
- **THEN** ve «Mis cursos» como `admin`, sin pasar por `/login`

#### Scenario: Por defecto
- **WHEN** la variable no está definida y alguien abre `/` sin sesión
- **THEN** se le redirige a `/login`

#### Scenario: Protecciones que se mantienen
- **WHEN** en modo libre se envía un formulario sin token CSRF
- **THEN** la consola lo rechaza
