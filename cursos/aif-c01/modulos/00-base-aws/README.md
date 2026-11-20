# Base de AWS

Este módulo reúne los conocimientos de AWS que la guía oficial recomienda al candidato antes de abordar los dominios del examen. No evalúa por sí solo ninguna tarea oficial: es el vocabulario común del resto del curso. Se trata al nivel mínimo necesario para reconocer cada concepto en una pregunta.

## Objetivos de aprendizaje

Al terminar el módulo, el estudiante podrá:

- Identificar para qué sirven los servicios centrales de AWS que aparecen en el examen (CP.1).
- Distinguir qué protege AWS y qué protege el cliente según el modelo de responsabilidad compartida (CP.2).
- Explicar cómo IAM autentica y autoriza el acceso a los recursos, y aplicar el criterio de mínimo privilegio (CP.3).
- Reconocer los modelos de precios de AWS y elegir el adecuado para una carga de trabajo (CP.4).

Estos conocimientos proceden de la sección «Recommended AWS knowledge» de la guía y se transcriben en [fuentes/conocimientos-previos.md](../../fuentes/conocimientos-previos.md).

## Mapa de cobertura

| Objetivo | Descripción | Sección |
|---|---|---|
| CP.1 | Servicios centrales de AWS y sus casos de uso | [Servicios centrales](#servicios-centrales) |
| CP.2 | Modelo de responsabilidad compartida | [Responsabilidad compartida](#responsabilidad-compartida) |
| CP.3 | AWS Identity and Access Management (IAM) | [IAM: identidades y permisos](#iam-identidades-y-permisos) |
| CP.4 | Modelos de precios de los servicios de AWS | [Modelos de precios](#modelos-de-precios) |

## Teoría

### Servicios centrales

#### Qué es la nube

AWS define la **computación en la nube** (*cloud computing*) como la entrega bajo demanda, por internet y con pago por uso, de capacidad de cómputo, bases de datos, almacenamiento, aplicaciones y otros recursos de TI. En lugar de comprar y mantener centros de datos y servidores, la empresa usa esos recursos cuando los necesita y paga por lo que consume.

AWS resume sus ventajas en seis ideas:

| Ventaja | Qué quiere decir |
|---|---|
| Cambiar gasto fijo por gasto variable | No se invierte por adelantado en servidores; se paga por el uso |
| Economías de escala masivas | Al agregar el uso de muchos clientes, el proveedor consigue precios por uso más bajos |
| Dejar de adivinar la capacidad | Se amplía o reduce según la demanda real, sin quedarse corto ni sobredimensionar |
| Velocidad y agilidad | Los recursos están disponibles en minutos, lo que abarata experimentar |
| Dejar de mantener centros de datos | El equipo se dedica a la aplicación, no al hardware |
| Desplegar en todo el mundo en minutos | La aplicación puede llegar a varias Regiones con poco esfuerzo |

**Modelos de despliegue** (*deployment models*). Dicen *dónde* se ejecuta la aplicación:

| Modelo | Qué es | Cuándo encaja |
|---|---|---|
| Nube (*cloud*), también llamada nube pública | Toda la aplicación se despliega y se ejecuta en la nube; la infraestructura del proveedor la comparten muchos clientes | Aplicaciones nuevas o migradas por completo |
| Híbrido (*hybrid*) | Conecta recursos de la nube con recursos que siguen fuera de ella, normalmente el centro de datos propio | Cuando parte de la carga debe quedarse en las instalaciones (sistemas heredados, requisitos de ubicación de los datos) y otra parte se lleva a la nube. AWS Outposts lleva infraestructura de AWS a las instalaciones del cliente (se nombra solo para reconocerlo) |
| Local (*on-premises*), también llamado nube privada | Recursos en el centro de datos propio, con herramientas de virtualización y de gestión | Control total del hardware. A cambio, la empresa compra, mantiene y renueva todo |

**Tipos de servicio en la nube.** Dicen *cuánto gestiona el proveedor*:

| Tipo | Qué ofrece | Qué gestiona el cliente | En AWS |
|---|---|---|---|
| IaaS (*Infrastructure as a Service*) | Los bloques básicos de TI: cómputo, almacenamiento y red | Sistema operativo, software, aplicación y datos | Amazon EC2, que AWS cita como IaaS en el modelo de responsabilidad compartida |
| PaaS (*Platform as a Service*) | Una plataforma para desarrollar y mantener aplicaciones sin gestionar la infraestructura de debajo | Su aplicación y sus datos | AWS no publica una lista de servicios por tipo |
| SaaS (*Software as a Service*) | Una aplicación completa que ejecuta y gestiona el proveedor | Solo su uso y su configuración, y sus datos | El ejemplo clásico es el correo web |

En la práctica, AWS no clasifica sus servicios con estas tres siglas: en el modelo de responsabilidad compartida distingue los servicios de **infraestructura** (como EC2) de los servicios **abstraídos** (como Amazon S3 o Amazon DynamoDB), en los que AWS opera la infraestructura, el sistema operativo y la plataforma. Lo que importa para el examen es la idea de fondo: **cuanto más gestionado es el servicio, menos tareas operativas asume el cliente**, como se ve en [Responsabilidad compartida](#responsabilidad-compartida).

```mermaid
flowchart LR
    subgraph SAAS["📦 <b>SaaS</b><br/>el proveedor lo gestiona todo"]
        direction TB
        subgraph PAAS["🧰 <b>PaaS</b><br/>plataforma gestionada"]
            direction TB
            subgraph IAAS["🧱 <b>IaaS</b><br/>cómputo, almacenamiento y red"]
                I1["🖥️ <b>Amazon EC2</b><br/>el cliente gestiona el SO"]
            end
            P1["⚙️ <b>Plataforma</b><br/>SO y entorno de ejecución"]
        end
        S1["📧 <b>Aplicación lista</b><br/>por ejemplo, correo web"]
    end
    class I1 servicio
    class P1 proceso
    class S1 accion
```

```nodos
SAAS:
  concepto: saas
IAAS:
  concepto: iaas
PAAS:
  concepto: paas
I1:
  concepto: amazon-ec2
  texto: AWS cita Amazon EC2 como ejemplo de IaaS. El cliente gestiona el sistema operativo invitado, sus parches, la aplicación y los grupos de seguridad.
  enlaces:
  - texto: Modelo de responsabilidad compartida
    url: https://aws.amazon.com/compliance/shared-responsibility-model/
P1:
  titulo: Plataforma gestionada
  texto: En PaaS, el proveedor gestiona también el sistema operativo y el entorno donde corre la aplicación. El cliente solo despliega su código y gestiona sus datos.
  enlaces:
  - texto: Tipos de computación en la nube
    url: https://aws.amazon.com/types-of-cloud-computing/
S1:
  titulo: Aplicación lista para usar
  texto: En SaaS, el proveedor ejecuta y gestiona la aplicación completa; el usuario solo la usa y la configura. El ejemplo clásico es el correo web.
  enlaces:
  - texto: Tipos de computación en la nube
    url: https://aws.amazon.com/types-of-cloud-computing/
```

#### Infraestructura global

La infraestructura de AWS se organiza en piezas que se contienen unas a otras:

- **Región:** ubicación geográfica, aislada de las demás, donde se crean los recursos.
- **Zona de disponibilidad** (*Availability Zone*, AZ): uno o varios centros de datos separados, con alimentación, red y conectividad redundantes, dentro de una Región. Cada Región tiene al menos tres. Repartir una aplicación entre varias AZ permite que siga funcionando si falla una: es la base de la **alta disponibilidad**.
- **Local Zone:** extensión de una Región que acerca cómputo, almacenamiento, bases de datos y otros servicios a grandes núcleos de población e industria, para dar **latencia muy baja** a los usuarios de esa zona.
- **Ubicación de borde** (*edge location* o punto de presencia): centro de datos de la red mundial donde **Amazon CloudFront** guarda copias en caché del contenido para entregarlo desde el punto más cercano al usuario.

```mermaid
flowchart LR
    subgraph REG["🌍 <b>Región</b><br/>ubicación geográfica aislada"]
        direction TB
        subgraph AZ1["🏢 <b>Zona de disponibilidad A</b>"]
            DC1["🧱 <b>Centros de datos</b><br/>uno o varios"]
        end
        subgraph AZ2["🏢 <b>Zona de disponibilidad B</b>"]
            DC2["🧱 <b>Centros de datos</b><br/>uno o varios"]
        end
        LZ["📍 <b>Local Zone</b><br/>cerca de una gran ciudad"]
    end
    EDGE["🚀 <b>Ubicación de borde</b><br/>caché de CloudFront"]
    REG ~~~ EDGE
    class DC1,DC2 servicio
    class LZ proceso
    class EDGE servicio
```

```nodos
REG:
  concepto: region-de-aws
AZ1:
  concepto: zona-de-disponibilidad
AZ2:
  concepto: zona-de-disponibilidad
  titulo: Varias zonas, alta disponibilidad
  texto: Si la aplicación se reparte entre al menos dos zonas de disponibilidad, sigue funcionando aunque una falle.
DC1:
  titulo: Centros de datos
  texto: Cada zona de disponibilidad está formada por uno o varios centros de datos separados, con alimentación, red y conectividad redundantes.
  enlaces:
  - texto: Infraestructura global de AWS
    url: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/global-infrastructure.html
DC2:
  titulo: Centros de datos
  texto: Una zona de disponibilidad no es un único centro de datos, sino uno o varios.
  enlaces:
  - texto: Zonas de disponibilidad
    url: https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-availability-zones.html
LZ:
  concepto: aws-local-zones
EDGE:
  concepto: ubicacion-de-borde
```

#### Elegir la Región

Una **Región** es una ubicación geográfica donde se crean los recursos; al preparar una carga de trabajo conviene elegir una Región que ofrezca los servicios y funcionalidades necesarios y que esté cerca de los usuarios para reducir la latencia, o que cumpla requisitos legales. La disponibilidad de servicios y funcionalidades **varía según la Región**, algo que el examen y los laboratorios de este curso tienen en cuenta (por ejemplo, para Amazon Bedrock).

Cómo se elige la Región de una carga de trabajo:

```mermaid
flowchart TB
    W["🧳 <b>Carga de trabajo</b><br/>por ejemplo, un asistente con Bedrock"] --> Q1{"🧩 <b>¿Tiene los servicios<br/>necesarios?</b>"}
    BR["✨ <b>Amazon Bedrock</b><br/>cada modelo, en unas Regiones"] -.-> Q1
    Q1 -->|"no"| X["🚫 <b>Descartar la Región</b><br/>la disponibilidad varía"]
    Q1 -->|"sí"| Q2{"⚖️ <b>¿Cumple los<br/>requisitos legales?</b>"}
    Q2 -->|"no"| X
    Q2 -->|"sí"| C["📍 <b>Región candidata</b>"]
    C --> R["✅ <b>La más cercana a los usuarios</b><br/>menos latencia"]
    class W dato
    class BR servicio
    class Q1,Q2 decision
    class X aviso
    class C proceso
    class R accion
```

```nodos
W:
  titulo: Carga de trabajo
  texto: 'Lo que se quiere desplegar: una aplicación, un modelo o un trabajo de datos. Sus recursos se crean en una Región concreta.'
  seccion: 00-base-aws/teoria#servicios-centrales
BR:
  concepto: amazon-bedrock
  titulo: Modelos de Bedrock por Región
  texto: Cada modelo de Amazon Bedrock está disponible en unas Regiones concretas. Antes de elegir la Región, se comprueba que tiene el modelo que necesita la aplicación; los laboratorios del curso indican la Región que usan.
  enlaces:
  - texto: Modelos por Región en Amazon Bedrock
    url: https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html
Q1:
  concepto: region-de-aws
  titulo: Servicios y funcionalidades
  texto: 'La disponibilidad de servicios y funcionalidades varía según la Región. Es el primer filtro: una Región sin el servicio o la funcionalidad necesarios no sirve, por cerca que esté.'
  enlaces:
  - texto: Regiones de AWS
    url: https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html
Q2:
  concepto: residencia-de-datos
  titulo: Requisitos legales
  texto: Algunas cargas deben quedarse en una geografía concreta por ley o por la normativa del sector (residencia de los datos). Se estudia en el módulo 05.
  seccion: 05-seguridad-gobierno/teoria#estrategias-de-gobierno-de-datos
X:
  titulo: Región descartada
  texto: Si falta un servicio o no se cumplen los requisitos legales, se busca otra Región.
C:
  titulo: Región candidata
  texto: Ofrece lo necesario y cumple los requisitos. Si hay varias, decide la latencia.
R:
  titulo: Cerca de los usuarios
  texto: Elegir la Región más cercana a los usuarios reduce la latencia.
  enlaces:
  - texto: Regiones de AWS
    url: https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html
  seccion: 00-base-aws/teoria#servicios-centrales
```

Además de los servicios, el **precio** puede variar de una Región a otra, así que entra en la comparación cuando hay varias candidatas.

#### Los servicios

Los servicios centrales que el examen da por conocidos son estos:

| Servicio | Qué es | Idea clave |
|---|---|---|
| Amazon EC2 | Capacidad de cómputo escalable bajo demanda: servidores virtuales (instancias) | Tú eliges tipo de instancia, red y almacenamiento, y gestionas el sistema operativo invitado |
| Amazon S3 | Almacenamiento de objetos con gran escalabilidad, disponibilidad y seguridad | Casos habituales según la documentación: lagos de datos, sitios web, aplicaciones móviles, copias de seguridad y restauración, y analítica de *big data* |
| AWS Lambda | Cómputo *serverless*: ejecuta código sin aprovisionar ni gestionar servidores | AWS se encarga de la infraestructura, la capacidad, el escalado y los parches |
| Amazon Bedrock | Servicio totalmente gestionado con acceso a modelos fundacionales de varios proveedores para crear aplicaciones de IA generativa | Se estudia a fondo en los módulos 02 y 03 |
| Amazon SageMaker AI | Servicio totalmente gestionado de aprendizaje automático para construir, entrenar y desplegar modelos | Se estudia en los módulos 01 y siguientes. Antes del 3 de diciembre de 2024 se llamaba Amazon SageMaker (ver la nota de abajo) |

> **Nombres de SageMaker.** El 3 de diciembre de 2024 el servicio de ML se renombró a **Amazon SageMaker AI**. Ese mismo día, el nombre **Amazon SageMaker** pasó a designar una plataforma unificada de datos, analítica e IA que *incluye* SageMaker AI (junto con otras capacidades de datos y Amazon Bedrock). En este curso, y en las preguntas del Dominio 1, «SageMaker» se refiere siempre a SageMaker AI.

Otros servicios de apoyo que aparecerán a menudo en el curso, sin necesidad de profundizar ahora:

| Servicio | Para qué sirve, en una frase |
|---|---|
| Amazon VPC | Red virtual privada en la que el cliente lanza sus recursos y controla quién puede llegar a ellos |
| Amazon CloudWatch | Métricas, registros y alarmas: *¿cómo está funcionando?* |
| AWS CloudTrail | Registro de llamadas a la API: *¿quién hizo qué y cuándo?* |

```mermaid
flowchart LR
    U(["👤 Usuarios y aplicaciones"]) --> L["⚡ <b>AWS Lambda</b><br/>código sin servidores"]
    U --> E["🖥️ <b>Amazon EC2</b><br/>servidores virtuales"]
    L --> S[("🪣 <b>Amazon S3</b><br/>almacenamiento de objetos")]
    E --> S
    L --> B["✨ <b>Amazon Bedrock</b><br/>modelos fundacionales"]
    S --> M["🛠️ <b>Amazon SageMaker AI</b><br/>entrenar y desplegar modelos"]
    class U accion
    class L,E servicio
    class S dato
    class B gen
    class M ml
```

```nodos
U:
  titulo: Usuarios y aplicaciones
  texto: Las personas y los sistemas que usan los servicios de AWS. Para acceder a los recursos necesitan identidades autenticadas y permisos de IAM, con el criterio de mínimo privilegio.
  enlaces:
    - {texto: "Qué es IAM", url: "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html"}
  seccion: 00-base-aws/teoria#iam-identidades-y-permisos
L:
  concepto: aws-lambda
  seccion: 00-base-aws/teoria#servicios-centrales
E:
  concepto: amazon-ec2
  seccion: 00-base-aws/teoria#servicios-centrales
S:
  concepto: amazon-s3
  seccion: 00-base-aws/teoria#servicios-centrales
B:
  concepto: amazon-bedrock
  seccion: 00-base-aws/teoria#servicios-centrales
M:
  concepto: amazon-sagemaker-ai
  seccion: 00-base-aws/teoria#servicios-centrales
```

*Serverless* no significa que no existan servidores, sino que el cliente no los aprovisiona ni los gestiona.

### Responsabilidad compartida

La seguridad y el cumplimiento normativo son una responsabilidad compartida entre AWS y el cliente. El modelo se resume en dos expresiones:

- **Seguridad *de* la nube** (*security of the cloud*): responsabilidad de AWS. Protege la infraestructura que ejecuta los servicios: hardware, software, redes e instalaciones. Auditores independientes verifican periódicamente su eficacia.
- **Seguridad *en* la nube** (*security in the cloud*): responsabilidad del cliente, y **depende del servicio que use**. Incluye la sensibilidad de sus datos, los requisitos de su empresa y las leyes y normativas aplicables.

El reparto cambia con el servicio. Con Amazon EC2, un servicio de infraestructura (IaaS), el cliente gestiona el sistema operativo invitado (incluidas actualizaciones y parches), el software de aplicación y la configuración de los grupos de seguridad. Con los servicios abstraídos, como Amazon S3 o Amazon DynamoDB, AWS opera la infraestructura, el sistema operativo y la plataforma, y el cliente gestiona sus datos (incluidas las opciones de **cifrado**) y los permisos de IAM. Con un servicio gestionado como Amazon Bedrock, AWS asume más tareas operativas, pero el cliente sigue siendo responsable de sus datos, de quién accede a ellos y de cómo usa los resultados del modelo.

Algunos controles son **compartidos**: cada parte los aplica en su terreno. AWS parchea y configura su infraestructura, y el cliente, sus sistemas operativos invitados y sus aplicaciones. AWS forma a sus empleados, y el cliente, a los suyos.

```mermaid
flowchart LR
    subgraph Cliente["👤 EN la nube: el cliente"]
        direction TB
        D["🔐 Datos y su sensibilidad"]
        A["🪪 Accesos e identidades"]
        C["⚙️ Configuración y aplicaciones"]
        K["🔒 Cifrado y tráfico de red"]
    end
    subgraph AWS["☁️ DE la nube: AWS"]
        direction TB
        I["🧱 Hardware, software y red"]
        F["🏢 Instalaciones físicas"]
    end
    Cliente --> AWS
    class D,A,C,K proceso
    class I,F servicio
```

```nodos
Cliente:
  titulo: "Seguridad EN la nube: el cliente"
  texto: La responsabilidad del cliente depende del servicio que use. Incluye la sensibilidad de sus datos, los requisitos de su empresa y las leyes y normativas aplicables.
  enlaces:
    - {texto: "Seguridad en Amazon Bedrock y responsabilidad compartida", url: "https://docs.aws.amazon.com/bedrock/latest/userguide/security.html"}
    - {texto: "Responsabilidad compartida (Well-Architected)", url: "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/shared-responsibility.html"}
  seccion: 00-base-aws/teoria#responsabilidad-compartida
AWS:
  titulo: "Seguridad DE la nube: AWS"
  texto: AWS protege la infraestructura que ejecuta los servicios de la nube de AWS. Auditores independientes prueban y verifican de forma periódica la eficacia de esa seguridad.
  enlaces:
    - {texto: "Seguridad en Amazon Bedrock y responsabilidad compartida", url: "https://docs.aws.amazon.com/bedrock/latest/userguide/security.html"}
    - {texto: "Responsabilidad compartida (Well-Architected)", url: "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/shared-responsibility.html"}
  seccion: 00-base-aws/teoria#responsabilidad-compartida
D:
  titulo: Datos y su sensibilidad
  texto: El cliente es responsable de la sensibilidad de sus datos y de cumplir las leyes y normativas que les apliquen, con independencia del servicio de AWS que use.
  enlaces:
    - {texto: "Seguridad en Amazon Bedrock", url: "https://docs.aws.amazon.com/bedrock/latest/userguide/security.html"}
  seccion: 00-base-aws/teoria#responsabilidad-compartida
A:
  concepto: aws-iam
  titulo: Accesos e identidades (IAM)
  seccion: 00-base-aws/teoria#iam-identidades-y-permisos
C:
  titulo: Configuración y aplicaciones
  texto: En un servicio como Amazon EC2, el cliente gestiona el sistema operativo invitado (incluidas las actualizaciones y los parches de seguridad), el software de aplicación y la configuración del firewall de grupos de seguridad.
  enlaces:
    - {texto: "Responsabilidad compartida (Well-Architected)", url: "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/shared-responsibility.html"}
    - {texto: "Amazon EC2", url: "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html"}
  seccion: 00-base-aws/teoria#responsabilidad-compartida
K:
  titulo: Cifrado y protección del tráfico
  texto: 'El cliente decide y configura el cifrado de sus datos y la protección del tráfico de red, también en los servicios abstraídos como Amazon S3: AWS ofrece las herramientas (por ejemplo, AWS KMS para las claves), pero elegirlas y aplicarlas es tarea del cliente.'
  enlaces:
    - {texto: "Modelo de responsabilidad compartida", url: "https://aws.amazon.com/compliance/shared-responsibility-model/"}
  seccion: 00-base-aws/teoria#responsabilidad-compartida
I:
  titulo: Hardware, software y red
  texto: AWS opera, gestiona y controla los componentes desde el sistema operativo del anfitrión y la capa de virtualización hasta la seguridad física de las instalaciones donde funciona el servicio.
  enlaces:
    - {texto: "Responsabilidad compartida (Well-Architected)", url: "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/shared-responsibility.html"}
  seccion: 00-base-aws/teoria#responsabilidad-compartida
F:
  titulo: Instalaciones físicas
  texto: La seguridad física de las instalaciones donde funciona el servicio es responsabilidad de AWS.
  enlaces:
    - {texto: "Responsabilidad compartida (Well-Architected)", url: "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/shared-responsibility.html"}
  seccion: 00-base-aws/teoria#responsabilidad-compartida
```

El Dominio 5 retoma este modelo aplicado a los sistemas de IA.

### IAM: identidades y permisos

AWS Identity and Access Management (IAM) es el servicio que controla de forma segura el acceso a los recursos de AWS: quién está **autenticado** (ha iniciado sesión) y quién está **autorizado** (tiene permisos) a usar qué recursos.

- Al crear una cuenta de AWS se empieza con una identidad de inicio de sesión, el **usuario raíz** (*root user*), con acceso completo. AWS recomienda no usarlo en las tareas diarias; para ellas se crean otras identidades (administradores, analistas, desarrolladores) con solo los permisos que necesitan.
- La autenticación asocia las credenciales a una entidad de confianza (*principal*): un usuario de IAM, una entidad federada, un **rol de IAM** o una aplicación. Después, la solicitud se autoriza si las políticas aplicables conceden el permiso.
- **Mínimo privilegio** (*least privilege*): conceder solo los permisos imprescindibles para cada tarea. Es la práctica recomendada central de IAM.
- Otras prácticas recomendadas: exigir **credenciales temporales** a las personas (federación con un proveedor de identidad) y a las cargas de trabajo (roles de IAM), exigir autenticación multifactor (MFA) y revisar y eliminar periódicamente usuarios, roles y permisos sin uso.
- Los permisos se escriben en **políticas** (documentos JSON que permiten o deniegan acciones sobre recursos). Las **basadas en identidad** se asocian a usuarios, grupos o roles; las **basadas en recursos** se asocian al propio recurso (por ejemplo, un bucket de S3). Un **grupo** reúne usuarios que comparten permisos; un **rol** no tiene credenciales permanentes: lo asume quien lo necesita (una persona federada, una función Lambda o un servicio de AWS) y recibe credenciales temporales.
- **IAM Access Analyzer** ayuda a revisar los permisos: detecta recursos compartidos con entidades externas a la cuenta u organización y accesos concedidos que no se usan, y puede generar políticas a partir de la actividad real registrada en AWS CloudTrail.
- IAM es **eventualmente consistente**: un cambio de permisos puede tardar un poco en replicarse y no debe formar parte de rutas críticas de una aplicación.

En los sistemas de IA, IAM decide quién puede invocar un modelo, leer los datos de entrenamiento o administrar un endpoint; se profundiza en el módulo 05.

**Ejemplo.** Una función Lambda que resume documentos con Amazon Bedrock no debe llevar claves de acceso en el código: se le asigna un **rol de IAM** cuya política solo permite invocar el modelo concreto que usa (mínimo privilegio) y leer el bucket de S3 de entrada.

Cómo decide IAM si una petición sigue adelante:

```mermaid
flowchart LR
    P["🪪 <b>Principal</b><br/>usuario, rol, federado o aplicación"] --> AU{"🔑 <b>Autenticación</b><br/>¿credenciales válidas?"}
    AU -->|"no"| N["⛔ <b>Petición rechazada</b>"]
    AU -->|"sí"| AZ{"📜 <b>Autorización</b><br/>¿las políticas lo permiten?"}
    PI["👤 <b>Política basada en identidad</b><br/>de un usuario, grupo o rol"] -.-> AZ
    PR["🪣 <b>Política basada en recurso</b><br/>por ejemplo, de un bucket de S3"] -.-> AZ
    AZ -->|"no"| N
    AZ -->|"sí"| OK["✅ <b>Acción permitida</b>"]
    class P dato
    class AU,AZ decision
    class N aviso
    class PI,PR proceso
    class OK accion
```

```nodos
P:
  titulo: Principal
  texto: 'La entidad que hace la petición: un usuario de IAM, una entidad federada, un rol de IAM o una aplicación. Ejemplo del apartado: una función Lambda que usa un rol de IAM, sin claves en el código.'
  enlaces:
  - texto: Qué es IAM
    url: https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html
  seccion: 00-base-aws/teoria#iam-identidades-y-permisos
AU:
  concepto: aws-iam
  titulo: Autenticación
  texto: 'Asocia las credenciales a una entidad de confianza: ¿quién eres? Las prácticas recomendadas piden credenciales temporales (federación y roles) y MFA.'
N:
  titulo: Petición rechazada
  texto: Sin autenticación, o sin una política que conceda el permiso, la petición no sigue adelante.
AZ:
  concepto: politica-de-iam
  titulo: Autorización
  texto: Una vez autenticada, la petición se autoriza si las políticas aplicables conceden el permiso para esa acción sobre ese recurso.
PI:
  concepto: politica-de-iam
  titulo: Política basada en identidad
  texto: 'Documento JSON asociado a un usuario, un grupo o un rol: qué acciones puede hacer sobre qué recursos.'
  enlaces:
  - texto: Políticas y permisos en IAM
    url: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html
PR:
  concepto: politica-de-iam
  titulo: Política basada en recurso
  texto: 'Documento JSON asociado al propio recurso, por ejemplo un bucket de S3: quién puede acceder a él.'
  enlaces:
  - texto: Políticas y permisos en IAM
    url: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html
OK:
  concepto: minimo-privilegio
  titulo: Acción permitida
  texto: 'La petición se ejecuta. Buena práctica al escribir las políticas: mínimo privilegio, solo los permisos imprescindibles. En el ejemplo, el rol de la Lambda solo puede invocar el modelo que usa y leer el bucket de entrada.'
  enlaces:
  - texto: Prácticas recomendadas de IAM
    url: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
```

### Modelos de precios

AWS factura por el uso de cada servicio, y cada servicio ofrece sus propias opciones. Para el examen basta reconocer la lógica general: **pagar por uso**, **comprometerse a cambio de descuento** o **aprovechar capacidad sobrante**.

| Idea | Ejemplo verificado en la documentación |
|---|---|
| Pago por uso, sin compromiso | Amazon EC2 *On-Demand*: se paga por segundo por las instancias lanzadas |
| Compromiso de uso a 1 o 3 años a cambio de menor coste | *Savings Plans* (compromiso en USD por hora; hay varios tipos, entre ellos de cómputo, de instancias de EC2 y de **SageMaker AI**) y *Reserved Instances* de EC2 (configuración concreta). El compromiso no se puede cambiar después de comprarlo |
| Capacidad sobrante a coste reducido | Amazon EC2 *Spot Instances*: instancias sin usar, con un coste significativamente menor. AWS puede recuperarlas avisando con **dos minutos** de antelación, así que solo son rentables si la aplicación es flexible en cuándo se ejecuta y admite interrupciones |
| Servidor físico dedicado | Amazon EC2 *Dedicated Hosts*: un servidor físico solo para el cliente. Permite reutilizar licencias de software por socket, por núcleo o por máquina virtual, o cumplir un requisito de hardware dedicado |
| Elegir la clase de almacenamiento según el patrón de acceso | Amazon S3: clase Standard por defecto y otras clases para datos de acceso infrecuente, raro o cambiante (*Intelligent-Tiering*) |
| Capacidad reservada con facturación por horas | Amazon Bedrock *Provisioned Throughput*: rendimiento fijo, facturado por horas |

Qué opción de pago encaja según cómo se usa el recurso:

```mermaid
flowchart TB
    U["💳 <b>¿Cómo se va a usar?</b>"] --> F{"⏸️ <b>¿Admite interrupciones<br/>y horario flexible?</b>"}
    F -->|"sí"| SPOT["🏷️ <b>Spot Instances</b><br/>capacidad sobrante, más barata"]
    F -->|"no"| E{"📅 <b>¿Uso estable<br/>y duradero?</b>"}
    E -->|"sí, en EC2"| SP["🤝 <b>Savings Plans o Reserved Instances</b><br/>compromiso de 1 o 3 años"]
    E -->|"sí, en Bedrock: tráfico alto<br/>o modelo personalizado"| PT["📦 <b>Provisioned Throughput</b><br/>se paga por horas aunque no se use"]
    E -->|"no: variable o imprevisible"| OD["⏱️ <b>On-Demand</b><br/>pago por uso, sin compromiso"]
    class U dato
    class F,E decision
    class OD,SP,PT,SPOT servicio
```

```nodos
U:
  titulo: Patrón de uso
  texto: 'La lógica general de precios de AWS: pagar por uso, comprometerse a cambio de descuento o aprovechar capacidad sobrante. Cada servicio ofrece sus propias opciones.'
  seccion: 00-base-aws/teoria#modelos-de-precios
F:
  titulo: Cargas flexibles
  texto: Si la carga puede ejecutarse cuando haya capacidad y tolera interrupciones (por ejemplo, un trabajo por lotes), aprovecha la capacidad sobrante, aunque su volumen sea variable.
SPOT:
  concepto: spot-instances
E:
  titulo: Uso estable
  texto: Si el consumo es predecible y se mantiene en el tiempo, comprometerse sale más barato. Si es variable o imprevisible, lo prudente es no comprometerse.
SP:
  concepto: savings-plans
  titulo: Savings Plans o Reserved Instances
  texto: 'Compromiso de uso a 1 o 3 años a cambio de menor coste: los Savings Plans se comprometen en USD por hora; las Reserved Instances, con una configuración concreta.'
  enlaces:
  - texto: Opciones de compra de EC2
    url: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html
PT:
  concepto: provisioned-throughput
  texto: 'Capacidad reservada de Amazon Bedrock con rendimiento fijo, facturada por horas: para tráfico alto y estable, o para un modelo personalizado. Lo aprovisionado se paga aunque no se use.'
OD:
  concepto: on-demand
```

#### Cómo se pagan los servicios de IA

Cada familia de servicios de IA tiene su propia unidad de facturación. Reconocerla ayuda a responder preguntas de coste:

| Tipo de servicio | Qué se paga | Ejemplo |
|---|---|---|
| Modelos fundacionales en Amazon Bedrock | *On-demand*: por *tokens* de entrada y de salida, sin compromiso. *Batch*: procesamiento por lotes, con un precio menor que *on-demand* en los modelos que lo admiten. *Provisioned Throughput*: capacidad reservada por horas | Un asistente con tráfico variable usa *on-demand*; uno con tráfico alto y estable, o un modelo personalizado, *Provisioned Throughput* |
| Amazon SageMaker AI | El tiempo de uso de las instancias que se eligen para entrenar y para alojar el modelo | Un *endpoint* en tiempo real factura mientras sus instancias están en marcha, aunque no reciba peticiones |
| Servicios de IA especializados | Por unidad procesada: caracteres (Translate, Polly), unidades de texto (Comprehend), duración del audio (Transcribe), imágenes o páginas | Traducir un millón de caracteres con Translate |
| *Serverless* (AWS Lambda) | Por número de peticiones y duración de la ejecución | No se paga nada mientras no hay invocaciones |

La idea que el examen explota: **lo aprovisionado se paga aunque no se use** (instancias de un *endpoint*, *Provisioned Throughput*), mientras que lo **bajo demanda** se paga solo por uso. La comparación de opciones de Bedrock se desarrolla en los módulos 02 y 03.

#### Controlar el gasto

- **AWS Pricing Calculator**: herramienta web gratuita para **estimar antes de desplegar** cuánto costará una arquitectura, según los servicios, la Región y el uso previsto. Es una estimación (no incluye impuestos): el coste real depende del uso.
- **AWS Budgets**: define un presupuesto y avisa cuando el gasto real o previsto lo supera. Es lo primero que conviene configurar antes de un laboratorio.
- **AWS Cost Explorer**: muestra y analiza el gasto histórico por servicio y su tendencia.
- **Capa gratuita (*Free Tier*)**: desde julio de 2025, las cuentas nuevas reciben créditos (100 USD al crearla, ampliables hasta 200 USD) y eligen entre un plan gratuito de hasta seis meses y un plan de pago. Algunos servicios mantienen además una cuota gratuita mensual permanente. Comprueba siempre las condiciones de tu cuenta.

Los precios concretos no se citan en este curso; consúltalos siempre en las páginas oficiales de precios de cada servicio.

## Puntos clave para el examen

- La nube es la entrega bajo demanda de recursos de TI por internet con pago por uso. Modelos de despliegue: nube, híbrido (nube y centro de datos propio conectados) y local. Tipos de servicio: IaaS (EC2), PaaS y SaaS, de menos a más gestionado por el proveedor.
- Una Región contiene al menos tres zonas de disponibilidad, y cada una tiene uno o varios centros de datos. Repartir entre varias AZ da alta disponibilidad; las Local Zones y las ubicaciones de borde (CloudFront) reducen la latencia.
- AWS protege la infraestructura (seguridad *de* la nube); el cliente protege sus datos, accesos y configuración (seguridad *en* la nube), y el reparto depende del servicio.
- Cuanto más gestionado es el servicio (por ejemplo, Lambda o Bedrock), menos tareas operativas asume el cliente, pero nunca deja de ser responsable de sus datos y de sus permisos.
- El usuario raíz no se usa en el día a día; se usan identidades con permisos mínimos.
- A las cargas de trabajo se les dan permisos mediante **roles de IAM** (credenciales temporales), no con claves de acceso permanentes.
- *Serverless* quiere decir «sin gestionar servidores», no «sin servidores».
- La disponibilidad de servicios y modelos depende de la Región elegida.
- Pago por uso (*On-Demand*) frente a compromiso (*Savings Plans*, *Reserved Instances*) frente a capacidad sobrante (*Spot*, con aviso de dos minutos antes de recuperarla) son las tres lógicas de precio que hay que reconocer. Pricing Calculator estima antes de desplegar; Budgets avisa después. En IA: *tokens* en Bedrock, tiempo de instancia en SageMaker AI y unidades procesadas en los servicios especializados.
- Lo aprovisionado (un *endpoint* encendido, *Provisioned Throughput*) se paga aunque no se use; AWS Budgets avisa antes de que el gasto se dispare.
- Amazon SageMaker AI es el nombre actual del servicio de ML que se llamaba Amazon SageMaker; «Amazon SageMaker» designa ahora una plataforma unificada más amplia.

## Referencias

Documentación oficial consultada el 14 de octubre de 2026 (las marcadas con «2026-11-20», en la revisión con las guías de estudio):

- Guía del examen AIF-C01, «Recommended AWS knowledge»: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html>
- Qué es la computación en la nube (2026-11-20): <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/what-is-cloud-computing.html>
- Seis ventajas de la computación en la nube (2026-11-20): <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/six-advantages-of-cloud-computing.html>
- Modelos de despliegue (2026-11-20): <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/types-of-cloud-computing.html>
- IaaS, PaaS y SaaS (2026-11-20): <https://aws.amazon.com/types-of-cloud-computing/>
- Infraestructura global (2026-11-20): <https://docs.aws.amazon.com/whitepapers/latest/aws-overview/global-infrastructure.html>
- Zonas de disponibilidad (2026-11-20): <https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-availability-zones.html>
- AWS Local Zones (2026-11-20): <https://docs.aws.amazon.com/local-zones/latest/ug/what-is-aws-local-zones.html>
- AWS Outposts (2026-11-20): <https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html>
- Amazon CloudFront y ubicaciones de borde (2026-11-20): <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html>
- Modelo de responsabilidad compartida (2026-11-20): <https://aws.amazon.com/compliance/shared-responsibility-model/>
- IAM Access Analyzer (2026-11-20): <https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html>
- Avisos de interrupción de Spot (2026-11-20): <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html>
- Dedicated Hosts (2026-11-20): <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html>
- Savings Plans (2026-11-20): <https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html>
- AWS Pricing Calculator (2026-11-20): <https://docs.aws.amazon.com/pricing-calculator/latest/userguide/what-is-pricing-calculator.html>
- Regiones de AWS: <https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html>
- Amazon EC2, ¿qué es?: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html>
- Amazon EC2, opciones de facturación y compra: <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html>
- Amazon S3, ¿qué es?: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>
- Amazon S3, clases de almacenamiento: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html>
- AWS Lambda, ¿qué es?: <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>
- Amazon Bedrock, visión general: <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>
- Amazon Bedrock, seguridad y modelo de responsabilidad compartida: <https://docs.aws.amazon.com/bedrock/latest/userguide/security.html>
- Amazon Bedrock, Provisioned Throughput: <https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html>
- Amazon SageMaker AI, ¿qué es?: <https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html>
- AWS Well-Architected, responsabilidad compartida: <https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/shared-responsibility.html>
- IAM, ¿qué es?: <https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html>
- IAM, prácticas recomendadas de seguridad: <https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html>
- IAM, políticas y permisos: <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html>
- Amazon VPC: <https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html>
- Amazon CloudWatch: <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html>
- AWS CloudTrail: <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html>
- Precios de Amazon Bedrock (modos *on-demand*, *batch* y *Provisioned Throughput*): <https://aws.amazon.com/bedrock/pricing/>
- Precios de Amazon SageMaker AI: <https://aws.amazon.com/sagemaker/ai/pricing/>
- Precios de AWS Lambda: <https://aws.amazon.com/lambda/pricing/>
- AWS Budgets: <https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html>
- AWS Cost Explorer: <https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html>
- Capa gratuita de AWS: <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html>
