## Why

El usuario quiere una revisión global: «cuadro resumen de los servicios que hay en AWS con su logo, como apartado de revisión global para hacernos una idea de la foto global, y un diagrama de dónde se usa o se relaciona cada uno» (issue #27).

## What Changes

- Página `/c/<curso>/mapa` («Mapa de servicios» en el menú) con los diagramas de `cursos/<curso>/mapa-servicios.md` y un cuadro resumen generado del glosario.
- Campo opcional `icono` en el glosario (validado) e iconos oficiales de AWS en `app/static/iconos/aws/`, excluidos de las licencias.
- Documentación, `LICENSE` y pruebas.

## Capabilities

### New Capabilities
- `mapa-servicios`: revisión global de los servicios del curso con iconos, alcance, módulos y diagramas de relaciones.

### Modified Capabilities
- `glosario-conceptos`: campo `icono`.

## Impact

`app/content.py`, `app/routes/course.py`, `app/templates/mapa.html` y `base.html`, `app/static/app.js` y `app.css`, `curso/alcance.py`, `curso/glosario.py`, `schemas/glosario.schema.json`, `cursos/aif-c01/glosario.yaml` y `mapa-servicios.md`, `LICENSE`. Sin migración.
