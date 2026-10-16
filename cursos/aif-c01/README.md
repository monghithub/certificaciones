# Curso AWS Certified AI Practitioner (AIF-C01)

Curso en español de España para preparar el examen **AWS Certified AI Practitioner (AIF-C01)**. Está pensado para perfiles junior con conocimientos básicos de programación y poca experiencia en AWS, y lo revisa un arquitecto de software sénior.

> Estado: **Iteración 3** completada (módulos 00 a 03, con 82 preguntas del Dominio 1, 81 del Dominio 2 y 94 del Dominio 3). Los módulos 04 a 06 están pendientes. Consulta [CHANGELOG.md](../../CHANGELOG.md).

Manifiesto del curso: [curso.yaml](curso.yaml).

## Datos del examen

Revalidados el 14 de octubre de 2026 contra la guía oficial (versión 1.1, publicada el 30 de abril de 2026) y la [página de la certificación](https://aws.amazon.com/certification/certified-ai-practitioner/).

| Aspecto | Valor |
|---|---|
| Duración | 90 minutos |
| Preguntas | 65 (50 puntuables y 15 no puntuables, sin identificar) |
| Puntuación | Escala 100–1.000; aprobado con 700; modelo compensatorio |
| Tipos de pregunta | Opción múltiple, respuesta múltiple, ordenación (3–5 elementos), emparejamiento (3–7 elementos) |
| Penalización | Ninguna por adivinar; las preguntas sin responder cuentan como incorrectas |
| Coste | 100 USD |
| Validez | 3 años |

| Dominio | Peso | Fuente oficial transcrita |
|---|---|---|
| D1. Fundamentos de IA y ML | 20 % | [fuentes/dominio-1.md](fuentes/dominio-1.md) |
| D2. Fundamentos de IA generativa | 24 % | [fuentes/dominio-2.md](fuentes/dominio-2.md) |
| D3. Aplicaciones de modelos fundacionales | 28 % | [fuentes/dominio-3.md](fuentes/dominio-3.md) |
| D4. Directrices para una IA responsable | 14 % | [fuentes/dominio-4.md](fuentes/dominio-4.md) |
| D5. Seguridad, cumplimiento y gobierno de soluciones de IA | 14 % | [fuentes/dominio-5.md](fuentes/dominio-5.md) |

Servicios dentro y fuera de alcance: [fuentes/servicios-alcance.md](fuentes/servicios-alcance.md).

## Índice del curso

| Módulo | Contenido | Dominio |
|---|---|---|
| [00 Base de AWS](modulos/00-base-aws/) | Conceptos de AWS necesarios para el resto del curso | Transversal |
| [01 Fundamentos de IA y ML](modulos/01-fundamentos-ia-ml/) | Conceptos, casos de uso y ciclo de vida de ML | D1 |
| [02 Fundamentos de IA generativa](modulos/02-fundamentos-genai/) | Conceptos, capacidades y servicios de GenAI | D2 |
| [03 Modelos fundacionales](modulos/03-modelos-fundacionales/) | Diseño, prompts, personalización y evaluación | D3 |
| [04 IA responsable](modulos/04-ia-responsable/) | Sesgo, equidad, transparencia y explicabilidad | D4 |
| [05 Seguridad y gobierno](modulos/05-seguridad-gobierno/) | Seguridad, cumplimiento y gobierno | D5 |
| [06 Simulacro](modulos/06-simulacro/) | 65 preguntas según los pesos oficiales | Todos |

Cada módulo contiene `README.md` (teoría), `servicios.md`, `trampas.md`, `preguntas.yaml` y, si aplica, `laboratorio.md`.

## Cómo estudiar

1. Lee el `README.md` del módulo y comprueba su mapa de cobertura frente a [fuentes/](fuentes/).
2. Repasa `servicios.md` (qué servicio, para qué y cuándo no usarlo) y `trampas.md`.
3. Haz el laboratorio, si lo hay. **Genera costes en tu cuenta de AWS: sigue siempre la sección de limpieza.**
4. Practica con el cuestionario: `python scripts/quiz.py --dominio 3 --n 10`.
5. Anota los fallos por tarea y vuelve a la teoría antes de pasar al siguiente módulo.
6. Al terminar el curso, haz el [conjunto oficial de práctica de AWS Skill Builder](#antes-de-reservar-el-examen).

## Plan de 4 semanas

| Semana | Módulos | Objetivo |
|---|---|---|
| 1 | 00 y 01 | Base de AWS y fundamentos de IA/ML |
| 2 | 02 y 03 (primera parte) | GenAI, selección de modelos, parámetros de inferencia y RAG |
| 3 | 03 (segunda parte), 04 y 05 | Prompts, personalización, evaluación, IA responsable, seguridad y gobierno |
| 4 | 06 y repaso | Simulacro, análisis de fallos por tarea y repaso de `chuleta.md` |

## Herramientas

Desde la raíz del repositorio:

```bash
pip install -r requirements-app.txt
python scripts/validar_preguntas.py --curso aif-c01   # valida el manifiesto y los bancos de preguntas
python scripts/quiz.py --curso aif-c01 --modulo 03    # cuestionario interactivo
python -m pytest                                      # tests de las herramientas y de la consola
```

La [consola web](../../docs/consola.md) permite estudiar este curso, hacer los tests y seguir el progreso de cada estudiante matriculado.

## Reglas de contenido

- Toda afirmación sobre servicios, límites, precios o formato del examen debe poder trazarse a una fuente oficial de AWS. Lo no verificado se marca con `> ⚠️ PENDIENTE DE VERIFICAR:`.
- Las preguntas son de elaboración propia. No se usan preguntas reales del examen ni material de terceros protegido.
- Más detalle para colaboradores y agentes en [AGENTS.md](../../AGENTS.md).

## Antes de reservar el examen

Valida tu preparación con el material oficial de AWS antes de reservar el examen. Este curso no lo sustituye ni garantiza el aprobado.

- [Conjunto oficial de preguntas de práctica AIF-C01](https://skillbuilder.aws/learn/4URFGY63KV/official-practice-question-set-aws-certified-ai-practitioner--aifc01--english/FVG43Y1PAX) en AWS Skill Builder: 20 preguntas gratuitas, con explicación de cada opción. Requiere iniciar sesión.
- [Página oficial de la certificación](https://aws.amazon.com/certification/certified-ai-practitioner/): reserva del examen y recursos de preparación.
- [Guía oficial del examen](https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html).

Usa el conjunto oficial como control final: si fallas una pregunta, vuelve al módulo del dominio correspondiente. Las preguntas de este curso son de elaboración propia y no reproducen las oficiales.

## Licencia

Código bajo MIT y contenido bajo CC BY 4.0. Consulta [LICENSE](../../LICENSE).
