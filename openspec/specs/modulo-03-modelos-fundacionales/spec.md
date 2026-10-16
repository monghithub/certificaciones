# modulo-03-modelos-fundacionales Specification

## Purpose
TBD - created by archiving change iteracion-3-modulo-03-fm. Update Purpose after archive.
## Requirements
### Requirement: Cobertura del Dominio 3
`modulos/03-modelos-fundacionales/README.md` SHALL incluir objetivos de aprendizaje, un mapa de cobertura con los 19 objetivos de `fuentes/dominio-3.md` enlazados a su sección, teoría con ejemplos de negocio y diagramas Mermaid, entre 5 y 10 puntos clave y referencias oficiales.

#### Scenario: Cobertura completa
- **WHEN** se ejecuta `comprobar_cobertura.py --curso aif-c01`
- **THEN** el módulo 03 informa 19/19 objetivos sin errores

### Requirement: Calidad del contenido
El módulo SHALL cumplir «Calidad del contenido» de `AGENTS.md`: disponibilidad y nombres vigentes de cada servicio, definición, criterio de decisión, ejemplo y trampa por objetivo, un ejemplo numérico de las métricas de evaluación y del coste de la personalización, y un caso de RAG de principio a fin.

#### Scenario: Revisión de cierre
- **WHEN** se cierra la iteración
- **THEN** una revisión independiente no encuentra errores factuales sin corregir y deja registro en `CHANGELOG.md` y `docs/journal.md`

### Requirement: Servicios y trampas
`servicios.md` SHALL listar en su primera columna cada servicio dentro de alcance tratado (servicio → caso de uso → cuándo NO usarlo), con entrada en el glosario, y `trampas.md` SHALL recoger los errores y distractores habituales del dominio.

#### Scenario: Servicio sin entrada en el glosario
- **WHEN** un servicio de `servicios.md` no tiene entrada en `glosario.yaml`
- **THEN** `validar_preguntas.py` falla

