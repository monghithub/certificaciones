## ADDED Requirements

### Requirement: Disponibilidad y nombres vigentes
Todo módulo SHALL indicar, para cada servicio o funcionalidad citada, si AWS la ha cerrado a clientes nuevos, la ha pasado a *Classic* o la ha renombrado, según su página en `docs.aws.amazon.com`, y no SHALL presentarla como opción para proyectos nuevos.

#### Scenario: Servicio cerrado a clientes nuevos
- **WHEN** un módulo cita un servicio cuya documentación dice *no longer open to new customers*
- **THEN** la teoría, `servicios.md` y el glosario lo indican

### Requirement: Profundidad por objetivo
Cada objetivo oficial SHALL tratarse con definición, criterio de decisión, ejemplo de negocio y trampa típica, y las métricas o cálculos con un ejemplo numérico.

#### Scenario: Revisión de cierre
- **WHEN** se cierra un módulo
- **THEN** una revisión independiente comprueba errores factuales, suficiencia para el examen, calidad del banco y didáctica, y registra los cambios en `CHANGELOG.md`

### Requirement: Laboratorios ejecutables
Los laboratorios SHALL distinguir los permisos de consola de los de CLI, describir la capa gratuita vigente y recomendar AWS Budgets antes de empezar.

#### Scenario: Consola con política mínima de API
- **WHEN** un laboratorio usa la consola de un servicio
- **THEN** indica una política suficiente para la consola (por ejemplo, la administrada de solo lectura)
