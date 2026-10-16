# Simulacro del examen

Este módulo es un **examen de prueba completo** con el formato del AIF-C01: 65 preguntas para hacer en 90 minutos, repartidas según los pesos oficiales de los cinco dominios. Todas las preguntas son de elaboración propia e **inéditas**: no repiten ninguna de los bancos de los módulos (el validador del repositorio lo comprueba). Hazlo cuando hayas terminado los módulos 00 a 05.

## Cómo hacerlo

1. En la consola, entra en **Tests** y elige **Empezar simulacro**. El cronómetro marca 90 minutos.
2. Responde todas las preguntas: en el examen real las preguntas sin responder cuentan como incorrectas y no hay penalización por fallar, así que **no dejes ninguna en blanco**.
3. Lee cada enunciado buscando la **restricción que decide** («con el MENOR esfuerzo operativo», «de la forma MÁS rentable», «sin que el tráfico salga a Internet»): suele ser lo que descarta las opciones plausibles.
4. En las preguntas de respuesta múltiple hay que acertar **todas** las correctas; en las de ordenación, el orden completo; en las de emparejamiento, todos los pares.
5. Al terminar, revisa la explicación de cada pregunta, también de las que aciertes.

Sin la consola, puedes hacerlo en la terminal: `python scripts/quiz.py --curso aif-c01 --modulo 06 --n 65` (sin cronómetro).

## Qué contiene

| Dominio | Peso oficial | Preguntas | Módulo para repasar |
|---|---|---|---|
| D1. Fundamentos de IA y ML | 20 % | 13 | [01](../01-fundamentos-ia-ml/README.md) |
| D2. Fundamentos de IA generativa | 24 % | 16 | [02](../02-fundamentos-genai/README.md) |
| D3. Aplicaciones de modelos fundacionales | 28 % | 18 | [03](../03-modelos-fundacionales/README.md) |
| D4. Directrices para una IA responsable | 14 % | 9 | [04](../04-ia-responsable/README.md) |
| D5. Seguridad, cumplimiento y gobierno | 14 % | 9 | [05](../05-seguridad-gobierno/README.md) |
| **Total** | 100 % | **65** | |

Tipos de pregunta: 41 de opción múltiple, 12 de respuesta múltiple, 5 de ordenación y 7 de emparejamiento. Dificultad: 13 baja, 39 media y 13 alta. Los dominios aparecen intercalados, como en el examen.

## Cómo interpretar el resultado

- **El porcentaje es orientativo.** El examen real puntúa en una escala de 100 a 1.000 y se aprueba con 700; además, 15 de sus 65 preguntas no puntúan y no se sabe cuáles son. Un porcentaje alto en el simulacro no garantiza el aprobado, pero uno bajo indica que hace falta repasar.
- **Analiza los fallos por dominio.** En **Mis estadísticas** de la consola verás el acierto por dominio y por tarea. Vuelve al módulo del dominio con peor resultado (tabla de arriba), relee sus **trampas** y repite sus preguntas en modo «dominio».
- **Busca el patrón de tus errores.** Si fallas por confundir servicios vecinos (por ejemplo, Config frente a CloudTrail, o RAG frente a *fine-tuning*), repasa las tablas «escenario → servicio» y la [chuleta](../../chuleta.md). Si fallas por no ver la restricción del enunciado, practica subrayándola antes de mirar las opciones.
- **Repite el simulacro** solo después de repasar: el banco es fijo y, si lo repites enseguida, medirás tu memoria y no tu preparación.

## Antes de reservar el examen

Haz el **conjunto oficial de preguntas de práctica** de AWS Skill Builder (20 preguntas gratuitas con explicaciones) como control final; el enlace está en el [README del curso](../../README.md#antes-de-reservar-el-examen). Si fallas alguna, vuelve al módulo de ese dominio. Las preguntas de este curso son propias y no reproducen las oficiales.

## Referencias

- Guía oficial del examen AIF-C01: <https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html>
- Página de la certificación: <https://aws.amazon.com/certification/certified-ai-practitioner/>
