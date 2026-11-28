# Glosario: Contenedores y Docker

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 15 términos.

## B

- **Bind mount** (bind mounts, montaje enlazado). *Concepto.* Montaje de un fichero o carpeta del anfitrión dentro del contenedor. Útil en desarrollo y para configuración; depende de la estructura de carpetas del anfitrión.
  - Referencia: <https://docs.docker.com/engine/storage/bind-mounts/>

## C

- **Capa** (capas). *Concepto.* Cada cambio de sistema de ficheros que añade una instrucción del Dockerfile (RUN, COPY, ADD). Las capas se comparten entre imágenes y se reutilizan en la caché de construcción.
  - Referencia: <https://docs.docker.com/build/cache/>
- **cgroups** (grupos de control, control groups). *Concepto.* Función del núcleo Linux que organiza procesos en grupos y limita y mide su uso de recursos (CPU, memoria, E/S). Docker la usa para los límites de los contenedores.
  - Referencia: <https://man7.org/linux/man-pages/man7/cgroups.7.html>
- **Construcción multietapa** (multi-stage, multietapa). *Técnica.* Dockerfile con varias instrucciones FROM en el que una etapa compila y otra, más ligera, copia solo el resultado. Reduce el tamaño y la superficie de ataque de la imagen final.
  - Referencia: <https://docs.docker.com/build/building/multi-stage/>
- **Contenedor** (contenedores). *Concepto.* Proceso (o grupo de procesos) aislado del resto del sistema mediante funciones del núcleo Linux, con su propio sistema de ficheros tomado de una imagen. Comparte el núcleo con el anfitrión.
  - Referencia: <https://docs.docker.com/learn/content/what-is-a-container/>
- **Contexto de construcción**. *Concepto.* Conjunto de ficheros que se envían al constructor al hacer docker build. El fichero .dockerignore excluye lo que no debe enviarse.
  - Referencia: <https://docs.docker.com/build/concepts/context/>

## D

- **Docker Compose** (Compose, compose.yaml). *Herramienta.* Herramienta para definir y ejecutar aplicaciones de varios contenedores con un fichero YAML (servicios, redes y volúmenes) y un solo comando.
  - Referencia: <https://docs.docker.com/compose/>
- **Dockerfile**. *Herramienta.* Fichero de texto con las instrucciones para construir una imagen (FROM, RUN, COPY, CMD…).
  - Referencia: <https://docs.docker.com/reference/dockerfile/>

## I

- **Imagen** (imágenes, imagen de contenedor). *Concepto.* Plantilla de solo lectura, formada por capas, con el sistema de ficheros y la configuración necesarios para crear contenedores.
  - Referencia: <https://docs.docker.com/learn/content/what-is-a-container/>

## M

- **Máquina virtual** (máquinas virtuales, VM). *Concepto.* Emulación de un ordenador completo, con su propio sistema operativo y núcleo, sobre un hipervisor. Aísla más que un contenedor, pero pesa más y arranca más despacio.
  - Referencia: <https://docs.docker.com/learn/content/what-is-a-container/>

## N

- **Namespace** (namespaces, espacios de nombres). *Concepto.* Función del núcleo Linux que da a un grupo de procesos su propia vista de un recurso global (procesos, red, puntos de montaje, usuarios, nombre de máquina). Es la base del aislamiento de los contenedores.
  - Referencia: <https://man7.org/linux/man-pages/man7/namespaces.7.html>

## O

- **OCI** (Open Container Initiative). *Protocolo.* Iniciativa abierta que define los estándares de formato de imagen, de ejecución y de distribución de contenedores, para que las imágenes funcionen con distintas herramientas (Docker, Podman, containerd).
  - Referencia: <https://opencontainers.org/>

## P

- **PID 1**. *Concepto.* Primer proceso de un espacio de nombres de procesos. En Linux, el PID 1 no recibe la acción por defecto de señales como SIGTERM si no instala un manejador, por lo que un contenedor puede tardar en pararse; --init añade un proceso init mínimo que lo resuelve.
  - Referencia: <https://docs.docker.com/reference/cli/docker/container/run/>

## R

- **Registro de imágenes** (registry, Docker Hub). *Herramienta.* Servicio que almacena y distribuye imágenes, como Docker Hub o un registro privado. docker push sube una imagen y docker pull la descarga.
  - Referencia: <https://docs.docker.com/learn/content/what-is-a-container/>

## V

- **Volumen** (volúmenes). *Concepto.* Almacenamiento gestionado por Docker que vive fuera del sistema de ficheros del contenedor y persiste aunque el contenedor se elimine.
  - Usar cuando: Datos que deben sobrevivir al contenedor (bases de datos, ficheros subidos).
  - Referencia: <https://docs.docker.com/engine/storage/volumes/>
