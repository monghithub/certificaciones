## ADDED Requirements

### Requirement: Despliegue con Docker
El proyecto SHALL incluir un `Dockerfile` que ejecute la app con usuario no root y un `compose.yaml` que monte un volumen persistente para la base de datos y el directorio del curso en solo lectura.

#### Scenario: Arranque
- **WHEN** se ejecuta `docker compose up`
- **THEN** la app queda accesible, aplica las migraciones y carga el contenido del curso

### Requirement: Configuración por entorno
La configuración (clave de sesión, ruta de base de datos, directorio del curso, datos del primer admin) SHALL leerse de variables de entorno, y la app SHALL negarse a arrancar sin clave de sesión.

#### Scenario: Sin clave de sesión
- **WHEN** falta `SECRET_KEY`
- **THEN** la app termina con un error explícito

### Requirement: Copias de seguridad
La documentación SHALL describir cómo respaldar y restaurar la base de datos SQLite.

#### Scenario: Restauración
- **WHEN** se sigue el procedimiento documentado con una copia válida
- **THEN** los usuarios y su historial quedan recuperados
