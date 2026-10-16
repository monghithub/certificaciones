# Laboratorio: mínimo privilegio, registro y auditoría en Amazon Bedrock

Laboratorio **práctico y opcional** (duración orientativa: 45–60 minutos). Se crea una política de IAM que solo permite invocar un modelo concreto de Amazon Bedrock, se comprueba que otro modelo queda denegado, se activa el registro de invocaciones en Amazon CloudWatch Logs y se audita la actividad con el registro y con el historial de eventos de AWS CloudTrail. No se crean recursos con coste por hora, y todo se borra al final.

## Objetivo y relación con el examen

Ver en la práctica cómo se combinan los permisos, el registro y la auditoría para proteger y gobernar una aplicación de IA generativa.

| Tarea del examen | Qué refuerza el laboratorio |
|---|---|
| 5.1.1 (servicios para proteger) | Políticas y roles de IAM con mínimo privilegio para un modelo de Bedrock |
| 5.1.4 (seguridad y privacidad) | Registro y auditoría de las interacciones con el modelo; datos sensibles en los registros |
| 5.2.1 (servicios de gobierno) | CloudTrail para saber quién llamó a la API |
| 5.2.2 (gobierno de datos) | Registro, monitorización y retención de los registros |

## Requisitos previos

- Una cuenta de AWS y un usuario administrador **distinto del usuario raíz** para preparar el laboratorio (crear la política, el usuario de prueba, el grupo de registros y la configuración de Bedrock).
- **Región recomendada:** US East (N. Virginia), `us-east-1`.
- **Modelo:** Amazon **Nova Micro** con su perfil de inferencia de EE. UU. `us.amazon.nova-micro-v1:0`, como en los laboratorios anteriores. Con Amazon Nova no hace falta solicitar acceso al modelo.
- AWS CLI v2 configurada (`aws configure`) con un perfil de administrador y otro para el usuario de prueba (partes 2 y 5).
- Tu ID de cuenta de 12 dígitos (aparece arriba a la derecha en la consola). En los ejemplos se usa `111122223333`: sustitúyelo.

## Estimación de coste y aviso de facturación

> **Aviso de facturación.** Amazon Bedrock y CloudWatch Logs se facturan por uso. Aunque este laboratorio genera un coste mínimo, **eres responsable de lo que uses en tu cuenta**. Configura antes de empezar un presupuesto con alerta en **AWS Budgets** (por ejemplo, de 1 USD) y revisa el panel de facturación al terminar.

