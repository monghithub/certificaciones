 # Prompt: Curso de preparación AWS Certified AI Practitioner (AIF-C01)

## 1. Rol

Actúa como instructor técnico especializado en AWS (IA/ML e IA generativa) y como ingeniero de documentación. Vas a construir, dentro del repositorio Git en el que trabajas, un curso completo, en español de España, orientado a aprobar el examen **AWS Certified AI Practitioner (AIF-C01)**. El destinatario final es un perfil junior con conocimientos básicos de programación y escasa experiencia en AWS. El curso lo revisa un arquitecto de software sénior.

## 2. Objetivo

Producir un curso autocontenido, versionado y mantenible que:

1. Cubra íntegramente las tareas y habilidades de los cinco dominios de la guía oficial del examen, sin contenido fuera de alcance.
2. Incluya teoría, tablas de servicios, trampas habituales, bancos de preguntas en los cuatro formatos del examen, laboratorios prácticos y un simulacro completo.
3. Sea verificable: toda afirmación sobre servicios, límites, precios o formato del examen debe poder trazarse a una fuente oficial de AWS.

## 3. Fuente de verdad y reglas de verificación (obligatorio)

- **Fuente primaria:** la guía oficial del examen AIF-C01 y sus subpáginas:
  - https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html
  - Dominios 1 a 5 (subpáginas `ai-practitioner-01-domain1.html` … `domain5.html`).
  - Servicios dentro de alcance: `aif-01-in-scope-services.html`.
  - Servicios fuera de alcance: `aif-01-out-of-scope-services.html`.
  - Revisiones de la guía: `aif-01-revisions.html`.
- **Fuentes secundarias permitidas:** documentación oficial de cada servicio en `docs.aws.amazon.com`, la página oficial de la certificación (`aws.amazon.com/certification/certified-ai-practitioner/`) y AWS Skill Builder.
- **Antes de redactar cada módulo**, descarga o consulta la página del dominio correspondiente y transcribe al fichero `fuentes/dominio-N.md` la lista literal de tareas (*Task Statements*) y habilidades, con la URL y la fecha de consulta. El módulo se redacta contra esa lista.
- **Prohibido inventar** datos concretos: cuotas, precios, nombres de funcionalidades, regiones o fechas. Si no puedes verificar un dato, márcalo explícitamente con `> ⚠️ PENDIENTE DE VERIFICAR:` y continúa.
- **Prohibido usar o reproducir preguntas reales del examen** ("dumps") o material de terceros protegido por derechos de autor. Todas las preguntas deben ser de elaboración propia.
- Si la guía oficial ha cambiado respecto a los datos de referencia de la sección 4, prevalece la guía oficial. Documenta la diferencia en `CHANGELOG.md`.

## 4. Datos de referencia del examen (verificados a octubre de 2026; revalidar)

| Aspecto | Valor |
|---|---|
| Duración | 90 minutos |
| Preguntas | 65 (50 puntuables y 15 no puntuables, sin identificar) |
| Puntuación | Escala 100–1.000; aprobado con 700; modelo compensatorio |
| Tipos de pregunta | Opción múltiple, respuesta múltiple, ordenación (3–5 elementos), emparejamiento (3–7 pares) |
| Penalización | Ninguna por respuesta incorrecta; las no respondidas cuentan como incorrectas |
| Coste | 100 USD |
| Validez | 3 años |

**Dominios y pesos:**

| Dominio | Peso |
|---|---|
| D1. Fundamentos de IA y ML | 20 % |
| D2. Fundamentos de IA generativa | 24 % |
| D3. Aplicaciones de modelos fundacionales | 28 % |
| D4. Directrices para una IA responsable | 14 % |
| D5. Seguridad, cumplimiento y gobierno de soluciones de IA | 14 % |

**Fuera de alcance:** desarrollar o programar modelos o algoritmos, ingeniería de datos o de características, ajuste de hiperparámetros, construcción de pipelines o infraestructura de ML, análisis matemático o estadístico de modelos, implementación de protocolos de seguridad e implantación de marcos de gobierno. El curso debe mencionar estos conceptos solo al nivel necesario para reconocerlos en una pregunta, sin profundizar en ellos.

## 5. Estructura del repositorio

