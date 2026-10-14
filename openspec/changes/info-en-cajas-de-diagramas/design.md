## Context

Hoy `app/content.py` convierte los bloques `mermaid` en `<figure class="diagrama">` y el JavaScript marca como pulsable un nodo cuyo texto contiene un alias del glosario (el más largo). Es implícito, ambiguo y no cubre cajas sin concepto. El modal solo muestra un enlace «Documentación oficial». No hay anclas en los encabezados renderizados, por lo que los enlaces `#ancla` (mapa de cobertura) no funcionan en la consola.

## Goals / Non-Goals

**Goals:**
- Información y enlaces en cualquier caja (nodos y subgrupos) de cualquier diagrama.
- Comportamiento explícito y predecible: lo decide el autor.
- Estilo de diagramas único y comprobado automáticamente.
- Enlaces internos funcionales en la consola.

**Non-Goals:**
- Soportar otros tipos de diagrama distintos de `flowchart`.
- Edición en la web ni traducciones.

## Decisions

1. **Formato: bloque `nodos` justo después del diagrama.** Un bloque de código con la etiqueta `nodos` y un mapa YAML `id_del_nodo → información` inmediatamente tras el bloque `mermaid` (solo líneas en blanco entre ambos). La consola lo consume y no lo muestra; en GitHub o en un editor se ve como YAML. Alternativas descartadas: comentarios `%%` dentro de Mermaid (no hay forma limpia de datos estructurados) y directivas `click` de Mermaid (desactivadas con `securityLevel: strict`).

   ```nodos
   A:
     concepto: inteligencia-artificial       # reutiliza el glosario
     enlaces: [{texto: "Guía de decisión", url: "https://docs.aws.amazon.com/..."}]
   B:
     titulo: Plantear el problema de ML
     texto: Se traduce el problema de negocio a ML…
     seccion: 01-fundamentos-ia-ml/teoria#etapas-de-un-pipeline-de-ia-y-ml
   ```

2. **Resolución de la información de una caja (servidor).** Si hay `concepto`, se parte de la entrada del glosario (título, categoría, definición, cuándo usarlo y no, enlaces); los campos de la caja (`titulo`, `texto`, `usar_cuando`, `no_usar_cuando`) sustituyen a los del glosario y sus `enlaces` se añaden a los del concepto. `seccion` (`modulo/seccion#ancla`) se convierte en un enlace interno «Ver en el curso» `/c/<curso>/modulo/<modulo>/<seccion>#<ancla>`. Los datos se incrustan en el JSON de la página bajo `diagramas[n][id]`.

3. **Modelo de datos uniforme para el modal.** Tanto conceptos como cajas se sirven como `{titulo, categoria?, texto, usar_cuando?, no_usar_cuando?, enlaces:[{texto,url}]}`. En los conceptos, `referencia` pasa a ser el primer enlace («Documentación oficial») y se añaden los `enlaces` extra del glosario. El modal pinta siempre la misma estructura (lista de enlaces con `rel="noopener noreferrer"` para los externos).

4. **Identificación de cajas en el DOM.** El JavaScript lee el `id` de cada `g.node` (`flowchart-<id>-<n>`) y de cada `g.cluster` (el id del subgrupo) y busca `diagramas[n][id]`, donde `n` es el índice del diagrama en la página (`data-diagrama`). Sin información no hay caja pulsable (el validador impide que ocurra). Se elimina la coincidencia automática por alias.

5. **Validador (`curso/diagramas.py`).** Analiza con expresiones regulares los bloques `mermaid` de todo `cursos/*/**/*.md`: tipo `flowchart`; ids y etiquetas de nodos (`ID["…"]`, `([…])`, `[(…)]`, `{…}`) y de `subgraph ID["…"]`; sentencias `class A,B tipo`; ausencia de `classDef`; etiqueta que empieza por emoji; clases del conjunto permitido (`ia, ml, dl, gen, dato, proceso, servicio, accion, aviso, decision`); cada nodo y subgrupo con clase (los subgrupos no la necesitan) e información en `nodos`; claves de `nodos` existentes; `concepto` presente en el glosario; URL `https`; `seccion` apuntando a un módulo, sección y ancla existentes. Los errores se informan como `fichero:diagrama N: mensaje`. Se integra en `validar_preguntas.py` (y por tanto en el CI).

6. **Anclas compartidas.** Se mueve la función de anclas de `comprobar_cobertura.py` a `curso/anclas.py` (estilo GitHub, con sufijo `-1`, `-2` ante duplicados) y se usa para: poner `id` a los encabezados renderizados (regla de `markdown-it`), validar `seccion` y comprobar el mapa de cobertura. Así los enlaces `#ancla` del Markdown funcionan en la consola y en GitHub por igual.

7. **Accesibilidad.** Cada caja pulsable es un botón (`role="button"`, `tabindex="0"`, `aria-label="Ver información de …"`), activable con `Enter` y espacio, con foco visible; el modal reutiliza la gestión de foco existente. Los subgrupos (que contienen otras cajas) se activan con clic en su título o fondo; pulsar una caja interior abre la de la caja interior.

8. **Estilo.** No se cambia: se fija como regla. El validador impide desviaciones y `AGENTS.md` documenta cómo escribir diagramas y `nodos`.

## Risks / Trade-offs

- [Más trabajo por diagrama] → El bloque `nodos` con `concepto` es una línea por caja; el validador da mensajes claros de lo que falta.
- [Análisis de Mermaid con expresiones regulares es limitado] → Se restringe el estilo permitido (flowchart, etiquetas entre comillas, una declaración por nodo) y se prueban casos límite; un diagrama fuera de ese subconjunto produce un error explícito en vez de pasar sin comprobar.
- [Los ids de nodo de Mermaid cambian entre versiones] → El patrón `flowchart-<id>-<n>` se cubre con una prueba de navegador sobre la versión empaquetada (11.4.1).
- [Clic en subgrupo frente a clic en nodo interior] → El manejador detiene la propagación para que prevalezca la caja más interna.
- [Enlaces rotos] → La comprobación de enlaces del CI (`lychee`) ya cubre Markdown; para el YAML de `nodos` y el glosario se verifica la URL en la entrega con `curl` (como en las referencias de preguntas).

## Migration Plan

Sin migración de datos. Se añaden los `nodos` a los diagramas existentes en el mismo cambio; mientras tanto el validador fallaría, por lo que se hace en orden: código y validador, contenido, y reconstrucción de la imagen.

## Open Questions

- ¿Quieres que además de enlaces externos cada caja muestre un botón «Ver en el curso» cuando existe `seccion`? Se incluye como enlace de la lista.
