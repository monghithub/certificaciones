## Why

Los módulos 00 a 05 están completos e integrados en `main` (401 preguntas). Falta la Iteración 6 de `cursos/aif-c01/promt.md`: el simulacro de 65 preguntas inéditas con los pesos oficiales, `glosario.md`, `chuleta.md` y la revisión cruzada de cobertura del curso completo. El usuario pidió continuar «con todo hasta el final».

## What Changes

- **Simulacro (`cursos/aif-c01/modulos/06-simulacro/`):** `README.md` con instrucciones (65 preguntas, 90 minutos, reparto por dominio y tipo, cómo interpretar el resultado y la recomendación del conjunto oficial de práctica) y `preguntas.yaml` con 65 preguntas `S-NNN` inéditas: 13 del Dominio 1, 16 del 2, 18 del 3, 9 del 4 y 9 del 5, con los tipos y la dificultad repartidos y los dominios intercalados.
- **Validador:** `scripts/validar_preguntas.py` comprueba que ningún enunciado del simulacro repite uno de los bancos de los módulos (comparación normalizada), con su prueba.
- **Glosario:** `scripts/generar_glosario.py` genera `cursos/<curso>/glosario.md` (términos con sus alias en inglés y español, por orden alfabético) a partir de `glosario.yaml`, que sigue siendo la fuente de verdad; con `--comprobar`, la CI falla si está desactualizado. Con su prueba.
- **Chuleta:** `cursos/aif-c01/chuleta.md`, resumen de 2–3 páginas por dominio con los criterios de decisión y las trampas más frecuentes.
- **Revisión cruzada:** 69/69 objetivos cubiertos, servicios dentro de alcance mencionados (se añaden al módulo 01 y al glosario los seis que faltaban: AWS Data Exchange, Amazon EMR, Amazon Redshift, Amazon ECS, Amazon EKS y Amazon CloudFront), ningún servicio fuera de alcance como respuesta correcta, y revisión de los marcadores `PENDIENTE DE VERIFICAR`.
- Revisión independiente del simulacro y de la chuleta; `CHANGELOG.md`, `docs/journal.md` y README.
- Fuera de alcance: la etiqueta `aif-c01-v1.0.0`, que exige no tener marcadores pendientes.

## Capabilities

### New Capabilities
- `simulacro-aif-c01`: simulacro de 65 preguntas inéditas con los pesos oficiales e instrucciones.
- `chuleta-y-glosario`: chuleta de repaso y glosario en Markdown generado desde el YAML.

### Modified Capabilities
- `question-validation`: el validador comprueba que las preguntas del simulacro son inéditas.

## Impact

- Ficheros nuevos: `cursos/aif-c01/modulos/06-simulacro/{README.md,preguntas.yaml}`, `cursos/aif-c01/chuleta.md`, `cursos/aif-c01/glosario.md`, `scripts/generar_glosario.py` y pruebas.
- Cambios: `scripts/validar_preguntas.py`, `.github/workflows/ci.yml`, módulo 01 (servicios por etapa) y `glosario.yaml`.
- La consola ya admite el simulacro cronometrado (toma las 65 primeras preguntas por `id`); no hay cambios de código en la consola.
- Git: rama `aif-c01/simulacro` con PR a `main`.
