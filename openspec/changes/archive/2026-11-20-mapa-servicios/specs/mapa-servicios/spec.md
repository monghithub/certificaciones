## ADDED Requirements

### Requirement: Mapa de servicios
Si el curso tiene glosario, la consola SHALL ofrecer `/c/<curso>/mapa` con los diagramas de `mapa-servicios.md` (si existe) y un cuadro de todos los servicios del glosario agrupados por la categoría de la lista oficial *in scope*, después los no listados y al final los fuera de alcance, con icono (si lo tiene), qué es, cuándo usarlo, cuándo no y los módulos que lo tratan.

#### Scenario: Servicio con icono y módulo
- **WHEN** el glosario da a Amazon S3 un icono y el `servicios.md` del módulo 00 lo lista
- **THEN** su fila muestra el icono y un enlace a los servicios del módulo 00

#### Scenario: Icono inexistente
- **WHEN** una entrada del glosario apunta a un icono que no está en `app/static/iconos/`
- **THEN** el validador informa del error
