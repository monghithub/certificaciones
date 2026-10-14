# Trampas habituales del módulo 00

## Responsabilidad compartida

- **«AWS se encarga de toda la seguridad».** Falso: AWS protege la infraestructura (seguridad *de* la nube); el cliente protege sus datos, accesos y configuración (seguridad *en* la nube).
- **«El reparto es siempre el mismo».** Falso: la responsabilidad del cliente **depende del servicio**. En EC2 incluye el sistema operativo invitado y sus parches; en un servicio gestionado, menos tareas operativas, pero nunca los datos ni los permisos.
- **Confundir *de* y *en*.** *Security of the cloud* es de AWS; *security in the cloud* es del cliente.

## IAM

- **Usar el usuario raíz a diario.** La recomendación es no usarlo para las tareas cotidianas.
- **Claves de acceso permanentes para una aplicación.** Lo recomendado para cargas de trabajo son los **roles de IAM** con credenciales temporales.
- **Dar permisos amplios «por si acaso».** El criterio correcto es el **mínimo privilegio**.
- **Confundir grupo y rol.** Un grupo reúne usuarios con permisos comunes; un rol lo *asume* una persona, una aplicación o un servicio y da credenciales temporales.
- **Esperar que un cambio de permisos sea instantáneo.** IAM es eventualmente consistente.

## Servicios

- **Serverless no es «sin servidores».** Significa que el cliente no los aprovisiona ni los gestiona.
- **S3 es almacenamiento de objetos**, no una base de datos ni un disco de un servidor.
- **La Región importa.** No todos los servicios, modelos y funcionalidades están en todas las Regiones: hay que comprobarlo antes de elegir.
- **SageMaker frente a SageMaker AI.** El servicio de ML que antes se llamaba Amazon SageMaker se llama Amazon SageMaker AI desde el 3 de diciembre de 2024. Desde ese día, «Amazon SageMaker» es otra cosa: una plataforma unificada de datos, analítica e IA que incluye SageMaker AI. Si un enunciado habla de entrenar o desplegar un modelo, se refiere a SageMaker AI.
- **CloudWatch frente a CloudTrail.** CloudWatch responde «¿cómo funciona?» (métricas, registros, alarmas); CloudTrail responde «¿quién hizo qué?» (auditoría de llamadas a la API).

## Precios

- **Confundir On-Demand con compromiso.** On-Demand no exige compromiso; *Savings Plans* y *Reserved Instances* sí (1 o 3 años).
- **Usar *Spot* para una carga que no admite interrupciones.** *Spot* aprovecha capacidad sobrante a menor coste y es rentable si la aplicación es flexible en cuándo se ejecuta y puede interrumpirse.
- **Pensar que un *endpoint* sin tráfico no cuesta.** Lo aprovisionado (instancias de un *endpoint* de SageMaker AI, *Provisioned Throughput* de Bedrock) se factura mientras existe, se use o no.
- **Confundir Budgets con Cost Explorer.** Budgets avisa al superar un umbral; Cost Explorer analiza el gasto.
- **Dar precios por sabidos.** Los precios cambian y dependen de la Región: se consultan en las páginas oficiales, no se memorizan.
