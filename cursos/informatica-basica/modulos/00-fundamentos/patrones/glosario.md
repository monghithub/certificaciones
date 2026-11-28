# Glosario: Patrones de diseño esenciales

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 19 términos.

## A

- **Adapter** (adaptador). *Patrón.* Patrón estructural que envuelve un objeto con una interfaz incompatible para que encaje en la interfaz que espera el cliente.
  - Usar cuando: Hay que integrar una biblioteca o un sistema externo cuya interfaz no se puede cambiar.
  - Referencia: <https://refactoring.guru/design-patterns/adapter>
- **Ámbito singleton** (bean singleton, singleton scope, singleton lifetime). *Concepto.* Configuración de un contenedor de inyección de dependencias por la que crea una sola instancia de un componente y la inyecta a todos los que la piden. Es única por contenedor y por definición de bean, no por clase. No es el patrón Singleton: la clase no sabe que es única y se le llega por el constructor.
  - Usar cuando: Servicios sin estado, clientes de otros sistemas y pools; es el ámbito por defecto en Spring.
  - No usar cuando: Para objetos que guardan datos de una petición o de un usuario; ahí, ámbito request, prototype o un parámetro.
  - Referencia: <https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html>
- **Antipatrón** (antipatrones, anti-pattern). *Concepto.* Solución habitual a un problema que parece útil pero suele producir más problemas de los que resuelve, como el uso indiscriminado de Singleton o los objetos dios.
  - Referencia: <https://en.wikipedia.org/wiki/Anti-pattern>

## B

- **Builder** (constructor por pasos). *Patrón.* Patrón creacional que construye un objeto complejo paso a paso y valida el resultado al final, en lugar de usar un constructor con muchos parámetros.
  - Usar cuando: Un objeto tiene muchos atributos opcionales o reglas de validez entre ellos.
  - No usar cuando: El objeto tiene pocos atributos obligatorios; basta un constructor o un record.
  - Referencia: <https://refactoring.guru/design-patterns/builder>

## C

- **Command** (comando). *Patrón.* Patrón de comportamiento que convierte una petición en un objeto, de modo que se puede guardar, encolar, registrar o deshacer.
  - Usar cuando: Hace falta deshacer, encolar o registrar operaciones.
  - Referencia: <https://refactoring.guru/design-patterns/command>
- **Composición sobre herencia** (composition over inheritance). *Concepto.* Principio del libro de la GoF que aconseja preferir la composición de objetos a la herencia de clases para reutilizar comportamiento, porque acopla menos y permite cambiar las piezas en tiempo de ejecución.
  - Referencia: <https://en.wikipedia.org/wiki/Composition_over_inheritance>

## D

- **Decorator** (decorador). *Patrón.* Patrón estructural que añade comportamiento a un objeto envolviéndolo en otro con la misma interfaz. Los decoradores se pueden apilar.
  - Usar cuando: Hay que combinar comportamientos opcionales (caché, registro, compresión) sin una subclase para cada combinación.
  - Referencia: <https://refactoring.guru/design-patterns/decorator>

## F

- **Facade** (fachada). *Patrón.* Patrón estructural que ofrece una interfaz simple a un subsistema complejo.
  - Usar cuando: Los clientes solo necesitan unas pocas operaciones de un subsistema grande.
  - Referencia: <https://refactoring.guru/design-patterns/facade>
- **Factory Method** (método fábrica). *Patrón.* Patrón creacional que delega en un método la decisión de qué clase concreta instanciar, de modo que el cliente trabaja con una interfaz sin conocer la clase.
  - Usar cuando: El tipo concreto depende de un dato (formato, configuración) y no se quiere repartir esa decisión por el código.
  - No usar cuando: Solo hay una clase y no se prevé otra.
  - Referencia: <https://refactoring.guru/design-patterns/factory-method>

## G

- **Gang of Four** (GoF, banda de los cuatro). *Concepto.* Apodo de Erich Gamma, Richard Helm, Ralph Johnson y John Vlissides, autores de Design Patterns (1994), el catálogo de 23 patrones orientados a objetos.
  - Referencia: <https://en.wikipedia.org/wiki/Design_Patterns>

## H

- **Holder** (initialization-on-demand holder, idioma del holder). *Técnica.* Forma de escribir un Singleton perezoso y seguro con hilos en Java guardando la instancia en una clase interna estática. La JVM inicializa esa clase una sola vez y solo cuando se usa por primera vez.
  - Referencia: <https://en.wikipedia.org/wiki/Initialization-on-demand_holder_idiom>

## I

- **Inyección de dependencias** (dependency injection, DI). *Técnica.* Técnica en la que un objeto recibe sus colaboradores desde fuera, normalmente por el constructor, en lugar de crearlos o buscarlos él. Es la alternativa a Singleton: sigue habiendo una sola instancia, pero la dependencia es visible y sustituible.
  - Referencia: <https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html>

## O

- **Observer** (observador, publicación-suscripción). *Patrón.* Patrón de comportamiento en el que un objeto notifica a sus suscriptores cuando cambia, sin conocer qué hace cada uno.
  - Usar cuando: Varias partes deben reaccionar a un cambio y no se quiere que el origen dependa de ellas.
  - No usar cuando: El orden o la garantía de entrega importan mucho; entonces conviene un mecanismo explícito.
  - Referencia: <https://refactoring.guru/design-patterns/observer>

## P

- **Patrón de diseño** (patrones de diseño, patrón). *Concepto.* Solución general y reutilizable a un problema de diseño que se repite, descrita con un nombre, el problema, la solución y sus consecuencias. No es código para copiar, sino una plantilla que se adapta.
  - Referencia: <https://en.wikipedia.org/wiki/Design_Patterns>
- **Proxy**. *Patrón.* Patrón estructural que coloca un sustituto con la misma interfaz delante de un objeto para controlar el acceso a él (carga perezosa, permisos, llamadas remotas, caché).
  - Referencia: <https://refactoring.guru/design-patterns/proxy>

## R

- **Raíz de composición** (composition root). *Patrón.* Único lugar del programa donde se crean los objetos y se conectan entre sí, como el main o una clase @Configuration de Spring. Decide cuántas instancias hay de cada cosa, sin que las clases lo sepan.
  - Referencia: <https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html>

## S

- **Singleton**. *Patrón.* Patrón creacional en el que una clase garantiza que solo tiene una instancia y da un punto de acceso global a ella. El problema no es la instancia única, sino que la clase controle su propia creación y que el acceso estático oculte la dependencia, comparta estado entre pruebas e impida sustituirla.
  - Usar cuando: En objetos inmutables, recursos únicos del proceso, el logger o bibliotecas sin raíz de composición, escrito con enum o con holder.
  - No usar cuando: Para configuración, repositorios, clientes de otros servicios, el reloj o datos del usuario; ahí, una instancia única inyectada.
  - Referencia: <https://refactoring.guru/design-patterns/singleton>
- **Strategy** (estrategia). *Patrón.* Patrón de comportamiento que encapsula una familia de algoritmos intercambiables tras una interfaz común, para elegir uno en tiempo de ejecución.
  - Usar cuando: Hay varias formas de hacer lo mismo (calcular un precio, ordenar) que se eligen según el caso.
  - Referencia: <https://refactoring.guru/design-patterns/strategy>

## T

- **Template Method** (método plantilla). *Patrón.* Patrón de comportamiento en el que una clase base define el esqueleto de un algoritmo y deja que las subclases rellenen algunos pasos.
  - No usar cuando: Las variaciones son muchas o se combinan; Strategy con composición suele ser más flexible.
  - Referencia: <https://refactoring.guru/design-patterns/template-method>
