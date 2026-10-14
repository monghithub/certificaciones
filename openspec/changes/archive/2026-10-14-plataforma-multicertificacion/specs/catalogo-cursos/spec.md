## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: Referencias en las fuentes oficiales del curso
El esquema de pregunta SHALL exigir que `referencia` sea una URL https, y cuando el manifiesto declare `fuentes_oficiales`, `validar_preguntas.py` SHALL fallar si el host de la referencia no es uno de esos hosts ni un subdominio suyo.

#### Scenario: Referencia de otro proveedor
- **WHEN** una pregunta de un curso con `fuentes_oficiales: [docs.aws.amazon.com, aws.amazon.com]` cita `https://learn.microsoft.com/...`
- **THEN** el validador informa de error indicando las fuentes aceptadas

#### Scenario: Curso sin fuentes declaradas
- **WHEN** un curso no declara `fuentes_oficiales`
- **THEN** se acepta cualquier referencia https
