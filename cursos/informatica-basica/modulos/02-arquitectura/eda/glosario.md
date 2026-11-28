# Glosario: Arquitectura dirigida por eventos

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## C

- **Captura de cambios de datos** (CDC, change data capture). *Técnica.* Leer los cambios de una base de datos desde su registro de transacciones para publicarlos como eventos; herramientas como Debezium lo usan para enviar la tabla outbox.
  - Referencia: <https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html>
- **Comando** (comandos). *Concepto.* Petición para que otro sistema haga algo (ReservarStock). A diferencia de un evento, va dirigida a un destinatario y puede rechazarse.
  - Referencia: <https://martinfowler.com/articles/201701-event-driven.html>
- **Coreografía** (choreography). *Técnica.* Forma de coordinar una saga en la que cada servicio reacciona a los eventos de los demás, sin un coordinador central.
  - Referencia: <https://microservices.io/patterns/data/saga.html>
- **CQRS** (Command Query Responsibility Segregation). *Patrón.* Patrón que usa modelos distintos para escribir y para leer. Fowler advierte que, en la mayoría de los sistemas, añade una complejidad arriesgada.
  - Usar cuando: Las lecturas y las escrituras tienen necesidades muy distintas y la complejidad compensa.
  - No usar cuando: La mayoría de los sistemas, donde un único modelo basta.
  - Referencia: <https://martinfowler.com/bliki/CQRS.html>

## D

- **Doble escritura** (dual write). *Concepto.* Escribir en la base de datos y publicar en el broker como dos operaciones separadas: si una falla, quedan incoherentes.
  - Referencia: <https://microservices.io/patterns/data/transactional-outbox.html>

## E

- **Event sourcing** (almacén de eventos, event store). *Patrón.* Patrón en el que cada cambio de estado se guarda como un evento y el estado se reconstruye reprocesándolos; el almacén de eventos es la fuente de verdad.
  - Usar cuando: Hace falta un historial completo y auditable, o reconstruir el estado de cualquier momento.
  - No usar cuando: Un CRUD normal basta; añade complejidad en consultas, versiones de eventos y migraciones.
  - Referencia: <https://martinfowler.com/eaaDev/EventSourcing.html>
- **Evento** (eventos, evento de dominio). *Concepto.* Hecho que ya ha ocurrido en el dominio y que se comunica a otros, nombrado en pasado (PedidoConfirmado). Quien lo emite no espera respuesta.
  - Referencia: <https://martinfowler.com/articles/201701-event-driven.html>

## N

- **Notificación de eventos** (event notification). *Patrón.* Patrón en el que un sistema avisa de un cambio con un evento pequeño y no espera respuesta; quien necesita los detalles los consulta al emisor.
  - Referencia: <https://martinfowler.com/articles/201701-event-driven.html>

## O

- **Orquestación** (orchestration, orquestador). *Técnica.* Forma de coordinar una saga en la que un orquestador indica a cada servicio qué paso ejecutar y decide las compensaciones.
  - Referencia: <https://microservices.io/patterns/data/saga.html>

## P

- **Patrón outbox** (outbox, bandeja de salida transaccional, transactional outbox). *Patrón.* Guardar el mensaje que se va a publicar en una tabla de la base de datos, en la misma transacción que el cambio de negocio; un proceso aparte lo envía al broker.
  - Referencia: <https://microservices.io/patterns/data/transactional-outbox.html>
- **Proyección** (proyecciones, modelo de lectura). *Concepto.* Vista de lectura construida a partir de los eventos o de los cambios, optimizada para unas consultas concretas.
  - Referencia: <https://martinfowler.com/bliki/CQRS.html>

## S

- **Saga** (sagas). *Patrón.* Secuencia de transacciones locales, una por servicio, en la que cada fallo se deshace con transacciones compensatorias. La propusieron Garcia-Molina y Salem en 1987 para transacciones largas.
  - Referencia: <https://microservices.io/patterns/data/saga.html>

## T

- **Transacción compensatoria** (compensación, compensaciones). *Concepto.* Operación que deshace el efecto de un paso ya confirmado de una saga (liberar el stock reservado, devolver un cobro).
  - Referencia: <https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction>
- **Transferencia de estado en el evento** (event-carried state transfer). *Patrón.* Patrón en el que el evento lleva los datos que cambiaron, para que los receptores mantengan su propia copia sin consultar al emisor.
  - Referencia: <https://martinfowler.com/articles/201701-event-driven.html>
