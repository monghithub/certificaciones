# Servicios del módulo 00

Servicios dentro de alcance que el examen da por conocidos. La columna final indica cuándo **no** conviene usarlos, que es lo que suelen explotar los distractores.

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon EC2 | Servidores virtuales cuando se necesita control del sistema operativo, de la red y del almacenamiento (por ejemplo, para alojar un modelo propio) | Cuando basta un servicio gestionado y no se quiere asumir parches, actualizaciones ni configuración del servidor |
| Amazon S3 | Almacenamiento de objetos: lagos de datos, copias de seguridad y restauración, sitios web y analítica de datos | Como base de datos transaccional o como sistema de ficheros de baja latencia para un servidor |
| AWS Lambda | Ejecutar código en respuesta a eventos sin gestionar servidores (por ejemplo, invocar un modelo cuando llega un fichero) | Cuando se necesita control sobre el servidor o el sistema operativo |
| AWS Identity and Access Management (IAM) | Definir quién puede hacer qué sobre qué recursos: usuarios, roles y políticas | No es un servicio de datos ni de cómputo: no sustituye al cifrado ni a las políticas de la propia aplicación |
| Amazon Bedrock | Usar modelos fundacionales de varios proveedores mediante API, sin gestionar la infraestructura | Cuando se necesita entrenar un modelo propio desde cero o controlar toda la infraestructura de entrenamiento |
| Amazon SageMaker AI | Construir, entrenar y desplegar modelos de aprendizaje automático propios | Cuando un servicio de IA preentrenado o gestionado resuelve el caso con menos esfuerzo |
| Amazon VPC | Aislar en una red privada los recursos propios (por ejemplo, un *endpoint* de modelo) | No es un servicio de cómputo ni de almacenamiento: solo define la red |
| Amazon CloudWatch | Métricas, registros y alarmas sobre el funcionamiento de recursos y aplicaciones | Para saber quién hizo una llamada a la API (es AWS CloudTrail) |
| AWS CloudTrail | Auditar la actividad de la cuenta: quién hizo qué llamada a la API y cuándo | Para vigilar la latencia o el uso de CPU (es Amazon CloudWatch) |
| AWS Budgets | Presupuestos de coste o uso con alertas al superarlos | Para analizar en detalle el gasto histórico (es AWS Cost Explorer) |
| AWS Cost Explorer | Visualizar y analizar el gasto por servicio y su tendencia | Para recibir una alerta automática al superar un umbral (es AWS Budgets) |

Referencias: las de [README.md](README.md#referencias).
