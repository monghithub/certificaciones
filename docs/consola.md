# Consola web del curso

Aplicación web para seguir cursos (índice, lectura de módulos), hacer cuestionarios y simulacros, y ver el progreso. Soporta varios cursos: los usuarios los da de alta un administrador, que además los matricula en los cursos que les correspondan. No hay registro público.

- **Stack:** FastAPI, SQLite (WAL), SQLAlchemy y Alembic, plantillas Jinja2 con HTMX. Sin CDN: HTMX y Mermaid van en `app/static/`.
- **Contenido:** cada curso se lee de `cursos/<curso>/` (su `curso.yaml`, `fuentes/` y `modulos/`), que es la única fuente de verdad. La aplicación no edita los cursos. Las preguntas que no cumplen el esquema, y los cursos con manifiesto inválido, se omiten y se avisan en el panel de administración.
- **Roles (globales):** `admin` (gestiona usuarios y matrículas, ve las estadísticas de todos y accede a todos los cursos) y `estudiante` (solo sus cursos y sus datos).
- **Matrícula:** el admin matricula a cada estudiante en uno o varios cursos, al darlo de alta o desde su ficha. Quien no está matriculado recibe un 404 al pedir un curso, de modo que no se revela qué cursos existen.
- **URL:** cada curso cuelga de `/c/<curso>/` (índice, `modulo/…`, `tests`, `estadisticas`). `/` muestra «Mis cursos», o entra directo si solo hay uno accesible.

## Puesta en marcha con Docker

```bash
cp .env.example .env
# Edita .env: SECRET_KEY obligatoria (mínimo 32 caracteres)
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
docker compose up -d --build
```

La consola queda en <http://127.0.0.1:8000> (solo en la máquina local). Para exponerla, ponla detrás de un proxy con TLS (Caddy, nginx o Traefik), pon `COOKIE_SECURE=true` y ajusta `FORWARDED_ALLOW_IPS` a la IP del proxy para que el límite de intentos use la IP real del cliente.

### Primer administrador

Opción A, variables en `.env` (solo se usan si no hay ningún usuario):

```text
ADMIN_USERNAME=admin
ADMIN_PASSWORD=una-contraseña-temporal-larga
```

Opción B, comando interactivo (pide la contraseña por terminal):

```bash
docker compose run --rm consola python -m app.crear_admin admin --nombre "Administrador"
```

En ambos casos la contraseña es temporal: se obliga a cambiarla en el primer acceso. No hay credenciales por defecto. Quita `ADMIN_PASSWORD` de `.env` después del primer arranque.

## Variables de entorno

| Variable | Obligatoria | Descripción |
|---|---|---|
| `SECRET_KEY` | Sí | Firma de las cookies de sesión (≥ 32 caracteres). Sin ella la aplicación no arranca. |
| `DATABASE_URL` | No | Por defecto `sqlite:////data/app.db` en el contenedor. |
| `COURSES_DIR` | No | Carpeta con los cursos (`<curso>/curso.yaml`). En el contenedor, `/cursos`. |
| `PASSWORD_MIN_LENGTH` | No | Longitud mínima de contraseña (10 por defecto, mínimo 1). Redúcela solo si la consola es de uso local. |
| `COOKIE_SECURE` | No | `true` cuando se sirve por HTTPS. |
| `ADMIN_USERNAME`, `ADMIN_PASSWORD` | No | Crea el primer administrador si no hay usuarios. |
| `PORT` | No | Puerto local publicado por Docker Compose (8000). |
| `FORWARDED_ALLOW_IPS` | No | IPs de proxies de confianza para `X-Forwarded-For`. |

## Qué se guarda

Usuarios (nombre de usuario, nombre, rol, hash argon2 de la contraseña, fecha de alta y último acceso), sus matrículas por curso, secciones leídas y completadas por curso, y cada intento de test con sus respuestas. No se guardan contraseñas en claro ni se registran en logs. El administrador puede ver el progreso y las estadísticas de todos los usuarios.

## Seguridad

Contraseñas con argon2; cookie de sesión `HttpOnly` y `SameSite=Lax` (`Secure` con `COOKIE_SECURE=true`); token CSRF en todas las peticiones que modifican datos; bloqueo de 5 minutos tras 5 fallos seguidos por usuario o por IP (en memoria, por proceso); mensaje de error genérico en el login; cabeceras CSP, `X-Frame-Options` y `X-Content-Type-Options`; Markdown renderizado sin HTML crudo; contenedor sin root, sistema de ficheros de solo lectura y sin capacidades. Una cuenta desactivada pierde la sesión en su siguiente petición. Contraseñas: mínimo 10 caracteres por defecto (configurable con `PASSWORD_MIN_LENGTH`).

El bloqueo por usuario permite que un tercero bloquee temporalmente una cuenta a base de intentos fallidos; se acepta por simplicidad en un grupo de estudio reducido.

## Glosario y diagramas

- **Conceptos pulsables.** Si el curso tiene `glosario.yaml`, la primera aparición de cada término del glosario en cada apartado se muestra resaltada solo al pasar el ratón (en pantallas táctiles lleva un subrayado punteado tenue) y, al pulsarla, abre un modal con su definición, cuándo usarlo y cuándo no (en servicios) y el enlace a la documentación oficial. Funciona con teclado (`Enter`, `Esc`), en móvil y en modo oscuro. En `/c/<curso>/glosario` está el listado completo con buscador.
- **Diagramas.** Los diagramas Mermaid usan un tema propio (claro y oscuro), colores por tipo, aparición escalonada y flechas animadas. Con la preferencia de sistema «reducir movimiento» no hay animaciones. **Cualquier caja** de un diagrama (nodo o subgrupo) abre un modal con su información y enlaces: externos (pestaña nueva) y «Ver en el curso» (apartado interno). Esa información la define el autor en el bloque `nodos` que sigue a cada diagrama, y el validador exige que no falte ninguna caja. Los títulos de apartado tienen ancla, así que los enlaces `#ancla` (mapa de cobertura, «Ver en el curso») llevan al lugar exacto.
- Las reglas para autores (entradas del glosario y clases de colores) están en [AGENTS.md](../AGENTS.md). Las pruebas manuales en navegador, en [tests/e2e](../tests/e2e/README.md).

