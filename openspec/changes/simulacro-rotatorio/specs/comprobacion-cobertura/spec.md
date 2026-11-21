## ADDED Requirements

### Requirement: Cobertura de objetivos del simulacro

Con `--preguntas`, si el manifiesto declara `banco.minimo_simulacro_por_objetivo`, el script SHALL comprobar que cada objetivo oficial de los dominios del manifiesto (`fuentes/dominio-N.md`) tiene al menos ese número de preguntas en el banco del simulacro, SHALL informar de un error por cada objetivo que no lo cumpla y SHALL imprimir una línea de resumen con los objetivos cubiertos frente a los totales. Sin ese campo, no SHALL comprobar el simulacro.

#### Scenario: Objetivo sin pregunta en el simulacro

- **WHEN** `minimo_simulacro_por_objetivo` es 1 y ninguna pregunta del simulacro declara el objetivo `1.2.3`
- **THEN** el script informa de error y termina con código 1

#### Scenario: Curso sin mínimo declarado

- **WHEN** el manifiesto no declara `minimo_simulacro_por_objetivo`
- **THEN** el script no comprueba la cobertura del simulacro
