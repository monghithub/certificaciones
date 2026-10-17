## Context

Las preguntas viven en `modulos/*/preguntas.yaml` y la consola las carga en `Contenido.preguntas`; los modos módulo, dominio y mixto ya muestran la corrección tras cada respuesta, el simulacro no. Las respuestas se guardan en `intento_respuesta` con dominio y tarea. El mapa de cobertura de cada README enlaza cada objetivo con su sección.

## Goals / Non-Goals

**Goals:**
- Preguntas de repaso cortas que enseñen (explicación de 2–4 frases y distractores explicados), separadas de las de examen.
- Ver la explicación de cada pregunta al responderla en cualquier test, con enlace a la teoría.
- Repetir lo fallado hasta acertarlo.

**Non-Goals:**
- Repetición espaciada con calendario (se puede añadir después sobre el modo «repetir falladas»).
- Cambiar los bancos de examen o el simulacro.

## Decisions

- **Fichero aparte (`repaso.yaml`) con el mismo esquema** en lugar de un campo en `preguntas.yaml`: los modos de examen, el simulacro y sus reglas de calidad no cambian, y el validador distingue el banco por el nombre del fichero.
- **Dominio 0 = conocimientos previos**, solo en bancos de repaso y solo si `curso.yaml` declara `repaso.previos`; tarea `CP` y objetivo `CP.N` (el mapa de cobertura del módulo 00 ya usa `CP.N`).
- **Estadísticas comunes:** las respuestas de repaso cuentan en los aciertos por dominio y tarea, porque miden el conocimiento de esa tarea; el dominio 0 aparece aparte con su nombre.
- **Modo estudio del simulacro en `filtro = "estudio"`**: evita una migración; el historial lo muestra como «simulacro · estudio». El cronómetro sigue igual.
- **Explicación plegable (`<details>`)** tras responder: el resultado y la solución se ven siempre; la explicación se abre con «Ver explicación», para intentar razonar antes de leerla. Abierta por defecto si la respuesta es incorrecta.
- **Enlace a la teoría:** `curso/cobertura.py` extrae del mapa de cobertura de cada README `objetivo → ancla` (lo usan la consola y `comprobar_cobertura.py`).
- **Contenido de repaso derivado de la teoría verificada**: cada pregunta se apoya en una afirmación del módulo y cita la misma fuente oficial; no introduce datos nuevos. Revisión independiente por módulo.

## Risks / Trade-offs

- [Preguntas de definición facilitan memorizar sin entender] → los bancos de examen siguen siendo escenarios; la ruta de estudio pasa de repaso a examen.
- [Modo estudio en el simulacro desvirtúa el examen] → es opcional y el resultado lo indica.
- [Volumen de ≈ 220 preguntas] → generación por módulo con revisión independiente y el validador.

## Open Questions

- Ninguna bloqueante.
