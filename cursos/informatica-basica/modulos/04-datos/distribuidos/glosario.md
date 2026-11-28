# Glosario: Sistemas distribuidos

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 13 términos.

## C

- **Clave de idempotencia** (idempotency key). *Técnica.* Identificador que el cliente manda con cada operación y repite en los reintentos, para que el servidor reconozca la repetición y no la aplique dos veces.
  - Referencia: <https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/>
- **Consenso**. *Concepto.* Que varios nodos acuerden un mismo valor, o la misma secuencia de operaciones, aunque algunos fallen. Necesita una mayoría disponible.
  - Referencia: <https://raft.github.io/>

## F

- **Fallo parcial** (fallos parciales). *Concepto.* Una parte del sistema falla mientras el resto sigue funcionando. Quien espera una respuesta no puede distinguir un nodo caído de uno lento o de una red que pierde mensajes.
  - Referencia: <https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/>

## H

- **Hashing consistente** (consistent hashing, anillo, nodos virtuales). *Técnica.* Reparto de claves en un anillo de hash en el que, al añadir o quitar un nodo, solo se mueven las claves de su tramo. Con nodos virtuales el reparto queda equilibrado.
  - Referencia: <https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf>

## L

- **Lease** (concesión, arrendamiento). *Concepto.* Derecho con caducidad que hay que renovar. Si el dueño deja de renovarlo, porque cayó o quedó aislado, caduca y otro puede tomarlo.
  - Referencia: <https://etcd.io/docs/v3.6/dev-guide/interacting_v3/>
- **Linealizabilidad** (linearizable, lectura linealizable). *Concepto.* Garantía de que el sistema se comporta como una sola copia, y cada lectura ve la última escritura confirmada. Es la consistencia más fuerte para un solo objeto.
  - Referencia: <https://jepsen.io/consistency>

## P

- **Partición de red** (partición, split brain). *Concepto.* La red se divide y unos nodos no pueden hablar con otros, aunque todos sigan funcionando. En etcd solo el lado con mayoría sigue aceptando escrituras.
  - Referencia: <https://etcd.io/docs/v3.6/op-guide/failures/>

## Q

- **Quórum** (quórums, mayoría, R + W > N). *Concepto.* Número mínimo de réplicas que deben responder. Si las escrituras esperan a W réplicas y las lecturas consultan R, con R + W > N toda lectura toca al menos una réplica con la última escritura.
  - Referencia: <https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf>

## R

- **Raft** (líder, término, term). *Protocolo.* Algoritmo de consenso con un líder elegido por mayoría en cada término. El líder replica un registro de operaciones y una entrada se confirma cuando la tiene la mayoría. Lo usan etcd y Consul.
  - Referencia: <https://raft.github.io/>
- **Reloj de Lamport** (relojes lógicos, reloj lógico). *Concepto.* Contador que cada proceso incrementa en cada evento y que, al recibir un mensaje, salta por encima del valor recibido. Si un evento causa otro, el primero tiene un valor menor.
  - Referencia: <https://lamport.azurewebsites.net/pubs/time-clocks.pdf>
- **Reloj monótono** (monotonic, time.monotonic). *Concepto.* Reloj que solo avanza, sin saltos por ajustes de hora. Sirve para medir duraciones y timeouts; no dice la hora del día.
  - Referencia: <https://docs.python.org/3/library/time.html>

## T

- **Token de fencing** (fencing token, fencing). *Técnica.* Número que crece cada vez que se concede un cerrojo. El recurso protegido rechaza las peticiones con un número menor que el último visto, de modo que un antiguo dueño que se creía con el cerrojo no puede escribir.
  - Referencia: <https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html>

## U

- **Última escritura gana** (last write wins, LWW). *Técnica.* Resolver escrituras en conflicto quedándose con la de marca de tiempo mayor. Con relojes desajustados puede descartar la escritura que de verdad fue posterior.
  - Referencia: <https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html>
