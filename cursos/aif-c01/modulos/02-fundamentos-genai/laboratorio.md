# Laboratorio: tokens, parámetros de inferencia y coste en Amazon Bedrock

Laboratorio **práctico y opcional** (duración orientativa: 40–50 minutos). No crea recursos persistentes: se envían unas decenas de *prompts* cortos a un modelo fundacional económico desde el *playground* de la consola de Amazon Bedrock y, opcionalmente, desde la AWS CLI.

## Objetivo y relación con el examen

Ver con tus propios ojos tres ideas del Dominio 2: el modelo trabaja con ***tokens*** y se paga por los de entrada y los de salida; los **parámetros de inferencia** cambian la variabilidad y la longitud de la respuesta; y el **contexto** que envías tiene un coste.

| Tarea del examen | Qué refuerza el laboratorio |
|---|---|
| 2.1.1 (conceptos) | *Tokens*, *prompt*, generación *token* a token |
| 2.1.4 (precios por *tokens*) | Contar *tokens* de entrada y de salida y estimar el coste |
| 2.1.5 (ingeniería de contexto) | Efecto de añadir contexto e instrucciones del sistema |
| 2.2.2 (no determinismo) | Temperatura, top-p y longitud máxima |
| 2.3.1 (servicios) | Uso de Amazon Bedrock y de un modelo de la familia Amazon Nova |

## Requisitos previos

