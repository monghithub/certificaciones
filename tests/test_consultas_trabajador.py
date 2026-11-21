"""Trabajador de «Preguntar a Claude» con un `claude` simulado (nunca se ejecuta el real) y una API simulada."""
import json
import os
import stat
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import consultas_trabajador as ct  # noqa: E402

# Sustituto de `claude -p`: registra sus argumentos y su cwd, y responde según CLAUDE_FALSO (ok | cuota | lenta | error | sesion).
FALSO = r'''
import json, os, sys, time
args = sys.argv[1:]
with open(os.environ["CLAUDE_FALSO_LOG"], "a", encoding="utf8") as f:
    f.write(json.dumps({"args": args, "cwd": os.getcwd()}) + "\n")
modo = os.environ.get("CLAUDE_FALSO", "ok")
sesion = args[args.index("--resume") + 1] if "--resume" in args else "nueva-123"
if modo == "lenta":
    time.sleep(5)
if modo == "sesion" and "--resume" in args:
    print("No conversation found with session ID: " + sesion, file=sys.stderr)
    sys.exit(1)
if modo == "cuota":
    print(json.dumps({"type": "result", "subtype": "success", "is_error": True,
                      "result": "Claude AI usage limit reached|1764000000", "session_id": sesion}))
    sys.exit(1)
if modo == "error":
    print(json.dumps({"type": "result", "subtype": "error_during_execution", "is_error": True, "result": "Algo falló"}))
    sys.exit(1)
print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "Respuesta de **Claude**",
                  "session_id": sesion, "terminal_reason": "completed", "total_cost_usd": 0.0123, "permission_denials": []}))
'''

PREGUNTA = {
    "id": "D3-001", "banco": "examen", "modulo": "03-modelos-fundacionales", "origen": None,
    "enunciado": "Una empresa quiere que un asistente responda usando sus manuales internos.", "tipo": "multiple_choice",
    "opciones": [{"id": "a", "texto": "Fine-tuning semanal"}, {"id": "b", "texto": "Amazon Bedrock Knowledge Bases (RAG)"}],
    "prompts": None, "correctas": ["b"], "explicacion": "RAG incorpora contenido actualizado sin reentrenar.",
    "distractores": {"a": "Reentrenar cada semana es costoso."}, "referencia": "https://docs.aws.amazon.com/bedrock/latest/userguide/kb.html",
    "teoria_url": "/c/aif-c01/modulo/03-modelos-fundacionales/teoria#rag", "teoria_fichero": "modulos/03-modelos-fundacionales/README.md",
}


def trabajo(**cambios):
    t = {"mensaje_id": 7, "consulta_id": 3, "sesion_claude": None, "texto": "¿Por qué no fine-tuning?", "intentos": 1, "reparto": 1,
         "curso": "aif-c01", "pregunta": dict(PREGUNTA), "respuesta_usuario": None, "respondida": False}
    t.update(cambios)
    return t


class APIFalsa:
    def __init__(self, trabajos=()):
        self.trabajos = list(trabajos)
        self.llamadas = []
        self.repartos = []
        self.pedidas = 0

    def siguiente(self):
        self.pedidas += 1
        return self.trabajos.pop(0) if self.trabajos else None

    # Se registra el reparto aparte para que las aserciones sigan siendo cortas.
    def respuesta(self, mid, reparto, texto, sesion):
        self.repartos.append(reparto)
        self.llamadas.append(("respuesta", mid, texto, sesion))

    def reintentar(self, mid, reparto, motivo, contar=True):
        self.repartos.append(reparto)
        self.llamadas.append(("reintentar", mid, motivo, contar))

    def error(self, mid, reparto, motivo):
        self.repartos.append(reparto)
        self.llamadas.append(("error", mid, motivo))


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    exe = tmp_path / "bin" / "claude"
    exe.parent.mkdir()
    exe.write_text(f"#!{sys.executable}\n{FALSO}", encoding="utf8")
    exe.chmod(exe.stat().st_mode | stat.S_IEXEC)
    log = tmp_path / "llamadas.jsonl"
    monkeypatch.setenv("CLAUDE_FALSO_LOG", str(log))
    monkeypatch.setenv("CLAUDE_FALSO", "ok")
    # El trabajador pasa a `claude` un entorno mínimo: el sustituto necesita además sus dos variables.
    monkeypatch.setattr(ct, "ENTORNO_CLAUDE", ct.ENTORNO_CLAUDE + ("CLAUDE_FALSO", "CLAUDE_FALSO_LOG"))
    (tmp_path / "cursos" / "aif-c01").mkdir(parents=True)
    (tmp_path / "libros" / "aif-c01").mkdir(parents=True)
    cfg = ct.Config(url="http://consola", token="t" * 40, claude=str(exe), dir=tmp_path / "trabajo",
                    cursos=tmp_path / "cursos", libros=tmp_path / "libros", timeout=20)

    def llamadas():
        return [json.loads(x) for x in log.read_text(encoding="utf8").splitlines()] if log.exists() else []

    return cfg, llamadas


