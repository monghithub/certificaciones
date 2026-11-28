# Glosario: Keycloak

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## A

- **Acción requerida** (acciones requeridas, required actions). *Concepto.* Tarea que el usuario debe completar en su siguiente inicio de sesión, como verificar el correo, actualizar la contraseña o configurar un segundo factor.
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html>

## C

- **Client scope** (client scopes). *Concepto.* Conjunto reutilizable de mapeadores y roles que se asocia a uno o varios clientes, y que determina qué claims y roles van en sus tokens.
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html>
- **Cliente de Keycloak** (clientId). *Concepto.* Aplicación o servicio registrado en un realm que puede pedir tokens o recibirlos. Se configura como público o confidencial y con los flujos que tiene permitidos.
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html>

## F

- **Federación de usuarios** (user federation, LDAP). *Técnica.* Conectar Keycloak a un directorio existente (LDAP o Active Directory) para autenticar y sincronizar usuarios sin migrarlos.
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html#_user-storage-federation>

## G

- **Grupo** (grupos). *Concepto.* Conjunto de usuarios al que se asignan roles y atributos; los miembros los heredan. Facilita gestionar permisos por equipos en lugar de usuario a usuario.
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html>

## I

- **Intermediación de identidad** (identity brokering, proveedor de identidad externo). *Técnica.* Permitir que los usuarios inicien sesión en Keycloak con otro proveedor (Google, Microsoft Entra ID, otro Keycloak) mediante OIDC o SAML.
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html#_identity_broker>

## K

- **Keycloak**. *Herramienta.* Servidor de gestión de identidades y accesos de código abierto que implementa OpenID Connect, OAuth 2.0 y SAML: inicio de sesión único, usuarios, roles, federación y proveedores externos.
  - Referencia: <https://www.keycloak.org/documentation>

## M

- **Mapeador de audiencia** (oidc-audience-mapper, audience mapper). *Técnica.* Mapeador que añade un cliente al claim aud del token de acceso, para que la API que valida la audiencia lo acepte.
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html#_audience>
- **Mapeador de protocolo** (mapeadores, protocol mapper, mapper). *Concepto.* Regla que añade o transforma claims en los tokens (atributos de usuario, grupos, audiencias, roles).
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html>
- **Modo de desarrollo** (start-dev). *Concepto.* Arranque de Keycloak con valores cómodos para pruebas: HTTP habilitado, resolución de hostname no estricta y base de datos dev-file. No sirve para producción.
  - Referencia: <https://www.keycloak.org/server/configuration>

## R

- **Realm** (realms). *Concepto.* Espacio aislado de Keycloak con sus propios usuarios, clientes, roles y configuración. El realm master está reservado para administrar Keycloak.
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html>
- **Rol de cliente** (roles de cliente, resource_access). *Concepto.* Rol definido dentro de un cliente concreto, normalmente la API que lo comprueba. En los tokens aparece en resource_access.<cliente>.roles.
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html>
- **Rol de realm** (roles de realm, realm_access). *Concepto.* Rol global del realm. En los tokens de acceso aparece en el claim realm_access.roles.
  - Referencia: <https://www.keycloak.org/docs/latest/server_admin/index.html>

## S

- **Servidor de recursos de Spring Security** (oauth2ResourceServer, resource server). *Herramienta.* Soporte de Spring Security para APIs que aceptan tokens Bearer: valida firma, emisor, caducidad y audiencia de los JWT, y convierte sus claims en autoridades.
  - Referencia: <https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html>