- Una cuenta de AWS y un usuario o rol de IAM dedicado al laboratorio. No uses el usuario raíz. Los permisos dependen de cómo hagas el laboratorio:
  - **Con la consola** (partes 1 a 3): la consola necesita listar modelos y abrir el *playground*, además de invocar el modelo. La forma más sencilla es la política administrada `AmazonBedrockLimitedAccess`, que da acceso a los servicios de Bedrock (y a las suscripciones de AWS Marketplace para modelos de terceros). `AmazonBedrockReadOnly` **no basta**: solo permite ver recursos.
  - **Solo con la CLI** (parte 4): basta una política de mínimo privilegio con la acción `bedrock:InvokeModel` (la API Converse se autoriza con esa acción).

  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      { "Effect": "Allow", "Action": "bedrock:InvokeModel", "Resource": "*" }
    ]
  }
  ```

  En un entorno real se restringiría `Resource` a los ARN del perfil de inferencia y del modelo; para el laboratorio basta así.

- **Región recomendada:** US East (N. Virginia), `us-east-1`.
- **Modelo:** Amazon **Nova Micro**, el modelo de solo texto más rápido y económico de la familia Nova (ventana de contexto de 128 000 *tokens* y hasta 10 000 *tokens* de salida, según su ficha en la documentación). En la CLI se usa su perfil de inferencia geográfico de EE. UU., `us.amazon.nova-micro-v1:0`, que reparte las peticiones entre Regiones de EE. UU. Si tu consola no lo muestra, elige otro modelo de texto barato de Amazon Nova.
- **Acceso a modelos:** según la documentación vigente, el acceso a muchos modelos está **activado por defecto**: basta con seleccionar el modelo en el catálogo de la consola de Bedrock y abrirlo en el *playground*. Los modelos de **terceros** requieren además permisos de AWS Marketplace y un método de pago válido, y los de Anthropic un formulario de primer uso; con Amazon Nova no hace falta nada de eso.
- AWS CLI v2 configurada (`aws configure`) si quieres hacer la parte 4.

## Estimación de coste y aviso de facturación

> **Aviso de facturación.** Amazon Bedrock se factura por uso: cada *token* de entrada y de salida tiene precio. Aunque este laboratorio genera un coste mínimo, **eres responsable de lo que uses en tu cuenta**. Configura antes de empezar un presupuesto con alerta en **AWS Budgets** (por ejemplo, de 1 USD) y revisa el panel de facturación al terminar.

- **Precio:** consulta el de Amazon Nova Micro en la [página de precios de Amazon Bedrock](https://aws.amazon.com/bedrock/pricing/) (pestaña Amazon → Amazon Nova) antes de empezar; varía por Región y por nivel de servicio. AWS lo presenta como un modelo de «muy bajo coste».
- **Consumo del laboratorio:** unas 30 peticiones de unos pocos cientos de *tokens* cada una, en total **menos de 20 000 *tokens***.
- **Orden de magnitud:** aunque se pagaran 2 USD por millón de *tokens* (bastante más que un modelo pequeño como Nova Micro), 20 000 *tokens* costarían 20 000 / 1 000 000 × 2 = **0,04 USD**.
- **Capa gratuita:** las cuentas nuevas reciben 100 USD en créditos al crearse (ampliables hasta 100 USD más) y eligen entre un plan gratuito de hasta seis meses o un plan de pago. El plan gratuito **no da acceso a ciertos servicios** que consumirían rápidamente los créditos: antes de empezar, comprueba en las preguntas frecuentes de la capa gratuita si Amazon Bedrock está disponible en tu plan. Consulta <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html>.
- **No hay recursos que generen coste por hora:** no se compra *Provisioned Throughput*, no se crean *endpoints*, bases de conocimiento ni agentes.

## Parte 1: el *playground* y los *tokens*

1. En la consola de AWS, selecciona la Región `us-east-1` y abre **Amazon Bedrock**.
2. En el catálogo de modelos, busca **Amazon Nova Micro** y ábrelo en el *playground* de chat o de texto. Los nombres de los menús pueden variar con las actualizaciones de la consola.
3. Envía este *prompt*: «Resume en dos frases qué es Amazon Bedrock.»
4. Localiza en la respuesta las **métricas de la invocación**: *tokens* de entrada, *tokens* de salida y latencia. Anótalas.
5. Repite el mismo *prompt* añadiendo delante un párrafo largo de contexto (por ejemplo, copia los tres primeros párrafos de la página «What is Amazon Bedrock?»). Anota de nuevo los *tokens* de entrada y la latencia.

**Qué observar:** los *tokens* de entrada crecen con el contexto, aunque la pregunta sea la misma. Ese es el coste de la ingeniería de contexto mal hecha: enviar más de lo necesario.

## Parte 2: temperatura, top-p y no determinismo

1. Pide: «Propón un eslogan de cinco palabras para una panadería de barrio.»
2. Pon la **temperatura al mínimo** y envía el *prompt* tres veces. Compara las respuestas.
3. Sube la **temperatura al máximo** que permita el *playground* y vuelve a enviarlo tres veces.
4. Con la temperatura alta, baja **top-p** (por ejemplo, a 0,1) y repite.

**Qué observar:** con temperatura baja las respuestas tienden a repetirse; con temperatura alta varían más. Bajar top-p restringe los candidatos y reduce la variedad aunque la temperatura sea alta. Recuerda: repetible no significa correcto.

## Parte 3: longitud máxima, instrucciones del sistema y coste

1. Pide: «Explica qué es un *embedding* para alguien sin formación técnica.»
2. Limita la **longitud máxima** (*max tokens*) a un valor bajo, por ejemplo 50. Observa que la respuesta se corta y fíjate en el motivo de parada si la consola lo muestra.
3. Súbela a 500 y compara los *tokens* de salida y la latencia.
4. Si el *playground* permite **instrucciones del sistema** (*system prompt*), añade: «Responde siempre en un máximo de tres viñetas.» Repite la pregunta con la longitud en 500 y compara los *tokens* de salida.
5. Con los números anotados, calcula el coste de cada petición con el precio de Nova Micro: *tokens* de entrada × precio de entrada + *tokens* de salida × precio de salida.

**Qué observar:** la longitud máxima corta la respuesta pero no la hace más concisa; una instrucción clara del sistema consigue respuestas más cortas **y** completas, con menos *tokens* de salida.

## Parte 4: equivalente con la AWS CLI (opcional)

```bash
export AWS_DEFAULT_REGION=us-east-1
MODELO=us.amazon.nova-micro-v1:0