def prompt_de(args):
    return args[args.index("-p") + 1]


def test_primer_mensaje_sin_solucion_si_no_ha_respondido(entorno):
    cfg, llamadas = entorno
    api = APIFalsa()
    assert ct.Trabajador(cfg, api).resolver(trabajo()) == "respondido"
    assert api.llamadas == [("respuesta", 7, "Respuesta de **Claude**", "nueva-123")]
    (ll,) = llamadas()
    args = ll["args"]
    assert Path(ll["cwd"]) == cfg.dir
    assert args[args.index("--model") + 1] == "sonnet" and args[args.index("--output-format") + 1] == "json"
    assert args[args.index("--tools") + 1] == "Read,Grep,Glob,WebFetch,WebSearch"
    assert {"--restricted", "--strict-mcp-config"} <= set(args) and args[args.index("--permission-mode") + 1] == "dontAsk"
    permitidas = args[args.index("--allowedTools") + 1].split(",")
    assert f"Read(/{cfg.cursos / 'aif-c01'}/**)" in permitidas and f"Read(/{cfg.libros / 'aif-c01'}/**)" in permitidas
    assert "WebFetch(domain:docs.aws.amazon.com)" in permitidas and "WebFetch(domain:aws.amazon.com)" in permitidas
    assert not {"Read", "Grep", "Glob", "WebFetch"} & set(permitidas)  # nada sin ruta ni dominio
    denegadas = args[args.index("--disallowedTools") + 1].split(",")
    assert f"Read(/{Path.home() / '.ssh'}/**)" in denegadas and f"Read(/{Path.home() / '.claude'}/**)" in denegadas
    assert "Read(//**/.env)" in denegadas and "Read(//**/data/**)" in denegadas
    assert api.repartos == [1]
    i = args.index("--add-dir")
    assert args[i + 1:i + 3] == [str(cfg.cursos / "aif-c01"), str(cfg.libros / "aif-c01")]
    assert "--resume" not in args and "--dangerously-skip-permissions" not in args
    assert "orienta sin revelar" in args[args.index("--append-system-prompt") + 1]
    p = prompt_de(args)
    assert "AÚN NO ha respondido" in p and "Una empresa quiere" in p and "¿Por qué no fine-tuning?" in p
    assert "Solución" not in p and "RAG incorpora" not in p and "costoso" not in p and "kb.html" not in p
    assert str(cfg.cursos / "aif-c01" / "modulos/03-modelos-fundacionales/README.md") in p


def test_solucion_si_la_pide_o_si_ya_respondio(entorno):
    cfg, llamadas = entorno
    ct.Trabajador(cfg, APIFalsa()).resolver(trabajo(texto="Dime la solución, por favor"))
    ct.Trabajador(cfg, APIFalsa()).resolver(trabajo(respondida=True, respuesta_usuario=["a"]))
    pide, respondida = (prompt_de(x["args"]) for x in llamadas())
    assert "Ha pedido expresamente la solución" in pide and "b) Amazon Bedrock Knowledge Bases (RAG)" in pide
    assert "ya ha respondido" in respondida and "a) Fine-tuning semanal" in respondida and "RAG incorpora" in respondida
    assert not ct.pide_solucion("¿Cuál es la diferencia entre RAG y fine-tuning?")


def test_seguimiento_con_resume(entorno):
    cfg, llamadas = entorno
    api = APIFalsa()
    ct.Trabajador(cfg, api).resolver(trabajo(sesion_claude="ses-9", texto="-¿Y si cambian a diario?"))
    args = llamadas()[0]["args"]
    assert args[args.index("--resume") + 1] == "ses-9"
    p = prompt_de(args)
    assert p.startswith("Nueva duda") and "Una empresa quiere" not in p and "-¿Y si cambian a diario?" in p
    assert api.llamadas[0][3] == "ses-9"


def test_sesion_perdida_abre_una_nueva_con_contexto(entorno, monkeypatch):
    cfg, llamadas = entorno
    monkeypatch.setenv("CLAUDE_FALSO", "sesion")
    api = APIFalsa()
    assert ct.Trabajador(cfg, api).resolver(trabajo(sesion_claude="perdida")) == "respondido"
    primera, segunda = llamadas()
    assert "--resume" in primera["args"] and "--resume" not in segunda["args"]
    assert "## Pregunta" in prompt_de(segunda["args"])
    assert api.llamadas == [("respuesta", 7, "Respuesta de **Claude**", "nueva-123")]


