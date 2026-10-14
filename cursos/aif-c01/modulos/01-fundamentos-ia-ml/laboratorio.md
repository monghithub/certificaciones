# Laboratorio: servicios de IA gestionados frente a un modelo propio

Laboratorio **demostrativo y opcional** (duración orientativa: 30–40 minutos). No crea recursos persistentes: se usan tres servicios de IA preentrenados mediante la consola y la CLI, sin entrenar nada.

## Objetivo y relación con el examen

Comprobar en la práctica qué significa «servicio gestionado preentrenado»: se obtiene el resultado llamando a una API, sin experiencia en ML, sin entrenar un modelo y sin gestionar infraestructura, a cambio de poder personalizar poco el modelo.

| Tarea del examen | Qué refuerza el laboratorio |
|---|---|
| 1.2.4 (aplicaciones reales de IA) | NLP, traducción y síntesis de voz como aplicaciones reales |
| 1.2.5 (servicios gestionados de AWS) | Capacidades de Amazon Comprehend, Amazon Translate y Amazon Polly |
| 1.3.3 (uso de un modelo en producción) | Consumo de un modelo como **API de servicio gestionado** |

## Requisitos previos

- Una cuenta de AWS y un usuario o rol de IAM dedicado al laboratorio. No uses el usuario raíz. Los permisos dependen de cómo hagas el laboratorio:
  - **Con la consola** (partes 1 a 3): la consola necesita más permisos que las llamadas a la API, porque también lista y describe recursos. La documentación de Comprehend advierte que, con una política más restrictiva que el mínimo, la consola no funciona como se espera, y recomienda la política administrada `ComprehendReadOnly`. Usa las políticas administradas de solo lectura de los tres servicios: `ComprehendReadOnly`, `TranslateReadOnly` y `AmazonPollyReadOnlyAccess`.
  - **Solo con la CLI**: basta una política de mínimo privilegio con `comprehend:DetectSentiment`, `comprehend:DetectEntities`, `translate:TranslateText` y `polly:SynthesizeSpeech`.
- **Región recomendada:** US East (N. Virginia), `us-east-1`. Amazon Comprehend, Amazon Translate y Amazon Polly tienen punto de enlace en esa Región según la documentación de AWS. Puedes usar otra Región si los tres servicios están disponibles en ella.

- AWS CLI v2 configurada (`aws configure`) si quieres hacer el apartado de la CLI.
- No se necesita acceso a modelos de Amazon Bedrock en este laboratorio.

## Estimación de coste y aviso de facturación

> **Aviso de facturación.** Estos servicios se facturan por uso. Aunque este laboratorio genera un coste mínimo, **eres responsable de lo que uses en tu cuenta**. Revisa el panel de facturación al terminar y configura antes de empezar un presupuesto con alerta en **AWS Budgets** (por ejemplo, de 1 USD).

Precios consultados el 14 de octubre de 2026 en las páginas oficiales de precios; pueden cambiar y varían según la Región, por lo que debes revisarlos antes de empezar:

| Servicio | Unidad de facturación | Dato verificado |
|---|---|---|
| Amazon Comprehend (análisis NLP) | Unidades de 100 caracteres, con un mínimo de 3 unidades (300 caracteres) por petición | Del orden de 0,0001 USD por unidad (es la tarifa del ejemplo de la página de precios; consulta la tabla de tu API); capa gratuita de 50 000 unidades (5 millones de caracteres) por API y mes durante 12 meses |
| Amazon Translate (traducción en tiempo real) | Caracteres traducidos | 15,00 USD por millón de caracteres; capa gratuita de 2 millones de caracteres al mes durante 12 meses desde la primera traducción |
| Amazon Polly (voces estándar) | Caracteres sintetizados | 4,00 USD por millón de caracteres; capa gratuita de 5 millones de caracteres al mes para voces estándar, según la página de precios |

> **Capa gratuita en cuentas nuevas.** Desde julio de 2025, las cuentas nuevas no reciben la capa gratuita de 12 meses de la tabla, sino créditos (100 USD al crear la cuenta, ampliables hasta 200 USD) y la elección entre un plan gratuito de hasta seis meses o un plan de pago. Este laboratorio consume una cantidad insignificante de esos créditos. Consulta <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html>.

**Estimación para este laboratorio:** unas decenas de peticiones de pocas líneas (unos pocos miles de caracteres en total) suponen una fracción de céntimo de dólar, cubierta por la capa gratuita o por los créditos si tu cuenta es elegible. **No hay recursos que generen coste por hora**: no se crean *endpoints*, modelos ni bases de datos.

