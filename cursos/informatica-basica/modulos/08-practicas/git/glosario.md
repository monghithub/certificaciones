# Glosario: Git en profundidad

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 15 términos.

## A

- **Árbol** (tree, árboles). *Concepto.* Objeto de Git que representa un directorio. Lista nombres, permisos y el hash del blob o del árbol de cada entrada.
  - Referencia: <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects>
- **Avance rápido** (fast-forward). *Concepto.* Fusión en la que la rama destino no tiene commits propios desde que se separaron, así que basta con mover su referencia hacia delante. No crea commit de fusión.
  - Referencia: <https://git-scm.com/docs/git-merge>

## B

- **Bisect** (git bisect, búsqueda binaria). *Herramienta.* Búsqueda binaria en la historia para encontrar el commit que introdujo un fallo. Con git bisect run, una prueba automática decide en cada paso.
  - Referencia: <https://git-scm.com/docs/git-bisect>
- **Blob** (blobs). *Concepto.* Objeto de Git que guarda el contenido de un fichero, sin su nombre. Su identificador es el hash de ese contenido, así que dos ficheros iguales comparten blob.
  - Referencia: <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects>

## C

- **Commit** (commits). *Concepto.* Objeto de Git con un árbol (la instantánea completa del proyecto), uno o varios padres, el autor, el confirmador, las fechas y el mensaje. Cambiar cualquiera de esos datos cambia su hash.
  - Referencia: <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects>
- **Commit de fusión** (fusión de tres vías, merge commit). *Concepto.* Commit con dos o más padres que une historias que han divergido. Git lo calcula a partir del ancestro común y las dos puntas.
  - Referencia: <https://git-scm.com/docs/git-merge>
- **Conventional Commits**. *Técnica.* Convención para los mensajes de commit, con un tipo y un ámbito opcional delante (feat(api), fix, docs…), que permite generar cambios de versión y notas de publicación de forma automática.
  - Referencia: <https://www.conventionalcommits.org/en/v1.0.0/>

## D

- **Desarrollo basado en el tronco** (trunk-based development, trunk-based). *Técnica.* Flujo en el que todos integran cambios pequeños en la rama principal con frecuencia, al menos a diario, con ramas de vida corta o sin ellas.
  - Referencia: <https://trunkbaseddevelopment.com/>

## H

- **HEAD** (HEAD separado, detached HEAD). *Concepto.* Referencia a lo que tienes desplegado. Normalmente apunta a una rama; si apunta directamente a un commit, se dice que HEAD está separado y los commits nuevos no pertenecen a ninguna rama.
  - Referencia: <https://git-scm.com/docs/gitglossary>

## I

- **Índice** (área de preparación, staging area). *Concepto.* La instantánea que se está preparando para el próximo commit. git add copia ahí el contenido de un fichero, y ya lo guarda como blob.
  - Referencia: <https://git-scm.com/docs/gitglossary>

## P

- **Push forzado con concesión** (force-with-lease, force-if-includes). *Técnica.* Push forzado que solo sustituye la rama remota si sigue donde la viste por última vez (--force-with-lease). Con --force-if-includes, además exige que tu rama incluya lo que trajiste con fetch.
  - Usar cuando: Tienes que publicar una rama reescrita con rebase.
  - Referencia: <https://git-scm.com/docs/git-push>

## R

- **Rebase** (rebasar). *Técnica.* Volver a aplicar una serie de commits sobre otra base. Crea commits nuevos, con otros hashes, y deja una historia lineal.
  - Usar cuando: Pones al día una rama tuya que nadie más usa antes de integrarla.
  - No usar cuando: Los commits ya están publicados y otros trabajan sobre ellos.
  - Referencia: <https://git-scm.com/docs/git-rebase>
- **Referencia** (referencias, ref, refs). *Concepto.* Nombre que apunta a un commit. Una rama es una referencia en refs/heads que avanza con cada commit; una etiqueta es una referencia fija.
  - Referencia: <https://git-scm.com/docs/gitglossary>
- **Reflog**. *Herramienta.* Registro local de por dónde ha pasado HEAD y cada rama. Permite recuperar commits tras un reset o un rebase mientras no caduquen sus entradas (90 días, o 30 si son inalcanzables, por defecto).
  - Referencia: <https://git-scm.com/docs/git-reflog>
- **Revert** (git revert). *Herramienta.* Crea un commit nuevo que deshace los cambios de otro. No reescribe la historia, así que es seguro en ramas compartidas.
  - Referencia: <https://git-scm.com/docs/git-revert>
