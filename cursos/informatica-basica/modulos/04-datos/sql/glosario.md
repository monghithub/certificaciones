# Glosario: SQL y modelado relacional

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 15 términos.

## C

- **Clave foránea** (FOREIGN KEY, REFERENCES, claves foráneas). *Concepto.* Columna que hace referencia a la clave primaria de otra tabla. La base de datos impide guardar valores que no existan en la tabla referenciada (integridad referencial).
  - Referencia: <https://www.postgresql.org/docs/current/ddl-constraints.html>
- **Clave primaria** (PRIMARY KEY, claves primarias). *Concepto.* Columna o conjunto de columnas que identifica de forma única cada fila de una tabla. No admite duplicados ni NULL.
  - Referencia: <https://www.postgresql.org/docs/current/ddl-constraints.html>
- **CTE** (WITH, expresión de tabla común). *Concepto.* Consulta con nombre definida con WITH que se usa como una tabla dentro de la consulta principal. Hace legibles las consultas complejas y permite consultas recursivas.
  - Referencia: <https://www.postgresql.org/docs/current/queries-with.html>

## D

- **Desnormalización**. *Técnica.* Introducir redundancia de forma deliberada (copiar datos o guardar valores calculados) para acelerar lecturas, a cambio de tener que mantenerla coherente.
  - Referencia: <https://en.wikipedia.org/wiki/Database_normalization>

## E

- **EXPLAIN**. *Herramienta.* Orden que muestra el plan con el que el motor ejecutará una consulta (recorrido secuencial, uso de índices, costes estimados). EXPLAIN ANALYZE además la ejecuta y mide.
  - Referencia: <https://www.postgresql.org/docs/current/using-explain.html>

## F

- **Función de agregado** (GROUP BY, HAVING, agregados). *Concepto.* Función que resume varias filas en un valor (count, sum, avg, max). GROUP BY forma los grupos y HAVING filtra grupos después de agregar.
  - Referencia: <https://www.postgresql.org/docs/current/functions-aggregate.html>
- **Función de ventana** (OVER, funciones de ventana, window function). *Concepto.* Función que calcula un valor para cada fila a partir de un conjunto de filas relacionadas (su ventana) sin agruparlas, como totales acumulados o rankings.
  - Referencia: <https://www.postgresql.org/docs/current/tutorial-window.html>

## I

- **Índice** (índices, CREATE INDEX). *Concepto.* Estructura adicional (normalmente un árbol B) que permite encontrar filas sin recorrer toda la tabla. Acelera las lecturas que lo aprovechan y ralentiza las escrituras, que deben mantenerlo.
  - Referencia: <https://www.postgresql.org/docs/current/indexes-types.html>

## J

- **JOIN** (INNER JOIN, LEFT JOIN). *Concepto.* Operación que combina filas de dos tablas según una condición. INNER JOIN devuelve solo las filas con pareja; LEFT JOIN devuelve también las de la izquierda sin pareja, con NULL en las columnas de la derecha.
  - Referencia: <https://www.postgresql.org/docs/current/tutorial-join.html>

## M

- **Modelo relacional**. *Concepto.* Modelo de datos propuesto por Edgar F. Codd en 1970 en el que los datos se organizan en relaciones (tablas) de tuplas (filas) con atributos (columnas), y se consultan con operaciones sobre conjuntos.
  - Referencia: <https://en.wikipedia.org/wiki/Relational_model>

## N

- **Normalización** (forma normal, formas normales, 1FN, 2FN, 3FN). *Técnica.* Proceso de organizar las tablas para eliminar la redundancia y las anomalías de inserción, actualización y borrado, siguiendo las formas normales (1FN, 2FN, 3FN…).
  - Referencia: <https://en.wikipedia.org/wiki/Database_normalization>
- **NULL**. *Concepto.* Marcador de valor desconocido o ausente. Cualquier comparación con NULL da desconocido (ni verdadero ni falso), así que se consulta con IS NULL e IS NOT NULL.
  - Referencia: <https://www.postgresql.org/docs/current/functions-comparison.html>

## R

- **Restricción** (restricciones, CHECK, NOT NULL, UNIQUE). *Concepto.* Regla que la base de datos hace cumplir a los datos (NOT NULL, UNIQUE, CHECK, claves primarias y foráneas). Rechaza cualquier escritura que la incumpla, venga de donde venga.
  - Referencia: <https://www.postgresql.org/docs/current/ddl-constraints.html>

## S

- **Selectividad**. *Métrica.* Proporción de filas que cumple una condición. Una condición muy selectiva (pocas filas) suele aprovechar un índice; una poco selectiva suele resolverse más rápido recorriendo la tabla.
  - Referencia: <https://www.postgresql.org/docs/current/using-explain.html>

## U

- **Upsert** (ON CONFLICT). *Técnica.* Inserción que, si choca con una restricción de unicidad, actualiza la fila existente en lugar de fallar. En PostgreSQL se escribe INSERT … ON CONFLICT … DO UPDATE.
  - Referencia: <https://www.postgresql.org/docs/current/sql-insert.html>