def test_cuota_agotada_vuelve_a_la_cola_y_espera(entorno, monkeypatch):
    cfg, _ = entorno
    monkeypatch.setenv("CLAUDE_FALSO", "cuota")
    api = APIFalsa([trabajo(intentos=5)])
    t = ct.Trabajador(cfg, api)
    esperas = []

    def dormir(s):
        esperas.append(s)
        t.parar.set()

    t.dormir = dormir
    t.ejecutar()
    assert api.llamadas[0][0] == "reintentar" and api.llamadas[0][3] is False and "usage limit" in api.llamadas[0][2]
    assert esperas == [cfg.espera_cuota]


def test_timeout_reintenta_y_al_tercer_intento_error(entorno, monkeypatch):
    cfg, _ = entorno
    cfg.timeout = 0.5
    monkeypatch.setenv("CLAUDE_FALSO", "lenta")
    api = APIFalsa()
    t = ct.Trabajador(cfg, api)
    assert t.resolver(trabajo(intentos=1)) == "reintentar"
    assert api.llamadas[0][:2] == ("reintentar", 7) and "no respondió" in api.llamadas[0][2] and api.llamadas[0][3] is True
    assert t.resolver(trabajo(intentos=3)) == "error"
    assert api.llamadas[1][:2] == ("error", 7)


def test_error_repetido(entorno, monkeypatch):
    cfg, _ = entorno
    monkeypatch.setenv("CLAUDE_FALSO", "error")
    api = APIFalsa()
    t = ct.Trabajador(cfg, api)
    assert [t.resolver(trabajo(intentos=k)) for k in (1, 2, 3)] == ["reintentar", "reintentar", "error"]
    assert api.llamadas[2] == ("error", 7, "Algo falló")


def test_ejecutable_inexistente_es_error(entorno):
    cfg, _ = entorno
    cfg.claude = str(cfg.dir / "no-existe")
    api = APIFalsa()
    assert ct.Trabajador(cfg, api).resolver(trabajo()) == "error"
    assert "No se pudo ejecutar" in api.llamadas[0][2]


def test_parada_a_mitad_devuelve_a_la_cola_sin_gastar_intento(entorno):
    cfg, _ = entorno
    api = APIFalsa()
    t = ct.Trabajador(cfg, api)

    def llamar(*_):
        t.parar.set()  # llega SIGTERM mientras Claude trabaja; systemd mata también el proceso de Claude
        return ct.Resultado(False, motivo="terminado")

    t.llamar = llamar
    assert t.resolver(trabajo()) == "reintentar"
    assert api.llamadas == [("reintentar", 7, "El trabajador se detuvo; se reintentará", False)]


def test_sin_trabajo_y_consola_caida(entorno):
    cfg, _ = entorno
    t = ct.Trabajador(cfg, APIFalsa())
    assert t.paso() == "vacio"

    class Caida(APIFalsa):
        def siguiente(self):
            raise ct.ErrorAPI("conexión rechazada")

    assert ct.Trabajador(cfg, Caida()).paso() == "api"


def test_configuracion_por_entorno():
    with pytest.raises(SystemExit):
        ct.Config.desde_entorno({})
    cfg = ct.Config.desde_entorno({"CONSULTAS_TOKEN": "t" * 40, "CONSULTAS_CURSOS": "/srv/cursos", "CONSULTAS_ESPERA": "3"})
    assert cfg.url == "http://127.0.0.1:8097" and cfg.modelo == "sonnet" and cfg.claude == "claude"
    assert cfg.cursos == Path("/srv/cursos") and cfg.libros is None and cfg.espera == 3 and cfg.espera_cuota == 900
    assert cfg.dir == Path(os.path.expanduser("~/.local/share/consultas-claude"))


def test_api_real_contra_la_consola(curso, tmp_path):
    """El cliente HTTP del trabajador habla con la consola de verdad (TestClient en lugar de la red)."""
    from fastapi.testclient import TestClient
    from conftest import crear_usuario, entrar, token

    from app.config import Settings
    from app.main import create_app

    app = create_app(Settings(secret_key="k" * 40, database_url=f"sqlite:///{tmp_path}/w.db", courses_dir=curso / "cursos",
                              schemas_dir=curso / "schemas", consultas_token="t" * 40))
    crear_usuario(app, "root", rol="admin")
    c = entrar(app, "root")
    c.post("/c/aif-c01/consultas/D3-001", data={"texto": "¿Por qué?", "csrf": token(c, "/c/aif-c01/dudas")})
    cliente = TestClient(app)

    class APIConsola(ct.API):
        def _post(self, ruta, datos=None):
            r = cliente.post("/api/consultas" + ruta, json=datos or {}, headers={"Authorization": f"Bearer {self.cfg.token}"})
            if r.status_code >= 400:
                raise ct.ErrorAPI(f"{ruta}: HTTP {r.status_code}")
            return r.status_code, (r.json() if r.content else None)

    cfg = ct.Config(url="http://consola", token="t" * 40)
    t = ct.Trabajador(cfg, APIConsola(cfg), llamar=lambda *_: ct.Resultado(True, texto="Hecho", sesion="s-1", coste=0.01))
    assert t.paso() == "respondido" and t.paso() == "vacio"
    assert "Hecho" in c.get("/c/aif-c01/consultas/D3-001/mensajes").text


