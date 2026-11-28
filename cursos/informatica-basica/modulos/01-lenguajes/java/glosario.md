# Glosario: Java moderno (17 a 25)

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 14 términos.

## B

- **Bloque de texto** (bloques de texto, text blocks). *Lenguaje.* Literal de cadena de varias líneas delimitado por tres comillas (JEP 378, Java 15), útil para JSON, SQL o HTML.
  - Referencia: <https://openjdk.org/jeps/378>

## C

- **Característica preliminar** (preview, --enable-preview). *Concepto.* Funcionalidad completa pero no definitiva que se publica para recoger opiniones; hay que activarla con --enable-preview y puede cambiar o desaparecer.
  - Referencia: <https://openjdk.org/jeps/12>
- **Clase sellada** (clases selladas, sealed, permits). *Lenguaje.* Clase o interfaz que declara qué tipos pueden extenderla o implementarla (JEP 409, Java 17). El compilador conoce todas las variantes.
  - Referencia: <https://openjdk.org/jeps/409>
- **Coincidencia de patrones** (pattern matching). *Lenguaje.* Comprobar la forma de un valor y extraer sus partes en un solo paso, con instanceof (JEP 394), switch (JEP 441) y patrones de record (JEP 440).
  - Referencia: <https://openjdk.org/jeps/441>
- **Colecciones secuenciadas** (SequencedCollection, sequenced collections). *Lenguaje.* Interfaces (JEP 431, Java 21) para colecciones con orden definido, con métodos comunes como getFirst, getLast y reversed.
  - Referencia: <https://openjdk.org/jeps/431>

## E

- **Expresión switch** (switch expressions). *Lenguaje.* switch que devuelve un valor, con etiquetas case -> sin caídas entre casos (JEP 361, Java 14). Con tipos sellados, el compilador exige cubrir todos los casos.
  - Referencia: <https://openjdk.org/jeps/361>

## F

- **Fichero fuente compacto** (ficheros compactos, compact source files, void main()). *Lenguaje.* Programa sin declarar la clase, con un método main de instancia (JEP 512, Java 25), pensado para empezar a programar y para scripts.
  - Referencia: <https://openjdk.org/jeps/512>

## H

- **Hilos virtuales** (hilo virtual, virtual threads). *Concepto.* Hilos ligeros gestionados por la JVM (JEP 444, Java 21) que permiten millones de tareas concurrentes que pasan la mayor parte del tiempo esperando E/S, con código bloqueante normal.
  - Usar cuando: Muchas tareas concurrentes que esperan E/S, como peticiones de un servidor.
  - No usar cuando: Tareas largas intensivas de CPU; no se deben reunir en pools.
  - Referencia: <https://docs.oracle.com/en/java/javase/25/core/virtual-threads.html>

## J

- **JEP** (JDK Enhancement Proposal, JEPs). *Concepto.* Propuesta de mejora del JDK. Cada cambio importante del lenguaje o la plataforma se describe y sigue en un JEP numerado en openjdk.org.
  - Referencia: <https://openjdk.org/jeps/0>

## L

- **LTS** (Long-Term Support, soporte a largo plazo). *Concepto.* Versión con soporte prolongado. Las LTS de Java son la 8, 11, 17, 21 y 25, y Oracle prevé una cada dos años (la siguiente, Java 29 en septiembre de 2027).
  - Referencia: <https://www.oracle.com/java/technologies/java-se-support-roadmap.html>

## P

- **Patrón de record** (record patterns, deconstrucción). *Lenguaje.* Patrón que descompone un record en sus componentes, por ejemplo case Tarjeta(var numero, var importe) (JEP 440, Java 21).
  - Referencia: <https://openjdk.org/jeps/440>

## R

- **Record** (records). *Lenguaje.* Clase inmutable y transparente para datos (JEP 395, Java 16): el compilador genera constructor, accesores, equals, hashCode y toString a partir de sus componentes.
  - Referencia: <https://openjdk.org/jeps/395>

## S

- **Stream gatherers** (Gatherers, gather). *Lenguaje.* Operaciones intermedias personalizadas para streams (JEP 485, Java 24), con gatherers predefinidos como windowFixed.
  - Referencia: <https://openjdk.org/jeps/485>

## V

- **var**. *Lenguaje.* Inferencia de tipo para variables locales (JEP 286, Java 10): el compilador deduce el tipo a partir del valor inicial.
  - Referencia: <https://openjdk.org/jeps/286>
