## ADDED Requirements

### Requirement: Información en cualquier caja de un diagrama
Cada nodo y cada subgrupo de un diagrama SHALL tener información definida de forma explícita en un bloque `nodos` situado inmediatamente después del bloque `mermaid`, como un mapa YAML de id de nodo a información (`concepto`, `titulo`, `texto`, `usar_cuando`, `no_usar_cuando`, `enlaces`, `seccion`). Al pulsar la caja, la consola SHALL abrir el modal con esa información. El bloque `nodos` no SHALL mostrarse en la página.

#### Scenario: Nodo con concepto
- **WHEN** el nodo `L` declara `concepto: aws-lambda`
- **THEN** al pulsarlo se abre el modal con la entrada «AWS Lambda» del glosario, incluidos sus enlaces

#### Scenario: Nodo con información propia
- **WHEN** el nodo `B` declara `titulo` y `texto` sin `concepto`
- **THEN** el modal muestra ese título y ese texto

#### Scenario: Subgrupo
- **WHEN** el usuario pulsa el título de un subgrupo con información
- **THEN** se abre el modal de ese subgrupo; y si pulsa un nodo interior, el de ese nodo

#### Scenario: Bloque no visible
- **WHEN** se renderiza una sección con un bloque `nodos`
- **THEN** el bloque no aparece en el HTML visible

### Requirement: Combinación de concepto y datos de la caja
Si una caja declara `concepto`, la información base SHALL provenir del glosario; los campos `titulo`, `texto`, `usar_cuando` y `no_usar_cuando` de la caja SHALL sustituir a los del glosario y sus `enlaces` SHALL añadirse a los del concepto.

#### Scenario: Sustitución del título
- **WHEN** una caja declara `concepto: amazon-s3` y `titulo: Almacén de datos`
- **THEN** el modal muestra «Almacén de datos» con la definición y los enlaces de Amazon S3

### Requirement: Enlaces en el modal
El modal SHALL mostrar una lista de enlaces cuando la información tiene alguno. Los enlaces externos (`https`) SHALL abrirse en una pestaña nueva con `rel="noopener noreferrer"`; los internos SHALL llevar al apartado del curso en la misma pestaña. Para un concepto, `referencia` SHALL ser el primer enlace («Documentación oficial») seguido de los `enlaces` adicionales del glosario.

#### Scenario: Enlace externo
- **WHEN** una caja tiene un enlace `https`
- **THEN** el enlace se abre en una pestaña nueva sin acceso a `window.opener`

#### Scenario: Ver en el curso
- **WHEN** una caja declara `seccion: 01-fundamentos-ia-ml/teoria#tipos-de-inferencia`
- **THEN** el modal incluye «Ver en el curso», que lleva a ese apartado del curso

#### Scenario: Esquemas peligrosos
- **WHEN** un enlace usa un esquema distinto de `https`
- **THEN** no se muestra

### Requirement: Enlaces adicionales en el glosario
Las entradas del glosario SHALL poder declarar `enlaces` (lista de `texto` y `url` `https`) además de `referencia`.

#### Scenario: Entrada con varios enlaces
- **WHEN** una entrada declara `referencia` y dos `enlaces`
- **THEN** el modal muestra tres enlaces, con la referencia en primer lugar

### Requirement: Anclas en los encabezados
Los encabezados del contenido renderizado SHALL tener un `id` con el mismo formato de ancla que GitHub (minúsculas, sin signos, espacios como guiones y sufijo numérico ante duplicados), de modo que los enlaces `#ancla` funcionen en la consola.

#### Scenario: Enlace del mapa de cobertura
- **WHEN** el usuario pulsa «Términos básicos de IA» en el mapa de cobertura
- **THEN** la página se desplaza al encabezado correspondiente

### Requirement: Accesibilidad de las cajas
Las cajas pulsables SHALL ser operables con teclado (`Enter` y espacio), exponer `role="button"` y una etiqueta accesible, y mostrar foco visible. SHALL tener cursor de mano y un realce al pasar el ratón.

#### Scenario: Teclado
- **WHEN** el usuario enfoca una caja y pulsa `Enter`
- **THEN** se abre el modal y, al cerrarlo con `Esc`, el foco vuelve a la caja
