## 1. Herramienta de cobertura

- [x] 1.1 Definir el formato del mapa de cobertura (tabla con id `N.M.K` en la primera columna y enlace a ancla) y documentarlo en `AGENTS.md`
- [x] 1.2 Implementar `scripts/comprobar_cobertura.py` (`--curso`, `--modulo`, `--preguntas`, resumen, código de salida)
- [x] 1.3 Tests con fixtures: cubierto, objetivo ausente, ancla rota, tarea sin preguntas, módulo vacío omitido
- [x] 1.4 Añadir el paso al CI

## 2. Fuente de conocimientos previos

- [x] 2.1 Consultar la sección «Recommended AWS knowledge» de la guía y crear `cursos/aif-c01/fuentes/conocimientos-previos.md` con URL, fecha y texto literal

## 3. Módulo 00 (base de AWS)

- [x] 3.1 Verificar contra documentación oficial: servicios centrales (EC2, S3, Lambda, y Bedrock/SageMaker a nivel de presentación), responsabilidad compartida, IAM y modelos de precios
- [x] 3.2 Redactar `README.md` con la plantilla (objetivos, mapa de cobertura frente a los cuatro conocimientos, teoría con Mermaid, puntos clave, referencias)
- [x] 3.3 Redactar `servicios.md` (servicio → caso de uso → cuándo NO usarlo)
- [x] 3.4 Redactar `trampas.md`

## 4. Módulo 01, Tarea 1.1 (conceptos y terminología)

- [x] 4.1 Verificar fuentes oficiales para los objetivos 1.1.1–1.1.5 (términos de IA, diferencias IA/ML/GenAI/deep learning/agentic AI, tipos de inferencia, tipos de datos, tipos de aprendizaje)
- [x] 4.2 Redactar la teoría de la Tarea 1.1 con diagramas Mermaid
- [x] 4.3 Escribir 10 preguntas de la Tarea 1.1 con referencias oficiales

## 5. Módulo 01, Tarea 1.2 (casos de uso)

- [x] 5.1 Verificar fuentes oficiales para los objetivos 1.2.1–1.2.6 (valor de IA/ML, cuándo no usarla, técnica adecuada, aplicaciones reales, servicios gestionados, ML tradicional frente a FMs)
- [x] 5.2 Redactar la teoría de la Tarea 1.2
- [x] 5.3 Escribir 12 preguntas de la Tarea 1.2 con referencias oficiales

## 6. Módulo 01, Tarea 1.3 (ciclo de vida)

- [x] 6.1 Verificar fuentes oficiales para los objetivos 1.3.1–1.3.6 (pipeline, fuentes de FMs, despliegue, servicios por etapa, MLOps, métricas)
- [x] 6.2 Redactar la teoría de la Tarea 1.3 con diagrama del ciclo de vida
- [x] 6.3 Escribir 10 preguntas de la Tarea 1.3 con referencias oficiales

## 7. Módulo 01, ficheros transversales

- [x] 7.1 Redactar `servicios.md` (solo servicios in scope; Amazon Q sin tratar como evaluable)
- [x] 7.2 Redactar `trampas.md`
- [x] 7.3 Componer `README.md`: objetivos, mapa de cobertura de los 17 objetivos, teoría integrada, 5–10 puntos clave y referencias
- [x] 7.4 Redactar `laboratorio.md` demostrativo con estimación de coste verificada (o pendiente), aviso de facturación y limpieza

## 8. Verificación y cierre

- [x] 8.1 Ejecutar `validar_preguntas.py`, `comprobar_cobertura.py`, `pytest` y `markdownlint` y corregir incidencias
- [x] 8.2 Comprobar que todas las URL de `referencia` y de las secciones Referencias responden con éxito
- [x] 8.3 Recargar la consola y probar con `test` y `admintest`: lectura de ambos módulos y un test del dominio 1 con los cuatro tipos
- [x] 8.4 Actualizar `CHANGELOG.md` y el índice del `README.md` del curso
- [x] 8.5 Generar el resumen de cierre (ficheros, cobertura 17/17, preguntas por tipo, marcadores pendientes, resultados) y detenerse para revisión humana
