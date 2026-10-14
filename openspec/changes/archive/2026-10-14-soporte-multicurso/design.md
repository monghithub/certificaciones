## Context

Estado actual: contenido en `modulos/` y `fuentes/` de la raíz; `schemas/pregunta.schema.json` limita `dominio` a 1–5 y `id` a `D1–D5|S`; `validar_preguntas.py` y la consola traen fijos los mínimos (30/65), el simulacro (65 preguntas, 90 min) y la lista de dominios; la consola carga un único directorio (`COURSE_DIR`), con rutas sin prefijo y tablas sin noción de curso. Hay una instancia en marcha con un administrador y sin datos de estudio, y otros cambios aún no archivados dependen de estas rutas.

## Goals / Non-Goals

**Goals:**
- Poder añadir un curso creando una carpeta `cursos/<slug>/` con su `curso.yaml`, sin tocar código.
- Matricular usuarios por curso y aislar el acceso.
- Progreso e historial por curso, con migración sin pérdida.
- Que las herramientas de calidad (validador, quiz, cobertura) funcionen por curso.

**Non-Goals:**
- Roles por curso, autoinscripción, edición de contenido desde la web, certificados.
- Ocultar la existencia de cursos al admin ni cuotas por curso.

## Decisions

1. **Layout `cursos/<slug>/` en este repositorio.** El `slug` (`^[a-z0-9][a-z0-9-]{1,62}$`) es la carpeta y el identificador estable en base de datos y URL. Un curso es válido si tiene `curso.yaml`. Alternativa descartada: un repositorio por curso (duplicaría herramientas o exigiría empaquetarlas). El esquema, el validador, el quiz y la consola quedan comunes.

2. **Manifiesto `curso.yaml`**, validado con `schemas/curso.schema.json`:
   ```yaml
   slug: aif-c01            # debe coincidir con la carpeta
   titulo: AWS Certified AI Practitioner (AIF-C01)
   idioma: es-ES
   dominios:
     - {id: 1, nombre: Fundamentos de IA y ML, peso: 20}
   examen:                  # opcional: habilita el simulacro
     preguntas: 65
     minutos: 90
   banco:
     minimo_por_modulo: 30
     minimo_simulacro: 65
     distribucion: {multiple_choice: 60, multiple_response: 20, ordering: 10, matching: 10}
   ```
   Los pesos de dominio suman 100. El módulo de simulacro es el que lleva el prefijo `06-` hoy; se generaliza con la clave opcional `simulacro: 06-simulacro` en el manifiesto (si falta, el curso no ofrece simulacro). Los módulos de dominio con banco exigible son los que no son el simulacro y tienen `preguntas.yaml` no vacío (el módulo 00 no lo tiene).

3. **Esquema de pregunta genérico.** `dominio`: entero ≥ 1; `id`: `^(D[0-9]{1,2}|S)-[0-9]{3}$`; `tarea`: `^[0-9]+\.[0-9]+$`. Las comprobaciones que dependen del curso (dominio declarado en el manifiesto, tarea presente en `fuentes/dominio-N.md`, mínimos, distribución) las hace el validador leyendo el manifiesto. El esquema del AIF-C01 sigue validando igual.

4. **Herramientas.** `validar_preguntas.py [--curso SLUG|RUTA] [--raiz]`: sin `--curso` valida todos los cursos de `cursos/` y sale con error si falla alguno; valida también cada `curso.yaml`. `quiz.py --curso SLUG`; si solo existe un curso, es opcional. Los parámetros salen del manifiesto, no de constantes.

5. **Consola: catálogo.** `COURSES_DIR` (por defecto `<repo>/cursos`) sustituye a `COURSE_DIR`. Una clase `Catalogo` descubre `*/curso.yaml`, crea un `Contenido` por curso (el cargador actual, parametrizado por la carpeta del curso y la ruta del esquema de preguntas) y expone `catalogo.cursos[slug]`. Un curso con manifiesto inválido se omite y genera un aviso visible para el admin. El esquema se empaqueta en la imagen (se elimina su montaje).

