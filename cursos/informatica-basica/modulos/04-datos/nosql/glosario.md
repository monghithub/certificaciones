# Glosario: Bases de datos NoSQL

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## B

- **Base de datos de documentos** (MongoDB, documento BSON). *Herramienta.* Base de datos que guarda documentos con estructura anidada (como JSON) y permite consultar e indexar sus campos. MongoDB es la más extendida.
  - Referencia: <https://www.mongodb.com/docs/manual/core/document/>

## C

- **Cache-aside** (caché perezosa, lazy loading). *Patrón.* La aplicación busca primero en la caché; si no está, lee del origen, lo guarda en la caché con una caducidad y lo devuelve. Al modificar el dato, se invalida.
  - Referencia: <https://redis.io/docs/latest/develop/use/patterns/>
- **COLLSCAN** (IXSCAN, explain). *Concepto.* Etapa de un plan de MongoDB que recorre toda la colección; IXSCAN recorre un índice. explain() muestra el plan y cuántos documentos y claves se examinaron.
  - Referencia: <https://www.mongodb.com/docs/manual/reference/explain-results/>
- **Conjunto de réplicas** (replica set, primario, secundario). *Concepto.* Grupo de servidores de MongoDB con los mismos datos: un primario recibe las escrituras y los secundarios las replican; si el primario cae, se elige otro.
  - Referencia: <https://www.mongodb.com/docs/manual/replication/>
- **Consistencia eventual** (eventual consistency, teorema CAP). *Concepto.* Garantía de que, si no hay escrituras nuevas, todas las réplicas acabarán con el mismo valor, aunque mientras tanto una lectura pueda devolver datos antiguos.
  - Referencia: <https://www.allthingsdistributed.com/2008/12/eventually_consistent.html>

## E

- **Embeber o referenciar** (embedding, referencing, desnormalización). *Técnica.* Decisión de modelado en bases de documentos: incluir los datos relacionados dentro del documento (se leen juntos) o guardarlos aparte con una referencia (crecen o se usan por separado).
  - Referencia: <https://www.mongodb.com/docs/manual/data-modeling/embedding/>

## I

- **Índice compuesto** (compound index, prefijo de índice). *Técnica.* Índice sobre varios campos en un orden; sirve para consultas que usan sus campos iniciales (su prefijo).
  - Referencia: <https://www.mongodb.com/docs/manual/core/indexes/index-types/index-compound/>

## N

- **NoSQL**. *Concepto.* Bases de datos que no siguen el modelo relacional de tablas: de documentos, clave-valor, columna ancha o grafos. Suelen priorizar la escala horizontal o un modelo de datos concreto.
  - Referencia: <https://martinfowler.com/bliki/PolyglotPersistence.html>

## P

- **Persistencia políglota** (polyglot persistence). *Patrón.* Usar varios tipos de base de datos en un mismo sistema, cada uno para los datos y accesos que mejor encajan.
  - Referencia: <https://martinfowler.com/bliki/PolyglotPersistence.html>

## R

- **Redis** (Valkey). *Herramienta.* Almacén de estructuras de datos en memoria (cadenas, listas, conjuntos, hashes, conjuntos ordenados…) con operaciones atómicas, muy usado como caché. Valkey es una bifurcación comunitaria.
  - Referencia: <https://redis.io/docs/latest/develop/data-types/>
- **Regla ESR** (igualdad, orden, rango). *Técnica.* Guía de MongoDB para ordenar los campos de un índice compuesto: primero los de igualdad, luego los de ordenación y por último los de rango.
  - Referencia: <https://www.mongodb.com/docs/manual/tutorial/equality-sort-range-guideline/>

## T

- **TTL** (caducidad, EXPIRE). *Concepto.* Tiempo de vida de una clave; al cumplirse, la clave se elimina sola.
  - Referencia: <https://redis.io/docs/latest/commands/expire/>
- **Tubería de agregación** ($lookup, aggregation pipeline). *Herramienta.* Secuencia de etapas de MongoDB ($match, $group, $sort…) que transforma documentos; la etapa $lookup une documentos de otra colección, similar a un join.
  - Referencia: <https://www.mongodb.com/docs/manual/aggregation/>

## W

- **Write concern** (read concern, w majority). *Concepto.* Nivel de confirmación que se pide a una escritura en MongoDB (por ejemplo, w majority: confirmada por la mayoría de miembros). El read concern fija qué datos puede ver una lectura.
  - Referencia: <https://www.mongodb.com/docs/manual/reference/write-concern/>
