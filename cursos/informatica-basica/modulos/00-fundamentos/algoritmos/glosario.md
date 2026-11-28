# Glosario: Algoritmos y estructuras de datos

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## A

- **Árbol de búsqueda equilibrado** (TreeMap, árbol rojo-negro). *Concepto.* Árbol que mantiene las claves ordenadas y su altura en O(log n), de modo que buscar, insertar y borrar cuestan O(log n) y permite consultas por orden y rango.
  - Referencia: <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/TreeMap.html>

## B

- **Búsqueda binaria** (binary search, bisect). *Técnica.* Búsqueda en una secuencia ordenada que descarta la mitad en cada paso: O(log n).
  - Referencia: <https://docs.python.org/3/library/bisect.html>
- **Búsqueda en anchura** (BFS, breadth-first search). *Técnica.* Recorrido de un grafo por niveles con una cola; encuentra el camino con menos aristas en grafos sin pesos.
  - Referencia: <https://en.wikipedia.org/wiki/Breadth-first_search>

## C

- **Cola doble** (deque, ArrayDeque). *Herramienta.* Estructura que permite añadir y quitar por los dos extremos en O(1); sirve como cola o como pila.
  - Referencia: <https://docs.python.org/3/library/collections.html#collections.deque>
- **Contrato de equals y hashCode** (hashCode, equals). *Concepto.* En Java, dos objetos iguales según equals deben tener el mismo hashCode; si no se respeta, las tablas hash no los encuentran.
  - Referencia: <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Object.html>
- **Coste amortizado** (amortizado). *Concepto.* Coste medio por operación a lo largo de una secuencia: añadir al final de una lista dinámica es O(1) amortizado aunque a veces haya que copiarla entera para crecer.
  - Referencia: <https://wiki.python.org/moin/TimeComplexity>

## G

- **Grafo** (nodo, arista, lista de adyacencia). *Concepto.* Conjunto de nodos unidos por aristas; se representa a menudo con una lista de adyacencia (cada nodo con sus vecinos).
  - Referencia: <https://en.wikipedia.org/wiki/Breadth-first_search>

## L

- **Lista dinámica** (array dinámico, ArrayList, list). *Concepto.* Secuencia en memoria contigua que crece reservando más capacidad de la necesaria. Acceso por índice O(1); insertar o borrar al principio, O(n).
  - Referencia: <https://wiki.python.org/moin/TimeComplexity>

## M

- **Memoización** (memoization, @cache). *Técnica.* Guardar el resultado de una función para cada argumento y reutilizarlo, evitando repetir cálculos en recursiones con subproblemas repetidos.
  - Referencia: <https://docs.python.org/3/library/functools.html#functools.cache>
- **Montículo** (heap, heapq, PriorityQueue, cola de prioridad). *Concepto.* Árbol guardado en un array en el que cada padre es menor (o mayor) que sus hijos; da el mínimo en O(1) y lo extrae en O(log n). Implementa colas de prioridad.
  - Referencia: <https://docs.python.org/3/library/heapq.html>

## N

- **Notación O** (Big O, complejidad). *Concepto.* Forma de describir cómo crece el coste de un algoritmo (tiempo o memoria) con el tamaño de la entrada, ignorando constantes: O(1), O(log n), O(n), O(n log n), O(n²).
  - Referencia: <https://en.wikipedia.org/wiki/Big_O_notation>

## O

- **Ordenación estable** (stable sort, Timsort). *Concepto.* Ordenación que conserva el orden original de los elementos con la misma clave.
  - Referencia: <https://docs.python.org/3/howto/sorting.html>

## P

- **Pila y cola** (stack, queue, LIFO, FIFO). *Concepto.* Una pila saca primero el último que entró (LIFO); una cola, el primero (FIFO).
  - Referencia: <https://docs.python.org/3/library/collections.html#collections.deque>

## T

- **Tabla hash** (hash table, HashMap, dict, set). *Concepto.* Estructura que guarda elementos en posiciones calculadas a partir del hash de la clave; búsqueda, inserción y borrado en O(1) de media.
  - Referencia: <https://en.wikipedia.org/wiki/Hash_table>