6. **Matrícula.** Tabla `matricula(id, usuario_id → usuario ON DELETE CASCADE, curso VARCHAR(64), creado)`, única por (usuario, curso). Se guarda el slug como texto y no una clave foránea, porque los cursos viven en el sistema de ficheros: si una carpeta desaparece, la matrícula y el historial se conservan. Los admin tienen acceso a todos los cursos sin matrícula. Quitar una matrícula no borra el historial; al volver a matricular reaparece.

7. **Rutas.** Todo lo del curso cuelga de `/c/{curso}`: `/`, `/modulo/{m}/{s}`, `/tests…`, `/estadisticas`. `/` global muestra «Mis cursos» (o redirige al único accesible). Una dependencia `requiere_curso` resuelve el slug, comprueba matrícula o rol admin y devuelve **404** si no existe o no hay acceso (no revela qué cursos existen). Se mantienen sin prefijo `/login`, `/logout`, `/cuenta/password` y `/admin/…`. No se añaden redirecciones desde las URL antiguas (instancia personal sin enlaces externos).

8. **Datos por curso.** Migración Alembic `0002`: añade `curso` (NOT NULL, `server_default='aif-c01'`) a `progreso_lectura` e `intento`; sustituye la restricción única de progreso por (usuario, curso, modulo, seccion) con operaciones por lotes; crea `matricula`; inserta una matrícula `aif-c01` por cada usuario con rol `estudiante`. El valor por defecto solo existe para migrar filas previas; el código siempre informa el curso. `intento_respuesta` hereda el curso del intento.

9. **Simulacro por curso.** Preguntas y minutos salen de `examen` en el manifiesto; si el curso no lo define, la opción no aparece. Los ajustes `simulacro_*` de `Settings` desaparecen (los tests los configuran con un manifiesto de prueba).

10. **Administración.** Alta de usuario con casillas de cursos; detalle de usuario con matrículas (añadir/quitar) y estadísticas con selector de curso; listado de usuarios con sus cursos; nueva página `/admin/cursos` con título, módulos, preguntas y matriculados; «Recargar contenido» recarga todo el catálogo.

11. **Orden de migración del repositorio.** Mover ficheros (`fuentes/`, `modulos/`) con `mv` —están sin versionar—, crear `curso.yaml` del AIF-C01 con los pesos oficiales ya transcritos (20/24/28/14/14), actualizar documentación, CI y Docker, y recién después tocar el código. Las pruebas existentes se adaptan a la nueva ruta.

## Risks / Trade-offs

- [Cambio de rutas rompe marcadores y documentación] → Actualizar README, AGENTS y docs en el mismo cambio; instancia personal, sin redirecciones.
- [Migración de BD sobre el volumen existente] → Prueba con una base creada en el esquema 0001 con datos sintéticos antes de aplicar; copia de seguridad documentada antes de migrar la instancia real.
- [Restricción única recreada en SQLite] → `render_as_batch` ya está activo en Alembic; se verifica con prueba de migración.
- [Slugs en tablas sin FK] → Se tolera un curso desaparecido: el historial muestra el slug y se marca «curso no disponible».
- [Generalizar esquema sin perder validación] → El validador mantiene todas las comprobaciones específicas leyendo el manifiesto; tests con un segundo curso de prueba con dominios distintos.
- [Complejidad adicional en la consola] → Una única dependencia de acceso y un prefijo común; las vistas actuales se reutilizan con el curso en el contexto.

## Migration Plan

1. Hacer copia de la base de datos de la instancia en marcha (procedimiento de `docs/consola.md`).
2. Mover ficheros, añadir manifiesto y ajustar herramientas; pasar tests.
3. Reconstruir la imagen: Alembic aplica `0002` al arrancar y matricula a los estudiantes existentes en `aif-c01`.
4. Comprobar acceso con admin y un estudiante de prueba. Reversión: restaurar la copia y la imagen anterior (`alembic downgrade` está implementado para `0002`).

## Open Questions

- `promt.md` es específico del AIF-C01: se deja en la raíz por ahora; ¿lo muevo a `cursos/aif-c01/`? Las reglas generales de colaboración seguirán en `AGENTS.md`.
- ¿El nombre visible del curso debe poder cambiarse desde la consola? Se asume que no (se edita en `curso.yaml`).
