# Glosario: Microservicios: límites, integración y datos

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 13 términos.

## B

- **Base de datos por servicio** (database per service). *Patrón.* Cada servicio es dueño de sus datos y solo él accede a su base de datos; los demás los obtienen por su API o por eventos.
  - Referencia: <https://microservices.io/patterns/data/database-per-service.html>

## C

- **Clave de idempotencia** (Idempotency-Key). *Técnica.* Identificador único que el cliente envía con una operación para que, si la repite, el servidor no la ejecute dos veces y devuelva el resultado ya calculado.
  - Referencia: <https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/>
- **Composición de APIs** (API composition). *Patrón.* Resolver una consulta que necesita datos de varios servicios llamando a cada uno y combinando las respuestas.
  - Referencia: <https://microservices.io/patterns/data/api-composition.html>

## F

- **Fallo en cascada** (cascading failure). *Concepto.* Situación en la que la lentitud o caída de un servicio agota los recursos de los que lo llaman y se propaga por el sistema.
  - Referencia: <https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker>

## I

- **Interruptor** (circuit breaker). *Patrón.* Componente que, tras varios fallos, deja de llamar a un servicio durante un tiempo y falla al instante, para no esperar en vano ni empeorar su situación.
  - Referencia: <https://martinfowler.com/bliki/CircuitBreaker.html>

## L

- **Ley de Conway** (Conway's law). *Concepto.* Las organizaciones diseñan sistemas que reproducen su estructura de comunicación; por eso los límites de los servicios y de los equipos deben alinearse.
  - Referencia: <https://martinfowler.com/bliki/ConwaysLaw.html>

## M

- **Microservicio** (microservicios, arquitectura de microservicios). *Concepto.* Estilo en el que una aplicación es un conjunto de servicios pequeños, cada uno en su proceso, organizados por capacidades de negocio, desplegables de forma independiente y comunicados por mecanismos ligeros.
  - Referencia: <https://martinfowler.com/articles/microservices.html>
- **Monolito distribuido** (distributed monolith). *Concepto.* Sistema partido en servicios que, por estar muy acoplados, hay que desplegar y cambiar juntos: tiene los costes de la distribución sin sus ventajas.
  - Referencia: <https://martinfowler.com/bliki/MonolithFirst.html>

## P

- **Pasarela de API** (API gateway, BFF, backend for frontend). *Patrón.* Punto de entrada único que enruta las peticiones a los servicios y concentra funciones comunes como autenticación o límites; un BFF es una pasarela específica para un tipo de cliente.
  - Referencia: <https://microservices.io/patterns/apigateway.html>
- **Prima de los microservicios** (microservice premium). *Concepto.* Coste adicional de complejidad operativa y de desarrollo que exigen los microservicios y que solo compensa en sistemas suficientemente complejos.
  - Referencia: <https://martinfowler.com/bliki/MicroservicePremium.html>
- **Pruebas de contrato** (consumer-driven contracts, Pact). *Técnica.* Pruebas en las que el consumidor de una API define lo que espera y el proveedor verifica que lo cumple, para detectar cambios incompatibles sin desplegar todo junto.
  - Referencia: <https://docs.pact.io/>

## R

- **Reintento con espera exponencial** (retry, backoff, jitter). *Técnica.* Repetir una llamada fallida esperando cada vez más, con una variación aleatoria, para superar fallos transitorios sin saturar al servicio.
  - Referencia: <https://learn.microsoft.com/en-us/azure/architecture/patterns/retry>

## T

- **Tiempo de espera** (timeout). *Técnica.* Límite de lo que se espera una respuesta antes de abandonar; sin él, un servicio lento bloquea a quienes lo llaman.
  - Referencia: <https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/>