## Tema de color

La web usa por defecto un tema claro de tonos suaves. El botón de la cabecera cambia entre **Claro**, **Oscuro** y **Sistema** (sigue al sistema operativo) y recuerda la elección en el navegador. Los ficheros estáticos se sirven siempre con revalidación y versión en la URL, así que tras actualizar la consola no hay que vaciar la caché del navegador.

## Añadir un curso y matricular usuarios

1. Crea `cursos/<slug>/` con su `curso.yaml` (el `slug` coincide con la carpeta; ejemplo en `cursos/aif-c01/curso.yaml` y esquema en `schemas/curso.schema.json`) y sus `modulos/`. Los cursos pueden ser de cualquier proveedor de certificaciones.
2. Comprueba el contenido: `python scripts/validar_preguntas.py --curso <slug>`.
3. En la consola, en **Cursos** o **Usuarios**, pulsa «Recargar contenido». Si hay avisos (manifiesto inválido, preguntas descartadas), aparecen ahí.
4. En la ficha de cada usuario, sección **Cursos**, matricúlalo. Retirar una matrícula no borra su historial: si lo vuelves a matricular, lo recupera.

Con Docker, `./cursos` se monta en solo lectura en `/cursos`, así que basta con añadir la carpeta y recargar, sin reconstruir la imagen.

## Copia de seguridad y restauración

Haz siempre una copia **antes de actualizar** la imagen: el arranque aplica las migraciones de base de datos (la `0002` añadió los cursos y las matrículas; los estudiantes existentes quedan matriculados en `aif-c01`).

Los datos están en el volumen `datos` (`/data/app.db`). Copia consistente con la API de copia de SQLite, que es segura con la aplicación en marcha:

```bash
docker compose exec -T consola python -c "import sqlite3; o=sqlite3.connect('/data/app.db'); d=sqlite3.connect('/data/copia.db'); o.backup(d); d.close()"
docker compose cp consola:/data/copia.db ./copia-$(date +%F).db
```

Restauración (con la aplicación parada):

```bash
docker compose stop consola
docker compose cp ./copia-AAAA-MM-DD.db consola:/data/restaurar.db
docker compose run --rm --no-deps consola python -c "import sqlite3; s=sqlite3.connect('file:/data/restaurar.db?mode=ro&immutable=1', uri=True); d=sqlite3.connect('/data/app.db'); s.backup(d)"
docker compose up -d
```

No copies el fichero directamente sobre `app.db`: `docker compose cp` lo deja con propietario root y la aplicación (usuario `app`) no podría escribir. Los ficheros temporales `copia.db` y `restaurar.db` quedan en el volumen y puedes borrarlos cuando quieras.

## Desarrollo local

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-app.txt
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(48))")
export DATABASE_URL=sqlite:///data/app.db
python -m app.crear_admin admin
uvicorn app.main:create_app --factory --reload
python -m pytest
```

## Comportamientos a tener en cuenta

- **Cambios de contenido:** los intentos guardan solo el `id` de pregunta. Si se retira una pregunta, el historial la muestra como «pregunta retirada». Usa «Recargar contenido» tras actualizar `cursos/`, sin reiniciar. Si desaparece la carpeta de un curso, las matrículas y el historial se conservan y la ficha del usuario lo marca como «curso no disponible».
- **Simulacro:** cada curso lo define en su `curso.yaml` (`simulacro`, `examen.preguntas`, `examen.minutos`); si no lo declara, no se ofrece. En AIF-C01 exige 65 preguntas en `modulos/06-simulacro/preguntas.yaml` y limita el tiempo a 90 minutos medidos en el servidor. Una respuesta enviada fuera de plazo no se registra. El porcentaje que se muestra es orientativo: el examen real usa una escala de 100–1.000 (aprobado con 700) que no equivale a un porcentaje.
- **Tests como ruta de estudio:** la página de tests ofrece, por este orden, el repaso de conocimientos (`repaso.yaml` de cada módulo), las preguntas de examen (por módulo, dominio o mixto), «Repetir falladas» (preguntas de repaso y de examen cuya última respuesta fue incorrecta; las del simulacro no entran) y el simulacro.
- **Explicación tras cada respuesta:** en todos los tests con corrección inmediata, al responder se ve si es correcta, la solución y un desplegable «Ver explicación» (abierto si se ha fallado) con la explicación, por qué fallan las demás opciones, la referencia oficial y un enlace a la sección de teoría del objetivo (sale del mapa de cobertura del README).
- **Modo estudio del simulacro:** casilla al empezarlo; con ella, cada respuesta se corrige y se explica al momento. El cronómetro es el mismo y el historial lo muestra como «simulacro · estudio».
- **Sin contenido:** con los módulos vacíos la consola funciona y muestra «Sin contenido todavía».
- **Cambio de URL:** antes de la versión multicurso las páginas colgaban de `/modulo/…` o `/tests`; ahora llevan el prefijo `/c/<curso>/`. No hay redirecciones desde las URL antiguas.
