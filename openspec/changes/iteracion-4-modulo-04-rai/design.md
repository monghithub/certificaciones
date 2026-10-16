## Context

El Dominio 4 tiene 2 tareas y 11 objetivos (`fuentes/dominio-4.md`, guía v1.1) y pesa el 14 %. La tarea 4.1 trata del desarrollo de sistemas de IA responsables (rasgos, herramientas, selección responsable de modelos, riesgos legales, características de los datos, sesgo y varianza, herramientas de detección y monitorización) y la 4.2, de la transparencia y la explicabilidad (diferencias, herramientas, compromisos con la seguridad y el rendimiento, diseño centrado en las personas). El módulo 01 ya presentó sobreajuste y subajuste y el 03, Guardrails frente a la inyección de *prompts* y Model Evaluation: el 04 los usa desde el punto de vista de la IA responsable.

## Goals / Non-Goals

**Goals:**
- Cubrir los 11 objetivos con definición, criterio de decisión, ejemplo de negocio y trampa.
- Reflejar el estado vigente de las herramientas: Clarify, Model Monitor, Ground Truth y Augmented AI (A2I) ya no admiten clientes nuevos, y AWS indica qué las sustituye.
- Un banco de unas 66–72 preguntas originales que pase todos los controles sin avisos, con al menos un 18 % de dificultad baja.
- Un laboratorio de coste mínimo, sin recursos con coste por hora.

**Non-Goals:**
- Seguridad, cumplimiento y gobierno (IAM, cifrado, CloudTrail, Config, marcos de gobierno): módulo 05.
- Calcular métricas de sesgo o implantar SHAP: el nivel es *foundational*; solo se reconocen.

## Decisions

- **Estructura de la teoría por tarea:**
  - 4.1: dimensiones de AWS (equidad, explicabilidad, privacidad y seguridad, seguridad frente a daños, controlabilidad, veracidad y robustez, gobierno, transparencia) más inclusividad y sesgo; herramientas (Guardrails con sus seis salvaguardas y niveles, Model Evaluation con métricas de responsabilidad, Clarify, Model Monitor, A2I) con diagrama; selección responsable de modelos (sostenibilidad, modelo más pequeño que cumple, eficiencia energética, AI Service Cards); riesgos legales (propiedad intelectual e indemnización, resultados sesgados, pérdida de confianza, riesgo para el usuario final, alucinaciones) con mitigaciones; características de los conjuntos de datos con ejemplo numérico de desequilibrio; sesgo y varianza con ejemplo numérico; detección y monitorización (calidad de etiquetas, auditorías humanas, análisis por subgrupos con ejemplo numérico).
  - 4.2: transparente/explicable frente a caja negra con tabla; herramientas (Model Cards, AI Service Cards, Model Evaluation, modelos y datos abiertos, licencias); compromisos entre interpretabilidad, rendimiento y seguridad con diagrama; diseño centrado en las personas (mecanismos de *feedback*, transparencia de las decisiones, supervisión humana, puntuaciones de confianza).
- **Verificación primero:** fuentes en `docs.aws.amazon.com` (Bedrock, SageMaker AI, Well-Architected Responsible AI Lens y Generative AI Lens, guía prescriptiva de interpretabilidad) y `aws.amazon.com` (Responsible AI, política de IA responsable, FAQ de Bedrock, AI Service Cards).
- **Laboratorio:** Amazon Bedrock Guardrails en la consola: crear un *guardrail* con filtros de contenido, un tema denegado, enmascarado de PII y *contextual grounding check*; probarlo en la ventana de prueba con un modelo económico de Amazon Nova; crear una versión; limpieza. Equivalente opcional con `apply-guardrail` de la AWS CLI. Coste con los precios oficiales de Guardrails por unidad de texto.
- **Banco:** unas 68 preguntas (≈41 de opción múltiple, 13 de respuesta múltiple, 7 de ordenación y 7 de emparejamiento), de 5 a 7 por objetivo. Distractores vecinos: filtros de contenido/temas denegados/filtros de palabras/datos sensibles/*grounding*/Automated Reasoning, Clarify/Model Monitor/Model Cards/Model Evaluation, sesgo/varianza, equidad/explicabilidad/transparencia/veracidad, interpretabilidad/explicabilidad.

## Risks / Trade-offs

- [Herramientas cerradas a clientes nuevos que el examen sigue citando] → se explican porque la guía las nombra, con el aviso y la sustitución que indica AWS; las preguntas no las presentan como opción para clientes nuevos.
- [Cifras de marketing (por ejemplo, porcentajes de bloqueo)] → no se usan en preguntas.
- [Coste del laboratorio] → precios por unidad de texto citados con fecha, pocas pruebas, AWS Budgets recomendado y limpieza del *guardrail*.

## Open Questions

- Ninguna bloqueante.
