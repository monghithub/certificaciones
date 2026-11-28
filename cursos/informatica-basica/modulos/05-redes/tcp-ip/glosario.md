# Glosario: TCP/IP, DNS y TLS

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 17 términos.

## A

- **Autoridad de certificación** (CA, autoridades de certificación, cadena de confianza). *Concepto.* Entidad que firma certificados. El cliente confía en un conjunto de raíces y acepta un certificado si puede construir una cadena de firmas, a través de intermedios, hasta una de ellas.
  - Referencia: <https://letsencrypt.org/certificates/>

## C

- **Certificado X.509** (certificado, certificados). *Concepto.* Documento firmado que vincula una clave pública con unos nombres (en la extensión Subject Alternative Name), con un periodo de validez y la firma de quien lo emite.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc5280.html>
- **CIDR** (notación CIDR, prefijo de red). *Concepto.* Notación que indica una red con su dirección y el número de bits fijos del prefijo. 192.168.1.0/24 son las 256 direcciones de 192.168.1.0 a 192.168.1.255.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc4632.html>

## D

- **Dirección IP** (direcciones IP, IPv4, IPv6). *Concepto.* Identificador de una interfaz de red. IPv4 usa 32 bits (192.168.1.10) e IPv6, 128 bits (2a04:4e42:600::347).
  - Referencia: <https://www.rfc-editor.org/rfc/rfc791.html>
- **DNS** (Domain Name System, sistema de nombres de dominio). *Protocolo.* Base de datos distribuida y jerárquica que traduce nombres (curl.se) a datos como direcciones IP. La raíz delega en los dominios de primer nivel y estos en los servidores autoritativos de cada dominio.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc1034.html>

## M

- **Modelo TCP/IP** (pila TCP/IP, capas de red). *Concepto.* Organización de las redes en capas, cada una apoyada en la de debajo. Enlace (Ethernet, wifi), internet (IP), transporte (TCP, UDP, QUIC) y aplicación (HTTP, DNS).
  - Referencia: <https://www.rfc-editor.org/rfc/rfc1122.html>

## N

- **NAT** (traducción de direcciones). *Técnica.* Traducción que hace un router entre direcciones privadas de una red interna y su dirección pública, para que muchos equipos compartan una sola IP pública.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc1918.html>

## P

- **Puerto** (puertos). *Concepto.* Número de 16 bits que identifica, dentro de un equipo, a qué proceso va una conexión TCP o un datagrama UDP. Un servidor escucha en un puerto conocido (443 para HTTPS).
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9293.html>

## R

- **Registro DNS** (registros DNS, registro A, registro CNAME). *Concepto.* Cada dato asociado a un nombre, con su tipo y su TTL. A (IPv4), AAAA (IPv6), CNAME (alias de otro nombre), MX (correo), TXT (texto), NS (servidores autoritativos).
  - Referencia: <https://www.rfc-editor.org/rfc/rfc1035.html#section-3.2.2>
- **Resolvedor recursivo** (resolvedor, resolver). *Concepto.* Servidor DNS que hace por el cliente todas las consultas, desde la raíz hasta el servidor autoritativo, y guarda las respuestas en caché durante su TTL.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc1034.html#section-2.4>

## S

- **Saludo en tres pasos** (three-way handshake, SYN, SYN-ACK, ACK). *Concepto.* Intercambio SYN, SYN-ACK y ACK con el que se abre una conexión TCP. Cuesta un viaje de ida y vuelta antes de poder enviar datos.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9293.html#section-3.5>
- **SNI** (Server Name Indication). *Protocolo.* Extensión de TLS con la que el cliente indica el nombre del servidor al que quiere llegar, para que una misma IP pueda servir varios sitios con certificados distintos.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc6066.html#section-3>

## T

- **TCP** (Transmission Control Protocol). *Protocolo.* Protocolo de transporte orientado a conexión que entrega un flujo de bytes fiable y en orden, con control de flujo y de congestión. Se define en el RFC 9293.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9293.html>
- **TIME_WAIT**. *Concepto.* Estado en el que queda durante un tiempo el extremo que cierra primero una conexión TCP, para que los paquetes retrasados de esa conexión no se confundan con los de una nueva.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9293.html#section-3.6>
- **TLS** (Transport Layer Security, TLS 1.3). *Protocolo.* Protocolo que cifra y autentica una conexión. En el saludo, el servidor demuestra su identidad con un certificado y ambos extremos acuerdan las claves. La versión actual es TLS 1.3 (RFC 8446).
  - Referencia: <https://www.rfc-editor.org/rfc/rfc8446.html>
- **TTL** (tiempo de vida). *Concepto.* Segundos durante los que un resolvedor puede guardar en caché un registro DNS. Un TTL alto ahorra consultas, pero retrasa la propagación de un cambio.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc1035.html#section-3.2.1>

## U

- **UDP** (User Datagram Protocol). *Protocolo.* Protocolo de transporte sin conexión. Envía datagramas independientes sin saludo, sin garantía de entrega ni de orden. Lo usan DNS y QUIC.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc768.html>
