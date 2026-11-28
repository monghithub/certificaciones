# Glosario: Principios SOLID

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 16 términos.

## A

- **Acoplamiento**. *Métrica.* Grado en que un módulo depende de otros. Con un acoplamiento alto, un cambio en un módulo obliga a cambiar los que dependen de él.
  - Referencia: <https://en.wikipedia.org/wiki/Coupling_(computer_programming)>

## C

- **Code smell** (olor de código, code smells). *Concepto.* Síntoma superficial en el código que suele indicar un problema de diseño más profundo, como una clase enorme o un switch sobre tipos repetido en varios sitios.
  - Referencia: <https://martinfowler.com/bliki/CodeSmell.html>
- **Cohesión**. *Métrica.* Grado en que los elementos de un módulo están relacionados entre sí y sirven a un mismo propósito. Se busca alta cohesión y bajo acoplamiento.
  - Referencia: <https://en.wikipedia.org/wiki/Cohesion_(computer_science)>

## I

- **Interfaz** (interfaces). *Concepto.* Contrato que declara qué operaciones ofrece un tipo sin decir cómo se implementan. En Java es la palabra clave interface; en Python se expresa con clases abstractas (abc) o con protocolos (typing.Protocol).
  - Referencia: <https://docs.oracle.com/javase/tutorial/java/IandI/createinterface.html>
- **Inyección de dependencias** (inyección por constructor). *Técnica.* Técnica en la que un objeto recibe sus colaboradores desde fuera (normalmente por el constructor) en lugar de crearlos. Es una forma habitual de aplicar la inversión de dependencias, pero no son lo mismo.
  - Referencia: <https://en.wikipedia.org/wiki/Dependency_injection>

## P

- **Polimorfismo**. *Concepto.* Capacidad de tratar objetos de tipos distintos a través de una misma interfaz, de modo que cada uno responda a la misma llamada con su propio comportamiento.
  - Referencia: <https://en.wikipedia.org/wiki/Polymorphism_(computer_science)>
- **Postcondición** (postcondiciones). *Concepto.* Condición que una operación garantiza al terminar. Un subtipo no puede ofrecer postcondiciones más débiles que su tipo base.
  - Referencia: <https://en.wikipedia.org/wiki/Liskov_substitution_principle>
- **Precondición** (precondiciones). *Concepto.* Condición que debe cumplirse antes de llamar a una operación. Según Liskov, un subtipo no puede exigir precondiciones más fuertes que su tipo base.
  - Referencia: <https://en.wikipedia.org/wiki/Liskov_substitution_principle>
- **Principio abierto/cerrado** (OCP, abierto/cerrado). *Concepto.* Un módulo debe estar abierto a la extensión y cerrado a la modificación: se puede añadir comportamiento nuevo sin cambiar el código que ya funciona. Lo formuló Bertrand Meyer en 1988.
  - Usar cuando: Hay un punto de variación que crece con frecuencia (tipos de descuento, formatos de exportación).
  - No usar cuando: Se preparan extensiones para variaciones que no existen y quizá nunca existan.
  - Referencia: <https://blog.cleancoder.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html>
- **Principio de inversión de dependencias** (DIP, inversión de dependencias). *Concepto.* Los módulos de alto nivel no deben depender de los de bajo nivel; ambos deben depender de abstracciones. Y las abstracciones no deben depender de los detalles, sino los detalles de las abstracciones.
  - Referencia: <https://en.wikipedia.org/wiki/Dependency_inversion_principle>
- **Principio de responsabilidad única** (SRP, responsabilidad única). *Concepto.* Un módulo debe tener una, y solo una, razón para cambiar. Robert C. Martin lo precisa así: las peticiones de cambio de un módulo deben venir de un único actor, es decir, de una persona o un grupo con una misma función de negocio.
  - Usar cuando: Una clase mezcla código que cambia por peticiones de áreas distintas (cálculo, presentación, persistencia).
  - No usar cuando: Se trocea una clase en muchas diminutas sin que haya motivos de cambio distintos.
  - Referencia: <https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html>
- **Principio de segregación de interfaces** (ISP, segregación de interfaces). *Concepto.* Ningún cliente debe verse obligado a depender de métodos que no usa. Es preferible tener varias interfaces pequeñas y específicas a una grande y general.
  - Referencia: <https://en.wikipedia.org/wiki/Interface_segregation_principle>
- **Principio de sustitución de Liskov** (LSP, sustitución de Liskov). *Concepto.* Los objetos de un subtipo deben poder usarse donde se espera el tipo base sin que el programa deje de ser correcto. Barbara Liskov lo presentó en 1987 y lo formalizó con Jeannette Wing en 1994.
  - Referencia: <https://en.wikipedia.org/wiki/Liskov_substitution_principle>
- **Protocolo** (typing.Protocol, Protocol). *Lenguaje.* Tipo de Python que define una interfaz estructural: cualquier clase con los métodos indicados lo cumple, sin necesidad de heredar de él. Lo comprueban los verificadores de tipos estáticos.
  - Referencia: <https://docs.python.org/3/library/typing.html#typing.Protocol>

## S

- **SOLID**. *Concepto.* Acrónimo de cinco principios de diseño orientado a objetos (responsabilidad única, abierto/cerrado, sustitución de Liskov, segregación de interfaces e inversión de dependencias). Robert C. Martin los reunió en 2000 y Michael Feathers acuñó el acrónimo hacia 2004.
  - Referencia: <https://en.wikipedia.org/wiki/SOLID>

## Y

- **YAGNI** (You Aren't Gonna Need It). *Concepto.* Principio de la programación extrema: no añadir funcionalidad ni flexibilidad hasta que haga falta de verdad. Equilibra la tentación de aplicar SOLID por adelantado.
  - Referencia: <https://martinfowler.com/bliki/Yagni.html>
