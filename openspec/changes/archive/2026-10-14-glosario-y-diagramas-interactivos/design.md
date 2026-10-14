## Context

El contenido llega a la consola como Markdown renderizado en servidor con `markdown-it-py` (HTML crudo desactivado) y los diagramas se dibujan en el navegador con Mermaid (`securityLevel: strict`, empaquetado en local). La CSP es `script-src 'self'`: sin scripts en línea ni `eval`. `htmx` hace `hx-boost` de la navegación, por lo que el JavaScript debe reiniciarse tras cada carga parcial. Hay ya un 5 diagramas y 2 módulos con contenido, y un único curso, pero la solución debe valer para cualquiera.

## Goals / Non-Goals

**Goals:**
- Que cualquier curso con un `glosario.yaml` tenga conceptos pulsables sin cambiar código.
- Modal accesible y sin dependencias nuevas; que funcione sin red y bajo la CSP actual.
- Diagramas agradables, animados con moderación, legibles en claro y oscuro y respetuosos con la preferencia de movimiento reducido.
- Que sea difícil olvidar el glosario: comprobación automática de servicios sin entrada.

**Non-Goals:**
- Linkificar en preguntas, enunciados o explicaciones de los tests.
- Editor de glosario en la web, traducciones o definiciones generadas por IA.
- Cambiar el motor de diagramas (se mantiene Mermaid).

## Decisions

1. **Fuente: `cursos/<curso>/glosario.yaml`**, lista de entradas con `id` (slug), `termino`, `alias` (opcional), `categoria` (`servicio` | `concepto` | `metrica` | `tecnica`), `definicion` (texto plano, 1–3 frases), `usar_cuando` y `no_usar_cuando` (opcionales, sobre todo para servicios), `referencia` (URL https) y `curso_ref` opcional. Validado con `schemas/glosario.schema.json`. El `glosario.md` alfabético que pide `promt.md` se generará desde este YAML en la Iteración 6 (una sola fuente de verdad). Alternativa descartada: marcar términos a mano en cada Markdown (frágil y repetitivo).

2. **Detección en el servidor, no en el navegador.** Una regla `core` de `markdown-it` recorre los `text` de los tokens `inline` y sustituye cada término por un token `html_inline` con `<button type="button" class="concepto" data-concepto="id">término</button>`. Así el HTML llega ya resuelto, se cachea con la sección y funciona aunque se retrase el JavaScript. Se excluyen: encabezados, enlaces, código en línea y bloques de código/`mermaid`. El texto visible del botón es el original (conserva mayúsculas y plural exacto) y el texto se escapa.

3. **Coincidencia.** Una expresión regular compilada por curso con todos los términos y alias, ordenados de mayor a menor longitud, con límites de palabra Unicode (`(?<!\w)…(?!\w)`). Sin distinguir mayúsculas salvo para términos cortos o en mayúsculas (≤ 5 caracteres o `ML`, `RAG`, `IAM`, `S3`…), que sí las distinguen para evitar falsos positivos. **Solo la primera aparición de cada concepto en cada apartado** (se reinicia al pasar por un encabezado), para evitar ruido visual y mantener cerca la ayuda. El conjunto de ids usados se devuelve junto al HTML.

4. **Datos del modal incrustados en la página** como `<script type="application/json" id="datos-glosario">` con solo los conceptos usados (y los alias, para los nodos de diagrama). Los bloques JSON no se ejecutan, por lo que la CSP lo permite, y se evita una petición por clic. El `<` se escapa como `<`. Alternativa descartada: endpoint por concepto con htmx (más peticiones y depende de red).

5. **Modal con `<dialog>` nativo** (`showModal()`): gestión de foco, `Esc`, capa de fondo y atributos ARIA incluidos. Un único `<dialog id="modal-concepto">` en `base.html` que el JavaScript rellena con `textContent` (nunca `innerHTML`). Cierra con botón, `Esc` o clic fuera, y devuelve el foco al elemento que lo abrió. En móvil ocupa casi todo el ancho. Delegación de eventos en `document` para sobrevivir a `hx-boost`.

