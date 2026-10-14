## Why

El objetivo del repositorio, ahora llamado `certificaciones`, es reunir en la misma consola **todos los cursos de certificación** que el usuario vaya estudiando, de cualquier proveedor, no solo AWS. Aún quedan restos del curso inicial atados a AWS o a AIF-C01: el esquema de pregunta solo admite referencias de `aws.amazon.com`, el título de la consola, el nombre de la imagen Docker, un `AGENTS.md` raíz con reglas específicas de AWS y `promt.md` (la especificación de AIF-C01) en la raíz.

## What Changes

- **Manifiesto:** nuevos campos `proveedor` y `fuentes_oficiales` (hosts de la documentación oficial del curso) en `curso.yaml` y en `schemas/curso.schema.json`.
- **Validación:** el esquema de pregunta admite cualquier URL https en `referencia`, y `validar_preguntas.py` exige que su host pertenezca a las `fuentes_oficiales` del curso (o a un subdominio). Sin `fuentes_oficiales`, basta con https.
- **Reglas:** `AGENTS.md` raíz pasa a ser genérico (reglas comunes, cómo añadir un curso, flujo de OpenSpec, convenciones de Git con ámbito y etiquetas por curso); lo propio de AWS y AIF-C01 se mueve a `cursos/aif-c01/AGENTS.md`.
- **Especificación del curso:** `promt.md` pasa a `cursos/aif-c01/promt.md`.
- **Consola y despliegue:** marca «Certificaciones», título de la API «Consola de certificaciones» e imagen `certificaciones-consola`.
- **README raíz:** visión multicertificación, tabla de cursos con proveedor y procedimiento para añadir un curso.
- Tests de las referencias por curso, incluido un curso de otro proveedor.

## Capabilities

### New Capabilities
<!-- Ninguna -->

### Modified Capabilities
- `catalogo-cursos`: el manifiesto declara proveedor y fuentes oficiales, y las referencias se validan contra ellas.
- `repo-docs`: estructura multicurso, README del curso y `AGENTS.md` comunes y por curso.

## Impact

- `schemas/`, `curso/manifiesto.py`, `scripts/validar_preguntas.py`, `cursos/aif-c01/curso.yaml`, `app/main.py`, `app/templates/base.html`, `compose.yaml`, `.github/workflows/ci.yml`, `.markdownlint-cli2.yaml`, `.lychee.toml`, `README.md`, `AGENTS.md`, `docs/consola.md` y tests.
- **Compatibilidad:** los cursos sin `fuentes_oficiales` siguen siendo válidos. La imagen Docker cambia de nombre: tras actualizar, `docker compose up -d --build` crea `certificaciones-consola` (la antigua `aif-c01-consola` puede borrarse). Los datos no se ven afectados.
