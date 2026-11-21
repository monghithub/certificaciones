# Instrucciones para Claude

Las reglas del repositorio están en [AGENTS.md](AGENTS.md), importado abajo, y son de obligado cumplimiento
(contenido, banco de preguntas, diagramas, flujo OpenSpec, Git y journal). Este fichero solo añade el resumen
operativo para empezar a trabajar.

Si existe `CLAUDE.local.md` (no versionado, solo en la instancia de trabajo), recoge el material local de consulta,
el despliegue y el **estado de trabajo y cómo retomarlo**: léelo antes de empezar.

@AGENTS.md
@CLAUDE.local.md

## Resumen operativo

- **Flujo:** issue → rama propia (`<slug>/<etapa>`, `feat/<tema>`, `docs/<tema>`) → commits *Conventional Commits*
  → PR a `main`. Nunca se trabaja directamente sobre `main`. Push y PR solo cuando lo pida el responsable.
- **Validación antes de cada commit:**

  ```bash
  python scripts/validar_preguntas.py && python scripts/comprobar_cobertura.py --preguntas \
    && python scripts/generar_glosario.py --comprobar && python -m pytest -q
  node tests/e2e/validar-mermaid.mjs cursos/*/modulos/*/README.md
  npx --yes markdownlint-cli2@0.17.2
  ```

- **Cierre de etapa:** `CHANGELOG.md` (qué cambia) y `docs/journal.md` (qué se hizo, qué se decidió y por qué).
- **Prohibido:** inventar datos, usar *dumps* o copiar material de terceros (el repositorio es público), y versionar
  secretos (`.env`).
