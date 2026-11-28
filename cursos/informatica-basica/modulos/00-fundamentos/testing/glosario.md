# Glosario: Pruebas: unitarias, de integración y de contrato

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 13 términos.

## C

- **Cobertura de código** (cobertura, coverage). *Métrica.* Porcentaje del código que ejecutan las pruebas. Sirve para encontrar partes sin probar, pero un valor alto no garantiza que las pruebas comprueben algo.
  - Referencia: <https://martinfowler.com/bliki/TestCoverage.html>

## D

- **Doble de prueba** (dobles de prueba, mock, mocks, stub, fake, spy). *Técnica.* Objeto que sustituye a una dependencia real en una prueba: dummy, stub, spy, mock o fake, según lo que simule y compruebe.
  - Referencia: <https://martinfowler.com/bliki/TestDouble.html>

## F

- **Fixture** (fixtures). *Herramienta.* En pytest, función que prepara lo que una prueba necesita (un objeto, una conexión) y lo entrega como parámetro; puede limpiar al terminar y compartirse entre pruebas.
  - Referencia: <https://docs.pytest.org/en/stable/how-to/fixtures.html>

## P

- **Parametrización** (parametrize, pytest.mark.parametrize). *Técnica.* Ejecutar la misma prueba con varios conjuntos de datos de entrada y resultado esperado, cada uno como un caso independiente.
  - Referencia: <https://docs.pytest.org/en/stable/how-to/parametrize.html>
- **Pirámide de pruebas** (test pyramid). *Concepto.* Modelo que recomienda muchas pruebas unitarias rápidas, menos de integración y muy pocas de extremo a extremo. La popularizó Mike Cohn en Succeeding with Agile (2009).
  - Referencia: <https://martinfowler.com/bliki/TestPyramid.html>
- **Preparar, actuar, comprobar** (Arrange, Act, Assert, AAA). *Técnica.* Estructura de una prueba en tres partes: preparar los datos, ejecutar la acción y comprobar el resultado.
  - Referencia: <https://docs.pytest.org/en/stable/how-to/fixtures.html>
- **Prueba de contrato** (pruebas de contrato, contract test). *Técnica.* Prueba que comprueba que un cliente y un proveedor (por ejemplo, dos microservicios) siguen respetando la interfaz que han acordado, sin desplegarlos juntos.
  - Referencia: <https://martinfowler.com/bliki/ContractTest.html>
- **Prueba de integración** (pruebas de integración). *Concepto.* Prueba que comprueba que el código funciona con una pieza real externa a él: una base de datos, un sistema de ficheros, otro servicio.
  - Referencia: <https://martinfowler.com/articles/practical-test-pyramid.html>
- **Prueba unitaria** (pruebas unitarias, unit test). *Concepto.* Prueba rápida y aislada de una unidad pequeña de código (una función, una clase), sin red ni base de datos reales.
  - Referencia: <https://martinfowler.com/articles/practical-test-pyramid.html>
- **Pruebas de mutación** (mutation testing). *Técnica.* Técnica que introduce pequeños cambios (mutantes) en el código y comprueba si alguna prueba falla; los mutantes que sobreviven revelan pruebas débiles.
  - Referencia: <https://en.wikipedia.org/wiki/Mutation_testing>

## T

- **TDD** (desarrollo guiado por pruebas, Test-Driven Development, rojo, verde, refactorizar). *Técnica.* Técnica desarrollada por Kent Beck a finales de los noventa: escribir una prueba que falla, el código mínimo para que pase y refactorizar, en ciclos cortos.
  - Referencia: <https://martinfowler.com/bliki/TestDrivenDevelopment.html>
- **Testcontainers**. *Herramienta.* Bibliotecas (Java, Python, Go, .NET y otras) que arrancan contenedores Docker desechables desde las pruebas, para probar contra bases de datos o servicios reales.
  - Referencia: <https://testcontainers.com/>

## U

- **unittest.mock** (unittest.mock.patch, Mock()). *Herramienta.* Módulo de la biblioteca estándar de Python para crear dobles (Mock) y sustituir objetos temporalmente (patch). Hay que parchear el nombre donde lo busca el código probado.
  - Referencia: <https://docs.python.org/3/library/unittest.mock.html>
