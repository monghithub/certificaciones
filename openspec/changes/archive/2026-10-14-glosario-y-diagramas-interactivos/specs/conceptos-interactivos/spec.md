## ADDED Requirements

### Requirement: Conceptos pulsables en el contenido
Al renderizar una sección, la consola SHALL convertir en botones los términos y alias del glosario del curso que aparezcan en texto normal, solo en la **primera aparición de cada concepto dentro de cada apartado** (se reinicia en cada encabezado), conservando el texto original.

#### Scenario: Primera aparición por apartado
- **WHEN** «Amazon Bedrock» aparece tres veces en un mismo apartado
- **THEN** solo la primera es un botón y las otras dos son texto

#### Scenario: Nuevo apartado
- **WHEN** «Amazon Bedrock» vuelve a aparecer tras un encabezado
- **THEN** la primera aparición de ese apartado vuelve a ser un botón

#### Scenario: Exclusiones
- **WHEN** el término aparece en un encabezado, en un enlace, en código en línea o en un bloque de código
- **THEN** no se convierte en botón

#### Scenario: Coincidencia exacta
- **WHEN** el texto contiene «PAIRS» y el glosario tiene el término «RAG» o «AI»
- **THEN** no se marca ninguna coincidencia dentro de otra palabra

#### Scenario: Mayúsculas en siglas
- **WHEN** el glosario tiene la sigla «RAG» y el texto contiene «drag»
- **THEN** no se marca

#### Scenario: Término más largo prevalece
- **WHEN** existen «Amazon Bedrock» y «Bedrock» y el texto dice «Amazon Bedrock»
- **THEN** se marca una sola vez el término más largo

### Requirement: Modal de concepto accesible
Al pulsar un concepto, la consola SHALL abrir un modal (`dialog`) con el término, su categoría, la definición, «cuándo usarlo» y «cuándo no» si existen, y un enlace a la documentación oficial que abra en una pestaña nueva con `rel="noopener noreferrer"`. SHALL cerrarse con el botón, `Esc` o clic fuera, devolver el foco al elemento de origen, funcionar con teclado y en pantallas estrechas, y respetar el modo claro y oscuro.

#### Scenario: Abrir y cerrar con teclado
- **WHEN** el usuario enfoca un concepto y pulsa `Enter`, y después `Esc`
- **THEN** el modal se abre con la definición y, al cerrarse, el foco vuelve al concepto

#### Scenario: Contenido seguro
- **WHEN** una definición contiene caracteres como `<` o `&`
- **THEN** se muestran como texto y no se interpretan como HTML

#### Scenario: Sin glosario
- **WHEN** un curso no tiene glosario
- **THEN** el contenido se muestra igual que antes, sin botones ni modal

### Requirement: Apariencia discreta de los conceptos
En reposo, un concepto pulsable SHALL verse como texto normal, sin caja, color de fondo ni subrayado. SHALL resaltarse (fondo suave y cursor de mano) solo al pasar el ratón por encima o al recibir el foco del teclado. En dispositivos sin ratón (`hover: none`) SHALL mostrar un subrayado punteado tenue como única pista.

#### Scenario: Reposo
- **WHEN** la página se muestra sin interacción en un dispositivo con ratón
- **THEN** los conceptos no tienen fondo ni borde visibles

#### Scenario: Pasar el ratón
- **WHEN** el usuario pasa el ratón por un concepto
- **THEN** aparece un resaltado suave y el cursor cambia a mano

#### Scenario: Pantalla táctil
- **WHEN** el dispositivo no admite «hover»
- **THEN** los conceptos muestran un subrayado punteado tenue

### Requirement: Funcionamiento con la navegación de la consola
Los conceptos y el modal SHALL funcionar tras cualquier navegación con `hx-boost` y sin peticiones de red adicionales, y sin romper la política de seguridad de contenido (`script-src 'self'`).

#### Scenario: Tras navegar
- **WHEN** el usuario cambia de sección mediante un enlace y pulsa un concepto
- **THEN** el modal se abre con los datos de la nueva página

### Requirement: Nodos de diagrama pulsables
Los nodos de un diagrama cuyo texto contenga un término o alias del glosario SHALL poder pulsarse (también con teclado) para abrir el mismo modal, y SHALL indicarlo con el cursor y el foco visibles.

#### Scenario: Pulsar un nodo
- **WHEN** el usuario pulsa el nodo «Amazon Bedrock» de un diagrama
- **THEN** se abre el modal de Amazon Bedrock

### Requirement: Datos de la página
El servidor SHALL incrustar en cada página solo los conceptos que usa (en texto o dentro de diagramas), como datos JSON no ejecutables.

#### Scenario: Concepto solo en un diagrama
- **WHEN** «Amazon S3» solo aparece en un diagrama de la sección
- **THEN** sus datos están en la página y el nodo es pulsable
