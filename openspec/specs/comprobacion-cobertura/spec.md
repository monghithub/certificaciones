# comprobacion-cobertura Specification

## Purpose
TBD - created by archiving change iteracion-1-modulos-00-01. Update Purpose after archive.
## Requirements
### Requirement: Comprobación de cobertura de objetivos
`scripts/comprobar_cobertura.py` SHALL aceptar `--curso` y `--modulo`, extraer los ids `N.M.K` de `fuentes/dominio-N.md` y comprobar que cada uno aparece en una fila del mapa de cobertura del README del módulo con un enlace a un ancla existente en ese README. SHALL terminar con código 1 si falta alguno.

#### Scenario: Objetivo sin cubrir
- **WHEN** el mapa de cobertura no incluye el objetivo `1.2.3`
- **THEN** el script lo lista como no cubierto y termina con código 1

#### Scenario: Enlace a ancla inexistente
- **WHEN** una fila enlaza a `#seccion-que-no-existe`
- **THEN** el script informa del enlace roto y termina con código 1

### Requirement: Comprobación de preguntas por tarea
Con `--preguntas`, el script SHALL comprobar que cada tarea del dominio tiene al menos el mínimo de preguntas configurado (por defecto 1) y que cada objetivo está referenciado por al menos una pregunta cuando las preguntas declaran `objetivo`.

#### Scenario: Tarea sin preguntas
- **WHEN** la tarea 1.3 no tiene ninguna pregunta
- **THEN** el script informa de error

### Requirement: Resumen de cobertura
El script SHALL imprimir, por módulo y tarea, los objetivos cubiertos frente a los totales y el número de preguntas, para usarse en el resumen de cierre de cada iteración.

#### Scenario: Resumen
- **WHEN** todo está cubierto
- **THEN** imprime, p. ej., `1.1: 5/5 objetivos, 10 preguntas` y termina con código 0

### Requirement: Integración en CI y módulos vacíos
El script SHALL ejecutarse en el CI y SHALL omitir los módulos sin README con mapa de cobertura salvo que se pida con `--modulo`.

#### Scenario: Módulos pendientes
- **WHEN** el módulo 02 aún no tiene contenido
- **THEN** el script lo omite sin error

