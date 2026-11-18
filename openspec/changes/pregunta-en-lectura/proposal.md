## Why

El usuario quiere comprobar lo que lee sin salir de la teoría: «me gustaría que en las pantallas apareciera un modal con alguna pregunta concreta tipo test de la página que estoy visitando. Pudiera cerrarla o, si no la cierro, me vaya haciendo cuestiones y vaya yo respondiendo hasta que me aburra y la cierre. Sobre todo de la página que esté en ese momento en la ventana del navegador». Hoy las preguntas solo están en «Tests», separadas de la lectura.

## What Changes

- **Botón «Ponme a prueba»** en las páginas de lectura de los módulos que tienen preguntas (no en el simulacro). Abre un modal con una pregunta tipo test.
- **Pregunta del apartado visible:** la consola toma el encabezado más cercano por encima del centro de la ventana y sus encabezados padres, busca los objetivos que el mapa de cobertura asocia a esas anclas y elige una de sus preguntas. Si el apartado no tiene preguntas (por ejemplo, en `servicios.md` o `trampas.md`), la elige del módulo. El modal indica de dónde sale.
- **Orden de los bancos:** primero preguntas de repaso; cuando se agotan las del apartado, las de examen del mismo apartado. Nunca del simulacro.
- **Flujo en el modal:** se responde (los cuatro tipos), se corrige al momento con la solución, la explicación, los motivos de las opciones incorrectas, la referencia oficial y el enlace a la teoría, y «Otra pregunta» pide la siguiente del apartado visible en ese momento, sin repetir las ya vistas. Se cierra con ✕, `Esc` o clic fuera.
- **Sin temporizador y sin registro:** el modal solo se abre con el botón y no guarda nada (no cuenta en estadísticas ni en «Repetir falladas»). Son decisiones del usuario.
- Documentación (`docs/consola.md`, CHANGELOG, journal) y pruebas.

## Capabilities

### New Capabilities
- `pregunta-en-lectura`: preguntas tipo test del apartado visible durante la lectura, en un modal y sin registro.

### Modified Capabilities
- Ninguna. `course-navigation` y `quiz-engine` no cambian de comportamiento.

## Impact

- Código: `app/content.py` (anclas → objetivos), `app/routes/lectura.py` (nuevo: elegir y corregir), `app/routes/quiz.py` (se reutiliza la lectura del formulario), `app/main.py` (router), `app/templates/seccion.html` y `base.html` (botón y modal), `app/static/app.js` y `app.css`.
- Sin migración ni cambios de contenido.
- Git: rama `feat/pregunta-en-lectura` con PR a `main`.
