"""Corrección de respuestas, compartida por la CLI (scripts/quiz.py) y la consola web."""

TIPOS = ("multiple_choice", "multiple_response", "ordering", "matching")


def corregir(p: dict, respuesta) -> bool:
    """Corrección exacta. multiple_*: conjunto; ordering: secuencia; matching: conjunto de pares."""
    c = p["correctas"]
    if p["tipo"] in ("multiple_choice", "multiple_response"):
        return set(respuesta) == set(c)
    if p["tipo"] == "ordering":
        return list(respuesta) == list(c)
    return {tuple(x) for x in respuesta} == {tuple(x) for x in c}
