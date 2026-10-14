## Context

La consola y las herramientas ya son multicurso (`soporte-multicurso`), pero el primer curso dejó supuestos de AWS en el esquema, en las reglas y en los nombres. El repositorio se ha renombrado a `certificaciones`.

## Goals / Non-Goals

**Goals:**
- Poder añadir un curso de cualquier proveedor sin tocar el código ni las reglas comunes.
- Mantener la exigencia de fuentes oficiales, ahora declaradas por curso.
- Separar las reglas comunes de las propias de cada curso.

**Non-Goals:**
- Crear un segundo curso.
- Cambiar el modelo de datos de la consola.

## Decisions

- **`fuentes_oficiales` como lista de hosts.** Se acepta el host exacto o un subdominio suyo (`docs.aws.amazon.com` encaja con `aws.amazon.com`). Es simple de declarar y de comprobar. Alternativa descartada: expresiones regulares por curso, más frágiles.
- **Opcional y compatible.** Sin `fuentes_oficiales`, solo se exige https. Así los cursos y los tests existentes siguen siendo válidos.
- **`AGENTS.md` por curso.** Es la convención de ficheros de reglas anidados: el más cercano complementa al raíz. La prevalencia queda escrita en el raíz.
- **Etiquetas por curso** (`<slug>-vX.Y.Z`) y ramas `<slug>/<etapa>`: cada curso avanza a su ritmo dentro del mismo repositorio.

## Risks / Trade-offs

- [Nombre nuevo de la imagen Docker] → documentado en el impacto y en el CHANGELOG; los volúmenes no cambian.
- [Reglas de AWS ya no visibles en el raíz] → el `AGENTS.md` raíz enlaza las reglas por curso y su orden de prevalencia.