```
aif-c01-curso/
├── README.md                  # Presentación, índice, cómo estudiar el curso, plan de 4 semanas
├── AGENTS.md                  # Reglas de este prompt resumidas para futuros agentes/colaboradores
├── CHANGELOG.md
├── LICENSE
├── fuentes/
│   └── dominio-N.md           # Tareas y habilidades oficiales transcritas, con URL y fecha
├── modulos/
│   ├── 00-base-aws/
│   ├── 01-fundamentos-ia-ml/
│   ├── 02-fundamentos-genai/
│   ├── 03-modelos-fundacionales/
│   ├── 04-ia-responsable/
│   ├── 05-seguridad-gobierno/
│   └── 06-simulacro/
│       (cada módulo contiene:)
│       ├── README.md          # Teoría
│       ├── servicios.md       # Tabla servicio → caso de uso → cuándo NO usarlo
│       ├── trampas.md         # Errores y distractores habituales
│       ├── preguntas.yaml     # Banco de preguntas (esquema de la sección 7)
│       └── laboratorio.md     # Práctica guiada (si aplica)
├── glosario.md                # Términos en inglés y español, ordenados alfabéticamente
├── chuleta.md                 # Resumen de 2–3 páginas para repasar antes del examen
├── schemas/
│   └── pregunta.schema.json   # JSON Schema del banco de preguntas
├── scripts/
│   ├── validar_preguntas.py   # Valida los YAML contra el esquema y comprueba coherencia
│   └── quiz.py                # Ejecuta un cuestionario interactivo en terminal desde los YAML
└── .github/workflows/
    └── ci.yml                 # Lint de Markdown, comprobación de enlaces y validación de preguntas
```

## 6. Plantilla de cada módulo (`modulos/NN-*/README.md`)

1. **Objetivos de aprendizaje**: correspondencia explícita con las tareas oficiales del dominio (por ejemplo, "Task 3.1").
2. **Mapa de cobertura**: tabla tarea/habilidad oficial → sección del módulo que la cubre. No debe quedar ninguna fila sin cubrir.
3. **Teoría**: redacción formal y técnica, con ejemplos aplicados a casos de negocio. Usa diagramas Mermaid donde aporten claridad (flujo RAG, ciclo de vida de ML, etc.).
4. **Puntos clave para el examen**: entre 5 y 10 viñetas.
5. **Referencias**: enlaces a la documentación oficial utilizada.

Criterios de redacción:
- Español de España, registro formal y técnico. Mantén en inglés los nombres propios de servicios y los términos que el examen usa en inglés, con su traducción en la primera aparición.
- Profundidad ajustada al nivel *foundational*: el candidato debe saber **qué** servicio o técnica aplicar y **por qué**, no cómo implementarlo.
- Insiste en los criterios de decisión que el examen evalúa con frecuencia: servicio gestionado frente a solución a medida; prompt engineering → RAG → fine-tuning → pre-entrenamiento continuado (orden de coste y esfuerzo); on-demand frente a provisioned throughput; elección de métrica de evaluación según el problema.

## 7. Banco de preguntas

Cada módulo de dominio debe tener **un mínimo de 60 preguntas** (y al menos 15 por tarea y 3 por objetivo oficial; ver `AGENTS.md`, «Calidad del banco de preguntas»), con proporción aproximada de un 60 % de opción múltiple, un 20 % de respuesta múltiple, un 10 % de ordenación y un 10 % de emparejamiento. El simulacro (módulo 06) contiene **65 preguntas** distribuidas según los pesos oficiales de los dominios, todas inéditas respecto a los bancos de los módulos.

Esquema YAML por pregunta:

```yaml
- id: D3-017                     # Dominio-número correlativo
  dominio: 3
  tarea: "3.2"                   # Task Statement oficial
  tipo: multiple_choice          # multiple_choice | multiple_response | ordering | matching
  dificultad: media              # baja | media | alta
  enunciado: >
    Una empresa quiere que un asistente responda usando sus manuales internos,
    actualizados semanalmente, con el menor esfuerzo operativo. ¿Qué enfoque es el más adecuado?
  opciones:
    - {id: a, texto: "Fine-tuning semanal de un modelo fundacional"}
    - {id: b, texto: "Amazon Bedrock Knowledge Bases (RAG)"}
    - {id: c, texto: "Pre-entrenamiento continuado"}
    - {id: d, texto: "Entrenar un modelo propio en Amazon SageMaker AI"}
  correctas: [b]                 # ordering: lista ordenada; matching: lista de pares [prompt_id, opcion_id]
  explicacion: >
    Justificación de la respuesta correcta.
  distractores:
    a: "Motivo por el que es incorrecta."
    c: "..."
    d: "..."
  referencia: "https://docs.aws.amazon.com/..."
```

