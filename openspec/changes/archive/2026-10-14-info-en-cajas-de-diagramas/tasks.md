## 1. Anclas compartidas

- [x] 1.1 Crear `curso/anclas.py` (ancla estilo GitHub, anclas de un Markdown) y usarlo en `comprobar_cobertura.py`
- [x] 1.2 Poner `id` a los encabezados renderizados con la misma función y tests

## 2. Glosario: enlaces y datos uniformes

- [x] 2.1 Añadir `enlaces` al esquema y a `Entrada`
- [x] 2.2 Servir cada concepto como `{titulo, categoria, texto, usar_cuando, no_usar_cuando, enlaces}` (con `referencia` como primer enlace) y adaptar tests

## 3. Bloque `nodos` y datos de la página

- [x] 3.1 Interpretar el bloque `nodos` tras cada diagrama (sin mostrarlo) y resolver la información de cada caja (concepto, sustituciones, enlaces, `seccion`)
- [x] 3.2 Incrustar los datos como `diagramas[n][id]` y marcar cada figura con su índice
- [x] 3.3 Tests del renderizado, de la resolución y de la seguridad de los enlaces

## 4. Interfaz

- [x] 4.1 Modal con lista de enlaces (externos en pestaña nueva, internos en la misma)
- [x] 4.2 JavaScript: cajas pulsables a partir de `nodos` (nodos y subgrupos), sin coincidencia automática, con accesibilidad y manejo de la caja más interna
- [x] 4.3 CSS de las cajas pulsables y de la lista de enlaces

## 5. Validación del estilo

- [x] 5.1 Crear `curso/diagramas.py` (análisis de los diagramas y de `nodos`, reglas de estilo y de información)
- [x] 5.2 Integrarlo en `scripts/validar_preguntas.py` y tests de cada regla

## 6. Contenido existente

- [x] 6.1 Añadir el bloque `nodos` a los 5 diagramas de los módulos 00 y 01, con información y enlaces verificados
- [x] 6.2 Comprobar que todas las URL nuevas responden

## 7. Verificación y documentación

- [x] 7.1 Prueba de navegador: cualquier caja abre su modal con enlaces, teclado, subgrupos, anclas y capturas
- [x] 7.2 Suite completa, validadores y `markdownlint`; reconstruir la instancia
- [x] 7.3 Documentar las reglas en `AGENTS.md` y `docs/consola.md` y actualizar `CHANGELOG.md`