def test_entorno_minimo_sin_token(monkeypatch):
    monkeypatch.setenv("CLAUDE_FALSO_LOG", "/tmp/x")
    monkeypatch.setenv("CONSULTAS_TOKEN", "t" * 40)
    monkeypatch.setenv("SECRET_KEY", "secreto")
    env = ct.entorno_claude()
    assert "CONSULTAS_TOKEN" not in env and "SECRET_KEY" not in env and "CLAUDE_FALSO_LOG" not in env
    assert env["HOME"] == os.environ["HOME"] and set(env) <= set(ct.ENTORNO_CLAUDE)


def test_patron_de_cuota_preciso():
    for t in ("Claude AI usage limit reached|1764000000", "API Error: 429 Too Many Requests", "rate limit exceeded",
              "API Error: 529 Overloaded", "overloaded_error"):
        assert ct.CUOTA_RE.search(t), t
    for t in ("Output token limit exceeded for this response", "El límite de palabras es 250", "Error 4290 en la línea 529x"):
        assert not ct.CUOTA_RE.search(t), t


def test_tope_de_reintentos_por_cuota(entorno, monkeypatch):
    cfg, _ = entorno
    monkeypatch.setenv("CLAUDE_FALSO", "cuota")
    api = APIFalsa()
    t = ct.Trabajador(cfg, api)
    assert t.resolver(trabajo(reparto=cfg.max_cuota - 1)) == "cuota"
    assert t.resolver(trabajo(reparto=cfg.max_cuota)) == "error"
    assert api.llamadas[1][0] == "error" and "siguió agotada" in api.llamadas[1][2]


def test_reintento_normal_espera_poco(entorno, monkeypatch):
    cfg, _ = entorno
    monkeypatch.setenv("CLAUDE_FALSO", "error")
    t = ct.Trabajador(cfg, APIFalsa([trabajo(intentos=1)]))
    esperas = []
    t.dormir = lambda s: (esperas.append(s), t.parar.set())
    t.ejecutar()
    assert esperas == [cfg.espera]


def test_tope_de_gasto_diario(entorno):
    cfg, _ = entorno
    cfg.coste_diario = 0.02
    api = APIFalsa([trabajo(), trabajo(mensaje_id=8)])
    t = ct.Trabajador(cfg, api)
    assert t.paso() == "respondido" and abs(t.gastado_hoy() - 0.0123) < 1e-9
    assert t.paso() == "respondido" and t.gastado_hoy() > cfg.coste_diario
    assert t.paso() == "tope" and api.pedidas == 2  # no pide más trabajo: las dudas siguen en cola
    esperas = []
    t.dormir = lambda s: (esperas.append(s), t.parar.set())
    t.ejecutar()
    assert esperas and 60 <= esperas[0] <= 86405
    # al cambiar de día se reanuda; el gasto sobrevive a un reinicio
    assert ct.Trabajador(cfg, APIFalsa()).gastado_hoy() == t.gastado_hoy()
    (cfg.dir / "gasto.json").write_text('{"fecha": "2000-01-01", "usd": 99}', encoding="utf8")
    assert not t.tope_alcanzado()
    cfg.coste_diario = 0
    assert ct.Config.desde_entorno({"CONSULTAS_TOKEN": "t" * 40, "CONSULTAS_COSTE_DIARIO": "0"}).coste_diario == 0


@pytest.mark.parametrize("texto", ["Dime la solución", "dame la respuesta, por favor", "¿Cuál es la respuesta correcta?",
                                   "¿cuál es la correcta?", "¿Qué opción es la correcta?", "Enséñame la solución"])
def test_pide_solucion_explicita(texto):
    assert ct.pide_solucion(texto)


@pytest.mark.parametrize("texto", ["¿Por qué la B no es la correcta?", "¿Cuál es la diferencia entre RAG y fine-tuning?",
                                   "No me digas la solución, solo una pista", "¿La solución pasa por usar RAG?",
                                   "¿Es correcta mi intuición de que sobra el fine-tuning?", "Explícame la respuesta B"])
def test_no_pide_solucion(texto):
    assert not ct.pide_solucion(texto)
