## Why

La consola se despliega en titan solo para la red local, y el usuario no quiere iniciar sesión: «la 15 significa quitar el login de la consola. Dejarla libre para poder entrar ya que solo va a funcionar en el entorno local» (issue #15).

## What Changes

- **Modo de acceso libre**, desactivado por defecto: con la variable `ACCESO_LIBRE_USUARIO=<usuario>`, quien entra sin sesión queda identificado automáticamente como ese usuario (activo y existente). Sin la variable, todo sigue como ahora (login obligatorio).
- En ese modo, `/login` lleva al inicio, se ocultan «Salir» y el formulario de acceso, y la cabecera muestra «Acceso libre (red local)».
- Se mantienen el resto de protecciones: CSRF, cabeceras de seguridad, contenedor sin privilegios y la restricción `lan-only` de Traefik.
- Despliegue en titan: `ACCESO_LIBRE_USUARIO` en el `.env` de `~/Sistema/aplicaciones/certificaciones`.
- Documentación (`docs/consola.md`, `.env.example`, CHANGELOG, journal) y pruebas. Cierra la issue #15.

## Capabilities

### New Capabilities
- `acceso-libre`: entrada sin login con un usuario fijo, para despliegues en red local.

### Modified Capabilities
- Ninguna: `auth-roles` no cambia cuando la variable no está definida.

## Impact

- Código: `app/config.py`, `app/deps.py`, `app/routes/auth.py`, `app/templates/base.html`.
- Sin migración.
- Riesgo aceptado por el usuario: cualquiera con acceso a la red local entra con los permisos de ese usuario.
