# Simulacro del examen

Este módulo es un **examen de prueba completo** con el formato del AIF-C01: 65 preguntas para hacer en 90 minutos, repartidas según los pesos oficiales de los cinco dominios. Las preguntas salen de un **banco rotatorio de 96**: cada intento extrae 65, así que dos intentos seguidos no son iguales. Todas las preguntas son de elaboración propia e **inéditas**: se redactaron con escenarios y decisiones distintos de los de los bancos de los módulos, aunque algunas tratan el mismo concepto que una pregunta de esos bancos desde otro planteamiento. El validador del repositorio comprueba que no se repite ningún enunciado y avisa de las preguntas muy parecidas a las de los bancos. Hazlo cuando hayas terminado los módulos 00 a 05.

## Cómo hacerlo

1. En la consola, entra en **Tests** y elige **Empezar simulacro**. El cronómetro marca 90 minutos.
2. Responde todas las preguntas: en el examen real las preguntas sin responder cuentan como incorrectas y no hay penalización por fallar, así que **no dejes ninguna en blanco**.
3. Lee cada enunciado buscando la **restricción que decide** («con el MENOR esfuerzo operativo», «de la forma MÁS rentable», «sin que el tráfico salga a Internet»): suele ser lo que descarta las opciones plausibles.
4. Como en el examen (guía v1.2), hay dos tipos de pregunta: **opción múltiple** (una correcta de cuatro) y **respuesta múltiple** (dos o más correctas de cinco o más; el enunciado dice cuántas y hay que acertarlas **todas**).
5. Al terminar, revisa la explicación de cada pregunta, también de las que aciertes.

Sin la consola, puedes hacerlo en la terminal: `python scripts/quiz.py --curso aif-c01 --simulacro` (con `--semilla N` para repetir la misma extracción). No reproduce las condiciones del examen: no tiene cronómetro y corrige cada pregunta al responderla.

## Qué contiene

Cada intento tiene siempre el mismo reparto, el del examen: por dominio según los pesos oficiales y por tipo según `examen.distribucion` de `curso.yaml` (80 % de opción múltiple y 20 % de respuesta múltiple).

| Dominio | Peso oficial | Por intento (opción múltiple + respuesta múltiple) | En el banco | Módulo para repasar |
|---|---|---|---|---|
| D1. Fundamentos de IA y ML | 20 % | 13 (11 + 2) | 18 (14 + 4) | [01](../01-fundamentos-ia-ml/README.md) |
| D2. Fundamentos de IA generativa | 24 % | 16 (13 + 3) | 28 (23 + 5) | [02](../02-fundamentos-genai/README.md) |
| D3. Aplicaciones de modelos fundacionales | 28 % | 18 (14 + 4) | 22 (16 + 6) | [03](../03-modelos-fundacionales/README.md) |
| D4. Directrices para una IA responsable | 14 % | 9 (7 + 2) | 12 (9 + 3) | [04](../04-ia-responsable/README.md) |
| D5. Seguridad, cumplimiento y gobierno | 14 % | 9 (7 + 2) | 16 (12 + 4) | [05](../05-seguridad-gobierno/README.md) |
| **Total** | 100 % | **65 (52 + 13)** | **96 (74 + 22)** | |

- **Tipos de pregunta:** opción múltiple y respuesta múltiple, los dos que enumera la guía del examen. Las preguntas de ordenación y emparejamiento se practican en los bancos de los módulos.
- **Cobertura:** el banco cubre las 14 tareas y los **69 objetivos oficiales**, cada uno con al menos una pregunta (todos los del Dominio 2 y del Dominio 5 tienen dos, así que ninguna pregunta sale en todos los intentos). Dentro de cada dominio, un intento no repite objetivo salvo cuando no hay más remedio: el Dominio 2 tiene 14 objetivos para 16 preguntas y el Dominio 5, 8 para 9, así que en cada intento se repiten 2 objetivos del D2 y 1 del D5.
- **Rotación:** entre las combinaciones válidas, la consola prefiere las preguntas que no salieron en tu intento de simulacro anterior; el resto se elige al azar y el orden también es aleatorio. La rotación se aplica después del reparto y de la variedad de objetivos, y el banco tiene 31 preguntas más que un intento: un segundo intento seguido trae unas 31 preguntas que no viste y repite unas 34.
- **Dificultad del banco:** 19 baja, 58 media y 19 alta.

## Cómo interpretar el resultado

- **El porcentaje es orientativo.** El examen real puntúa en una escala de 100 a 1.000 y se aprueba con 700; además, 15 de sus 65 preguntas no puntúan y no se sabe cuáles son. Un porcentaje alto en el simulacro no garantiza el aprobado, pero uno bajo indica que hace falta repasar.
- **Analiza los fallos por dominio.** En **Mis estadísticas** de la consola verás el acierto por dominio y por tarea. Vuelve al módulo del dominio con peor resultado (tabla de arriba), relee sus **trampas** y repite sus preguntas en modo «dominio».
- **Busca el patrón de tus errores.** Si fallas por confundir servicios vecinos (por ejemplo, Config frente a CloudTrail, o RAG frente a *fine-tuning*), repasa las tablas «escenario → servicio» y la [chuleta](../../chuleta.md). Si fallas por no ver la restricción del enunciado, practica subrayándola antes de mirar las opciones.
- **Repite el simulacro** solo después de repasar. Cada intento cambia parte de las preguntas, pero el banco es limitado (96 preguntas para intentos de 65): si lo repites enseguida, reconocerás muchas y medirás tu memoria más que tu preparación.

## Antes de reservar el examen

Haz el **conjunto oficial de preguntas de práctica** de AWS Skill Builder (20 preguntas gratuitas con explicaciones) como control final; el enlace está en el [README del curso](../../README.md#antes-de-reservar-el-examen). Si fallas alguna, vuelve al módulo de ese dominio. Las preguntas de este curso son propias y no reproducen las oficiales.

## Referencias

- Guía oficial del examen AIF-C01: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html>
- Página de la certificación: <https://aws.amazon.com/certification/certified-ai-practitioner/>
