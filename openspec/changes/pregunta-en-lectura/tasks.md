## 1. Servidor

- [x] 1.1 `Contenido`: índice (módulo, ancla) → objetivos con todas las anclas del mapa de cobertura
- [x] 1.2 `app/routes/lectura.py`: `GET pregunta` (anclas, excluir, repaso antes que examen, módulo como respaldo, sin simulacro) y `POST corregir` (validación, corrección y explicación, sin registro)
- [x] 1.3 Registrar el router; extraer la vista de la pregunta y la lectura de la respuesta para compartirlas con `quiz.py`

## 2. Cliente

- [x] 2.1 `seccion.html` y `base.html`: botón «Ponme a prueba» y `<dialog id="modal-pregunta">`
- [x] 2.2 `app.js`: apartado visible, petición, pintado de los cuatro tipos con `textContent`, corrección, «Otra pregunta», cierre y foco
- [x] 2.3 `app.css`: botón fijo y estilos del modal, en claro y oscuro y en móvil

## 3. Pruebas y documentación

- [x] 3.1 pytest de las rutas (elección por ancla, respaldo del módulo, excluir, simulacro, CSRF, sin registro)
- [x] 3.2 Prueba en navegador
- [x] 3.3 `docs/consola.md`, CHANGELOG y journal
- [x] 3.4 Commit, push, PR y archivo del cambio (cuando el usuario lo pida)
