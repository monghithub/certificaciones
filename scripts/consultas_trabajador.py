#!/usr/bin/env python3
"""Trabajador de «Preguntar a Claude»: resuelve en segundo plano las dudas de los tests con Claude Code.

Se ejecuta en el anfitrión (no en el contenedor de la consola), con la sesión de Claude Code de la cuenta del
responsable. Recoge las dudas pendientes de la API interna de la consola (protegida con CONSULTAS_TOKEN), las
resuelve de una en una con `claude -p` (modelo Sonnet, solo herramientas de lectura y búsqueda) y devuelve la
respuesta. Los mensajes siguientes de una conversación continúan la sesión de Claude con `--resume`.

Solo biblioteca estándar. Configuración por variables de entorno (ver `docs/consola.md`):

    CONSULTAS_URL           http://127.0.0.1:8097     base de la consola
    CONSULTAS_TOKEN         (obligatoria)             el mismo que en el .env de la consola
    CONSULTAS_CLAUDE        claude                    ejecutable de Claude Code
    CONSULTAS_MODELO        sonnet
    CONSULTAS_DIR           ~/.local/share/consultas-claude   directorio de trabajo fijo (las sesiones dependen de él)
    CONSULTAS_CURSOS        (recomendada)             carpeta cursos/ desplegada
    CONSULTAS_LIBROS        (opcional)                libros de estudio en Markdown
    CONSULTAS_ESPERA        10                        segundos entre sondeos sin trabajo
    CONSULTAS_ESPERA_CUOTA  900                       espera tras cuota agotada o error transitorio
    CONSULTAS_TIMEOUT       300                       tiempo máximo de cada llamada a Claude

Uso: python3 scripts/consultas_trabajador.py [--una-vez]
"""
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

HERRAMIENTAS = "Read,Grep,Glob,WebFetch,WebSearch"  # solo lectura y búsqueda: sin terminal ni edición
MAX_INTENTOS = 3
CUOTA_RE = re.compile(r"limit|overloaded", re.I)  # «usage limit», «rate limit», «limit reached»…
SESION_PERDIDA_RE = re.compile(r"no conversation found|session[^\n]{0,80}(not found|does not exist|no existe)", re.I)
PIDE_SOLUCION_RE = re.compile(
    r"soluci[oó]n|respuesta (correcta|buena)|(la|las) correctas?\b|cu[aá]l(es)? (es|son) (la|las) (respuesta|correcta|buena|opci[oó]n)"
    r"|dime (la|las) respuestas?|qu[eé] (opci[oó]n|respuesta) es", re.I)

SISTEMA = """Eres el tutor de la consola de estudio del curso {curso} (certificación AWS Certified AI Practitioner, nivel foundational).
Respondes dudas sobre una pregunta de test concreta, en español de España, claro y breve (máximo ~250 palabras salvo que pidan más),
manteniendo en inglés los nombres de servicios y términos del examen.
- Si el estudiante aún no ha respondido, orienta sin revelar la respuesta correcta, salvo que la pida expresamente.
- Apóyate en la teoría del curso (ficheros en {cursos}/{curso}/modulos y glosario.yaml) y verifica los datos en la documentación
  oficial de AWS (docs.aws.amazon.com, aws.amazon.com). Termina con la URL oficial que respalda lo principal.
- Los libros de {libros} son material de terceros de 2025: úsalos solo para entender el tema; si chocan con la documentación vigente,
  prevalece la documentación, y no cites el libro como fuente.
- Si detectas un error en la pregunta o en el curso, dilo claramente al final con «Posible error en el curso:».
- No ejecutes nada ni modifiques ficheros: solo lees y buscas.
- Escribe en Markdown, con los enlaces en formato [texto](URL)."""


