## Context

La consola ya convierte cada bloque Mermaid en un diagrama animado (aparición escalonada, flechas animadas, respeto a «reducir movimiento») en el que **cada caja** abre un modal con definición, enlaces y «Ver en el curso», a partir del bloque `nodos` que sigue al diagrama. `AGENTS.md` fija el estilo y el validador lo comprueba.

## Goals / Non-Goals

**Goals:** reforzar con un gráfico los conceptos con estructura (decisión, flujo, ciclo, jerarquía, espectro); que cada caja enseñe algo al pulsarla y lleve al apartado o a la documentación oficial.

**Non-Goals:** nuevos tipos de gráfico o código en la consola; datos nuevos (los diagramas solo dibujan lo que ya dice la teoría verificada).

## Decisions

- **Mismo sistema que los 25 existentes** (Mermaid `flowchart` + `nodos`): ya es dinámico e interactivo, funciona en claro, oscuro y móvil, y lo valida la CI.
- **Sin datos nuevos:** cada caja resume una afirmación del apartado y enlaza su fuente oficial (la misma que cita el texto). Si un diagrama necesitara un dato no verificado, se descarta esa caja.
- **Decisiones como árbol** con nodos `decision` (rombos) y salidas `servicio`/`proceso`; **inclusión con `subgraph` anidados** (regla de `AGENTS.md`); ciclos con una flecha de vuelta.
- **Tamaño contenido:** de 4 a 9 cajas, legibles en móvil; dirección `TB` en los árboles de decisión.
- **Revisión independiente** de los diagramas contra el texto de cada apartado antes del PR.

## Risks / Trade-offs

- [Diagramas que repiten la tabla de al lado] → solo se dibuja la estructura (orden, condiciones, inclusión) y la tabla conserva el detalle.
- [Más carga de página] → Mermaid ya está cargado; los diagramas se dibujan al cargar.

## Open Questions

- Ninguna bloqueante.
