# Glosario: Mensajería: colas y Kafka

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## A

- **Apache Kafka** (Kafka). *Herramienta.* Plataforma distribuida de flujos de eventos que guarda los eventos en registros particionados y replicados, de los que los consumidores leen a su ritmo. Desde la versión 4.0 solo funciona en modo KRaft, sin ZooKeeper.
  - Referencia: <https://kafka.apache.org/41/getting-started/introduction/>

## B

- **Broker de mensajería** (broker, brokers). *Herramienta.* Servidor intermedio que recibe mensajes de los productores, los guarda y los entrega a los consumidores, como Kafka o RabbitMQ.
  - Referencia: <https://kafka.apache.org/41/getting-started/introduction/>

## C

- **Canal de mensajes muertos** (dead letter queue, DLQ, cola de mensajes muertos). *Patrón.* Destino al que se envían los mensajes que no se pueden procesar tras varios intentos, para analizarlos sin bloquear el resto.
  - Referencia: <https://www.enterpriseintegrationpatterns.com/patterns/messaging/DeadLetterChannel.html>
- **Canal punto a punto** (cola, colas, point-to-point). *Patrón.* Canal en el que cada mensaje lo procesa un solo consumidor, aunque haya varios escuchando. Sirve para repartir trabajo.
  - Referencia: <https://www.enterpriseintegrationpatterns.com/patterns/messaging/PointToPointChannel.html>

## E

- **Entrega al menos una vez** (at least once, al menos una vez). *Concepto.* Garantía en la que ningún mensaje se pierde, pero alguno puede entregarse más de una vez. Obliga a que el consumidor sea idempotente.
  - Referencia: <https://kafka.apache.org/41/design/design/>

## G

- **Grupo de consumidores** (consumer group, grupos de consumidores). *Concepto.* Conjunto de consumidores que se reparten las particiones de un tema: cada partición la lee un solo consumidor del grupo. Grupos distintos leen el tema de forma independiente.
  - Referencia: <https://kafka.apache.org/41/design/design/>

## L

- **Lag** (retraso del consumidor). *Métrica.* Diferencia entre el último offset de una partición y el offset confirmado por un grupo: cuántos eventos le quedan por procesar.
  - Referencia: <https://kafka.apache.org/41/design/design/>

## O

- **Offset** (offsets, desplazamiento). *Concepto.* Posición de un evento dentro de su partición. Cada grupo de consumidores guarda por partición el offset del siguiente evento que debe leer.
  - Referencia: <https://kafka.apache.org/41/design/design/>

## P

- **Partición** (particiones, partition). *Concepto.* Registro ordenado y solo de añadir en el que se divide un tema. Los eventos con la misma clave van a la misma partición, y dentro de ella se leen en el orden en que se escribieron.
  - Referencia: <https://kafka.apache.org/41/getting-started/introduction/>
- **Productor idempotente** (enable.idempotence). *Técnica.* Opción del productor de Kafka (activada por defecto) que asegura que los reintentos no escriben copias duplicadas de un mensaje en el registro.
  - Referencia: <https://kafka.apache.org/41/configuration/producer-configs/>
- **Publicación-suscripción** (publish-subscribe, pub/sub). *Patrón.* Canal en el que cada mensaje llega a todos los suscriptores interesados. Sirve para difundir eventos a varios sistemas independientes.
  - Referencia: <https://www.enterpriseintegrationpatterns.com/patterns/messaging/PublishSubscribeChannel.html>

## R

- **Receptor idempotente** (consumidor idempotente, idempotent receiver). *Patrón.* Consumidor que puede recibir el mismo mensaje varias veces sin efectos duplicados, por ejemplo guardando el identificador de los mensajes ya procesados.
  - Referencia: <https://www.enterpriseintegrationpatterns.com/patterns/messaging/IdempotentReceiver.html>
- **Retención** (retention, log.retention.hours). *Concepto.* Tiempo (o tamaño) durante el que Kafka conserva los eventos de un tema, se hayan consumido o no. Por defecto, 168 horas (7 días).
  - Referencia: <https://kafka.apache.org/41/configuration/broker-configs/>

## T

- **Tema** (topic, topics, temas de Kafka). *Concepto.* Flujo de eventos con nombre en Kafka (por ejemplo, pedidos), dividido en particiones.
  - Referencia: <https://kafka.apache.org/41/getting-started/introduction/>