- **Modelo:** consulta el precio de Nova Micro en la [página de precios de Amazon Bedrock](https://aws.amazon.com/bedrock/pricing/). Las pruebas suman menos de 10 000 *tokens*; aunque se pagaran 2 USD por millón, serían **0,02 USD**.
- **CloudWatch Logs:** se cobra por GB ingerido y almacenado ([precios de CloudWatch](https://aws.amazon.com/cloudwatch/pricing/)); en los ejemplos de esa página, la ingesta estándar cuesta 0,50 USD por GB por encima de los 5 GB gratuitos. El laboratorio genera menos de 1 MB: aunque se pagara todo, sería menos de **0,001 USD**. La retención del grupo se fija en 1 día.
- **IAM y el historial de eventos de CloudTrail** no tienen coste.
- **Capa gratuita:** las cuentas nuevas reciben créditos y eligen entre un plan gratuito de hasta seis meses o un plan de pago; el plan gratuito no da acceso a ciertos servicios. Comprueba antes si Amazon Bedrock está disponible en tu plan: <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html>.
- **No hay recursos que generen coste por hora.** No se crean *trails* de CloudTrail (el historial de eventos ya existe y es gratuito), Knowledge Bases, *endpoints* ni *Provisioned Throughput*.

## Parte 1: política de mínimo privilegio

1. En la consola de **IAM**, elige **Policies** → **Create policy** → pestaña **JSON** y pega esta política. Permite invocar **solo** Nova Micro y **solo** a través de su perfil de inferencia de EE. UU. Como indica la guía de perfiles de inferencia, hace falta permitir el perfil y el modelo en cada Región a la que el perfil puede enviar la petición; aquí se usa `*` en la Región del modelo y la condición `bedrock:InferenceProfileArn` para que el modelo solo se pueda usar a través de ese perfil.

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "PerfilNovaMicro",
         "Effect": "Allow",
         "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
         "Resource": "arn:aws:bedrock:us-east-1:111122223333:inference-profile/us.amazon.nova-micro-v1:0"
       },
       {
         "Sid": "ModeloNovaMicroSoloPorElPerfil",
         "Effect": "Allow",
         "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
         "Resource": "arn:aws:bedrock:*::foundation-model/amazon.nova-micro-v1:0",
         "Condition": {
           "StringLike": {
             "bedrock:InferenceProfileArn": "arn:aws:bedrock:us-east-1:111122223333:inference-profile/us.amazon.nova-micro-v1:0"
           }
         }
       }
     ]
   }
   ```

2. Llama a la política `lab-bedrock-solo-nova-micro` y créala.
3. En **Users** → **Create user**, crea `lab-auditoria` **sin acceso a la consola**, adjúntale solo esa política y, en la pestaña **Security credentials**, crea una **clave de acceso** para la CLI. Guárdala en un perfil de la CLI: `aws configure --profile lab-auditoria`.

> En un entorno real se preferirían roles y credenciales temporales (por ejemplo, con IAM Identity Center) a claves de acceso de larga duración. Aquí se usa una clave solo para el laboratorio y se borra al final.

## Parte 2: comprobar el permiso y la denegación

Con el perfil del usuario de prueba, invoca el modelo permitido y uno que no lo está. La API Converse llama a la acción `bedrock:InvokeModel`.

```bash
# 1. Permitido: Nova Micro a través de su perfil de inferencia
aws bedrock-runtime converse --profile lab-auditoria --region us-east-1 \
  --model-id us.amazon.nova-micro-v1:0 \
  --messages '[{"role":"user","content":[{"text":"Resume en una frase qué es el mínimo privilegio."}]}]'

# 2. Denegado: otro modelo de Amazon Nova que la política no incluye
aws bedrock-runtime converse --profile lab-auditoria --region us-east-1 \
  --model-id us.amazon.nova-lite-v1:0 \
  --messages '[{"role":"user","content":[{"text":"Hola"}]}]'
```

La primera llamada devuelve una respuesta. La segunda termina con un error **AccessDeniedException**: el usuario no tiene permiso para ese modelo. Esa es la idea del mínimo privilegio: cada identidad puede hacer solo lo que necesita. (Si la segunda devuelve otro error, por ejemplo porque ese perfil no existe en tu Región, prueba con otro modelo de texto de Amazon Nova).

## Parte 3: activar el registro de invocaciones

1. En la consola de **CloudWatch** → **Log groups** → **Create log group**, crea `lab-bedrock-invocaciones` con **retención de 1 día**. Recuerda que, por defecto, los grupos de registros guardan los datos indefinidamente.
2. En la consola de **Amazon Bedrock** (`us-east-1`) → **Settings** → **Model invocation logging**, activa el registro:
   - Modalidades: solo **Text**.
   - Destino: **CloudWatch Logs only**, con el grupo `lab-bedrock-invocaciones`.
   - Rol: deja que la consola cree un rol de servicio nuevo, si lo ofrece, o crea uno con la relación de confianza y la política que indica la guía de registro de invocaciones (permiso `logs:CreateLogStream` y `logs:PutLogEvents` sobre ese grupo, y confianza en `bedrock.amazonaws.com`). Anota su nombre para la limpieza.
3. Guarda la configuración.

## Parte 4: auditar la actividad

1. Repite la llamada permitida de la parte 2 (la de Nova Micro), esta vez escribiendo en el *prompt* un dato inventado como «mi teléfono es 600 000 000».
2. En **CloudWatch** → `lab-bedrock-invocaciones`, abre el flujo de registros (`aws/bedrock/modelinvocations`). En el evento verás, entre otros campos:
   - la **identidad** que hizo la petición (`identity.arn`, con el usuario `lab-auditoria`);
   - el **modelo**, la **entrada** (tu *prompt*, con el teléfono tal cual) y la **salida**;
   - los *tokens* de entrada y de salida.
3. En la consola de **CloudTrail** → **Event history**, filtra por **Event name** = `Converse` (o por **User name** = `lab-auditoria`). Verás quién llamó, cuándo, desde qué IP y a qué modelo, pero **no** el texto del *prompt*. Bedrock registra `InvokeModel` y `Converse` como eventos de administración, por eso aparecen en el historial sin configurar nada. La llamada denegada de la parte 2 también aparece, con su código de error.

| Pregunta de auditoría | Dónde se responde |
|---|---|
| ¿Quién invocó el modelo y cuándo? | **CloudTrail** (y la identidad del registro de invocaciones) |
| ¿Qué se preguntó y qué respondió el modelo? | **Registro de invocaciones de Bedrock** |
| ¿Alguien intentó usar un modelo sin permiso? | **CloudTrail** (error de acceso denegado) |

## Parte 5: equivalente con la AWS CLI (opcional)

Con el perfil de administrador:

```bash
# Ver la configuración del registro de invocaciones
aws bedrock get-model-invocation-logging-configuration --region us-east-1