@dataclass
class Config:
    url: str
    token: str
    claude: str = "claude"
    modelo: str = "sonnet"
    dir: Path = Path("~/.local/share/consultas-claude").expanduser()
    cursos: Path | None = None
    libros: Path | None = None
    espera: float = 10
    espera_cuota: float = 900
    timeout: float = 300

    @classmethod
    def desde_entorno(cls, env=None) -> "Config":
        env = os.environ if env is None else env
        token = (env.get("CONSULTAS_TOKEN") or "").strip()
        if len(token) < 32:
            raise SystemExit("CONSULTAS_TOKEN es obligatoria (mínimo 32 caracteres), la misma que en el .env de la consola")

        def ruta(nombre):
            v = (env.get(nombre) or "").strip()
            return Path(v).expanduser() if v else None

        return cls(url=(env.get("CONSULTAS_URL") or "http://127.0.0.1:8097").rstrip("/"), token=token,
                   claude=env.get("CONSULTAS_CLAUDE") or "claude", modelo=env.get("CONSULTAS_MODELO") or "sonnet",
                   dir=ruta("CONSULTAS_DIR") or Path("~/.local/share/consultas-claude").expanduser(),
                   cursos=ruta("CONSULTAS_CURSOS"), libros=ruta("CONSULTAS_LIBROS"),
                   espera=float(env.get("CONSULTAS_ESPERA") or 10), espera_cuota=float(env.get("CONSULTAS_ESPERA_CUOTA") or 900),
                   timeout=float(env.get("CONSULTAS_TIMEOUT") or 300))


def log(*partes):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), *partes, flush=True)


# ---------------------------------------------------------------- API de la consola

class ErrorAPI(Exception):
    pass


