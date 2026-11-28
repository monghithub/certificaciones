# Glosario: Código limpio y refactorización

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 19 términos.

## C

- **Cláusula de guarda** (cláusulas de guarda, guard clause). *Técnica.* Comprobación al principio de una función que sale en cuanto se cumple un caso especial. Sustituye a los condicionales anidados y deja el caso normal sin sangrar.
  - Referencia: <https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html>
- **Código heredado** (legacy code, código legado). *Concepto.* Para Michael Feathers, el código sin pruebas, sea antiguo o no. Cambiarlo es arriesgado porque nada avisa si se rompe el comportamiento.
  - Referencia: <https://en.wikipedia.org/wiki/Characterization_test>
- **Código limpio** (clean code). *Concepto.* Código que otra persona entiende y cambia con poco esfuerzo y poco riesgo. No es un estilo concreto, sino una propiedad que se mide por lo que cuesta modificarlo.
  - Usar cuando: Siempre que el código vaya a leerse o cambiarse más de una vez, que es casi siempre.
  - No usar cuando: En un prototipo que se va a tirar, pulirlo no compensa; si sobrevive, deja de ser un prototipo.
  - Referencia: <https://martinfowler.com/bliki/TechnicalDebt.html>
- **Complejidad ciclomática** (complejidad de McCabe, McCabe). *Métrica.* Número de caminos independientes de una función. Se calcula sumando uno al número de puntos de decisión (if, bucles, operadores lógicos). Cuanto más alta, más casos hay que entender y probar.
  - Referencia: <https://docs.astral.sh/ruff/rules/complex-structure/>
- **Costura** (costuras, seam). *Técnica.* Lugar donde se puede cambiar el comportamiento de un programa sin editar el código en ese punto, por ejemplo pasando una dependencia por parámetro. El término es de Michael Feathers.
  - Referencia: <https://martinfowler.com/bliki/LegacySeam.html>

## D

- **Deuda técnica** (technical debt, deuda). *Concepto.* Metáfora de Ward Cunningham: las deficiencias de calidad interna funcionan como una deuda cuyos intereses son el esfuerzo extra que cuesta cada cambio. Puede ser deliberada o inadvertida, y prudente o imprudente.
  - Usar cuando: Para decidir qué limpiar primero, que es lo que se toca a menudo y por eso paga más intereses.
  - No usar cuando: Como excusa para todo; el código de una zona que casi nadie toca puede no merecer el pago.
  - Referencia: <https://martinfowler.com/bliki/TechnicalDebtQuadrant.html>

## E

- **Extraer función** (Extract Function, extraer una función). *Técnica.* Refactorización que lleva un fragmento de código a una función nueva cuyo nombre dice qué hace. La función original pasa a leerse como un resumen.
  - Referencia: <https://refactoring.com/catalog/extractFunction.html>

## H

- **Higuera estranguladora** (Strangler Fig, estrangulador). *Patrón.* Sustituir un sistema heredado poco a poco, desviando partes de su funcionalidad a código nuevo hasta que el antiguo se puede retirar, en lugar de reescribirlo de una vez.
  - Referencia: <https://martinfowler.com/bliki/StranglerFigApplication.html>

## I

- **Índice de mantenibilidad** (maintainability index). *Métrica.* Métrica de 0 a 100 que combina volumen de Halstead, complejidad ciclomática, líneas de código y porcentaje de comentarios. radon la clasifica en A (20 a 100), B (10 a 19) y C (0 a 9). Es una señal gruesa.
  - Referencia: <https://radon.readthedocs.io/en/latest/commandline.html>

## M

- **Mutante** (mutantes). *Concepto.* Copia del código con un cambio pequeño (> por >=, un número por otro). Las pruebas deberían detectarlo; si no, sobrevive.
  - Referencia: <https://pitest.org/>

## N

- **Número mágico** (números mágicos, valor mágico, valores mágicos, magic value). *Concepto.* Literal sin nombre en el código (1.04, 50, 100) cuyo significado hay que deducir del contexto. Se sustituye por una constante con nombre.
  - Referencia: <https://refactoring.com/catalog/replaceMagicLiteral.html>

## O

- **Obsesión por primitivos** (primitive obsession). *Concepto.* Representar conceptos del dominio con tipos básicos (un entero para el tipo de envío, un diccionario para el cliente, un float para el dinero) en lugar de con tipos propios que validen y den nombre.
  - Referencia: <https://refactoring.com/catalog/replacePrimitiveWithObject.html>
- **Olor de código** (olores de código, olor, olores, code smell). *Concepto.* Señal superficial, fácil de ver, que suele corresponder a un problema más profundo del diseño: una función larga, un nombre críptico, código duplicado. No es un error: hay que mirar si de verdad hay un problema.
  - Referencia: <https://martinfowler.com/bliki/CodeSmell.html>

## P

- **Prueba de caracterización** (pruebas de caracterización, golden master). *Técnica.* Prueba que graba lo que hace hoy el código, sea correcto o no, y avisa si cambia. Protege una refactorización de código heredado; no dice si el comportamiento es el deseado.
  - Usar cuando: Antes de refactorizar código sin pruebas cuyo comportamiento exacto no está documentado.
  - No usar cuando: Como prueba definitiva; cuando se entienden las reglas, se sustituye por pruebas que las nombren.
  - Referencia: <https://en.wikipedia.org/wiki/Characterization_test>
- **Prueba de mutación** (pruebas de mutación, mutación, mutation testing). *Técnica.* Técnica que introduce pequeños fallos en el código (mutantes) y ejecuta las pruebas. Si alguna falla, el mutante muere; si todas pasan, sobrevive y revela un caso que las pruebas no comprueban.
  - Usar cuando: Para medir la calidad de las pruebas de un módulo crítico, más allá de la cobertura.
  - No usar cuando: En cada commit de un proyecto grande, porque ejecuta las pruebas una vez por mutante y es lenta.
  - Referencia: <https://pitest.org/>

## R

- **radon**. *Herramienta.* Herramienta de Python que calcula métricas de código, como la complejidad ciclomática (radon cc) y el índice de mantenibilidad (radon mi).
  - Referencia: <https://radon.readthedocs.io/en/latest/commandline.html>
- **Refactorización** (refactorizar, refactorizaciones, refactoring). *Técnica.* Cambio en la estructura interna del software para hacerlo más fácil de entender y más barato de modificar sin cambiar su comportamiento observable. Se hace en pasos pequeños, cada uno con las pruebas en verde.
  - Usar cuando: Antes o después de un cambio en código que se va a seguir tocando, y siempre con pruebas que comprueben el comportamiento.
  - No usar cuando: A la vez que se corrige un fallo o se añade una función; son cambios distintos y van en pasos distintos.
  - Referencia: <https://martinfowler.com/bliki/DefinitionOfRefactoring.html>
- **Regla del campamento** (camp site rule). *Técnica.* Dejar el código un poco mejor de como se encontró cada vez que se trabaja en él. Es la pauta detrás de la refactorización oportunista. Si todo el equipo lo hace, la base de código mejora a diario sin proyectos de limpieza aparte.
  - Referencia: <https://martinfowler.com/bliki/OpportunisticRefactoring.html>
- **ruff**. *Herramienta.* Linter y formateador de Python escrito en Rust. Reúne reglas de pycodestyle, pylint, mccabe y otros, pero muchas hay que activarlas en la configuración.
  - Referencia: <https://docs.astral.sh/ruff/settings/>
