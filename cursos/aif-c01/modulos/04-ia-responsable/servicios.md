# Servicios del módulo 04

Servicios y herramientas de AWS relevantes para el Dominio 4. La columna final recoge cuándo **no** conviene usarlos, que es donde suelen estar los distractores. Referencias: las de [README.md](README.md#referencias). Disponibilidad comprobada el 16 de octubre de 2026.

## Salvaguardas y evaluación

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon Bedrock Guardrails | Filtrar contenido dañino, temas no deseados, palabras y datos personales; detectar alucinaciones con *contextual grounding check* y validar reglas con Automated Reasoning checks. Con `ApplyGuardrail`, también para modelos fuera de Bedrock | Como sustituto de los permisos IAM o del cifrado; con modelos de *embeddings*, reordenación o generación de imágenes, que no lo admiten |
| Amazon Bedrock Model Evaluation | Comparar modelos y aplicaciones con métricas de robustez, toxicidad, nocividad, estereotipos y rechazo, además de exactitud y evaluación humana | Para documentar el uso previsto y el riesgo de un modelo (Model Cards) o para filtrar respuestas en producción (Guardrails) |
| Amazon SageMaker Clarify | Clientes actuales: métricas de sesgo (CI, DPL, DI…) y explicaciones SHAP de modelos de ML clásico | Proyectos nuevos: **ya no admite clientes nuevos**. Para modelos fundacionales, Bedrock Evaluations |
| Amazon SageMaker Model Monitor | Clientes actuales: deriva de calidad, de sesgo y de atribución de características en producción | Proyectos nuevos: **ya no admite clientes nuevos**; AWS remite a sus soluciones abiertas de monitorización con CloudWatch |
| Amazon Augmented AI | Clientes actuales: revisión humana de predicciones con baja confianza | Proyectos nuevos: **ya no admite clientes nuevos** |
| Amazon SageMaker Ground Truth | Clientes actuales: etiquetado de datos con trabajadores humanos | Proyectos nuevos: **ya no admite clientes nuevos** |

## Transparencia y documentación

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| Amazon SageMaker Model Cards | Documentar uso previsto, calificación de riesgo, entrenamiento y evaluación de un modelo propio, con versiones inmutables y exportación a PDF | Para medir sesgo o explicar predicciones: documenta, no mide |
| AWS AI Service Cards | Conocer el uso previsto, las limitaciones y las decisiones de diseño responsable de los servicios y modelos de AWS | Para documentar un modelo propio (Model Cards) |
| Amazon SageMaker JumpStart | Desplegar modelos de código abierto cuyos pesos se pueden inspeccionar y auditar | Cuando basta consumir un modelo por API sin gestionar infraestructura (Bedrock) |
| Amazon SageMaker Model Registry | Catalogar versiones de modelos con su estado de aprobación; integra las Model Cards para auditoría | Para el uso previsto o las limitaciones de un servicio de AWS (AI Service Cards) |

## Eficiencia y sostenibilidad

| Servicio | Caso de uso | Cuándo NO usarlo |
|---|---|---|
| AWS Inferentia | Inferencia de modelos de *deep learning* con mejor rendimiento por vatio que instancias comparables | Cuando se usa un modelo por API en Bedrock y no se gestiona infraestructura |
| AWS Lambda | Lógica *serverless* que solo consume recursos cuando se invoca (por ejemplo, llamar a `ApplyGuardrail` antes de un modelo externo) | Cargas de inferencia pesadas y continuas con GPU |
