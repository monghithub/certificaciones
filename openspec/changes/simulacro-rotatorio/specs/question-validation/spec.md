## MODIFIED Requirements

### Requirement: Mínimos y distribución

El validador SHALL exigir al menos 30 preguntas por módulo de dominio con banco no vacío (o `banco.minimo_por_modulo`) y, en el simulacro, `banco.minimo_simulacro`, e informar de la distribución por tipos, avisando cuando se aleje más de 10 puntos porcentuales de 60/20/10/10 (o del reparto de `banco.distribucion`). En el simulacro, si el manifiesto declara `examen.distribucion`, el aviso SHALL usar ese reparto. Una opción `--sin-minimos` SHALL desactivar la exigencia de mínimos.

#### Scenario: Banco con menos de 30

- **WHEN** un módulo de dominio tiene 12 preguntas y no se pasa `--sin-minimos`
- **THEN** se reporta error

#### Scenario: Distribución desviada

- **WHEN** un banco de 30 preguntas tiene 100 % multiple_choice
- **THEN** se emite aviso sin error

#### Scenario: Reparto del simulacro

- **WHEN** el simulacro solo tiene preguntas de opción múltiple y `examen.distribucion` es `{multiple_choice: 100}`
- **THEN** el validador no avisa de que falten preguntas de ordenación o de emparejamiento

#### Scenario: Banco del simulacro por debajo del mínimo

- **WHEN** `banco.minimo_simulacro` es 80 y el simulacro tiene 70 preguntas
- **THEN** se reporta error

## ADDED Requirements

### Requirement: Banco del simulacro suficiente para formar un examen

Si el banco del simulacro tiene más preguntas que `examen.preguntas`, el validador SHALL calcular las cuotas por dominio y tipo de un intento (capacidad `simulacro-rotatorio`) y SHALL dar un error por cada dominio y tipo en el que el banco tenga menos preguntas que la cuota. SHALL imprimir en el resumen el reparto de un intento y las repeticiones de objetivo inevitables por dominio. Si el banco tiene exactamente `examen.preguntas`, SHALL mantenerse el comportamiento anterior (solo el aviso de reparto).

#### Scenario: Celda insuficiente

- **WHEN** la cuota de respuesta múltiple del Dominio 3 es 4 y el banco solo tiene 3
- **THEN** el validador informa de un error que nombra el dominio, el tipo, la cuota y las disponibles

#### Scenario: Banco del tamaño del examen con reparto desviado

- **WHEN** el simulacro tiene 65 preguntas, `examen.preguntas` es 65 y 14 son de respuesta múltiple
- **THEN** el validador no informa de error por las cuotas

### Requirement: Ids del simulacro

El validador SHALL dar un error si una pregunta del módulo de simulacro no tiene un id con formato `S-NNN` o si una pregunta de otro banco usa ese formato.

#### Scenario: Id de módulo en el simulacro

- **WHEN** una pregunta del simulacro tiene el id `D3-099`
- **THEN** se reporta error
