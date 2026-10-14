# Journal del proyecto

Diario de trabajo del curso AIF-C01 y de su consola. Recoge **qué se hizo, qué se decidió y por qué** en cada etapa, con sus commits y cambios de OpenSpec. El detalle de los cambios está en [CHANGELOG.md](../CHANGELOG.md); los requisitos vigentes, en [openspec/specs/](../openspec/specs/).

## Cómo se trabaja

1. **Proponer** cada etapa como un cambio de OpenSpec (`/opsx:propose`): `proposal.md`, `design.md`, `specs/` y `tasks.md`.
2. **Revisar** la propuesta con el usuario antes de implementar.
3. **Implementar** (`/opsx:apply`) en una rama propia (`modulo/NN-…` o `feat/…`), marcando las tareas.
4. **Verificar**: `validar_preguntas.py`, `comprobar_cobertura.py --preguntas`, markdownlint, Mermaid (`tests/e2e`) y `pytest`.
5. **Revisión independiente** del contenido al cerrar cada módulo (ver `AGENTS.md`, «Calidad del contenido»).
6. **Cerrar la etapa**: archivar el cambio (`/opsx:archive`), actualizar `CHANGELOG.md` y este journal, commit con *Conventional Commits*, push y PR a `main`.

---

## 2026-10-14

### Iteración 0: fundación del curso

- Estructura del repositorio, `AGENTS.md`, licencia propuesta (MIT para el código y CC BY 4.0 para el contenido, pendiente de confirmar), esquema JSON del banco, `validar_preguntas.py`, `quiz.py` y CI (markdownlint, lychee, validación y aviso de pendientes).
- Transcripción literal de la guía oficial v1.1 (30 de abril de 2026): 69 objetivos en 14 tareas y listas de servicios dentro y fuera de alcance.
- Decisión: se llaman **objetivos** (`N.M.K`) a lo que `promt.md` llamaba habilidades, como hace la guía v1.1.
- OpenSpec: `2026-10-14-iteracion-0-fundacion-curso`.

### Consola web, soporte multicurso, glosario y diagramas

- Consola web (FastAPI) con roles `admin` y `estudiante`, lectura con seguimiento, cuestionarios, simulacro cronometrado y estadísticas.
- Multicurso: el contenido pasa a `cursos/<slug>/` con manifiesto `curso.yaml`; matrícula por curso.
- Glosario por curso con modal y diagramas Mermaid con estilo único validado, en los que cada caja abre información y enlaces.
- OpenSpec: `consola-web-curso`, `soporte-multicurso`, `glosario-y-diagramas-interactivos` e `info-en-cajas-de-diagramas` (archivados con fecha 2026-10-14).

### Iteración 1: módulos 00 y 01

- Módulo 00 (base de AWS) y módulo 01 (Dominio 1) con mapa de cobertura de los 17 objetivos, laboratorio demostrativo y 32 preguntas.
- Nueva herramienta `comprobar_cobertura.py`.
- OpenSpec: `2026-10-14-iteracion-1-modulos-00-01`.

### Revisión de calidad de la Iteración 1

- **Encargo:** revisión crítica independiente de los módulos 00 y 01 como experto en AIF-C01 y en didáctica para perfiles junior, sin modificar ficheros. Primera valoración: 6,5/10 de preparación para el Dominio 1.
- **Hallazgos verificados en la documentación oficial:**
  - D1-026 afirmaba que la mayoría de los servicios de IA no admiten *endpoints* de VPC. Es falso según la lista de PrivateLink; la frase venía de una guía de decisión de mayo de 2024.
  - SageMaker Experiments es ahora *Classic*; AWS recomienda MLflow.
  - Desde el 3 de diciembre de 2024, «Amazon SageMaker» es una plataforma unificada que incluye SageMaker AI.
  - La política IAM del laboratorio no servía para la consola.
  - La capa gratuita cambió en julio de 2025 (créditos y plan de seis meses).
  - Ground Truth tampoco admite clientes nuevos; se suma a Model Monitor, Clarify y Bedrock Agents Classic.
- **Lagunas:** servicios por etapa (datos), capacidades de SageMaker AI (Canvas, Pipelines, Model Registry), Amazon Nova, restricciones operativas, matriz de confusión y exactitud con clases desequilibradas.
- **El usuario pidió:**
  1. Mejorar todo lo posible.
  2. Que las mejoras de procedimiento valgan para todo el proyecto.
  3. Muchas más preguntas, al estilo de las típicas del examen.
  4. Enlazar AWS Skill Builder.
