# Glosario: Linux y shell para desarrolladores

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## C

- **Código de salida** (códigos de salida, exit code, $?). *Concepto.* Número de 0 a 255 que devuelve un proceso al terminar. 0 es éxito y cualquier otro, fallo. Si lo mata una señal, la shell informa 128 más el número de la señal (143 para SIGTERM, 137 para SIGKILL).
  - Referencia: <https://tiswww.case.edu/php/chet/bash/bashref.html#Exit-Status>

## D

- **Descriptor de fichero** (stdin, stdout, stderr, descriptores). *Concepto.* Número con el que un proceso se refiere a un fichero abierto. Todo proceso empieza con 0 (entrada estándar), 1 (salida estándar) y 2 (salida de errores).
  - Referencia: <https://tiswww.case.edu/php/chet/bash/bashref.html#Redirections>

## J

- **journald** (journalctl, diario de systemd). *Herramienta.* Servicio que recoge los registros del sistema y de los servicios. journalctl los consulta por unidad, fecha o prioridad.
  - Referencia: <https://www.freedesktop.org/software/systemd/man/latest/journalctl.html>

## P

- **Permisos** (permisos de fichero, rwx). *Concepto.* Lectura (r), escritura (w) y ejecución (x) para el propietario, el grupo y el resto. Se escriben como rwxr-xr-x o en octal (755), y en un directorio x permite entrar en él.
  - Referencia: <https://man7.org/linux/man-pages/man1/chmod.1.html>
- **pipefail** (set -o pipefail). *Técnica.* Opción de bash por la que una tubería falla si falla cualquiera de sus comandos, no solo el último.
  - Referencia: <https://tiswww.case.edu/php/chet/bash/bashref.html#The-Set-Builtin>
- **Proceso** (procesos, PID). *Concepto.* Programa en ejecución, con su identificador (PID), su proceso padre (PPID), su usuario y sus descriptores de ficheros abiertos. Se ve en /proc/PID y con ps.
  - Referencia: <https://man7.org/linux/man-pages/man5/proc.5.html>

## S

- **Señal** (señales, SIGTERM, SIGKILL). *Concepto.* Aviso asíncrono a un proceso. SIGTERM (15) le pide que termine y se puede capturar para cerrar limpiamente; SIGKILL (9) lo mata sin que pueda reaccionar.
  - Referencia: <https://man7.org/linux/man-pages/man7/signal.7.html>
- **set -e** (errexit, set -euo pipefail). *Técnica.* Opción de bash que termina el script cuando un comando falla. Tiene excepciones importantes, como los comandos dentro de un if o a la izquierda de && o ||, incluidas las funciones llamadas ahí.
  - Referencia: <https://tiswww.case.edu/php/chet/bash/bashref.html#The-Set-Builtin>
- **setuid** (bit setuid). *Concepto.* Permiso especial (la s en rwsr-xr-x) por el que un programa se ejecuta con la identidad de su propietario, no de quien lo lanza. passwd lo usa para poder escribir en /etc/shadow.
  - Referencia: <https://man7.org/linux/man-pages/man1/chmod.1.html>
- **ShellCheck**. *Herramienta.* Analizador estático de scripts de shell que detecta errores comunes, como variables sin comillas, cd sin comprobar o bucles sobre la salida de ls.
  - Referencia: <https://www.shellcheck.net/wiki/SC2086>
- **systemd** (systemctl, unidad de systemd). *Herramienta.* Gestor del sistema y de los servicios en la mayoría de distribuciones Linux. Cada servicio es una unidad con su configuración de arranque, reinicio, usuario y límites, y se controla con systemctl.
  - Referencia: <https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html>

## T

- **trap**. *Herramienta.* Orden de bash que ejecuta un código al recibir una señal o al salir (EXIT). Se usa para limpiar ficheros temporales o cerrar un servicio con elegancia.
  - Referencia: <https://tiswww.case.edu/php/chet/bash/bashref.html#Bourne-Shell-Builtins>
- **Tubería** (pipe, tuberías). *Técnica.* Une la salida estándar de un comando con la entrada del siguiente (cmd1 | cmd2). El código de la tubería es el del último comando, salvo con set -o pipefail.
  - Referencia: <https://tiswww.case.edu/php/chet/bash/bashref.html#Pipelines>

## U

- **umask**. *Concepto.* Máscara que quita permisos a los ficheros y directorios nuevos. Con 022, un fichero nuevo queda en 644 y un directorio en 755; con 077, solo el propietario puede acceder.
  - Referencia: <https://man7.org/linux/man-pages/man2/umask.2.html>