# Temperatura baja: ejecútalo dos o tres veces y compara
aws bedrock-runtime converse --model-id "$MODELO" \
  --messages '[{"role":"user","content":[{"text":"Propón un eslogan de cinco palabras para una panadería de barrio."}]}]' \
  --inference-config '{"temperature":0.0,"maxTokens":50}' \
  --query '{texto: output.message.content[0].text, uso: usage, parada: stopReason}'

# Temperatura alta y top-p, con instrucciones del sistema
aws bedrock-runtime converse --model-id "$MODELO" \
  --system '[{"text":"Responde en un máximo de tres viñetas."}]' \
  --messages '[{"role":"user","content":[{"text":"Explica qué es un embedding para alguien sin formación técnica."}]}]' \
  --inference-config '{"temperature":0.9,"topP":0.9,"maxTokens":300}' \
  --query '{texto: output.message.content[0].text, uso: usage, parada: stopReason}'
```

El campo `usage` devuelve `inputTokens`, `outputTokens` y `totalTokens`, y `stopReason` indica por qué se detuvo el modelo (por ejemplo, `end_turn` si terminó o `max_tokens` si alcanzó la longitud máxima). Referencia del comando: [aws bedrock-runtime converse](https://docs.aws.amazon.com/cli/latest/reference/bedrock-runtime/converse.html). Si recibes `AccessDeniedException`, revisa los permisos de IAM y que el modelo esté disponible en la Región.

## Preguntas para reflexionar

1. ¿Qué ha pasado con los *tokens* de entrada al añadir el párrafo de contexto en la parte 1? ¿Qué harías en una aplicación real para no pagar ese contexto en cada petición?
2. Con temperatura mínima, ¿las respuestas fueron idénticas? ¿Significa eso que son correctas?
3. ¿Por qué es mejor una instrucción del sistema que limitar la longitud máxima para obtener respuestas cortas?
4. Si este asistente recibiera 100 000 peticiones al mes con los *tokens* que has medido, ¿cuánto costaría? ¿Qué opción de Bedrock usarías si las respuestas pudieran esperar a la noche?
5. ¿Qué cambiaría en el coste si compraras *Provisioned Throughput* para este laboratorio?

**Respuestas orientativas:** 1) Crecen proporcionalmente al texto añadido; enviaría solo los fragmentos relevantes (RAG), resumiría el historial o usaría *prompt caching* si el contexto se repite. 2) Tienden a repetirse, pero un modelo puede repetir una respuesta incorrecta: la temperatura reduce la variabilidad, no las alucinaciones. 3) La longitud máxima corta la respuesta a medias; la instrucción hace que el modelo planifique una respuesta breve y completa. 4) (*tokens* de entrada × 100 000 × precio de entrada) + (*tokens* de salida × 100 000 × precio de salida); para respuestas que pueden esperar, inferencia por lotes, un 50 % más barata en los modelos que la admiten. 5) Se pagaría por horas aunque no se usara: para un laboratorio, muchísimo más caro que bajo demanda.

## Limpieza de recursos

Este laboratorio **no crea recursos persistentes**, así que no hay nada que eliminar en Amazon Bedrock. Aun así:

1. Comprueba en la consola de Bedrock que **no** has comprado *Provisioned Throughput* ni creado bases de conocimiento, agentes o trabajos por lotes por error. Si existe alguno, elimínalo: el *Provisioned Throughput* se factura por horas hasta que se borra.
2. Si creaste un usuario, un rol o una política de IAM solo para el laboratorio, elimínalos o quítales las políticas (IAM → Usuarios/Roles/Políticas). Si creaste claves de acceso para la CLI, desactívalas y bórralas.
3. Si configuraste credenciales temporales de la CLI, bórralas de `~/.aws/credentials` o cierra la sesión.
4. Al día siguiente, revisa el panel de **Facturación** (servicio Amazon Bedrock) para confirmar que el cargo es el esperado.
