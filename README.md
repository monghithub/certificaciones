# Certificaciones

Repositorio con **todos los cursos de preparación de certificaciones** que se vayan estudiando, de cualquier proveedor (AWS, Microsoft, Google Cloud, Kubernetes, etc.), en español de España. Incluye una consola web común para estudiarlos, hacer cuestionarios y simulacros y seguir el progreso de cada estudiante.

Cada curso es autocontenido en `cursos/<curso>/`, con su manifiesto, sus fuentes oficiales y, si las necesita, sus propias reglas. Las herramientas de calidad, las reglas comunes ([AGENTS.md](AGENTS.md)) y la consola son compartidas.

## Cursos

| Proveedor | Curso | Estado | Contenido |
|---|---|---|---|
| AWS | [AWS Certified AI Practitioner (AIF-C01)](cursos/aif-c01/README.md) | En construcción: módulos 00 a 05 completados (dominios 1 a 5, 401 preguntas) | [cursos/aif-c01/](cursos/aif-c01/) |

## Estructura

```text
cursos/<curso>/
├── curso.yaml        Manifiesto: título, proveedor, fuentes oficiales, dominios y pesos, simulacro y mínimos del banco
├── fuentes/          Guía oficial del examen transcrita
├── modulos/NN-*/     README.md, servicios.md, trampas.md, preguntas.yaml, laboratorio.md
├── glosario.yaml     Glosario del curso
├── AGENTS.md         Reglas propias del curso (opcional)
├── promt.md          Especificación del curso (opcional)
└── README.md         Presentación y plan de estudio del curso
schemas/              JSON Schema de preguntas y de manifiestos de curso
scripts/              Validador de preguntas y quiz de terminal
app/, curso/          Consola web y lógica de corrección compartida
docs/consola.md       Puesta en marcha, usuarios, matrículas y copias de seguridad
docs/journal.md       Diario de trabajo: qué se hizo, qué se decidió y por qué
openspec/             Propuestas, diseños y specs de cada etapa (OpenSpec)
```

## Añadir un curso

1. Propón el curso como un cambio de OpenSpec (`/opsx:propose`); el procedimiento completo está en [AGENTS.md](AGENTS.md#añadir-un-curso-nuevo).
2. Crea `cursos/<slug>/curso.yaml` (el `slug` debe coincidir con la carpeta; consulta [schemas/curso.schema.json](schemas/curso.schema.json) y el manifiesto de [AIF-C01](cursos/aif-c01/curso.yaml)). Declara `proveedor` y `fuentes_oficiales`: los hosts de la documentación oficial que podrán citar las preguntas.
3. Transcribe la guía oficial del examen en `fuentes/` y añade `modulos/NN-nombre/` con su `README.md` y, si procede, `preguntas.yaml`.
4. Valida con `python scripts/validar_preguntas.py --curso <slug>` y `python scripts/comprobar_cobertura.py --curso <slug> --preguntas`.
5. En la consola, pulsa «Recargar contenido» y matricula a los usuarios en el curso desde la administración.

## Consola web

Índice de cada curso, lectura de módulos, tests, simulacro cronometrado y estadísticas. El administrador da de alta a los usuarios (`admin` o `estudiante`) y los matricula en los cursos que correspondan; cada estudiante solo ve los suyos. Detalles en [docs/consola.md](docs/consola.md).

```bash
cp .env.example .env   # define SECRET_KEY
docker compose up -d --build
```

## Herramientas

```bash
pip install -r requirements-app.txt
python scripts/validar_preguntas.py     # valida todos los cursos
python scripts/quiz.py --curso aif-c01  # cuestionario interactivo
python -m pytest                        # tests
```

## Reglas de contenido

Reglas comunes para colaboradores y agentes en [AGENTS.md](AGENTS.md); las propias de cada curso, en `cursos/<curso>/AGENTS.md`. En todos los cursos, lo no verificable contra una fuente oficial se marca con `> ⚠️ PENDIENTE DE VERIFICAR:` y no se afirma, y las preguntas son de elaboración propia.

## Licencia

Código bajo MIT y contenido bajo CC BY 4.0. Consulta [LICENSE](LICENSE).
