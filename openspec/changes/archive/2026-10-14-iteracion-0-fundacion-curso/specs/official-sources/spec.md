## ADDED Requirements

### Requirement: Revalidación de datos del examen
Antes de crear ficheros de contenido, el proceso SHALL contrastar con la guía oficial los datos de la sección 4 de `promt.md` (duración, número de preguntas, puntuación, tipos de pregunta, coste, validez, dominios y pesos).

#### Scenario: Datos coinciden
- **WHEN** todos los datos coinciden con la guía oficial
- **THEN** `CHANGELOG.md` lo registra con la fecha de comprobación

#### Scenario: Datos difieren
- **WHEN** algún dato difiere
- **THEN** se adopta el valor oficial y se documenta la diferencia en `CHANGELOG.md`

### Requirement: Transcripción de tareas por dominio
Los ficheros `fuentes/dominio-1.md` … `fuentes/dominio-5.md` SHALL existir, cada uno con la URL de origen, la fecha de consulta y la lista literal de Task Statements y sus habilidades/objetivos, con un encabezado `## Task Statement N.M` por tarea.

#### Scenario: Fichero de dominio completo
- **WHEN** se abre `fuentes/dominio-3.md`
- **THEN** contiene URL, fecha de consulta y todas las Task Statements `3.x` publicadas, con sus habilidades literales

#### Scenario: Dato no verificable
- **WHEN** una página oficial no es accesible o su contenido es dudoso
- **THEN** el fichero contiene `> ⚠️ PENDIENTE DE VERIFICAR:` en lugar de contenido inventado

### Requirement: Referencias a listas de servicios
`fuentes/` SHALL incluir (en `servicios-alcance.md` o equivalente) la URL, fecha y listado de servicios in scope y out of scope de la guía oficial.

#### Scenario: Listas disponibles
- **WHEN** un módulo necesita saber si un servicio es evaluable
- **THEN** puede consultarlo en `fuentes/servicios-alcance.md`
