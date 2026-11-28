# Glosario: Transacciones, aislamiento y concurrencia

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## A

- **ACID**. *Concepto.* Las cuatro garantías de una transacción: atomicidad (todo o nada), consistencia (respeta las reglas), aislamiento (las transacciones concurrentes no se pisan) y durabilidad (lo confirmado no se pierde).
  - Referencia: <https://en.wikipedia.org/wiki/ACID>
- **Actualización perdida** (lost update). *Concepto.* Dos transacciones leen un valor, lo modifican en la aplicación y lo escriben; la segunda escritura borra la primera.
  - Referencia: <https://en.wikipedia.org/wiki/Isolation_(database_systems)>

## B

- **Bloqueo optimista** (optimistic locking, columna de versión). *Técnica.* Detectar conflictos al escribir en lugar de bloquear al leer: se guarda un número de versión y la actualización solo se aplica si la versión no ha cambiado desde la lectura.
  - Referencia: <https://en.wikipedia.org/wiki/Optimistic_concurrency_control>

## E

- **Error de serialización** (serialization failure, could not serialize access). *Concepto.* Error que PostgreSQL devuelve en REPEATABLE READ o SERIALIZABLE cuando confirmar la transacción violaría el aislamiento. La aplicación debe repetir la transacción.
  - Referencia: <https://www.postgresql.org/docs/current/transaction-iso.html>

## I

- **Interbloqueo** (deadlock, interbloqueos). *Concepto.* Situación en la que dos o más transacciones esperan cada una un bloqueo que tiene la otra. PostgreSQL lo detecta y aborta una de ellas.
  - Referencia: <https://www.postgresql.org/docs/current/explicit-locking.html>

## L

- **Lectura fantasma** (phantom read, fantasma). *Concepto.* Repetir una consulta con una condición y obtener otro conjunto de filas porque otra transacción insertó o borró filas que la cumplen.
  - Referencia: <https://www.postgresql.org/docs/current/transaction-iso.html>
- **Lectura no repetible** (non-repeatable read). *Concepto.* Leer dos veces la misma fila dentro de una transacción y obtener valores distintos porque otra transacción la cambió y confirmó entre medias.
  - Referencia: <https://www.postgresql.org/docs/current/transaction-iso.html>
- **Lectura sucia** (dirty read). *Concepto.* Leer datos que otra transacción ha escrito pero aún no ha confirmado. PostgreSQL no la permite en ningún nivel.
  - Referencia: <https://www.postgresql.org/docs/current/transaction-iso.html>

## M

- **MVCC** (control de concurrencia multiversión). *Técnica.* Técnica en la que la base de datos guarda varias versiones de cada fila y cada transacción lee una instantánea coherente, de modo que las lecturas no bloquean a las escrituras ni al revés.
  - Referencia: <https://www.postgresql.org/docs/current/mvcc-intro.html>

## N

- **Nivel de aislamiento** (niveles de aislamiento, isolation level, READ COMMITTED, REPEATABLE READ, SERIALIZABLE). *Concepto.* Grado en que una transacción ve los cambios de otras concurrentes. El estándar SQL define cuatro; en PostgreSQL hay tres efectivos, y el predeterminado es READ COMMITTED.
  - Referencia: <https://www.postgresql.org/docs/current/transaction-iso.html>

## S

- **SELECT … FOR UPDATE** (FOR UPDATE). *Técnica.* Lectura que bloquea las filas leídas hasta el final de la transacción, de modo que otras que quieran modificarlas o bloquearlas esperan.
  - Referencia: <https://www.postgresql.org/docs/current/sql-select.html>

## T

- **Transacción** (transacciones). *Concepto.* Conjunto de operaciones que la base de datos trata como una unidad: o se aplican todas (COMMIT) o ninguna (ROLLBACK).
  - Referencia: <https://www.postgresql.org/docs/current/tutorial-transactions.html>

## W

- **WAL** (write-ahead log, registro de escritura anticipada). *Técnica.* Registro en el que la base de datos anota los cambios antes de aplicarlos a los ficheros de datos; garantiza la durabilidad y permite recuperar tras una caída.
  - Referencia: <https://www.postgresql.org/docs/current/wal-intro.html>
- **Write skew** (sesgo de escritura, anomalía de serialización). *Concepto.* Dos transacciones leen datos que se solapan, cada una decide según lo leído y escriben filas distintas, de modo que juntas incumplen una regla que cada una respetaba por separado.
  - Referencia: <https://www.postgresql.org/docs/current/transaction-iso.html>
