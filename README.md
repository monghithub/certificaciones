# Plataforma de cursos

Repositorio de cursos en español de España con una consola web para estudiarlos, hacer cuestionarios y seguir el progreso de cada estudiante. Cada curso es autocontenido en `cursos/<curso>/`; las herramientas de calidad y la consola son comunes.

## Cursos

| Curso | Estado | Contenido |
|---|---|---|
| [AWS Certified AI Practitioner (AIF-C01)](cursos/aif-c01/README.md) | En construcción: módulos 00 y 01 completados (Dominio 1) | [cursos/aif-c01/](cursos/aif-c01/) |

## Estructura

```text
cursos/<curso>/
├── curso.yaml        Manifiesto: título, dominios y pesos, simulacro y mínimos del banco
├── fuentes/          Fuentes oficiales transcritas (si el curso las usa)
├── modulos/NN-*/     README.md, servicios.md, trampas.md, preguntas.yaml, laboratorio.md
└── README.md         Presentación y plan de estudio del curso
schemas/              JSON Schema de preguntas y de manifiestos de curso
scripts/              Validador de preguntas y quiz de terminal
app/, curso/          Consola web y lógica de corrección compartida
docs/consola.md       Puesta en marcha, usuarios, matrículas y copias de seguridad
```

## Añadir un curso

1. Crea `cursos/<slug>/curso.yaml` (el `slug` debe coincidir con la carpeta; consulta [schemas/curso.schema.json](schemas/curso.schema.json) y el manifiesto de [AIF-C01](cursos/aif-c01/curso.yaml)).
2. Añade `modulos/NN-nombre/` con su `README.md` y, si procede, `preguntas.yaml`.
3. Valida con `python scripts/validar_preguntas.py --curso <slug>`.
4. En la consola, pulsa «Recargar contenido» y matricula a los usuarios en el curso desde la administración.

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

Resumen para colaboradores y agentes en [AGENTS.md](AGENTS.md). En todos los cursos, lo no verificable contra una fuente oficial se marca con `> ⚠️ PENDIENTE DE VERIFICAR:` y no se afirma.

## Licencia

Código bajo MIT y contenido bajo CC BY 4.0. Consulta [LICENSE](LICENSE).
