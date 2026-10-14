# modulo-01-fundamentos-ia-ml Specification

## Purpose
TBD - created by archiving change iteracion-1-modulos-00-01. Update Purpose after archive.
## Requirements
### Requirement: Plantilla de módulo y mapa de cobertura
`modulos/01-fundamentos-ia-ml/README.md` SHALL incluir objetivos de aprendizaje con correspondencia a las tareas 1.1, 1.2 y 1.3, un mapa de cobertura, teoría con diagramas Mermaid, entre 5 y 10 puntos clave y referencias oficiales.

#### Scenario: Estructura completa
- **WHEN** se lee el README del módulo 01
- **THEN** contiene las cinco secciones de la plantilla en ese orden

### Requirement: Cobertura íntegra del Dominio 1
El mapa de cobertura SHALL tener una fila por cada uno de los 17 objetivos de `fuentes/dominio-1.md` (identificados como `1.M.K`), cada una enlazada a la sección que lo cubre.

#### Scenario: Todos los objetivos cubiertos
- **WHEN** se ejecuta `comprobar_cobertura.py --curso aif-c01 --modulo 01`
- **THEN** informa de 17/17 objetivos cubiertos y termina con código 0

### Requirement: Servicios, trampas y criterios de decisión
El módulo SHALL incluir `servicios.md` (tabla servicio → caso de uso → cuándo NO usarlo) y `trampas.md` (errores y distractores habituales), y SHALL tratar los criterios de decisión del Dominio 1: cuándo ML no es apropiado, elección de técnica (regresión, clasificación, clustering), servicio gestionado frente a modelo propio, y modelo tradicional frente a modelo fundacional.

#### Scenario: Tabla de servicios
- **WHEN** se lee `servicios.md`
- **THEN** cada fila indica el caso de uso y cuándo no usarlo, y solo incluye servicios dentro de alcance

### Requirement: Alcance
El módulo SHALL mencionar solo para su reconocimiento los temas fuera de alcance del examen (programar modelos, ingeniería de datos o de *features*, ajuste de hiperparámetros, pipelines, matemáticas) y SHALL NOT tratar como evaluable ningún servicio de la lista out of scope ni Amazon Q mientras el marcador de `servicios-alcance.md` siga abierto.

#### Scenario: Servicio fuera de alcance
- **WHEN** el texto menciona un servicio de la lista out of scope
- **THEN** lo hace indicando que no es materia evaluable

### Requirement: Laboratorio demostrativo
Si se incluye `laboratorio.md`, SHALL contener objetivo y relación con tareas, requisitos previos, pasos por consola (y CLI o boto3 si es razonable), estimación de coste basada en precios oficiales o marcada como pendiente, advertencia de facturación y una sección de limpieza de recursos.

#### Scenario: Limpieza presente
- **WHEN** se lee `laboratorio.md`
- **THEN** existe una sección de limpieza aunque no queden recursos persistentes

