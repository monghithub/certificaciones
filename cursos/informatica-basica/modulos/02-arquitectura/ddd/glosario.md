# Glosario: Domain-Driven Design táctico y estratégico

Términos del tema en orden alfabético, con sus variantes en inglés y en español. **Fichero generado** con `python scripts/generar_glosario.py` a partir de `glosario.yaml`: no lo edites a mano; edita el YAML y vuelve a generarlo.

Total: 13 términos.

## A

- **Agregado** (aggregate, raíz del agregado). *Patrón.* Grupo de objetos del dominio que se trata como una unidad de consistencia, con una raíz que es el único punto de acceso y que garantiza sus invariantes. Se carga y se guarda entero.
  - Referencia: <https://martinfowler.com/bliki/DDD_Aggregate.html>

## C

- **Capa anticorrupción** (anticorruption layer, ACL). *Patrón.* Capa de traducción entre el modelo propio y el de otro sistema, para que los conceptos ajenos no contaminen el dominio.
  - Referencia: <https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer>
- **Concurrencia optimista** (optimistic locking, versión). *Técnica.* Detectar escrituras concurrentes sobre un agregado comparando la versión leída con la guardada, y rechazar la que llegue tarde.
  - Referencia: <https://martinfowler.com/bliki/DDD_Aggregate.html>
- **Contexto delimitado** (bounded context). *Patrón.* Límite dentro del cual un modelo y su lenguaje son coherentes; la misma palabra puede significar cosas distintas en contextos distintos.
  - Referencia: <https://martinfowler.com/bliki/BoundedContext.html>

## D

- **Domain-Driven Design** (DDD, diseño guiado por el dominio). *Técnica.* Enfoque de Eric Evans en su libro de 2004 que centra el diseño del software en un modelo del dominio del negocio, construido junto con los expertos y expresado en su lenguaje.
  - Referencia: <https://martinfowler.com/bliki/DomainDrivenDesign.html>

## E

- **Evento de dominio** (domain event). *Patrón.* Hecho relevante para el negocio que ya ha ocurrido (PedidoConfirmado), emitido por un agregado para que otras partes reaccionen.
  - Referencia: <https://martinfowler.com/eaaDev/DomainEvent.html>

## I

- **Invariante** (regla de consistencia). *Concepto.* Regla del negocio que debe cumplirse siempre dentro de un agregado, como «el total de un pedido no supera 1000 €».
  - Referencia: <https://martinfowler.com/bliki/DDD_Aggregate.html>

## L

- **Lenguaje ubicuo** (ubiquitous language). *Concepto.* Vocabulario común y preciso que comparten expertos del negocio y desarrolladores dentro de un contexto, y que aparece tal cual en el código.
  - Referencia: <https://martinfowler.com/bliki/UbiquitousLanguage.html>

## M

- **Mapa de contextos** (context map). *Técnica.* Representación de los contextos delimitados de un sistema y de las relaciones entre ellos (socios, núcleo compartido, cliente-proveedor, conformista, capa anticorrupción…).
  - Referencia: <https://github.com/ddd-crew/context-mapping>
- **Modelo anémico** (anemic domain model). *Concepto.* Antipatrón en el que los objetos del dominio solo tienen datos y getters y setters, y toda la lógica está en servicios externos que pueden saltarse las reglas.
  - Referencia: <https://martinfowler.com/bliki/AnemicDomainModel.html>

## R

- **Repositorio** (repository). *Patrón.* Abstracción con aspecto de colección para obtener y guardar agregados completos, uno por tipo de agregado.
  - Referencia: <https://www.domainlanguage.com/ddd/reference/>

## S

- **Servicio de dominio** (domain service). *Patrón.* Operación del dominio que no pertenece de forma natural a ninguna entidad ni objeto valor, como calcular un precio que depende de varios agregados.
  - Referencia: <https://www.domainlanguage.com/ddd/reference/>
- **Subdominio** (dominio central, core domain, subdominio genérico, subdominio de soporte). *Concepto.* Parte del negocio. El central es lo que diferencia a la empresa y merece el mejor diseño; los de soporte y genéricos se resuelven de forma más sencilla o se compran.
  - Referencia: <https://www.domainlanguage.com/ddd/reference/>
