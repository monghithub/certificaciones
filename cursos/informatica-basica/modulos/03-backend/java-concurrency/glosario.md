# Glosario: Concurrencia en Java

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 13 términos.

## C

- **Cerrojo** (synchronized, ReentrantLock, lock). *Herramienta.* Mecanismo de exclusión mutua; solo un hilo a la vez ejecuta la sección protegida. synchronized es el integrado en el lenguaje, y ReentrantLock añade intentos con plazo e interrupción.
  - Referencia: <https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html#jls-17.1>
- **Cola bloqueante** (BlockingQueue, productor-consumidor). *Patrón.* Cola que bloquea al productor cuando está llena y al consumidor cuando está vacía. Con un tamaño máximo, frena al productor si el consumidor no da abasto.
  - Referencia: <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/package-summary.html>
- **CompletableFuture**. *Herramienta.* Resultado futuro que se puede componer (thenCombine, thenCompose), limitar en el tiempo (completeOnTimeout, orTimeout) y recuperar de errores (exceptionally) sin bloquear.
  - Referencia: <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/CompletableFuture.html>
- **Concurrencia estructurada** (StructuredTaskScope). *Técnica.* Forma de lanzar subtareas concurrentes dentro de un ámbito, de modo que terminan todas juntas; si una falla, las demás se cancelan. En noviembre de 2026 sigue en preview (séptima en JDK 27).
  - Referencia: <https://openjdk.org/jeps/533>
- **ConcurrentHashMap**. *Herramienta.* Mapa seguro para varios hilos. Cada operación es atómica, pero una secuencia de ellas (get y después put) no; para eso están merge, compute y putIfAbsent.
  - Referencia: <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html>
- **Condición de carrera** (condiciones de carrera, race condition). *Concepto.* Fallo en el que el resultado depende del orden en que se intercalan los hilos. contador++ no es atómico (leer, sumar, escribir), y dos hilos pueden pisarse los incrementos.
  - Referencia: <https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html>

## E

- **Ejecutor** (ExecutorService, pool de hilos). *Herramienta.* Servicio que ejecuta tareas en un grupo de hilos y devuelve un Future por cada una. Separa qué se hace de cómo se reparte entre hilos.
  - Referencia: <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ExecutorService.html>

## I

- **Interbloqueo** (deadlock). *Concepto.* Dos o más hilos esperan cada uno un cerrojo que tiene otro, y ninguno avanza. Se evita tomando los cerrojos siempre en el mismo orden.
  - Referencia: <https://docs.oracle.com/en/java/javase/25/docs/api/java.management/java/lang/management/ThreadMXBean.html>

## O

- **Ocurre antes** (happens-before). *Concepto.* Relación del modelo de memoria de Java que garantiza que las escrituras anteriores a una acción son visibles tras otra, por ejemplo al liberar y tomar el mismo cerrojo o al escribir y leer una variable volatile.
  - Referencia: <https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html#jls-17.4.5>

## P

- **Pinning** (hilo virtual fijado). *Concepto.* Situación en la que un hilo virtual no puede desmontarse de su hilo portador mientras espera. Hasta JDK 23 ocurría dentro de synchronized; el JEP 491 lo eliminó en JDK 24.
  - Referencia: <https://openjdk.org/jeps/491>

## V

- **Valores con ámbito** (ScopedValue, scoped values). *Herramienta.* Valores inmutables que se comparten con los métodos llamados y con las subtareas durante un ámbito acotado. Definitivos desde JDK 25 (JEP 506); sustituyen a ThreadLocal en muchos usos.
  - Referencia: <https://openjdk.org/jeps/506>
- **Variables atómicas** (AtomicLong, LongAdder, atómicos). *Herramienta.* Clases de java.util.concurrent.atomic que hacen operaciones como incrementar en un solo paso indivisible, sin cerrojos. LongAdder reparte el contador para escalar con mucha contención.
  - Referencia: <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/atomic/LongAdder.html>
- **Visibilidad** (volatile). *Concepto.* Garantía de que lo que escribe un hilo lo ve otro. Sin una relación «ocurre antes» (volatile, synchronized, un cerrojo), un hilo puede no ver nunca el cambio.
  - Referencia: <https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html#jls-17.4.5>
