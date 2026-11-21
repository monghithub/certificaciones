## ADDED Requirements

### Requirement: Simulacro en la terminal

`scripts/quiz.py --simulacro` SHALL componer el cuestionario con la misma extracción que la consola (cuotas por dominio y tipo y objetivos sin repetir), admitir `--semilla` para obtener siempre la misma selección y no aplicar los filtros `--modulo`, `--dominio`, `--tipo` ni `--n`.

#### Scenario: Simulacro reproducible

- **WHEN** se ejecuta dos veces `quiz.py --curso aif-c01 --simulacro --semilla 3`
- **THEN** ambas plantean las mismas 65 preguntas en el mismo orden
