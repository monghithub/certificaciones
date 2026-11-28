# Glosario: Diseño de APIs

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## C

- **Cambio incompatible** (breaking change, cambios incompatibles). *Concepto.* Cambio en una API que rompe a clientes existentes, como quitar o renombrar un campo, cambiar su tipo, hacer obligatorio un parámetro o cambiar el significado de un código.
  - Referencia: <https://martinfowler.com/bliki/TolerantReader.html>
- **Clave de idempotencia** (Idempotency-Key). *Técnica.* Identificador único que el cliente envía con una petición no idempotente, como un POST de pago. El servidor guarda el resultado asociado a la clave y, si llega otra vez, devuelve el mismo en lugar de repetir la operación.
  - Usar cuando: El cliente puede reintentar una operación con efectos, como un cobro, después de un fallo de red.
  - Referencia: <https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/>
- **Concurrencia optimista** (If-Match, actualización condicional). *Técnica.* El cliente envía con If-Match el ETag de la versión que leyó, y el servidor solo aplica el cambio si sigue siendo la actual. Si no, responde 412 y el cliente vuelve a leer.
  - Usar cuando: Varios clientes pueden modificar el mismo recurso y no quieres que uno pise los cambios del otro.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9110.html#section-13.1.1>
- **Contrato primero** (contract-first, diseño guiado por el contrato). *Técnica.* Escribir y acordar la especificación OpenAPI antes que el código, y generar o validar la implementación a partir de ella. Lo contrario es generar el contrato desde el código.
  - Usar cuando: Varios equipos dependen de la API y quieren trabajar en paralelo.
  - Referencia: <https://spec.openapis.org/oas/latest.html>

## D

- **Deprecation y Sunset** (Deprecation, Sunset, cabecera Deprecation). *Protocolo.* Cabeceras de respuesta que anuncian que un recurso está obsoleto (Deprecation, RFC 9745) y cuándo dejará de responder (Sunset, RFC 8594).
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9745.html>

## G

- **gRPC**. *Herramienta.* Marco de llamadas a procedimiento remoto sobre HTTP/2. El contrato se define con Protocol Buffers, y admite llamadas unarias y streaming en cualquiera de los dos sentidos.
  - Usar cuando: Comunicación entre servicios internos con contratos estrictos, mucho tráfico o streaming.
  - No usar cuando: La API la consumen navegadores o terceros sin herramientas de gRPC.
  - Referencia: <https://grpc.io/docs/what-is-grpc/introduction/>

## L

- **Lector tolerante** (tolerant reader). *Patrón.* Cliente que solo lee los campos que necesita e ignora los desconocidos, para no romperse cuando la API añade información.
  - Referencia: <https://martinfowler.com/bliki/TolerantReader.html>

## M

- **Modelo de madurez de Richardson** (nivel de madurez). *Concepto.* Escala de Leonard Richardson, popularizada por Fowler, para valorar una API HTTP. Nivel 0, un único punto de entrada; nivel 1, recursos; nivel 2, métodos y códigos de HTTP; nivel 3, enlaces de hipermedia.
  - Referencia: <https://martinfowler.com/articles/richardsonMaturityModel.html>

## O

- **OpenAPI** (especificación OpenAPI, Swagger). *Herramienta.* Formato estándar, en YAML o JSON, para describir una API HTTP. Recoge rutas, parámetros, cuerpos, respuestas y esquemas, y se usa para documentar, validar y generar clientes y servidores.
  - Referencia: <https://spec.openapis.org/oas/latest.html>

## P

- **Paginación por cursor** (cursor, keyset, paginación por clave). *Técnica.* Paginación en la que cada página devuelve un cursor opaco con la posición del último elemento, y la siguiente continúa desde ahí. No se salta ni repite elementos si la colección cambia, a diferencia del desplazamiento.
  - Usar cuando: Colecciones grandes o que cambian a menudo, y listados infinitos.
  - No usar cuando: El usuario necesita saltar directamente a la página 37.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc8288.html>
- **Problem Details** (application/problem+json, detalles del problema). *Protocolo.* Formato estándar para los errores de una API HTTP (RFC 9457), con los campos type, title, status, detail e instance, más los miembros de extensión que necesite cada problema.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9457.html>
- **Protocol Buffers** (protobuf, .proto). *Herramienta.* Lenguaje de definición de esquemas y formato binario de serialización. Cada campo tiene un número que lo identifica en el mensaje, y por eso los números no se reutilizan.
  - Referencia: <https://protobuf.dev/programming-guides/proto3/>

## R

- **Recurso** (recursos). *Concepto.* Cualquier cosa con identidad propia que una API expone con una URI, como un producto, un pedido o la colección de pedidos de un cliente. Los métodos HTTP actúan sobre él.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9110.html#section-3.1>
- **REST** (Representational State Transfer, RESTful). *Concepto.* Estilo de arquitectura descrito por Roy Fielding en su tesis de 2000. Recursos identificados por URI, interfaz uniforme, comunicación sin estado, respuestas que se pueden cachear y enlaces entre representaciones.
  - Referencia: <https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm>
