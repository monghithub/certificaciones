## 1. Base del proyecto

- [x] 1.1 Crear `app/` con FastAPI, configuración por entorno y arranque con comprobación de `SECRET_KEY`
- [x] 1.2 Añadir SQLAlchemy, Alembic y modelos `usuario`, `progreso_lectura`, `intento`, `intento_respuesta` con SQLite en modo WAL
- [x] 1.3 Extraer la corrección de `scripts/quiz.py` a un módulo compartido `curso/correccion.py`
- [x] 1.4 Crear `Dockerfile` (no root) y `compose.yaml` con volúmenes
- [x] 1.5 Ampliar el CI con tests de la app

## 2. Autenticación y usuarios (auth-roles, user-admin)

- [x] 2.1 Implementar hash argon2, login/logout, sesión por cookie firmada y CSRF
- [x] 2.2 Implementar limitación de intentos de login
- [x] 2.3 Implementar dependencias de autorización por rol
- [x] 2.4 Comando `python -m app.crear_admin` y creación opcional por entorno
- [x] 2.5 Panel admin: alta, edición, desactivación, reactivación y restablecimiento de contraseña
- [x] 2.6 Cambio obligatorio de contraseña temporal y cambio de contraseña propio
- [x] 2.7 Proteger al último admin activo
- [x] 2.8 Tests de autenticación y autorización por rol

## 3. Navegación del curso (course-navigation)

- [x] 3.1 Cargador de contenido desde `COURSE_DIR` con índice en memoria
- [x] 3.2 Renderizado Markdown sanitizado y Mermaid empaquetado localmente
- [x] 3.3 Vistas de índice y módulo con estado de progreso
- [x] 3.4 Registro de última sección, marcar completada y "continuar"
- [x] 3.5 Tests de navegación y renderizado

## 4. Motor de tests (quiz-engine)

- [x] 4.1 Carga y validación de preguntas con el esquema de la Iteración 0
- [x] 4.2 Inicio de cuestionario por módulo, dominio o mixto
- [x] 4.3 Vistas de pregunta para los cuatro tipos (incl. ordenación y emparejamiento con HTMX)
- [x] 4.4 Corrección, explicaciones y registro de respuestas
- [x] 4.5 Simulacro de 65 preguntas con cronómetro de servidor de 90 minutos
- [x] 4.6 Gestión de preguntas retiradas en el historial
- [x] 4.7 Tests del motor y del cronómetro

## 5. Estadísticas (progress-stats)

- [x] 5.1 Consultas agregadas por dominio y tarea
- [x] 5.2 Vista de estadísticas del estudiante y puntos débiles
- [x] 5.3 Vista admin: listado de usuarios y detalle por estudiante
- [x] 5.4 Tests de agregación y aislamiento entre usuarios

## 6. Cierre

- [x] 6.1 Documentar despliegue, variables, copia de seguridad y restauración en `docs/consola.md`
- [x] 6.2 Prueba de extremo a extremo con `docker compose up` y fixtures
- [x] 6.3 Resumen de cierre y parada para revisión humana
