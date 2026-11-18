## Context

`usuario_sin_forzar` lee `uid` de la sesión firmada y, si no hay, redirige a `/login`. El resto de dependencias (`requiere_usuario`, `requiere_admin`, `requiere_curso`) parten de ahí.

## Goals / Non-Goals

**Goals:** entrar sin login en el despliegue de casa, sin cambiar el comportamiento por defecto.

**Non-Goals:** usuarios anónimos sin cuenta; quitar CSRF u otras protecciones; abrir la consola fuera de la LAN.

## Decisions

- **Usuario fijo y existente** (`ACCESO_LIBRE_USUARIO`), no un usuario anónimo: el progreso, las estadísticas y las matrículas siguen funcionando sin tocar el modelo de datos. Si el usuario no existe o está desactivado, se vuelve al login normal y se registra un aviso.
- **Se crea la sesión al vuelo** en `usuario_sin_forzar` (misma cookie firmada y mismo CSRF), así el resto del código no cambia.
- **Desactivado por defecto** y solo por variable de entorno: un despliegue que no la define sigue exigiendo login.
- **Logout:** en este modo «Salir» no tiene sentido (se volvería a entrar solo) y se oculta; `POST /logout` redirige al inicio.

## Risks / Trade-offs

- [Cualquiera en la LAN entra con ese usuario] → solo LAN por Traefik (`lan-only`) y puerto del contenedor en `127.0.0.1`; decisión del usuario.
- [Si un día se publica en internet con la variable puesta] → `docs/consola.md` y `.env.example` lo advierten; el router de Traefik solo existe para `*.titan`.
