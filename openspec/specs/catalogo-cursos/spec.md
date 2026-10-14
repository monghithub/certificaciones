# catalogo-cursos Specification

## Purpose
TBD - created by archiving change soporte-multicurso. Update Purpose after archive.
## Requirements
### Requirement: Estructura de un curso
Cada curso SHALL residir en `cursos/<slug>/` con un manifiesto `curso.yaml`, un directorio `fuentes/` y un directorio `modulos/`. El `slug` SHALL coincidir con el nombre de la carpeta y cumplir `^[a-z0-9][a-z0-9-]{1,62}$`.

#### Scenario: Curso válido
- **WHEN** existe `cursos/aif-c01/curso.yaml` con `slug: aif-c01`
- **THEN** el catálogo lo reconoce como curso `aif-c01`

#### Scenario: Slug distinto de la carpeta
- **WHEN** `cursos/aif-c01/curso.yaml` declara `slug: otro`
- **THEN** el validador informa de error y la consola omite el curso con un aviso

### Requirement: Manifiesto del curso
El manifiesto SHALL declarar `slug`, `titulo`, `idioma` y `dominios` (cada uno con `id`, `nombre` y `peso`, sumando los pesos 100), y MAY declarar `proveedor` (nombre del proveedor de la certificación), `fuentes_oficiales` (lista de hosts de su documentación oficial), `examen` (preguntas y minutos del simulacro), `simulacro` (módulo del simulacro) y `banco` (mínimos y distribución por tipos). SHALL validarse con `schemas/curso.schema.json`.

#### Scenario: Pesos que no suman 100
- **WHEN** los pesos de los dominios suman 95
- **THEN** la validación del manifiesto falla

#### Scenario: Curso sin simulacro
- **WHEN** el manifiesto no declara `examen` ni `simulacro`
- **THEN** el curso es válido y no ofrece simulacro

#### Scenario: Curso de otro proveedor
- **WHEN** un curso declara `proveedor: Microsoft` y `fuentes_oficiales: [learn.microsoft.com]`
- **THEN** el manifiesto es válido sin cambios de código

### Requirement: Esquema de pregunta independiente del curso
`schemas/pregunta.schema.json` SHALL admitir cualquier dominio entero ≥ 1 y ids con formato `D<n>-NNN` o `S-NNN`. El validador SHALL comprobar que el `dominio` de cada pregunta exista en el manifiesto de su curso y que la `tarea` exista en `fuentes/dominio-N.md` de ese curso.

#### Scenario: Dominio no declarado
- **WHEN** una pregunta de un curso con dominios 1–3 declara `dominio: 4`
- **THEN** el validador informa de error

#### Scenario: Curso con dominios distintos
- **WHEN** un segundo curso declara los dominios 1–3 y sus preguntas son coherentes
- **THEN** el validador las acepta sin cambios de código

### Requirement: Herramientas por curso
`validar_preguntas.py` SHALL aceptar `--curso` (slug o ruta) y, sin él, validar todos los cursos de `cursos/` terminando con error si alguno falla. `quiz.py` SHALL aceptar `--curso` y SHALL tomarlo implícitamente cuando solo existe un curso. Mínimos, distribución y número de dominios SHALL salir del manifiesto.

#### Scenario: Validar todos los cursos
- **WHEN** se ejecuta `validar_preguntas.py` sin argumentos con dos cursos y errores en uno
- **THEN** informa de los errores indicando el curso y termina con código 1

#### Scenario: Quiz con varios cursos sin indicar curso
- **WHEN** hay dos cursos y se ejecuta `quiz.py` sin `--curso`
- **THEN** el script lo indica, lista los cursos disponibles y termina con error

### Requirement: Catálogo en la consola
La consola SHALL descubrir los cursos en `COURSES_DIR`, cargar cada uno de forma independiente y omitir con aviso (visible para el admin) los que tengan manifiesto o contenido inválido sin impedir el arranque.

#### Scenario: Un curso inválido no bloquea a los demás
- **WHEN** un curso tiene un `curso.yaml` malformado y otro es válido
- **THEN** la consola arranca, ofrece solo el válido y muestra el aviso al admin

### Requirement: Referencias en las fuentes oficiales del curso
El esquema de pregunta SHALL exigir que `referencia` sea una URL https, y cuando el manifiesto declare `fuentes_oficiales`, `validar_preguntas.py` SHALL fallar si el host de la referencia no es uno de esos hosts ni un subdominio suyo.

#### Scenario: Referencia de otro proveedor
- **WHEN** una pregunta de un curso con `fuentes_oficiales: [docs.aws.amazon.com, aws.amazon.com]` cita `https://learn.microsoft.com/...`
- **THEN** el validador informa de error indicando las fuentes aceptadas

#### Scenario: Curso sin fuentes declaradas
- **WHEN** un curso no declara `fuentes_oficiales`
- **THEN** se acepta cualquier referencia https

