## ADDED Requirements

### Requirement: Chuleta de repaso
`cursos/aif-c01/chuleta.md` SHALL resumir en 2–3 páginas, por dominio, los criterios de decisión, los servicios y las trampas más frecuentes, con enlaces a los módulos.

#### Scenario: Repaso la víspera
- **WHEN** un estudiante lee la chuleta
- **THEN** encuentra para cada dominio las decisiones clave sin abrir los módulos

### Requirement: Glosario en Markdown sincronizado
`scripts/generar_glosario.py` SHALL generar `cursos/<curso>/glosario.md` desde `glosario.yaml` (término, alias, categoría y definición, por orden alfabético) y, con `--comprobar`, SHALL terminar con error si el fichero no coincide con el generado.

#### Scenario: Glosario desactualizado
- **WHEN** se añade una entrada a `glosario.yaml` sin regenerar `glosario.md`
- **THEN** `generar_glosario.py --comprobar` falla en la CI
