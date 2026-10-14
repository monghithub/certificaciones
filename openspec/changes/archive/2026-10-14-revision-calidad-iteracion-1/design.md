## Context

Revisión de la Iteración 1 a petición del usuario. Se verificó cada afirmación dudosa en la documentación oficial (páginas de servicio, lista de PrivateLink, capa gratuita, guía del examen v1.1). El conjunto oficial de práctica de AWS Skill Builder requiere iniciar sesión y no puede reproducirse; los *dumps* están prohibidos por `promt.md`.

## Goals / Non-Goals

**Goals:**
- Eliminar errores factuales y datos desactualizados del material existente.
- Cubrir con suficiente profundidad los 17 objetivos del Dominio 1.
- Un banco amplio y exigente, con preguntas originales al estilo del examen.
- Que las lecciones aprendidas se apliquen automáticamente al resto del proyecto.

**Non-Goals:**
- Escribir los módulos 02 a 06 (iteraciones posteriores).
- Cambios en la consola web.

## Decisions

- **Reglas en `AGENTS.md` y controles en la CI.** Las reglas escritas guían a quien redacta; los controles automáticos (posición de la respuesta, opciones repetidas, mínimo por objetivo) impiden regresiones. Las heurísticas con falsos positivos (absolutos en distractores, enunciados cortos) son avisos, no errores.
- **Mínimos: 60 por módulo, 15 por tarea, 3 por objetivo.** Garantizan profundidad en todos los objetivos y no solo en los fáciles. Alternativa descartada: un mínimo proporcional al peso del dominio, más complejo de explicar.
- **Reparto de la posición de la respuesta en el propio banco.** El quiz y la consola no barajan las opciones; repartirlas en el YAML evita sesgos sin tocar el código de la consola.
- **Alias genéricos fuera del glosario.** «SageMaker Pipelines» o «SageMaker Canvas» en lugar de «Pipelines» o «Canvas», para no enlazar palabras comunes.

## Risks / Trade-offs

- [Mínimos más altos alargan las iteraciones 2–5] → se compensa con calidad del banco y con las reglas ya escritas.
- [Los avisos heurísticos pueden ignorarse] → `AGENTS.md` pide revisar los `AVISO` antes de cada commit.
- [Este cambio se documenta después de implementarse] → se registra en el journal; los siguientes cambios seguirán el flujo propuesta → implementación → archivo.
