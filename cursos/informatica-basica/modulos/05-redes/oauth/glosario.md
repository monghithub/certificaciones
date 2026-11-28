# Glosario: OAuth 2.0 y OpenID Connect

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 16 términos.

## C

- **Cliente OAuth** (cliente público, cliente confidencial, clientes públicos, clientes confidenciales). *Concepto.* Aplicación que pide acceso a un recurso en nombre del usuario. Es confidencial si puede guardar un secreto (un backend) y pública si no puede (una SPA o una aplicación móvil).
  - Referencia: <https://www.rfc-editor.org/rfc/rfc6749>
- **Credenciales de cliente** (client credentials, client_credentials). *Técnica.* Flujo en el que un cliente confidencial obtiene un token en su propio nombre, sin usuario, autenticándose con su identificador y su secreto. Es el flujo de servicio a servicio.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc6749>

## F

- **Flujo implícito** (implicit grant, implicit). *Técnica.* Flujo antiguo en el que el token se devolvía directamente en la URL de redirección. El RFC 9700 indica que los clientes no deberían usarlo; se sustituye por el flujo de código con PKCE.
  - No usar cuando: En aplicaciones nuevas, nunca.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9700>

## I

- **ID token** (id_token). *Concepto.* JWT de OpenID Connect que dice al cliente quién se ha autenticado, cuándo y ante qué proveedor. Es para el cliente, no para enviarlo a las API.
  - Referencia: <https://openid.net/specs/openid-connect-core-1_0.html>
- **Introspección** (introspection). *Técnica.* Endpoint (RFC 7662) al que un servidor de recursos pregunta si un token sigue activo y qué datos tiene. Útil con tokens opacos o para detectar revocaciones.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc7662>

## J

- **JWKS** (JSON Web Key Set, jwks_uri). *Protocolo.* Conjunto de claves públicas del servidor de autorización, publicado en una URL, con el que las API validan la firma de los tokens.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc7517>
- **JWT** (JSON Web Token). *Protocolo.* Formato compacto (RFC 7519) de tres partes en base64url (cabecera, carga y firma) para transportar afirmaciones (claims) firmadas. La firma garantiza la integridad, no la confidencialidad.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc7519>

## O

- **OAuth 2.0** (OAuth). *Protocolo.* Marco de autorización (RFC 6749, 2012) que permite a una aplicación obtener acceso limitado a un recurso en nombre de su propietario, mediante tokens emitidos por un servidor de autorización, sin conocer su contraseña.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc6749>
- **OpenID Connect** (OIDC). *Protocolo.* Capa de identidad sobre OAuth 2.0 que permite a una aplicación autenticar al usuario y obtener información básica sobre él mediante un ID token y el endpoint userinfo.
  - Referencia: <https://openid.net/specs/openid-connect-core-1_0.html>

## P

- **PKCE** (Proof Key for Code Exchange, code_verifier, code_challenge). *Técnica.* Extensión (RFC 7636) del flujo de código en la que el cliente genera un secreto aleatorio por petición y envía su resumen al pedir el código; al canjearlo, demuestra que lo conoce. Impide que un código interceptado sirva a otro.
  - Usar cuando: Siempre en el flujo de código; el RFC 9700 lo exige a los clientes públicos.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc7636>

## R

- **Refresh token** (token de refresco, refresh_token). *Concepto.* Credencial de larga duración con la que el cliente obtiene nuevos tokens de acceso sin volver a pedir al usuario que inicie sesión.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc6749>
- **RFC 9700** (BCP 240, Best Current Practice for OAuth 2.0 Security). *Protocolo.* Buenas prácticas actuales de seguridad de OAuth 2.0 (enero de 2025): PKCE obligatorio para clientes públicos, no usar el flujo implícito y prohibir el de contraseña del propietario, entre otras.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9700>

## S

- **Scope** (scopes). *Concepto.* Indicador de qué acceso se pide (por ejemplo, pedidos:leer). En OpenID Connect, el scope openid activa la autenticación, y profile y email piden datos del usuario.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc6749>
- **Servidor de autorización** (authorization server, proveedor de identidad, IdP). *Concepto.* Servidor que autentica al usuario, obtiene su consentimiento y emite los tokens. Keycloak y Microsoft Entra ID son ejemplos.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc6749>
- **Servidor de recursos** (resource server). *Concepto.* Servidor que aloja los recursos protegidos (una API) y acepta peticiones con un token de acceso válido.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc6749>

## T

- **Token de acceso** (access token, access_token). *Concepto.* Credencial que el cliente presenta al servidor de recursos para acceder a una API. Suele durar minutos y expresa qué se puede hacer (scope) y para quién (audiencia).
  - Referencia: <https://www.rfc-editor.org/rfc/rfc6749>
