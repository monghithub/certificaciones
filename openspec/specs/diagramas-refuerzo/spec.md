# diagramas-refuerzo Specification

## Purpose
Diagramas de refuerzo en los apartados con procesos, decisiones, ciclos o jerarquías.
## Requirements

### Requirement: Diagramas de refuerzo
Los apartados de teoría con un proceso, una decisión, un ciclo, una jerarquía o un espectro SHALL incluir un diagrama Mermaid con el estilo del proyecto y un bloque `nodos` que cubra todas sus cajas. Cada caja SHALL resumir una afirmación del propio apartado, sin datos nuevos, y enlazar su fuente oficial o el apartado del curso.

#### Scenario: Regiones
- **WHEN** el estudiante lee «Servicios centrales» del módulo 00
- **THEN** ve un diagrama de cómo se elige una Región y, al pulsar cada criterio, su explicación y la documentación oficial

#### Scenario: Validación
- **WHEN** un diagrama nuevo tiene una caja sin entrada en `nodos`
- **THEN** `validar_preguntas.py` informa del error y la CI falla