- Precios de Amazon Comprehend: <https://aws.amazon.com/comprehend/pricing/>
- Precios de Amazon Translate: <https://aws.amazon.com/translate/pricing/>
- Precios de Amazon Polly: <https://aws.amazon.com/polly/pricing/>

## Parte 1: Amazon Comprehend (NLP)

1. En la consola de AWS, selecciona la Región y abre **Amazon Comprehend**.
2. Abre el análisis **en tiempo real** (*Real-time analysis*) y pega una reseña de cliente en español, por ejemplo: «El envío llegó con dos días de retraso, pero el soporte técnico de Madrid resolvió mi incidencia enseguida. Muy contento.»
3. Pulsa **Analizar** y revisa las pestañas: entidades, frases clave, idioma y opinión (*sentiment*).
4. Anota qué has tenido que **configurar** (casi nada) y qué has podido **personalizar** (solo la entrada).
5. Fíjate en la puntuación de confianza de cada resultado: el modelo da un resultado **probabilístico**, no una certeza (objetivo 1.2.2).

Los nombres exactos de los menús pueden variar con las actualizaciones de la consola.

## Parte 2: Amazon Translate

1. Abre **Amazon Translate** y usa la traducción de texto en tiempo real.
2. Elige español como idioma de origen e inglés como destino, pega el mismo texto y traduce.
3. Prueba otro idioma de destino y compara.

## Parte 3: Amazon Polly

1. Abre **Amazon Polly** y entra en el área de prueba de síntesis de texto a voz.
2. Selecciona un idioma español, una voz estándar y reproduce el texto de la reseña.
3. Descarga el audio si quieres y comprueba que el resultado es voz sintetizada, no una grabación.

## Equivalente con la AWS CLI (opcional)

```bash
export AWS_DEFAULT_REGION=us-east-1
TEXTO="El envío llegó con dos días de retraso, pero el soporte técnico resolvió mi incidencia enseguida. Muy contento."

aws comprehend detect-sentiment --language-code es --text "$TEXTO"
aws comprehend detect-entities  --language-code es --text "$TEXTO"
aws translate translate-text --source-language-code es --target-language-code en --text "$TEXTO"
aws polly synthesize-speech --output-format mp3 --voice-id Lucia --text "$TEXTO" resena.mp3
```

Referencias de los comandos: [detect-sentiment](https://docs.aws.amazon.com/cli/latest/reference/comprehend/detect-sentiment.html), [detect-entities](https://docs.aws.amazon.com/cli/latest/reference/comprehend/detect-entities.html), [translate-text](https://docs.aws.amazon.com/cli/latest/reference/translate/translate-text.html) y [synthesize-speech](https://docs.aws.amazon.com/cli/latest/reference/polly/synthesize-speech.html). La voz `Lucia` figura en la lista de voces de Amazon Polly; si tu Región no la ofrece, elige otra voz en español.

## Preguntas para reflexionar

1. ¿Cuánta experiencia en ML ha sido necesaria? ¿Qué parte del modelo has podido cambiar?
2. Si quisieras que el análisis de opinión distinguiera categorías propias de tu empresa, ¿qué servicio o enfoque necesitarías y qué esfuerzo supondría? (Pista: Amazon SageMaker AI o una personalización del servicio.)
3. ¿Cómo se clasifica este uso entre los métodos de producción de la Tarea 1.3: API gestionada o alojada por el cliente?
4. ¿Cómo se factura cada servicio que has usado y qué pasaría con el coste si, en lugar de llamar a la API, hubieras desplegado un modelo propio en un *endpoint* en tiempo real que estuviera encendido todo el mes?

**Respuestas orientativas:** 1) Ninguna experiencia en ML; solo has cambiado la entrada. 2) Un clasificador personalizado de Comprehend o un modelo propio en SageMaker AI, con datos etiquetados: más esfuerzo. 3) API de servicio gestionado. 4) Por caracteres o unidades procesadas; el *endpoint* se facturaría por las horas de instancia encendida aunque no tuviera tráfico.

## Limpieza de recursos

Este laboratorio **no crea recursos persistentes**, así que no hay nada que eliminar en los servicios. Aun así:

1. Elimina el fichero `resena.mp3` y cualquier texto de prueba que no quieras conservar.
2. Cierra la sesión de la consola y, si creaste un usuario, un rol o una política de IAM solo para el laboratorio, elimínalos o quítales las políticas (IAM → Usuarios/Roles/Políticas). Si creaste claves de acceso para la CLI, desactívalas y bórralas.
3. Si configuraste credenciales de la CLI temporales, bórralas de `~/.aws/credentials` o cierra la sesión.
4. Al día siguiente, revisa el panel de **Facturación** para confirmar que no hay cargos inesperados.
