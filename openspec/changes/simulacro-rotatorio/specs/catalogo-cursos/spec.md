## MODIFIED Requirements

### Requirement: Manifiesto del curso

El manifiesto SHALL declarar `slug`, `titulo`, `idioma` y `dominios` (cada uno con `id`, `nombre` y `peso`, sumando los pesos 100), y MAY declarar `proveedor` (nombre del proveedor de la certificación), `fuentes_oficiales` (lista de hosts de su documentación oficial), `examen` (preguntas y minutos del simulacro, y opcionalmente `tipos` y `distribucion`, que fija el reparto de tipos de cada intento), `simulacro` (módulo del simulacro) y `banco` (mínimos y distribución por tipos, incluido `minimo_simulacro_por_objetivo`, el mínimo de preguntas del banco del simulacro por objetivo oficial). SHALL validarse con `schemas/curso.schema.json`.

#### Scenario: Pesos que no suman 100

- **WHEN** los pesos de los dominios suman 95
- **THEN** la validación del manifiesto falla

#### Scenario: Curso sin simulacro

- **WHEN** el manifiesto no declara `examen` ni `simulacro`
- **THEN** el curso es válido y no ofrece simulacro

#### Scenario: Curso de otro proveedor

- **WHEN** un curso declara `proveedor: Microsoft` y `fuentes_oficiales: [learn.microsoft.com]`
- **THEN** el manifiesto es válido sin cambios de código

#### Scenario: Mínimo por objetivo en el simulacro

- **WHEN** un curso declara `banco: {minimo_simulacro_por_objetivo: 1}`
- **THEN** el manifiesto es válido y `Manifiesto.minimo_simulacro_por_objetivo` vale 1
