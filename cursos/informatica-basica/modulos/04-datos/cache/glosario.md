# Glosario: Caché y rendimiento

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 12 términos.

## C

- **Cache-aside** (lazy loading). *Patrón.* La aplicación busca en la caché; si no está, lee del origen y guarda el resultado. Al escribir, actualiza el origen y borra la entrada de la caché.
  - Referencia: <https://redis.io/docs/latest/develop/use/keyspace/>
- **Clave caliente** (hot key). *Concepto.* Clave que recibe una parte desproporcionada de las peticiones y satura el nodo de caché que la tiene. Se mitiga con una copia en memoria local o repartiéndola en varias claves.
  - Referencia: <https://redis.io/docs/latest/develop/use/keyspace/>

## E

- **Estampida** (cache stampede, thundering herd). *Concepto.* Muchas peticiones encuentran a la vez una clave caducada y van todas al origen, que se satura justo cuando la caché debía protegerlo.
  - Referencia: <https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/>

## I

- **Invalidación** (invalidar). *Técnica.* Quitar o actualizar una entrada de caché cuando cambia el origen. Es la parte difícil de cachear, porque las escrituras y las lecturas concurrentes pueden dejar datos obsoletos.
  - Referencia: <https://martinfowler.com/bliki/TwoHardThings.html>

## P

- **Percentil** (percentiles, p50, p95, p99). *Métrica.* Valor por debajo del cual queda un porcentaje de las medidas. El p99 de la latencia es el tiempo que supera solo el 1 % de las peticiones. Describe mejor la experiencia que la media.
  - Referencia: <https://sre.google/sre-book/monitoring-distributed-systems/>
- **Perfilador** (profiler, cProfile, perfil). *Herramienta.* Herramienta que mide en qué funciones se va el tiempo de un programa. Evita optimizar a ciegas.
  - Referencia: <https://docs.python.org/3/library/profile.html>
- **Política de expulsión** (eviction, maxmemory-policy, LRU, LFU). *Concepto.* Qué claves quita la caché cuando se llena. En Redis, noeviction (la de por defecto) rechaza las escrituras, y allkeys-lru o allkeys-lfu quitan las menos usadas.
  - Referencia: <https://redis.io/docs/latest/develop/reference/eviction/>

## S

- **stale-while-revalidate**. *Protocolo.* Directiva de Cache-Control que permite servir una respuesta caducada mientras se obtiene la nueva en segundo plano, para que nadie espere al origen.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc5861.html>

## T

- **Tasa de aciertos** (hit ratio, acierto, fallo de caché). *Métrica.* Proporción de lecturas que encuentra el dato en la caché. Una caché con pocos aciertos añade una consulta extra sin ahorrar casi nada.
  - Referencia: <https://redis.io/docs/latest/develop/reference/eviction/>
- **TTL** (caducidad, tiempo de vida). *Concepto.* Tiempo tras el que una entrada de caché caduca. Es la red de seguridad contra las invalidaciones que fallan, y conviene añadirle una variación aleatoria.
  - Referencia: <https://redis.io/docs/latest/commands/set/>

## W

- **Write-behind** (write-back, escritura diferida). *Patrón.* La escritura se hace en la caché y se lleva al origen más tarde, en lotes. Es rápido, pero si la caché cae antes de escribir, se pierden datos.
  - Referencia: <https://docs.spring.io/spring-framework/reference/integration/cache.html>
- **Write-through** (escritura directa). *Patrón.* Cada escritura va a la caché y al origen a la vez, de modo que la caché queda al día. Las escrituras son más lentas.
  - Referencia: <https://docs.spring.io/spring-framework/reference/integration/cache.html>