# Buscar en el historial de CloudTrail las llamadas del usuario de prueba
aws cloudtrail lookup-events --region us-east-1 \
  --lookup-attributes AttributeKey=Username,AttributeValue=lab-auditoria \
  --max-results 10 --query 'Events[].[EventTime,EventName]'
```

## Preguntas para reflexionar

1. **¿Por qué el registro de invocaciones guarda el teléfono aunque tuvieras un *guardrail* que lo enmascara?** *Respuesta orientativa:* el enmascarado de Guardrails solo afecta a lo que entra al modelo y a lo que devuelve; el registro de invocaciones guarda la petición original. Por eso los registros deben protegerse (permisos, retención corta, protección de datos de CloudWatch Logs).
2. **¿Qué ventaja tiene permitir el modelo solo a través del perfil de inferencia?** *Respuesta orientativa:* se controla exactamente por dónde y a qué modelo se accede; si alguien intenta invocar el modelo directamente o por otro perfil, se deniega.
3. **¿CloudTrail o el registro de invocaciones para investigar una respuesta ofensiva del asistente?** *Respuesta orientativa:* el registro de invocaciones, que guarda el contenido. CloudTrail dice quién llamó y cuándo, pero no qué se dijo.
4. **¿Qué pasaría con los registros si no fijaras la retención?** *Respuesta orientativa:* CloudWatch Logs los guardaría indefinidamente, con su coste y su riesgo si contienen datos personales. La retención forma parte del gobierno de los datos.

## Limpieza de recursos

1. En **Amazon Bedrock** → **Settings**, **desactiva** el registro de invocaciones y guarda. Con la CLI: `aws bedrock delete-model-invocation-logging-configuration --region us-east-1`.
2. En **CloudWatch** → **Log groups**, borra `lab-bedrock-invocaciones`.
3. En **IAM**:
   - borra la clave de acceso y el usuario `lab-auditoria`;
   - borra la política `lab-bedrock-solo-nova-micro`;
   - borra el rol de servicio que creaste para el registro (y su política, si la creaste aparte).
4. Borra el perfil `lab-auditoria` de la CLI (`~/.aws/credentials` y `~/.aws/config`).
5. Revisa el panel de facturación al día siguiente y mantén la alerta de AWS Budgets.

No quedan otros recursos: el laboratorio no crea *trails* de CloudTrail, *buckets*, Knowledge Bases, *endpoints* ni *Provisioned Throughput*.

## Referencias

- Requisitos de los perfiles de inferencia (permisos): <https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-prereq.html>
- Registro de invocaciones de modelos: <https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html>
- Bedrock y CloudTrail: <https://docs.aws.amazon.com/bedrock/latest/userguide/logging-using-cloudtrail.html>
- Historial de eventos de CloudTrail: <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html>
- Retención en CloudWatch Logs: <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>
- Filtros de información sensible (alcance del enmascarado): <https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html>
- Precios de Amazon Bedrock: <https://aws.amazon.com/bedrock/pricing/>
- Precios de Amazon CloudWatch: <https://aws.amazon.com/cloudwatch/pricing/>
