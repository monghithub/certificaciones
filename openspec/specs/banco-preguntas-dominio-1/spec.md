# banco-preguntas-dominio-1 Specification

## Purpose
TBD - created by archiving change iteracion-1-modulos-00-01. Update Purpose after archive.
## Requirements
### Requirement: Tamaño y distribución del banco
`modulos/01-fundamentos-ia-ml/preguntas.yaml` SHALL contener al menos 60 preguntas con ids `D1-NNN`, con una proporción aproximada de 60 % `multiple_choice`, 20 % `multiple_response`, 10 % `ordering` y 10 % `matching` (dentro de la tolerancia del validador), y la respuesta correcta de opción múltiple SHALL estar repartida entre las letras.

#### Scenario: Banco válido
- **WHEN** se ejecuta `validar_preguntas.py --curso aif-c01`
- **THEN** valida el banco sin errores ni avisos

### Requirement: Reparto por tareas
Cada tarea 1.1, 1.2 y 1.3 SHALL tener al menos 15 preguntas, y cada objetivo SHALL estar cubierto por al menos 3 preguntas, indicando en `tarea` la Task Statement y en `objetivo` el objetivo oficial.

#### Scenario: Objetivo con pocas preguntas
- **WHEN** algún objetivo del Dominio 1 tiene menos de 3 preguntas
- **THEN** `comprobar_cobertura.py --preguntas` informa de error

### Requirement: Calidad de las preguntas
Las preguntas SHALL ser escenarios de negocio realistas, de elaboración propia (sin reproducir preguntas reales del examen ni material de terceros), con todos los distractores plausibles y explicados, sin «todas/ninguna de las anteriores», y con dificultad repartida entre baja, media y alta.

#### Scenario: Distractor sin explicar
- **WHEN** una opción incorrecta carece de entrada en `distractores`
- **THEN** el validador informa de error

### Requirement: Referencias verificables
Cada pregunta SHALL incluir en `referencia` una URL oficial de AWS que responda correctamente y respalde la respuesta correcta.

#### Scenario: URL rota
- **WHEN** la URL de una referencia no responde con éxito
- **THEN** la comprobación de enlaces de la entrega la señala y se corrige antes del cierre

### Requirement: Disponibilidad en la consola
Tras recargar el catálogo, el banco SHALL aparecer en la consola para los estudiantes matriculados en `aif-c01`, y las preguntas SHALL poder responderse en sus cuatro tipos.

#### Scenario: Test por dominio
- **WHEN** un estudiante matriculado inicia un test del dominio 1
- **THEN** se le presentan preguntas del módulo 01 sin errores de carga

