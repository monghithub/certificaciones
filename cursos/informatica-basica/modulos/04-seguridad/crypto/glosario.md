# Glosario: Criptografía aplicada

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## A

- **Acuerdo de claves** (Diffie-Hellman, X25519, ECDH). *Técnica.* Protocolo con el que dos partes obtienen el mismo secreto intercambiando solo sus claves públicas. TLS lo usa en cada conexión.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc7748.html>

## C

- **Cifrado autenticado** (AEAD, AES-GCM, ChaCha20-Poly1305). *Técnica.* Cifrado que además de ocultar el contenido detecta cualquier modificación, con una etiqueta de autenticación. AES-GCM y ChaCha20-Poly1305 son los habituales.
  - Usar cuando: Cifras datos con una clave simétrica; es la opción por defecto.
  - Referencia: <https://cryptography.io/en/latest/hazmat/primitives/aead/>
- **Criptografía de clave pública** (clave pública, clave privada, asimétrica). *Concepto.* Criptografía con un par de claves. La privada se guarda y la pública se reparte. Sirve para firmar, cifrar para alguien o acordar un secreto común sin haberlo compartido antes.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc8032.html>

## F

- **Firma digital** (firma, Ed25519). *Técnica.* Valor que solo puede calcular quien tiene la clave privada y que cualquiera puede comprobar con la pública. Demuestra el origen y que el mensaje no se ha modificado.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc8032.html>
- **Función hash** (hash, resumen, SHA-256). *Concepto.* Función que convierte cualquier dato en un resumen de tamaño fijo. Las criptográficas, como SHA-256, hacen inviable encontrar dos entradas con el mismo resumen o recuperar la entrada a partir de él.
  - Referencia: <https://csrc.nist.gov/pubs/fips/180-4/upd1/final>

## G

- **Generador aleatorio criptográfico** (CSPRNG, secrets). *Herramienta.* Generador de números aleatorios cuyas salidas no se pueden predecir. En Python es el módulo secrets; el módulo random no sirve para seguridad.
  - Referencia: <https://docs.python.org/3/library/secrets.html>
- **Gestión de secretos** (gestor de secretos, vault, rotación de secretos). *Técnica.* Guardar, repartir, auditar y rotar las contraseñas, claves y tokens de las aplicaciones fuera del código, con acceso mínimo y caducidad.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>

## H

- **Hash de contraseñas** (argon2id, bcrypt, scrypt). *Técnica.* Función deliberadamente lenta y con mucha memoria (argon2id, scrypt, bcrypt) para guardar contraseñas, de modo que probar millones de candidatas cueste caro.
  - Usar cuando: Guardas contraseñas de usuarios.
  - No usar cuando: Necesitas un resumen rápido de datos; para eso está SHA-256.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- **HMAC**. *Técnica.* Código de autenticación de mensajes calculado con una clave secreta compartida y una función hash. Lo comprueba quien tiene la misma clave; se usa en webhooks y en JWT con HS256.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc2104.html>

## J

- **JWT** (JSON Web Token). *Protocolo.* Token con una cabecera, una carga y una firma, codificadas en Base64URL. La carga se lee sin clave; la firma solo garantiza que nadie la ha modificado.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc8725.html>

## M

- **Modo ECB** (ECB). *Concepto.* Modo de cifrado por bloques que cifra cada bloque por separado, así que bloques iguales dan resultados iguales y se ven los patrones de los datos. No se debe usar.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html>

## N

- **Nonce** (IV, vector de inicialización). *Concepto.* Valor que se usa una sola vez con una misma clave. En AES-GCM, reutilizarlo revela la relación entre los mensajes y rompe la autenticación.
  - Referencia: <https://csrc.nist.gov/pubs/sp/800/38/d/final>

## S

- **Sal** (salt). *Concepto.* Valor aleatorio distinto para cada contraseña que se mezcla antes de calcular el hash. Hace que dos contraseñas iguales den hashes distintos e inutiliza las tablas precalculadas.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- **Solicitud de firma de certificado** (CSR). *Concepto.* Petición que se envía a una CA con la clave pública y los datos del certificado, firmada con la clave privada, que no sale del servidor.
  - Referencia: <https://docs.openssl.org/3.5/man1/openssl-req/>
