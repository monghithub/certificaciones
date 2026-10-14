## Why

Con la Iteración 0 (cimientos), la consola web y el soporte multicurso (el contenido vive ahora en `cursos/aif-c01/`) ya disponibles, el curso no tiene todavía contenido que estudiar ni preguntas que practicar. La Iteración 1 (sección 11 de `promt.md`) escribe el primer bloque: la base de AWS que necesita un perfil junior y el Dominio 1 (Fundamentos de IA y ML, 20 % del examen), de modo que ya se pueda estudiar y practicar de principio a fin en la consola.

## What Changes

- **Módulo 00 (Base de AWS):** `README.md` (teoría), `servicios.md` y `trampas.md` con los conocimientos de AWS que la guía oficial recomienda al candidato (servicios centrales, modelo de responsabilidad compartida, IAM y modelos de precios), tratados solo al nivel necesario para reconocerlos en una pregunta. Sin banco de preguntas: no corresponde a ningún dominio ni tarea oficial.
- **Módulo 01 (Fundamentos de IA y ML, Dominio 1):** `README.md` con objetivos de aprendizaje, **mapa de cobertura** de los 17 objetivos de las Task Statements 1.1, 1.2 y 1.3, teoría con diagramas Mermaid, puntos clave y referencias; `servicios.md`; `trampas.md`; `preguntas.yaml` con **al menos 30 preguntas** originales (≈60/20/10/10 por tipo) repartidas entre las tres tareas; y un `laboratorio.md` demostrativo opcional con estimación de coste y limpieza.
- **Herramienta nueva:** `scripts/comprobar_cobertura.py --curso <slug>`, que verifica que cada objetivo de `cursos/<curso>/fuentes/dominio-N.md` aparece en el mapa de cobertura del módulo y que cada tarea tiene preguntas. Se integra en el CI.
- Verificación de cada dato de servicio contra la documentación oficial de AWS; lo no verificable se marca `> ⚠️ PENDIENTE DE VERIFICAR:`.
- Actualización de `CHANGELOG.md` y del índice del `README.md`.
- Fuera de alcance: módulos 02–06, glosario y chuleta (iteraciones posteriores), y cualquier cambio en la consola.

## Capabilities

### New Capabilities
- `modulo-00-base-aws`: contenido del módulo 00 y su mapa de cobertura frente a los conocimientos de AWS recomendados por la guía.
- `modulo-01-fundamentos-ia-ml`: contenido del módulo 01 (teoría, servicios, trampas, laboratorio) y cobertura completa del Dominio 1.
- `banco-preguntas-dominio-1`: banco de al menos 30 preguntas del Dominio 1, con distribución por tareas y por tipos y referencias oficiales verificables.
- `comprobacion-cobertura`: script que comprueba la cobertura de objetivos y tareas, ejecutado en CI.

### Modified Capabilities
<!-- Ninguna: el formato de preguntas, el validador y la consola no cambian de requisitos. -->

## Impact

- Ficheros nuevos en `cursos/aif-c01/modulos/00-base-aws/` y `cursos/aif-c01/modulos/01-fundamentos-ia-ml/`, y `scripts/comprobar_cobertura.py` con sus tests.
- La consola web los muestra automáticamente en el curso `aif-c01` (índice, lectura y tests); no requiere cambios de código.
- `.github/workflows/ci.yml` incorpora la comprobación de cobertura; `lychee` comprobará las referencias nuevas.
- Requiere acceso web a `docs.aws.amazon.com` para verificar los datos. Los precios y cuotas no se afirman sin fuente.
- Git: según `promt.md` cada módulo va en su rama y se integra por PR; el repositorio aún no tiene commits (ver Open Questions del diseño).
