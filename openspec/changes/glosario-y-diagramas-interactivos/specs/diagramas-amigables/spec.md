## ADDED Requirements

### Requirement: Interfaz clara y suave
La consola SHALL usar por defecto un tema claro de tonos suaves (botones tonales, bordes y sombras discretos), con selector de tema en la cabecera (claro, oscuro y sistema) cuya elección se guarda en el navegador y se aplica antes de pintar la página. El tema por defecto SHALL ser claro aunque el sistema esté en modo oscuro.

#### Scenario: Valor por defecto
- **WHEN** un usuario entra por primera vez con el sistema en modo oscuro
- **THEN** la web se muestra en el tema claro

#### Scenario: Cambiar de tema
- **WHEN** el usuario pulsa el selector de tema
- **THEN** cambia cíclicamente entre claro, oscuro y sistema, y la elección se recuerda al recargar

### Requirement: Sin copias antiguas de los estáticos
Los ficheros estáticos SHALL servirse con revalidación (`Cache-Control: no-cache`) y enlazarse con una versión derivada de su contenido, de modo que tras una actualización el navegador nunca use CSS o JavaScript antiguos.

#### Scenario: Tras una actualización
- **WHEN** cambia `app.css` o `app.js`
- **THEN** las páginas enlazan una URL con otra versión y el navegador descarga el fichero nuevo

### Requirement: Tema amable y coherente
Los diagramas Mermaid SHALL usar un tema propio con colores suaves, bordes redondeados, tipografía legible, curvas suaves y espaciado generoso, que siga automáticamente el modo claro u oscuro de la aplicación, y SHALL adaptarse al ancho de la pantalla.

#### Scenario: Modo oscuro
- **WHEN** el sistema está en modo oscuro
- **THEN** los diagramas usan fondos y textos con contraste suficiente sin intervención del autor

### Requirement: Clases semánticas
Los autores SHALL poder colorear nodos por tipo mediante las clases `ia`, `ml`, `dl`, `gen`, `dato`, `proceso`, `servicio`, `accion`, `aviso` y `decision`, definidas en CSS con variables para ambos modos, sin `classDef` en línea.

#### Scenario: Nodo con clase
- **WHEN** un nodo se declara con `class A servicio`
- **THEN** se muestra con el color de «servicio» en modo claro y oscuro

### Requirement: Animación suave
Los diagramas SHALL animar la aparición escalonada de sus nodos al entrar en pantalla y el flujo de las flechas, mediante CSS. SHALL aplicar un efecto al pasar el ratón sobre nodos pulsables.

#### Scenario: Entrada
- **WHEN** un diagrama entra en el área visible
- **THEN** sus nodos aparecen de forma escalonada

#### Scenario: Movimiento reducido
- **WHEN** el usuario tiene activada la preferencia de movimiento reducido
- **THEN** no hay ninguna animación y todos los elementos son visibles desde el inicio

#### Scenario: Sin JavaScript
- **WHEN** el JavaScript no se ejecuta
- **THEN** ningún elemento queda oculto por la animación

### Requirement: Diagramas existentes actualizados
Los diagramas de los módulos 00 y 01 SHALL reescribirse con las clases semánticas y etiquetas claras, manteniendo su significado y una sintaxis Mermaid válida.

#### Scenario: Validez
- **WHEN** se analizan los diagramas con el analizador de Mermaid
- **THEN** todos son válidos

### Requirement: Guía para autores
`AGENTS.md` SHALL documentar las clases semánticas y las reglas para escribir diagramas y añadir conceptos al glosario.

#### Scenario: Reglas visibles
- **WHEN** un colaborador consulta `AGENTS.md`
- **THEN** encuentra la lista de clases y la obligación de añadir al glosario los servicios y conceptos nuevos