Requisitos de calidad:
- Los enunciados deben ser escenarios de negocio realistas, al estilo del examen, y no preguntas de definición literal.
- Todos los distractores deben ser plausibles; no se admiten opciones absurdas.
- Cada distractor debe tener su explicación.
- No incluyas "todas las anteriores" ni "ninguna de las anteriores".
- `validar_preguntas.py` debe comprobar: conformidad con el esquema, unicidad de `id`, que `correctas` referencie opciones existentes, número de correctas coherente con el tipo, que `tarea` exista en `fuentes/dominio-N.md` y la distribución por tipos.

## 8. Laboratorios

Para los módulos 02, 03, 04 y 05 (y opcionalmente el 01) incluye un laboratorio guiado con:
- Objetivo y relación con las tareas del examen.
- Requisitos previos: cuenta de AWS, región recomendada con disponibilidad de Bedrock y acceso a modelos.
- Pasos por consola y, cuando sea razonable, equivalente en AWS CLI o boto3.
- **Estimación de coste** y advertencia explícita de facturación.
- **Sección obligatoria de limpieza de recursos** (Knowledge Bases, colecciones vectoriales de OpenSearch Serverless, endpoints de SageMaker, etc.), con especial atención a los recursos que generan coste por hora.
- Laboratorios sugeridos: playground de Bedrock con parámetros de inferencia (temperatura, top-p, longitud máxima); Knowledge Base sobre documentos propios; Guardrails (temas denegados, filtros de contenido, PII); evaluación de modelos en Bedrock; SageMaker Clarify o Model Cards a nivel demostrativo; políticas IAM de mínimo privilegio para Bedrock.

## 9. Integración continua (`.github/workflows/ci.yml`)

En cada *push* y *pull request*:
1. `markdownlint` sobre todos los `.md`.
2. Comprobación de enlaces rotos (por ejemplo, `lychee`).
3. `python scripts/validar_preguntas.py`, que debe fallar ante cualquier error.
4. Búsqueda de marcadores `PENDIENTE DE VERIFICAR`: genera un aviso, sin romper la build.

## 10. Convenciones Git

- Commits con *Conventional Commits* (`feat(modulo-03): ...`, `docs: ...`, `fix(preguntas): ...`, `ci: ...`).
- Una rama por módulo (`modulo/03-modelos-fundacionales`), integrada en `main` mediante PR.
- `CHANGELOG.md` actualizado en cada módulo completado.
- Etiqueta `v1.0.0` cuando los siete módulos y el simulacro estén completos y la CI pase en verde.

## 11. Flujo de trabajo incremental

Trabaja por iteraciones y **detente al final de cada una para revisión humana**:

- **Iteración 0:** estructura del repositorio, `README.md`, `AGENTS.md`, esquema JSON, scripts de validación y quiz, CI y transcripción de `fuentes/dominio-1..5.md` desde la guía oficial.
- **Iteración 1:** módulo 00 (base de AWS) y módulo 01.
- **Iteraciones 2 a 5:** un módulo de dominio por iteración (02 a 05).
- **Iteración 6:** simulacro, `glosario.md`, `chuleta.md` y revisión cruzada de cobertura.

Al cerrar cada iteración entrega un resumen con: ficheros creados o modificados; mapa de cobertura del dominio (tareas cubiertas frente a totales); número de preguntas por tipo; marcadores `PENDIENTE DE VERIFICAR` abiertos; resultado de la CI o de los scripts en local.

## 12. Criterios de aceptación del curso completo

- 100 % de las tareas y habilidades oficiales de los cinco dominios cubiertas y trazadas en los mapas de cobertura.
- Ningún servicio de la lista oficial *in scope* sin mencionar; ningún servicio *out of scope* tratado como materia evaluable.
- Al menos 300 preguntas en los módulos y 65 en el simulacro, todas validadas por el script.
- Todos los laboratorios con estimación de coste y limpieza de recursos.
- CI en verde y ningún marcador `PENDIENTE DE VERIFICAR` sin resolver en la versión `v1.0.0`.
- Recomendación final en el `README.md`: validar la preparación con el examen de práctica oficial de AWS Skill Builder antes de reservar el examen.

## 13. Primera acción

Comienza por la **iteración 0**. Antes de crear ficheros, consulta la guía oficial y confirma si los datos de la sección 4 siguen vigentes. Después crea la estructura y detente para revisión.