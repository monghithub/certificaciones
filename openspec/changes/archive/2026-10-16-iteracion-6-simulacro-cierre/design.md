## Context

El manifiesto declara `simulacro: 06-simulacro`, 65 preguntas y 90 minutos; la consola ofrece el simulacro cuando el banco del módulo tiene al menos 65 preguntas y toma las 65 primeras por `id`. El esquema de preguntas admite ids `S-NNN` y cualquier dominio del manifiesto. Hay 5 marcadores `PENDIENTE DE VERIFICAR` abiertos que dependen de contradicciones en las propias fuentes de AWS.

## Goals / Non-Goals

**Goals:**
- Un simulacro con los pesos oficiales (20/24/28/14/14 → 13/16/18/9/9), reparto de tipos ≈60/20/10/10, dificultad ≈20/60/20, letras repartidas, la correcta como opción más larga en torno a un 20–25 % y escenarios nuevos.
- Un control automático de que el simulacro no repite enunciados de los bancos.
- `glosario.md` siempre sincronizado con `glosario.yaml`.
- Una chuleta breve y útil la víspera del examen.

**Non-Goals:**
- Cambios en la consola o en el esquema.
- Etiquetar la versión 1.0.0.

## Decisions

- **Orden del simulacro:** las preguntas se escriben por dominio y se barajan con una semilla fija antes de numerarlas, para que los dominios aparezcan intercalados como en el examen.
- **Inéditas:** comparación de enunciados normalizados (minúsculas, sin signos ni espacios repetidos). Detecta copias literales; la novedad de los escenarios se garantiza en la redacción y en la revisión independiente.
- **Glosario Markdown generado:** una sola fuente de verdad (`glosario.yaml`, usado por la consola) y un Markdown derivado para leer en GitHub. `--comprobar` evita que se desincronicen.
- **Revisión cruzada de servicios:** comprobación puntual (no permanente) de que cada servicio de la lista oficial dentro de alcance aparece en algún módulo; se documenta en el journal.

## Risks / Trade-offs

- [El simulacro reutiliza conceptos de los módulos] → escenarios y datos nuevos; ningún enunciado repetido.
- [Marcadores pendientes] → se mantienen visibles; sin etiqueta 1.0.0 hasta resolverlos.

## Open Questions

- Ninguna bloqueante.
