# Glosario: Seguridad en aplicaciones web (OWASP)

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## A

- **Argon2id** (hash de contraseñas, bcrypt, scrypt). *Herramienta.* Función de derivación de claves lenta y con mucha memoria, recomendada por OWASP para guardar contraseñas; incluye una sal aleatoria en cada hash.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- **Atributos de cookie** (HttpOnly, Secure, SameSite). *Técnica.* Opciones de Set-Cookie que protegen la sesión: HttpOnly impide leerla desde JavaScript, Secure exige HTTPS y SameSite limita su envío desde otros sitios.
  - Referencia: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie>

## C

- **Cadena de suministro de software** (supply chain, pip-audit). *Concepto.* Todo lo que interviene en el software que se despliega además del código propio: dependencias, herramientas de compilación y tuberías. Sus fallos son la categoría A03 del Top 10:2025.
  - Referencia: <https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/>
- **Consulta parametrizada** (prepared statement, parámetros enlazados). *Técnica.* Consulta en la que los valores se envían aparte del texto SQL, con marcadores como ?, de modo que nunca se interpretan como código.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html>
- **Content Security Policy** (CSP). *Protocolo.* Cabecera HTTP que indica al navegador de qué orígenes puede cargar scripts y otros recursos, como defensa adicional contra XSS.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html>
- **CSRF** (cross-site request forgery). *Concepto.* Ataque que hace que el navegador de la víctima envíe una petición autenticada no deseada a otro sitio. Se mitiga con SameSite en las cookies y con tokens anti-CSRF.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>

## D

- **Defensa en profundidad** (defense in depth). *Concepto.* Varias capas de protección independientes, de modo que el fallo de una no deja el sistema expuesto.
  - Referencia: <https://owasp.org/Top10/2025/>

## F

- **Fallar cerrado** (fail closed, fail open, fallar abierto). *Concepto.* Ante un error inesperado en un control de seguridad, denegar el acceso en lugar de permitirlo.
  - Referencia: <https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/>

## I

- **IDOR** (referencia directa insegura a objetos). *Concepto.* Fallo de control de acceso en el que basta cambiar un identificador (/pedidos/2) para acceder a datos de otro usuario, porque el servidor no comprueba la propiedad.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html>
- **Inyección SQL** (SQL injection, SQLi). *Concepto.* Ataque en el que datos de entrada se interpretan como parte de la consulta SQL. Se evita con consultas parametrizadas.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html>

## O

- **OWASP Top 10**. *Concepto.* Lista de las diez categorías de riesgo más importantes en aplicaciones web, publicada por OWASP a partir de datos de vulnerabilidades reales. La edición vigente es la de 2025.
  - Referencia: <https://owasp.org/Top10/2025/>

## S

- **Sal** (salt). *Concepto.* Valor aleatorio distinto para cada contraseña que se combina con ella antes de calcular el hash, para que dos contraseñas iguales den hashes distintos.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>
- **SSRF** (falsificación de peticiones del lado del servidor). *Concepto.* Ataque en el que se consigue que el servidor haga peticiones a destinos elegidos por el atacante, como servicios internos. En el Top 10:2025 forma parte de A01.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html>

## X

- **XSS** (cross-site scripting). *Concepto.* Ataque en el que se inyecta código JavaScript en una página que verán otros usuarios. Se evita escapando la salida según el contexto y con CSP.
  - Referencia: <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>
