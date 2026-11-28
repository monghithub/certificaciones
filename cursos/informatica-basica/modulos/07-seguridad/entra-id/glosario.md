# Glosario: Microsoft Entra ID para desarrolladores

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## C

- **Consentimiento** (consentimiento de administrador, admin consent). *Concepto.* Autorización que un usuario o un administrador da a una aplicación para usar unos permisos. Algunos permisos solo los puede conceder un administrador para toda la organización.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/permissions-consent-overview>

## E

- **Entidad de servicio** (service principal, entidades de servicio, aplicación empresarial). *Concepto.* Instancia local de una aplicación en un tenant concreto. Define qué puede hacer la aplicación en ese tenant: quién tiene acceso, qué permisos se le concedieron. Hay una en cada tenant donde se usa la aplicación.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals>

## F

- **Federación de identidades de carga de trabajo** (workload identity federation, credencial federada). *Técnica.* Configuración en la que un registro de aplicación o una identidad administrada confía en los tokens de otro proveedor (GitHub Actions, Kubernetes, Google), de modo que la carga de trabajo obtiene tokens de Entra ID sin guardar secretos.
  - Referencia: <https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation>

## I

- **Identidad administrada** (identidades administradas, managed identity, managed identities). *Concepto.* Identidad que Azure gestiona para un recurso (una máquina virtual, una app de App Service), sin credenciales que el desarrollador tenga que guardar ni rotar. Puede ser asignada por el sistema o por el usuario.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview>
- **Identificador de cliente** (client ID, application ID, appId). *Concepto.* GUID único global que identifica un registro de aplicación. Es el client_id de OAuth.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals>

## M

- **Microsoft Entra ID** (Entra ID, Azure AD, Azure Active Directory). *Herramienta.* Servicio de identidad y acceso en la nube de Microsoft, antes llamado Azure Active Directory. Microsoft lo renombró en 2023 manteniendo las URL de inicio de sesión, las API y las bibliotecas.
  - Referencia: <https://learn.microsoft.com/en-us/entra/fundamentals/new-name>
- **MSAL** (Microsoft Authentication Library). *Herramienta.* Bibliotecas de Microsoft para obtener tokens de Entra ID en .NET, Java, Python, JavaScript (Node, React, Angular), Android e iOS. Gestionan los flujos, la caché y la renovación de tokens.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/msal-overview>

## O

- **oid** (object ID). *Concepto.* Claim con el identificador inmutable del usuario o la entidad de servicio en el tenant; es el mismo para todas las aplicaciones del tenant, a diferencia de sub, que cambia por aplicación.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/access-token-claims-reference>

## P

- **Permiso de aplicación** (permisos de aplicación, application permission, app-only). *Concepto.* Permiso con el que la aplicación actúa por sí misma, sin usuario, en escenarios como procesos en segundo plano. Siempre requiere consentimiento de un administrador y aparece en el claim roles.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/permissions-consent-overview>
- **Permiso delegado** (permisos delegados, delegated permission, scp). *Concepto.* Permiso con el que la aplicación actúa en nombre de un usuario que ha iniciado sesión; solo accede a lo que el usuario podría. En el token aparece en el claim scp.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/permissions-consent-overview>

## R

- **Registro de aplicación** (registros de aplicación, app registration, objeto de aplicación). *Concepto.* Definición global de una aplicación en su tenant de origen: identificador de cliente, URI de redirección, credenciales, permisos que pide y API que expone.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals>
- **Rol de aplicación** (roles de aplicación, app roles, app role). *Concepto.* Rol definido en el registro de una aplicación o API, que se asigna a usuarios, grupos o entidades de servicio. Entra ID lo incluye en el claim roles del token.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/howto-add-app-roles-in-apps>

## S

- **Scope /.default** (.default). *Concepto.* Scope especial que pide todos los permisos ya configurados para un recurso. En el flujo de credenciales de cliente es obligatorio, por ejemplo, `https://graph.microsoft.com/.default`.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow>

## T

- **Tenant** (tenants, inquilino, tenant ID). *Concepto.* Instancia dedicada de Entra ID de una organización, con sus usuarios, grupos y aplicaciones. Se identifica con un GUID (tenant ID) que aparece en el claim tid.
  - Referencia: <https://learn.microsoft.com/en-us/entra/identity-platform/single-and-multi-tenant-apps>
