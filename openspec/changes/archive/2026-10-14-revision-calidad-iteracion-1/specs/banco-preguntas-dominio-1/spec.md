## MODIFIED Requirements

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