- **Hecho:**
  - Correcciones y ampliaciones en los módulos 00 y 01, el laboratorio y el glosario (18 entradas nuevas).
  - Banco de 32 a **82 preguntas**, al menos 3 por objetivo y la posición de la respuesta repartida (12–13 por letra).
  - Reglas permanentes en `AGENTS.md`: «Calidad del contenido» y «Calidad del banco de preguntas».
  - Mínimos más altos (60 por módulo, 15 por tarea, 3 por objetivo).
  - Controles nuevos en la CI (posición de la respuesta, opciones repetidas, mínimo por objetivo, avisos por absolutos y por enunciados cortos).
  - Enlace al conjunto oficial de práctica de Skill Builder.
- **Decisiones:**
  - Las preguntas son siempre originales. El conjunto oficial de Skill Builder (20 preguntas, requiere iniciar sesión) solo se recomienda como control final y no se copia. No se usan *dumps*.
  - La posición de la respuesta se reparte en el YAML, porque el quiz y la consola no barajan las opciones.
  - Las heurísticas con falsos positivos son avisos; los controles objetivos son errores.
- **Verificación:** validador sin avisos, cobertura, markdownlint, 5/5 diagramas Mermaid y 215 tests en verde.
- OpenSpec: `2026-10-14-revision-calidad-iteracion-1`, documentado a posteriori porque la revisión empezó como informe y el usuario pidió aplicar los cambios sobre la marcha.

### Cierre de etapas y primera subida al repositorio

- Primeros commits del repositorio, agrupados por bloque: fundación y herramientas, consola, módulos 00 y 01, y OpenSpec. Identidad de git local del repositorio: `monghithub <monghit@gmail.com>`.
- Archivados los 7 cambios completados de OpenSpec. Para poder archivarlos se corrigieron dos requisitos antiguos que no usaban la palabra normativa SHALL (`official-sources`, `glosario-conceptos`). Los 26 specs consolidados en `openspec/specs/` validan en modo estricto.
- Push inicial de `main` a `origin` (`github.com/monghithub/aw-saif-c01`). A partir de aquí, cada etapa en su rama y con PR.
- La primera CI en GitHub falló solo por la comprobación de enlaces: `docs/consola.md` cita `http://127.0.0.1:8000/`. Se excluyen los enlaces locales en `.lychee.toml` y la CI pasa a verde en `main`.

### Renombrado del repositorio

- A petición del usuario, el repositorio de GitHub pasa de `aw-saif-c01` a **`certificaciones`** (`github.com/monghithub/certificaciones`). GitHub redirige el nombre antiguo, y el remoto `origin` local ya apunta al nuevo. La carpeta local del clon conserva su nombre.

### Plataforma multicertificación

- **Visión del usuario:** el repositorio reunirá en la consola todos los cursos de certificación que vaya estudiando, de cualquier proveedor, no solo de AWS.
- **Hecho** (rama `feat/plataforma-multicertificacion`, cambio de OpenSpec `plataforma-multicertificacion`):
  - Campos `proveedor` y `fuentes_oficiales` en el manifiesto; las referencias de las preguntas se validan contra las fuentes oficiales de su curso.
  - `AGENTS.md` raíz genérico, con el procedimiento para añadir un curso, y reglas propias de AWS y AIF-C01 en `cursos/aif-c01/AGENTS.md`.
  - `promt.md` movido a `cursos/aif-c01/`.
  - Consola «Certificaciones», imagen `certificaciones-consola` y README raíz con tabla de cursos por proveedor.
- **Decisiones:**
  - Las fuentes oficiales se declaran como hosts (se aceptan los subdominios) y son opcionales, para no romper los cursos existentes.
  - Cada curso lleva su propio `AGENTS.md`, que complementa al raíz.
  - Ramas `<slug>/<etapa>` y etiquetas `<slug>-vX.Y.Z` por curso.
- **Verificación:** validador, cobertura y 219 tests en verde (4 nuevos).

### Pendiente

- Iteraciones 2 a 5: módulos 02 a 05, con al menos 60 preguntas cada uno y laboratorio obligatorio.
- Iteración 6: simulacro de 65 preguntas inéditas, `chuleta.md`, decidir sobre `glosario.md` (hoy existe `glosario.yaml`) y revisión cruzada.
- Marcadores `PENDIENTE DE VERIFICAR` en `fuentes/servicios-alcance.md` (Amazon Q; incoherencia de la lista out of scope de AWS).
- Decisiones del usuario: licencia y formato de `ordering`/`matching`.
- Borrar los usuarios de prueba `test` y `admintest` de la consola local al terminar los desarrollos.
- Etiqueta `v1.0.0` con todo completo, la CI en verde y sin pendientes.
