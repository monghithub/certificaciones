## ADDED Requirements

### Requirement: Inicio y cierre de sesión
El sistema SHALL autenticar con usuario y contraseña, mantener la sesión mediante cookie firmada `HttpOnly` y `SameSite`, y permitir cerrar sesión. No SHALL existir registro público.

#### Scenario: Login correcto
- **WHEN** un usuario activo envía credenciales válidas
- **THEN** se crea la sesión y se redirige al índice del curso

#### Scenario: Credenciales inválidas
- **WHEN** las credenciales son incorrectas
- **THEN** se muestra un error genérico sin revelar si el usuario existe

#### Scenario: Limitación de intentos
- **WHEN** se superan 5 intentos fallidos consecutivos para un usuario o IP
- **THEN** el sistema bloquea temporalmente nuevos intentos

### Requirement: Control de acceso por rol
El sistema SHALL tener los roles `admin` y `estudiante`. Las rutas de administración SHALL ser accesibles solo al admin y un estudiante SHALL acceder solo a sus propios datos.

#### Scenario: Estudiante accede a administración
- **WHEN** un estudiante solicita una ruta `/admin/*`
- **THEN** recibe 403

#### Scenario: Sin sesión
- **WHEN** un visitante anónimo solicita cualquier ruta salvo login
- **THEN** se redirige al login

### Requirement: Almacenamiento seguro de contraseñas
Las contraseñas SHALL almacenarse únicamente como hash argon2 y nunca registrarse en logs.

#### Scenario: Base de datos inspeccionada
- **WHEN** se consulta la tabla de usuarios
- **THEN** no existe ninguna contraseña en claro
