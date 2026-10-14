## ADDED Requirements

### Requirement: Workflow de CI
`.github/workflows/ci.yml` SHALL ejecutarse en cada `push` y `pull_request` y SHALL incluir markdownlint sobre los `.md`, comprobación de enlaces rotos con lychee, ejecución de `python scripts/validar_preguntas.py` y los tests del repositorio.

#### Scenario: Error de validación
- **WHEN** `validar_preguntas.py` termina con error
- **THEN** el workflow falla

#### Scenario: Enlace roto
- **WHEN** un `.md` contiene un enlace roto
- **THEN** el paso de lychee falla

### Requirement: Aviso de marcadores pendientes
El workflow SHALL buscar `PENDIENTE DE VERIFICAR` y emitir una anotación de aviso sin hacer fallar la build.

#### Scenario: Marcadores abiertos
- **WHEN** existen ficheros con `PENDIENTE DE VERIFICAR`
- **THEN** se emite un aviso con su ubicación y el job continúa con éxito
