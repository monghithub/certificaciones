## 1. Reorganización del repositorio

- [x] 1.1 Hacer copia de la base de datos de la instancia en marcha (procedimiento de `docs/consola.md`)
- [x] 1.2 Mover `fuentes/` y `modulos/` a `cursos/aif-c01/` y crear `cursos/aif-c01/curso.yaml` con dominios y pesos oficiales (20/24/28/14/14), simulacro `06-simulacro` (65 preguntas, 90 minutos) y banco (30/65, 60/20/10/10)
- [x] 1.3 Crear `schemas/curso.schema.json` (slug, título, dominios con pesos que suman 100, examen, simulacro, banco)
- [x] 1.4 Actualizar rutas y textos en `README.md`, `AGENTS.md`, `docs/consola.md`, `CHANGELOG.md`, `.markdownlint-cli2.yaml`, `.lychee.toml`, `.dockerignore`
- [x] 1.5 Actualizar `compose.yaml` (montar `./cursos`, `COURSES_DIR=/cursos`) y `Dockerfile` (empaquetar `schemas/`, quitar el montaje de esquemas)

## 2. Esquemas y herramientas por curso

- [x] 2.1 Generalizar `schemas/pregunta.schema.json` (dominio ≥ 1, ids `D<n>-NNN|S-NNN`, tarea `N.M`)
- [x] 2.2 Crear el módulo común de lectura y validación de manifiestos (usable por scripts y consola)
- [x] 2.3 Adaptar `scripts/validar_preguntas.py`: `--curso`, validar todos los cursos, validar manifiestos, dominio contra manifiesto, mínimos y distribución desde el manifiesto
- [x] 2.4 Adaptar `scripts/quiz.py`: `--curso`, curso implícito si solo hay uno, error con lista si hay varios
- [x] 2.5 Adaptar fixtures y tests existentes a `cursos/<slug>/` y añadir tests con un segundo curso de dominios distintos y manifiestos inválidos

## 3. Consola: catálogo y modelo de datos

- [x] 3.1 Sustituir `COURSE_DIR` por `COURSES_DIR` en `Settings`, compose y docs; eliminar `simulacro_*` de `Settings`
- [x] 3.2 Implementar `Catalogo` (descubrimiento, carga por curso, avisos, recarga) y parametrizar `Contenido` por curso
- [x] 3.3 Añadir columna `curso` a `Intento` y `ProgresoLectura` y el modelo `Matricula`
- [x] 3.4 Escribir la migración Alembic `0002` (columnas con valor por defecto, restricción única por curso, tabla `matricula`, matrícula de estudiantes existentes) con su `downgrade`
- [x] 3.5 Probar la migración sobre una base 0001 con datos sintéticos (2 estudiantes, intentos y lecturas)

## 4. Consola: rutas y acceso

- [x] 4.1 Dependencia `requiere_curso` (admin o matriculado; 404 en otro caso) y contexto de curso para las plantillas
- [x] 4.2 Mover rutas de curso, tests y estadísticas bajo `/c/{curso}` y filtrar todas las consultas por curso
- [x] 4.3 Simulacro desde el manifiesto del curso (preguntas, minutos, disponibilidad)
- [x] 4.4 Inicio «Mis cursos» con redirección si solo hay uno y aviso si no hay ninguno
- [x] 4.5 Actualizar plantillas (navegación con el curso actual, enlaces, selector)

## 5. Consola: administración

- [x] 5.1 Matrícula en el alta de usuario (casillas de cursos válidos)
- [x] 5.2 Matrículas en el detalle del usuario (añadir/quitar) y estadísticas con selector de curso
- [x] 5.3 Listado de usuarios con sus cursos y página `/admin/cursos`
- [x] 5.4 «Recargar contenido» recarga todo el catálogo y muestra avisos por curso

## 6. Pruebas y despliegue

- [x] 6.1 Adaptar los tests de la consola y añadir los de matrícula, aislamiento entre cursos, 404 sin acceso, selector, simulacro por curso y progreso por curso
- [x] 6.2 Ejecutar la suite completa, `validar_preguntas.py` y `markdownlint`
- [x] 6.3 Reconstruir la instancia local: comprobar migración sobre el volumen real, acceso del admin y alta de un estudiante matriculado
- [x] 6.4 Actualizar `docs/consola.md` (añadir un curso, matrículas, backup antes de migrar) y `CHANGELOG.md`

## 7. Retomar la Iteración 1

- [x] 7.1 Ajustar `proposal.md`, `design.md` y rutas del cambio `iteracion-1-modulos-00-01` a `cursos/aif-c01/…`
