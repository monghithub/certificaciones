## Why

La revisión técnica independiente de los módulos 00 y 01 (2026-10-14), contrastada con la documentación oficial de AWS, encontró errores factuales y datos desactualizados: D1-026 afirmaba que la mayoría de los servicios de IA no admiten *endpoints* de VPC; SageMaker Experiments es ahora *Classic*; «SageMaker» y «SageMaker AI» se trataban como sinónimos; el laboratorio tenía una política IAM insuficiente para la consola y una capa gratuita desactualizada. Encontró también lagunas de examen (servicios por etapa, capacidades de SageMaker AI, métricas con clases desequilibradas) y un banco de preguntas demasiado fácil, con distractores absurdos y pistas. El usuario pidió corregirlo todo, ampliar mucho el banco y que las mejoras de procedimiento se mantengan en todo el proyecto.

## What Changes

- Correcciones factuales en los módulos 00 y 01, el laboratorio y el glosario, verificadas en `docs.aws.amazon.com`.
- Contenido nuevo en el módulo 00 (políticas, grupos y roles de IAM; VPC, CloudWatch y CloudTrail; precios de los servicios de IA; Budgets, Cost Explorer y capa gratuita) y en el módulo 01 (diagrama anidado con IA agéntica, aprendizaje autosupervisado, matices de inferencia, escenarios por servicio, capacidades de SageMaker AI, servicios de datos por etapa, Amazon Nova, matriz de confusión con ejemplo, trampa de la exactitud, métricas de negocio).
- Banco del Dominio 1: de 32 a 82 preguntas originales, al estilo de escenario del examen, con la posición de la respuesta correcta repartida.
- Glosario: 18 entradas nuevas y corrección del alias de SageMaker.
- Reglas permanentes: secciones «Calidad del contenido» y «Calidad del banco de preguntas» en `AGENTS.md`; mínimos más altos en `curso.yaml` y `promt.md`.
- Herramientas: `minimo_por_objetivo` en el manifiesto y en `comprobar_cobertura.py`; nuevos controles de calidad en `validar_preguntas.py`, con tests.
- Enlace al conjunto oficial de práctica de AWS Skill Builder en el README del curso.

## Capabilities

### New Capabilities
- `calidad-contenido`: reglas de calidad y verificación aplicables a todo módulo del proyecto.
- `validacion-calidad-banco`: controles automáticos de calidad del banco de preguntas y mínimo por objetivo.

### Modified Capabilities
- `banco-preguntas-dominio-1`: tamaño mínimo y reparto por tareas y objetivos más exigentes.

## Impact

- `cursos/aif-c01/` (módulos 00 y 01, glosario, README, `curso.yaml`, fuentes), `AGENTS.md`, `promt.md`, `CHANGELOG.md`.
- `scripts/validar_preguntas.py`, `scripts/comprobar_cobertura.py`, `curso/manifiesto.py`, `schemas/curso.schema.json` y sus tests.
- Los módulos 02 a 05 deberán cumplir los nuevos mínimos (60 por módulo, 15 por tarea, 3 por objetivo) y los controles de calidad desde su primera versión.
