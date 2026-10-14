# Pruebas de navegador y de diagramas

Pruebas **manuales** (no forman parte del CI) que necesitan Node.js, Google Chrome y la consola en marcha.

```bash
cd tests/e2e
npm install
npm run mermaid -- ../../cursos/aif-c01/modulos/*/README.md       # sintaxis de los diagramas
CONSOLA_USUARIO=estudiante CONSOLA_CLAVE=... npm run consola      # clic, teclado, oscuro, movimiento reducido y móvil
```

La segunda prueba usa una cuenta de estudiante matriculada en `aif-c01` y genera capturas en `tests/e2e/capturas/` (ignorada por Git). Variables opcionales: `CONSOLA_URL` (por defecto `http://127.0.0.1:8000`), `CHROME` (ruta del ejecutable) y `CAPTURAS`.

Qué comprueba: conceptos pulsables, apertura y cierre del modal (clic, `Enter`, `Esc`, botón y fondo), retorno del foco, nodos de diagrama pulsables, navegación con `hx-boost`, página de glosario con filtro, animación de las flechas, modo oscuro, movimiento reducido (sin animaciones), ancho móvil y ausencia de errores de consola.
