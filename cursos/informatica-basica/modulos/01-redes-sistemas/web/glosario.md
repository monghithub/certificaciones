# Glosario: HTTP y la web

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 17 términos.

## A

- **ALPN** (Application-Layer Protocol Negotiation). *Protocolo.* Extensión de TLS con la que cliente y servidor acuerdan, durante el saludo, qué protocolo de aplicación usarán sobre la conexión (h2 o http/1.1).
  - Referencia: <https://www.rfc-editor.org/rfc/rfc7301>

## C

- **Cache-Control**. *Protocolo.* Cabecera con las directivas que controlan si una respuesta se puede guardar en caché, durante cuánto tiempo y en qué cachés (max-age, no-cache, no-store, private, public…).
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9111#section-5.2>
- **Código de estado** (códigos de estado, status code). *Concepto.* Número de tres cifras de la respuesta que indica el resultado. La primera cifra da la clase, 1xx informativo, 2xx éxito, 3xx redirección, 4xx error del cliente y 5xx error del servidor.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9110#section-15>
- **Cookie** (cookies). *Protocolo.* Dato que el servidor pide guardar al navegador con Set-Cookie y que este reenvía en la cabecera Cookie de las peticiones siguientes. Da estado a un protocolo que no lo tiene.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc6265>
- **CORS** (Cross-Origin Resource Sharing). *Protocolo.* Protocolo, definido en el estándar Fetch, con el que un servidor indica mediante cabeceras qué otros orígenes pueden leer sus respuestas y con qué métodos y cabeceras.
  - Referencia: <https://fetch.spec.whatwg.org/#http-cors-protocol>

## E

- **ETag** (etiqueta de entidad). *Protocolo.* Identificador de una versión concreta de una representación. El cliente lo reenvía en If-None-Match, y el servidor responde 304 si no ha cambiado.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9110#section-8.8.3>

## H

- **HTTP** (Hypertext Transfer Protocol). *Protocolo.* Protocolo de aplicación sin estado basado en peticiones y respuestas. Su semántica (métodos, códigos de estado, cabeceras) es común a todas las versiones y se define en el RFC 9110.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9110>
- **HTTP/2**. *Protocolo.* Versión binaria de HTTP que multiplexa muchas peticiones como flujos dentro de una sola conexión TCP y comprime las cabeceras con HPACK. Se define en el RFC 9113.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9113>
- **HTTP/3**. *Protocolo.* HTTP sobre QUIC, un transporte sobre UDP con TLS 1.3 integrado. Evita que la pérdida de un paquete bloquee los demás flujos. Se define en el RFC 9114.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9114>

## I

- **Idempotencia** (idempotente, idempotentes). *Concepto.* Propiedad de un método por la que repetir la misma petición varias veces tiene el mismo efecto en el servidor que hacerla una vez. Son idempotentes los métodos seguros, PUT y DELETE; POST no lo es.
  - Usar cuando: Hay que decidir si un cliente puede reintentar automáticamente una petición que falló a medias.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9110#section-9.2.2>

## M

- **Método HTTP** (métodos HTTP, método, verbo HTTP). *Concepto.* La acción que pide la petición sobre el recurso, como GET, POST, PUT, DELETE o PATCH. Cada método tiene una semántica definida, y de ella depende si es seguro o idempotente.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9110#section-9>
- **Método seguro** (métodos seguros, seguro). *Concepto.* Método cuya semántica es de solo lectura, como GET, HEAD u OPTIONS. El cliente no pide ningún cambio en el servidor al usarlo.
  - Usar cuando: Lees un recurso; los navegadores, rastreadores y cachés pueden repetir la petición sin riesgo.
  - No usar cuando: La petición cambia estado; nunca debe hacerlo un GET.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9110#section-9.2.1>

## O

- **Origen** (origin, mismo origen). *Concepto.* La combinación de esquema, host y puerto de una URL. Dos URL son del mismo origen solo si coinciden en los tres.
  - Referencia: <https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy>

## P

- **Petición condicional** (peticiones condicionales, revalidación, revalidar). *Técnica.* Petición con una condición sobre el estado del recurso (If-None-Match, If-Modified-Since). Si la copia del cliente sigue valiendo, el servidor responde 304 Not Modified sin cuerpo.
  - Usar cuando: Una respuesta en caché ha caducado y quieres saber si sigue siendo válida sin descargarla otra vez.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9110#section-13>
- **Petición de verificación previa** (preflight, verificación previa). *Técnica.* Petición OPTIONS que el navegador envía antes de una petición entre orígenes que no es simple (otro método o cabeceras propias), para preguntar si el servidor la acepta.
  - Referencia: <https://fetch.spec.whatwg.org/#cors-preflight-fetch>
- **Política del mismo origen** (same-origin policy). *Concepto.* Regla de seguridad del navegador por la que el código de una página no puede leer las respuestas de otro origen salvo que este lo permita.
  - Referencia: <https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy>

## S

- **SameSite**. *Protocolo.* Atributo de cookie que decide si se envía en peticiones que vienen de otro sitio. Strict no la envía nunca desde otro sitio; Lax solo en navegaciones de nivel superior con métodos seguros; None siempre, y exige Secure.
  - Usar cuando: Proteges una cookie de sesión frente a CSRF; Lax es un buen punto de partida.
  - Referencia: <https://datatracker.ietf.org/doc/draft-ietf-httpbis-rfc6265bis/>
