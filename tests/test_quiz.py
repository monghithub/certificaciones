import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from conftest import FIX, segundo_curso  # noqa: E402
from quiz import cargar, corregir, main, parsear  # noqa: E402

P = {p["id"]: p for p in yaml.safe_load((FIX / "valido.yaml").read_text(encoding="utf8"))}


def test_multiple_choice():
    assert corregir(P["D3-001"], ["b"]) and not corregir(P["D3-001"], ["a"])


def test_multiple_response_parcial_es_incorrecta():
    assert corregir(P["D3-002"], ["b", "c"]) and not corregir(P["D3-002"], ["b"])
    assert not corregir(P["D3-002"], ["b", "c", "a"])


def test_ordering_exige_orden():
    assert corregir(P["D3-003"], list("abcd")) and not corregir(P["D3-003"], list("abdc"))


def test_matching_pares_exactos():
    assert corregir(P["D3-004"], [["3", "c"], ["1", "b"], ["2", "a"]])
    assert not corregir(P["D3-004"], [["1", "a"], ["2", "b"], ["3", "c"]])


def test_parsear():
    assert parsear(P["D3-002"], "b,c") == ["b", "c"]
    assert parsear(P["D3-002"], "bc") == ["b", "c"]
    assert parsear(P["D3-004"], "1=b, 2=a,3=c") == [["1", "b"], ["2", "a"], ["3", "c"]]
    for p, t in ((P["D3-001"], "ab"), (P["D3-004"], "1b"), (P["D3-001"], " ")):
        try:
            parsear(p, t)
            assert False
        except ValueError:
            pass


def test_filtros(repo):
    assert len(cargar(repo, "aif-c01", dominio=3)) == 4
    assert cargar(repo, "aif-c01", dominio=2) == []
    assert len(cargar(repo, "aif-c01", tipo="matching")) == 1


def test_sesion_completa(repo, capsys, monkeypatch):
    import quiz
    respuestas = {"D3-001": "b", "D3-002": "b,c", "D3-003": "a,b,c,d", "D3-004": "1=b,2=a,3=c"}
    actual = []
    mostrar = quiz.mostrar
    monkeypatch.setattr(quiz, "mostrar", lambda p, n, t: (actual.append(p["id"]), mostrar(p, n, t)))
    code = main(["--raiz", str(repo), "--dominio", "3", "--n", "4", "--semilla", "1"], entrada=lambda: respuestas[actual[-1]])
    assert code == 0
    assert "Resultado: 4/4 (100 %)" in capsys.readouterr().out


def test_sin_preguntas(repo):
    assert main(["--raiz", str(repo), "--dominio", "2"]) == 1


def test_curso_implicito_si_solo_hay_uno(repo, capsys):
    assert main(["--raiz", str(repo), "--dominio", "2"]) == 1  # curso resuelto; sin preguntas del dominio 2


def test_varios_cursos_exigen_curso(repo, capsys):
    segundo_curso(repo)
    assert main(["--raiz", str(repo)]) == 2
    err = capsys.readouterr().err
    assert "--curso" in err and "aif-c01" in err and "otro-curso" in err


def test_curso_inexistente(repo, capsys):
    assert main(["--raiz", str(repo), "--curso", "nada"]) == 2
    assert "no encontrado" in capsys.readouterr().err


def test_quiz_de_un_curso_no_mezcla_otro(repo, capsys):
    segundo_curso(repo)
    respuestas = {"D2-001": "b"}
    import quiz
    actual = []
    mostrar = quiz.mostrar
    quiz.mostrar = lambda p, n, t: (actual.append(p["id"]), mostrar(p, n, t))
    try:
        code = main(["--raiz", str(repo), "--curso", "otro-curso", "--n", "5"], entrada=lambda: respuestas[actual[-1]])
    finally:
        quiz.mostrar = mostrar
    assert code == 0 and actual == ["D2-001"]
