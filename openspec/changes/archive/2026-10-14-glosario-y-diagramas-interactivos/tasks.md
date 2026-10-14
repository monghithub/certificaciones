## 1. Formato y validación del glosario

- [x] 1.1 Crear `schemas/glosario.schema.json` (id, termino, alias, categoria, definicion, usar_cuando, no_usar_cuando, referencia)
- [x] 1.2 Crear el módulo común de lectura del glosario (`curso/glosario.py`: carga, validación, expresión regular de términos, búsqueda en texto)
- [x] 1.3 Ampliar la validación (unicidad de ids, términos y alias, URL https, servicios de `servicios.md` con entrada) y conectarla al CI y a `scripts/validar_preguntas.py`
- [x] 1.4 Tests del módulo y del validador

## 2. Contenido: glosario inicial del curso AIF-C01

- [x] 2.1 Redactar `cursos/aif-c01/glosario.yaml` para los módulos 00 y 01 (servicios, conceptos, métricas y técnicas) a partir de la documentación ya consultada, con su referencia oficial
- [x] 2.2 Validar que cada servicio de los `servicios.md` existentes tiene entrada

## 3. Renderizado en el servidor

- [x] 3.1 Cargar el glosario en `Contenido` (con avisos si es inválido) y compilar las expresiones de coincidencia
- [x] 3.2 Regla de `markdown-it` que convierte términos en botones (primera aparición por apartado, exclusiones, escape, término más largo, siglas sensibles a mayúsculas)
- [x] 3.3 Extraer los conceptos que aparecen dentro de los bloques `mermaid` y devolver el conjunto de ids usados por la sección
- [x] 3.4 Incrustar el JSON de datos en `seccion.html` (escapado) y exponer los alias
- [x] 3.5 Ruta y plantilla de la página de glosario con buscador, y enlace en la navegación del curso
- [x] 3.6 Tests de renderizado, seguridad (escape) y acceso

## 4. Modal e interacción

- [x] 4.1 Añadir el `<dialog>` a `base.html` y los estilos (claro, oscuro, móvil)
- [x] 4.2 JavaScript: delegación de eventos, rellenado con `textContent`, cierre con botón, `Esc` y clic fuera, retorno de foco y compatibilidad con `hx-boost`
- [x] 4.3 Nodos de diagrama pulsables tras renderizar Mermaid (coincidencia con alias, accesibilidad por teclado)

## 5. Diagramas amables y animados

- [x] 5.1 Tema de Mermaid con variables CSS y configuración (curva, espaciado, tipografía, `useMaxWidth`)
- [x] 5.2 CSS de las clases semánticas en claro y oscuro
- [x] 5.3 Animación de entrada escalonada (observador de visibilidad), flujo de flechas y efecto al pasar el ratón
- [x] 5.4 Movimiento reducido y comportamiento sin JavaScript
- [x] 5.5 Reescribir los 5 diagramas de los módulos 00 y 01 con clases semánticas y etiquetas claras, y validar su sintaxis

## 6. Verificación en navegador

- [x] 6.1 Prueba con Chrome sin interfaz: clic, `Enter`, `Esc`, foco, nodos pulsables, tras `hx-boost`, modo oscuro y movimiento reducido
- [x] 6.2 Capturas de pantalla (claro, oscuro y móvil) revisadas visualmente
- [x] 6.3 Suite completa (`pytest`, validadores, `markdownlint`) y reconstrucción de la instancia local

## 7. Documentación

- [x] 7.1 Reglas para autores en `AGENTS.md` (glosario y clases de diagramas) y `docs/consola.md`
- [x] 7.2 Actualizar `CHANGELOG.md`
