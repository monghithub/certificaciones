# Glosario: Estilos de arquitectura comparados

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 12 términos.

## A

- **ArchUnit**. *Herramienta.* Biblioteca de Java para escribir pruebas que comprueban reglas de arquitectura, como dependencias entre paquetes o capas.
  - Referencia: <https://www.archunit.org/userguide/html/000_Index.html>
- **Arquitectura cebolla** (onion architecture). *Patrón.* Estilo de Jeffrey Palermo (2008) con el modelo de dominio en el centro y capas concéntricas, en el que todo el acoplamiento apunta hacia el centro.
  - Referencia: <https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/>
- **Arquitectura en capas** (layered architecture, capas). *Patrón.* Organización en capas horizontales (presentación, lógica de negocio, acceso a datos) en la que cada capa solo depende de las inferiores.
  - Referencia: <https://martinfowler.com/bliki/PresentationDomainDataLayering.html>
- **Arquitectura limpia** (clean architecture). *Patrón.* Estilo de Robert C. Martin (2012) con círculos concéntricos (entidades, casos de uso, adaptadores de interfaz, frameworks y drivers) y la regla de que las dependencias solo apuntan hacia dentro.
  - Referencia: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
- **Atributo de calidad** (quality attribute, ISO 25010). *Concepto.* Característica no funcional que se busca en un sistema, como la mantenibilidad, el rendimiento, la fiabilidad o la seguridad; la norma ISO/IEC 25010 las clasifica.
  - Referencia: <https://iso25000.com/en/iso-25000-standards/iso-25010>

## E

- **Estilo de arquitectura** (architectural style). *Concepto.* Conjunto de reglas sobre cómo se reparten las responsabilidades de un sistema y en qué dirección pueden ir sus dependencias, con unas ventajas y unos costes conocidos.
  - Referencia: <https://martinfowler.com/architecture/>

## F

- **Función de aptitud** (fitness function). *Técnica.* Comprobación automática y repetible de una característica de la arquitectura (límites, rendimiento, dependencias) que se ejecuta, por ejemplo, en la CI.
  - Referencia: <https://www.thoughtworks.com/radar/techniques/architectural-fitness-function>

## I

- **import-linter** (contratos de importación). *Herramienta.* Herramienta de Python que comprueba contratos sobre las importaciones entre paquetes, como capas o importaciones prohibidas.
  - Referencia: <https://import-linter.readthedocs.io/en/stable/>

## M

- **Monolito modular** (modular monolith, modulito). *Patrón.* Aplicación que se despliega como una unidad pero está dividida en módulos por contexto de negocio, con API públicas y detalles internos ocultos, y límites comprobados.
  - Referencia: <https://docs.spring.io/spring-modulith/reference/fundamentals.html>

## R

- **Registro de decisión de arquitectura** (ADR, architecture decision record). *Técnica.* Documento breve que recoge una decisión de arquitectura con su contexto, la decisión, su estado y sus consecuencias, guardado junto al código.
  - Referencia: <https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
- **Regla de dependencia** (dependency rule). *Concepto.* Las dependencias del código fuente solo pueden apuntar hacia dentro, hacia las políticas de más alto nivel; nada interior conoce lo exterior.
  - Referencia: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>

## S

- **Spring Modulith** (ApplicationModules). *Herramienta.* Proyecto de Spring que trata cada paquete de primer nivel como un módulo y verifica que no se usan tipos internos de otros módulos ni hay ciclos entre ellos.
  - Referencia: <https://docs.spring.io/spring-modulith/reference/verification.html>