6. **Nodos de diagrama pulsables.** Tras renderizar Mermaid, el JavaScript busca en el texto de cada nodo un alias del glosario (límite de palabra, el más largo) y, si coincide, lo marca como botón (`role="button"`, `tabindex="0"`, `Enter`/`Espacio`). Como los diagramas viven en bloques de código, el servidor también extrae los conceptos que aparecen dentro de los bloques `mermaid` para incluirlos en los datos de la página.

7. **Tema de Mermaid propio.** `theme: base` con `themeVariables` leídas de las variables CSS de la aplicación (así siguen el modo claro/oscuro), curva suave (`basis`), mayor `padding`, tipografía del sistema y `useMaxWidth`. El color por tipo se logra con **clases semánticas** (`class A ia`) sin `classDef` en línea; los colores se definen en CSS con variables, de modo que el modo oscuro es automático. Clases: `ia`, `ml`, `dl`, `gen`, `dato`, `proceso`, `servicio`, `accion`, `aviso` y `decision`. Se pueden usar emojis en las etiquetas.

8. **Animación solo con CSS y un observador.** Flechas: `stroke-dasharray` con `stroke-dashoffset` animado (flujo continuo y suave). Nodos: entrada escalonada (`opacity`/`transform`) con un índice por nodo (`--i`) que fija el JavaScript, disparada cuando el diagrama entra en pantalla (`IntersectionObserver`). Interacción: realce al pasar el ratón y foco visible. La animación de entrada solo se activa si el JavaScript añade la clase `anim-lista`, para que sin JavaScript nada quede oculto. Con `prefers-reduced-motion: reduce` se desactiva todo movimiento.

9. **Validación y consistencia.** Se amplía `validar_preguntas.py` (o se añade `validar_glosario.py` invocado por el mismo CI) para: esquema, ids únicos, términos/alias sin colisiones (sin distinguir mayúsculas), URL `https`, y que todo servicio de la primera columna de las tablas de `servicios.md` tenga entrada. Si un curso no tiene `glosario.yaml`, la función se desactiva y el contenido se muestra como hasta ahora.

10. **Página de glosario.** `/c/<curso>/glosario`: lista alfabética con filtro instantáneo en el cliente; cada entrada es un botón que abre el modal. Enlazada desde la navegación del curso.

11. **Pruebas.** Unitarias para la detección (exclusiones, primera aparición por apartado, límites de palabra, escape, alias, mayúsculas) y el validador. Una prueba de navegador con Chrome sin interfaz (Playwright) comprueba clic, `Esc`, foco, nodos pulsables, modo oscuro y movimiento reducido, y genera capturas para revisión visual.

## Risks / Trade-offs

- [Falsos positivos de términos genéricos («modelo», «datos»)] → El glosario solo incluye términos con valor didáctico; los cortos o en mayúsculas distinguen mayúsculas; solo la primera aparición por apartado.
- [Demasiados botones empeoran la lectura] → Estilo sutil (subrayado punteado), primera aparición por apartado.
- [Un término dentro de otro más largo] → Se ordena por longitud descendente y se consume el texto emparejado.
- [Mermaid varía el HTML interno entre versiones] → Las clases se aplican con la API estándar (`class`); el JavaScript trabaja sobre `g.node` y `path.flowchart-link`, y las pruebas de navegador fijan el comportamiento con la versión empaquetada (11.4.1).
- [Animaciones molestas o lentas] → Sutiles, solo CSS, paradas con movimiento reducido, y sin efecto si no hay JavaScript.
- [El texto del glosario podría quedar desactualizado] → Cada entrada enlaza a la fuente oficial y el validador exige URL; las reglas de `AGENTS.md` piden revisarlas con el contenido.

## Migration Plan

Sin migración de datos. Se despliega reconstruyendo la imagen; los cursos sin `glosario.yaml` no cambian. Reversión: volver a la imagen anterior (el contenido Markdown no cambia salvo los diagramas, que siguen siendo Mermaid válido).

## Open Questions

- ¿Quieres que el modal incluya, cuando exista, enlaces «Dónde se estudia» a las secciones del curso? Se deja fuera de esta primera versión.
- ¿Prefieres que se enlace cada aparición del término en vez de solo la primera por apartado? Se empieza por la primera para no saturar.
