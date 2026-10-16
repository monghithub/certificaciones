# Trampas habituales del módulo 05

## Proteger sistemas de IA

- **AWS se encarga de toda la seguridad de Bedrock.** AWS protege la nube; el cliente sigue siendo responsable de sus datos, permisos, cifrado con sus claves, red, *guardrails* y registros.
- **Bedrock usa mis *prompts* para entrenar modelos.** AWS y los proveedores no usan las entradas ni las salidas de Bedrock para entrenar modelos, y no se comparten con los proveedores.
- **PrivateLink cifra los datos.** PrivateLink mantiene el tráfico **fuera de Internet**; el cifrado en tránsito es TLS y el cifrado en reposo, KMS.
- **Macie frente a Guardrails.** Macie busca datos sensibles **almacenados en S3**; el filtro de información sensible de Guardrails actúa sobre **las entradas y respuestas** del modelo en tiempo real.
- **KMS frente a Secrets Manager.** KMS gestiona **claves de cifrado**; Secrets Manager guarda **secretos** (claves de API, contraseñas) y los rota.
- **AgentCore Identity frente a Policy in AgentCore.** Identity responde a **quién es el agente y con qué credenciales** accede en nombre del usuario; Policy decide **qué puede hacer** con cada herramienta.
- **Guardrails sustituye a IAM.** Guardrails filtra contenido; IAM decide quién accede a qué. Hacen falta los dos.
- **El modelo protege los datos que recibe.** Un modelo fundacional no tiene control de acceso a los datos del contexto: los permisos se aplican **antes** de añadir datos al *prompt*.

## Datos, origen y alucinaciones

- **Citas frente a linaje.** Las citas dicen de qué documento sale **una respuesta**; el linaje dice con qué datos y pasos se construyó **un modelo**.
- **Glue Data Catalog frente a Lake Formation.** El catálogo **describe** los datos (ubicación, esquema); Lake Formation **controla quién accede** a ellos con detalle.
- **Borrar un dato del modelo es fácil.** Si un dato personal se usó para ajustar el modelo, la forma eficaz de quitarlo es reentrenar sin él. Mejor no meter PII en el entrenamiento y aportarla en la inferencia con RAG.
- **Temperatura 0 elimina las alucinaciones.** Hace la respuesta menos variable, no más veraz. Contra las alucinaciones: RAG con citas, *grounding check*, Automated Reasoning, validación y confianza.
- ***Grounding* alto basta.** La comprobación de Guardrails mide **dos** cosas: si la respuesta se basa en la fuente (*grounding*) y si responde a la pregunta (relevancia). Puede fallar por cualquiera de las dos.

## Gobierno y cumplimiento

- **Si Guardrails enmascara la PII, los registros quedan limpios.** El enmascarado solo afecta a la entrada del modelo y a su respuesta; el registro de invocaciones guarda la petición original. Hay que proteger los registros (protección de datos de CloudWatch Logs, permisos, retención).
- **Config frente a CloudTrail.** Config: **cómo está configurado** un recurso y cómo cambió. CloudTrail: **quién hizo** una llamada a la API y cuándo.
- **CloudTrail guarda los *prompts*.** CloudTrail registra la llamada a `InvokeModel`, no su contenido. El texto de las peticiones y respuestas se guarda con el **registro de invocaciones de Bedrock**, desactivado por defecto.
- **Artifact certifica mi aplicación.** Artifact ofrece los informes de cumplimiento **de AWS**; el cumplimiento de la aplicación del cliente es responsabilidad del cliente.
- **Inspector frente a Trusted Advisor.** Inspector **escanea vulnerabilidades** de *software*; Trusted Advisor da **recomendaciones** de buenas prácticas (coste, seguridad, límites).
- **Audit Manager para un proyecto nuevo.** Ya no admite clientes nuevos.
- **Los registros se borran solos.** Los grupos de CloudWatch Logs guardan los datos **indefinidamente por defecto**; hay que fijar la retención o usar S3 Lifecycle.
- **La inferencia entre Regiones global respeta la residencia en la UE.** Para mantener el procesamiento dentro de una geografía se usa un perfil **geográfico**, no el global.
- **Ámbitos de la *Security Scoping Matrix*.** Usar un chatbot público = ámbito 1; un SaaS con IA = 2; una app propia sobre un modelo de Bedrock = 3; un modelo ajustado = 4; un modelo entrenado desde cero = 5. Más ámbito, más responsabilidades.
