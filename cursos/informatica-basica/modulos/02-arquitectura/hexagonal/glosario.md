# Glosario: Arquitectura hexagonal (puertos y adaptadores)

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 22 términos.

## A

- **Actor primario** (actores primarios). *Concepto.* Quien pone en marcha a la aplicación para que haga una de sus funciones (un usuario, otro programa, una prueba). Cockburn toma el término de los casos de uso; entra por los puertos de entrada.
  - Referencia: <https://alistair.cockburn.us/hexagonal-architecture/>
- **Actor secundario** (actores secundarios). *Concepto.* Sistema al que la aplicación pone en marcha, para obtener una respuesta o solo para notificarle (una base de datos, un servicio de correo). Se alcanza por los puertos de salida.
  - Referencia: <https://alistair.cockburn.us/hexagonal-architecture/>
- **Adaptador** (adaptadores). *Concepto.* Pieza que traduce entre un puerto y una tecnología concreta (HTTP, SQL, una cola de mensajes, un fichero). Puede haber varios adaptadores para el mismo puerto.
  - Referencia: <https://alistair.cockburn.us/hexagonal-architecture/>
- **Adaptador de entrada** (adaptadores de entrada, adaptador primario). *Concepto.* Adaptador que recibe una petición de una tecnología (un controlador REST, un consumidor de mensajes, una línea de comandos), la traduce y llama a un puerto de entrada. No contiene reglas de negocio.
  - Referencia: <https://alistair.cockburn.us/hexagonal-architecture/>
- **Adaptador de salida** (adaptadores de salida, adaptador secundario). *Concepto.* Adaptador que implementa un puerto de salida con una tecnología concreta, por ejemplo un repositorio JPA o un cliente HTTP.
  - Referencia: <https://alistair.cockburn.us/hexagonal-architecture/>
- **Arquitectura cebolla** (Onion Architecture). *Patrón.* Variante descrita por Jeffrey Palermo en 2008, con el modelo de dominio en el centro y anillos de servicios a su alrededor; comparte con hexagonal la regla de que las dependencias apuntan hacia el centro.
  - Referencia: <https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/>
- **Arquitectura en capas** (arquitectura de tres capas, capas tradicionales). *Patrón.* Organización en capas apiladas (presentación, negocio, datos) en la que cada capa usa la de debajo. En su forma clásica, el negocio depende de la capa de datos.
  - Referencia: <https://martinfowler.com/bliki/PresentationDomainDataLayering.html>
- **Arquitectura hexagonal** (puertos y adaptadores, Ports and Adapters, hexagonal). *Patrón.* Estilo de arquitectura, descrito por Alistair Cockburn en 2005, que separa la aplicación de su entorno con puertos (interfaces definidas por la aplicación) y adaptadores (traducciones a cada tecnología), de modo que pueda funcionar igual con usuarios, programas, pruebas o scripts, y sin su base de datos real.
  - Usar cuando: La lógica de negocio tiene peso propio, va a vivir años o tiene que probarse sin infraestructura.
  - No usar cuando: La aplicación es un CRUD fino sobre una base de datos, un script de un solo uso o un prototipo que se va a tirar.
  - Referencia: <https://alistair.cockburn.us/hexagonal-architecture/>

## C

- **Caso de uso** (casos de uso, servicio de aplicación). *Concepto.* Operación que la aplicación ofrece (reservar, cancelar, consultar). Orquesta el trabajo (carga, pide al dominio que decida, guarda, notifica), pero no decide las reglas de negocio.
  - Referencia: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
- **Clean Architecture** (arquitectura limpia). *Patrón.* Síntesis de Robert C. Martin (2012) de hexagonal, cebolla y otras: círculos concéntricos (entidades, casos de uso, adaptadores de interfaz, frameworks) y una regla de dependencias hacia dentro.
  - Referencia: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>

## D

- **Doble de prueba** (dobles de prueba, test double, stub, mock, fake). *Técnica.* Objeto que sustituye a una dependencia real en una prueba. Hay varios tipos (dummy, stub, spy, mock y fake), según lo que simulen y lo que comprueben.
  - Referencia: <https://martinfowler.com/bliki/TestDouble.html>
- **Dominio** (modelo de dominio). *Concepto.* Parte del código que representa los conceptos y las reglas del negocio. En hexagonal no depende de frameworks, bases de datos ni protocolos.
  - Referencia: <https://martinfowler.com/bliki/AnemicDomainModel.html>

## E

- **Entidad** (entidades). *Concepto.* Objeto del dominio con identidad propia que se mantiene aunque cambien sus datos (una sala, un pedido).
  - Referencia: <https://martinfowler.com/bliki/ValueObject.html>

## I

- **Inversión de dependencias** (principio de inversión de dependencias, DIP). *Concepto.* Principio según el cual los módulos de alto nivel no dependen de los de bajo nivel, sino ambos de abstracciones. En hexagonal, la aplicación define la interfaz (el puerto) y la infraestructura la implementa.
  - Referencia: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
- **Inyección de dependencias** (inyección por constructor). *Técnica.* Técnica en la que un objeto recibe sus colaboradores desde fuera (normalmente por el constructor) en lugar de crearlos él. Permite sustituir un adaptador por otro, por ejemplo en las pruebas.
  - Referencia: <https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html>

## M

- **Modelo anémico** (modelo de dominio anémico, anemic domain model). *Concepto.* Antipatrón en el que las clases del dominio solo tienen datos (getters y setters) y las reglas de negocio viven en servicios. Pierde la principal ventaja de tener un modelo de dominio.
  - Referencia: <https://martinfowler.com/bliki/AnemicDomainModel.html>

## O

- **Objeto valor** (objetos valor, value object). *Patrón.* Objeto que se define por sus atributos y no por una identidad, y que normalmente es inmutable (una franja horaria, un importe). Dos objetos valor con los mismos datos son iguales.
  - Usar cuando: Un concepto del negocio tiene reglas propias de validez o de comparación.
  - No usar cuando: El objeto tiene identidad propia y cambia con el tiempo; entonces es una entidad.
  - Referencia: <https://martinfowler.com/bliki/ValueObject.html>

## P

- **Puerto** (puertos). *Concepto.* Interfaz que define la aplicación para conversar con el exterior con un propósito concreto. La escribe la aplicación, con su vocabulario, y no depende de ninguna tecnología.
  - Referencia: <https://alistair.cockburn.us/hexagonal-architecture/>
- **Puerto de entrada** (puertos de entrada, puerto primario, driving port). *Concepto.* Puerto por el que el exterior pide algo a la aplicación (por ejemplo, «reservar una sala»). Lo implementa la aplicación y lo invocan los adaptadores de entrada.
  - Referencia: <https://alistair.cockburn.us/hexagonal-architecture/>
- **Puerto de salida** (puertos de salida, puerto secundario, driven port). *Concepto.* Puerto por el que la aplicación pide algo al exterior (guardar datos, notificar, consultar otro servicio). Lo define la aplicación y lo implementa un adaptador de salida.
  - Referencia: <https://alistair.cockburn.us/hexagonal-architecture/>

## R

- **Raíz de composición** (arranque, composition root). *Patrón.* Único lugar del programa donde se crean los adaptadores y se conectan con los casos de uso. En Spring Boot suele ser una clase de configuración con métodos @Bean.
  - Referencia: <https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html>
- **Regla de dependencias**. *Concepto.* Las dependencias del código solo apuntan hacia dentro, de la infraestructura a la aplicación y de la aplicación al dominio. Nada de dentro conoce a nada de fuera.
  - Referencia: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
