# Glosario: Spring Boot en profundidad

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## A

- **Actuator** (Spring Boot Actuator, /actuator/health). *Herramienta.* Módulo que añade endpoints de operación (salud, métricas, información). Por web solo se exponen los que se indiquen.
  - Referencia: <https://docs.spring.io/spring-boot/reference/actuator/endpoints.html>
- **Autoconfiguración** (auto-configuration, autoconfiguraciones). *Concepto.* Configuración que Spring Boot aplica según lo que hay en el classpath y en las propiedades (por ejemplo, un DataSource si hay un controlador de base de datos), y que se retira si defines tu propio bean.
  - Referencia: <https://docs.spring.io/spring-boot/reference/using/auto-configuration.html>
- **Autoinvocación** (self-invocation). *Concepto.* Llamada de un método de un bean a otro método del mismo bean. No pasa por el proxy, así que anotaciones como @Transactional no se aplican.
  - Referencia: <https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html>

## B

- **Bean Validation** (Valid, NotBlank, Jakarta Validation). *Herramienta.* Especificación para declarar restricciones con anotaciones (@NotBlank, @DecimalMin) y validarlas; Spring la aplica a los cuerpos de las peticiones marcados con @Valid.
  - Referencia: <https://docs.spring.io/spring-boot/reference/io/validation.html>

## M

- **MockMvcTester**. *Herramienta.* Cliente de pruebas de Spring con aserciones de AssertJ para lanzar peticiones a los controladores sin servidor real.
  - Referencia: <https://docs.spring.io/spring-framework/reference/testing/mockmvc/assertj.html>

## P

- **Perfil** (perfiles, profiles, spring.profiles.active). *Concepto.* Conjunto de configuración que se activa según el entorno (dev, prod), con ficheros como application-prod.yml.
  - Referencia: <https://docs.spring.io/spring-boot/reference/features/profiles.html>
- **Problem Details** (ProblemDetail, application/problem+json, RFC 9457). *Protocolo.* Formato estándar (RFC 9457) para describir errores de una API HTTP en JSON, con type, title, status, detail e instance.
  - Referencia: <https://www.rfc-editor.org/rfc/rfc9457>
- **Propiedades tipadas** (@ConfigurationProperties, ConfigurationProperties). *Técnica.* Vincular un grupo de propiedades de configuración (tienda.*) a una clase o record, con validación, en lugar de leerlas una a una con @Value.
  - Referencia: <https://docs.spring.io/spring-boot/reference/features/external-config.html>
- **Proxy de Spring** (proxy, SpringCGLIB). *Concepto.* Objeto que Spring pone delante de un bean para añadir comportamiento (transacciones, seguridad, caché) a las llamadas que recibe desde fuera.
  - Referencia: <https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html>
- **Prueba por capa** (test slice, @WebMvcTest, @DataJpaTest). *Técnica.* Prueba que arranca solo la parte de la aplicación necesaria para una capa (la web o la persistencia), más rápida que levantar todo el contexto con @SpringBootTest.
  - Referencia: <https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html>

## S

- **Spring Boot**. *Herramienta.* Proyecto que facilita crear aplicaciones con Spring listas para producción, con dependencias agrupadas en starters, autoconfiguración, servidor web integrado y funciones de operación (Actuator).
  - Referencia: <https://docs.spring.io/spring-boot/reference/using/auto-configuration.html>
- **Spring Data JPA** (JpaRepository, consultas derivadas). *Herramienta.* Módulo que genera repositorios JPA a partir de interfaces; las consultas se pueden derivar del nombre del método, como findByPrecioLessThan.
  - Referencia: <https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html>
- **Starter** (starters). *Herramienta.* Dependencia que agrupa lo necesario para una tecnología (por ejemplo, spring-boot-starter-webmvc). En Spring Boot 4, cada starter tiene un compañero de pruebas (…-test).
  - Referencia: <https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide>

## T

- **Transactional** (@Transactional). *Herramienta.* Anotación que hace que un método se ejecute en una transacción. Spring la aplica con un proxy, así que solo funciona en llamadas que pasan por él, no en la autoinvocación.
  - Referencia: <https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html>