class API:
    def __init__(self, cfg: Config):
        self.cfg = cfg

    def _post(self, ruta: str, datos: dict | None = None):
        req = urllib.request.Request(self.cfg.url + "/api/consultas" + ruta, method="POST",
                                     data=json.dumps(datos or {}).encode(),
                                     headers={"Authorization": f"Bearer {self.cfg.token}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                cuerpo = r.read()
                return r.status, (json.loads(cuerpo) if cuerpo else None)
        except urllib.error.HTTPError as e:
            raise ErrorAPI(f"{ruta}: HTTP {e.code}") from None
        except (urllib.error.URLError, OSError, ValueError) as e:
            raise ErrorAPI(f"{ruta}: {e}") from None

    def siguiente(self) -> dict | None:
        estado, datos = self._post("/siguiente")
        return datos if estado == 200 else None

    def respuesta(self, mid: int, texto: str, sesion: str | None):
        self._post(f"/mensajes/{mid}/respuesta", {"texto": texto, "sesion_claude": sesion})

    def reintentar(self, mid: int, motivo: str, contar: bool = True):
        self._post(f"/mensajes/{mid}/reintentar", {"motivo": motivo, "contar": contar})

    def error(self, mid: int, motivo: str):
        self._post(f"/mensajes/{mid}/error", {"motivo": motivo})


# ---------------------------------------------------------------- prompt

def pide_solucion(texto: str) -> bool:
    return bool(PIDE_SOLUCION_RE.search(texto or ""))


def _lineas_respuesta(p: dict, valor) -> list[str]:
    """Respuesta o solución (ids) en líneas legibles, como en la consola."""
    if not valor:
        return []
    texto = {o.get("id"): o.get("texto") for o in p.get("opciones") or []}
    opcion = lambda i: f"{i}) {texto[i]}" if i in texto else str(i)  # noqa: E731
    if p.get("tipo") == "ordering":
        return [f"{k}.º {opcion(i)}" for k, i in enumerate(valor, 1)]
    if p.get("tipo") == "matching":
        izq = {x.get("id"): x.get("texto") for x in p.get("prompts") or []}
        return [f"{a}. {izq.get(a, '')} → {opcion(b)}" for a, b in valor]
    return [opcion(i) for i in valor]


def prompt_inicial(trabajo: dict, cfg: Config) -> str:
    """Primer mensaje de la conversación: contexto completo de la pregunta y, al final, la duda.

    Si el estudiante aún no ha respondido, no se incluye la solución (ni la explicación, los distractores o la
    referencia, que la delatan) salvo que la duda la pida expresamente: así Claude no puede revelarla sin querer."""
    p, curso = trabajo["pregunta"], trabajo["curso"]
    respondida = bool(trabajo.get("respondida"))
    con_solucion = respondida or pide_solucion(trabajo["texto"])
    l = ["## Pregunta", "", f"Curso: {curso}. Pregunta {p.get('id')} ({p.get('tipo')}; banco: {p.get('banco')}; módulo: {p.get('modulo')}).", ""]
    l += [p.get("enunciado", "").strip(), ""]
    if p.get("prompts"):
        l += ["Elementos (columna izquierda):"] + [f"{x.get('id')}. {x.get('texto')}" for x in p["prompts"]] + [""]
    l += ["Opciones:"] + [f"{o.get('id')}) {o.get('texto')}" for o in p.get("opciones") or []] + [""]
    if respondida:
        l += ["El estudiante ya ha respondido. Su respuesta:"] + _lineas_respuesta(p, trabajo.get("respuesta_usuario")) + [""]
    else:
        l += ["El estudiante AÚN NO ha respondido esta pregunta."
              + (" Ha pedido expresamente la solución." if con_solucion else " No le reveles la respuesta correcta: oriéntale."), ""]
    if con_solucion:
        l += ["Solución:"] + _lineas_respuesta(p, p.get("correctas")) + [""]
        if p.get("explicacion"):
            l += [f"Explicación del curso: {p['explicacion'].strip()}", ""]
        if p.get("distractores"):
            l += ["Por qué no son correctas las demás:"] + [f"{k}) {v}" for k, v in p["distractores"].items()] + [""]
        if p.get("referencia"):
            l += [f"Referencia oficial de la pregunta: {p['referencia']}", ""]
    if p.get("teoria_fichero") and cfg.cursos:
        l += [f"Teoría del módulo: {cfg.cursos / curso / p['teoria_fichero']}"]
    if p.get("teoria_url"):
        l += [f"Sección de la teoría en la consola: {p['teoria_url']}"]
    l += ["", "## Duda del estudiante", "", trabajo["texto"].strip()]
    return "\n".join(l)


def prompt_seguimiento(trabajo: dict) -> str:
    """Mensajes siguientes (con --resume): solo la duda nueva, con una nota si el estudiante ya ha respondido."""
    l = []
    if trabajo.get("respondida"):
        p = trabajo["pregunta"]
        l += ["(Nota: el estudiante ya ha respondido la pregunta. Su respuesta: "
              + "; ".join(_lineas_respuesta(p, trabajo.get("respuesta_usuario")))
              + ". Solución: " + "; ".join(_lineas_respuesta(p, p.get("correctas"))) + ". Ya puedes comentarla.)", ""]
    l += ["Nueva duda del estudiante:", "", trabajo["texto"].strip()]
    return "\n".join(l)


def sistema(curso: str, cfg: Config) -> str:
    return SISTEMA.format(curso=curso, cursos=cfg.cursos or "(no disponible)", libros=cfg.libros or "(no disponibles)")


# ---------------------------------------------------------------- llamada a Claude

@dataclass
class Resultado:
    ok: bool
    texto: str = ""
    sesion: str | None = None
    coste: float | None = None
    motivo: str = ""
    cuota: bool = False
    sesion_perdida: bool = False


def argumentos(cfg: Config, prompt: str, curso: str, sesion: str | None) -> list[str]:
    args = [cfg.claude, "-p", prompt, "--model", cfg.modelo, "--output-format", "json",
            "--tools", HERRAMIENTAS, "--allowedTools", HERRAMIENTAS]
    dirs = []
    if cfg.cursos:
        dirs.append(str(cfg.cursos / curso))
    if cfg.libros:
        dirs.append(str(cfg.libros / curso if (cfg.libros / curso).is_dir() else cfg.libros))
    if dirs:
        args += ["--add-dir", *dirs]
    args += ["--append-system-prompt", sistema(curso, cfg)]
    if sesion:
        args += ["--resume", sesion]
    return args


def llamar_claude(cfg: Config, prompt: str, curso: str, sesion: str | None) -> Resultado:
    cfg.dir.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(argumentos(cfg, prompt, curso, sesion), cwd=cfg.dir, capture_output=True, text=True,
                           timeout=cfg.timeout, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return Resultado(False, motivo=f"Claude no respondió en {int(cfg.timeout)} s")
    except OSError as e:
        return Resultado(False, motivo=f"No se pudo ejecutar Claude Code ({e})")
    datos = None
    try:
        datos = json.loads(r.stdout) if r.stdout.strip() else None
    except ValueError:
        pass
    if isinstance(datos, list):  # por si alguna versión devuelve la lista de eventos
        datos = next((d for d in reversed(datos) if isinstance(d, dict) and d.get("type") == "result"), None)
    if not isinstance(datos, dict):
        datos = {}
    resultado = datos.get("result") if isinstance(datos.get("result"), str) else ""
    if r.returncode == 0 and datos and not datos.get("is_error") and resultado.strip():
        return Resultado(True, texto=resultado.strip(), sesion=datos.get("session_id"), coste=datos.get("total_cost_usd"))
    motivo = " ".join(x.strip() for x in (resultado, r.stderr or "") if x and x.strip())
    motivo = (motivo or (r.stdout or "").strip() or f"código de salida {r.returncode}")[:500]
    return Resultado(False, motivo=motivo, coste=datos.get("total_cost_usd"),
                     cuota=bool(CUOTA_RE.search(motivo)), sesion_perdida=bool(sesion and SESION_PERDIDA_RE.search(motivo)))


# ---------------------------------------------------------------- bucle

class Trabajador:
    def __init__(self, cfg: Config, api: API | None = None, llamar=llamar_claude):
        self.cfg = cfg
        self.api = api or API(cfg)
        self.llamar = llamar
        self.parar = threading.Event()

    def dormir(self, segundos: float):
        self.parar.wait(segundos)

    def resolver(self, trabajo: dict) -> str:
        """Resuelve una duda y la devuelve a la consola. Devuelve el resultado: respondido | reintentar | cuota | error."""
        mid, curso, sesion = trabajo["mensaje_id"], trabajo["curso"], trabajo.get("sesion_claude")
        inicio = time.monotonic()
        prompt = prompt_seguimiento(trabajo) if sesion else prompt_inicial(trabajo, self.cfg)
        r = self.llamar(self.cfg, prompt, curso, sesion)
        if not r.ok and r.sesion_perdida:  # la sesión ya no existe (directorio cambiado o borrada): se empieza otra con contexto
            log(f"mensaje {mid}: sesión {sesion} no encontrada; se abre una nueva con el contexto")
            r = self.llamar(self.cfg, prompt_inicial(trabajo, self.cfg), curso, None)
        duracion = time.monotonic() - inicio
        coste = f"{r.coste:.4f} USD" if isinstance(r.coste, (int, float)) else "—"
        if r.ok:
            self.api.respuesta(mid, r.texto, r.sesion)
            resultado = "respondido"
        elif self.parar.is_set():  # parada del servicio a mitad: vuelve a la cola sin gastar un intento
            self.api.reintentar(mid, "El trabajador se detuvo; se reintentará", contar=False)
            resultado = "reintentar"
        elif r.cuota:
            self.api.reintentar(mid, f"Cuota de Claude agotada o servicio saturado: {r.motivo[:200]}", contar=False)
            resultado = "cuota"
        elif trabajo.get("intentos", 1) < MAX_INTENTOS and not r.motivo.startswith("No se pudo ejecutar"):
            self.api.reintentar(mid, r.motivo)
            resultado = "reintentar"
        else:
            self.api.error(mid, r.motivo)
            resultado = "error"
        log(f"mensaje {mid} (consulta {trabajo.get('consulta_id')}, {curso}/{trabajo['pregunta'].get('id')}): {resultado}"
            f" en {duracion:.1f} s, coste {coste}" + ("" if r.ok else f" — {r.motivo[:200]}"))
        return resultado

    def paso(self) -> str:
        """Un ciclo: pide trabajo y lo resuelve. Devuelve vacio | respondido | reintentar | cuota | error | api."""
        try:
            trabajo = self.api.siguiente()
            if not trabajo:
                return "vacio"
            return self.resolver(trabajo)
        except ErrorAPI as e:
            log(f"consola no disponible: {e}")
            return "api"

    def ejecutar(self, una_vez: bool = False):
        log(f"trabajador iniciado: consola {self.cfg.url}, modelo {self.cfg.modelo}, directorio {self.cfg.dir}")
        while not self.parar.is_set():
            r = self.paso()
            if una_vez:
                return r
            if r in ("vacio", "api"):
                self.dormir(self.cfg.espera)
            elif r in ("cuota", "reintentar"):
                self.dormir(self.cfg.espera_cuota)
        log("trabajador detenido")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    cfg = Config.desde_entorno()
    t = Trabajador(cfg)
    for s in (signal.SIGTERM, signal.SIGINT):
        signal.signal(s, lambda *_: t.parar.set())
    t.ejecutar(una_vez="--una-vez" in argv)


if __name__ == "__main__":
    main()
