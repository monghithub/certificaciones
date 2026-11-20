"""Presentación y lectura de respuestas de preguntas, compartidas por los tests y las preguntas durante la lectura."""


def vista_pregunta(c, pid: str) -> dict | None:
    """Pregunta sin la solución, para mostrarla antes de responder."""
    p = c.preguntas.get(pid)
    if not p:
        return None
    vista = {k: p.get(k) for k in ("id", "tipo", "enunciado", "opciones", "prompts", "tarea", "dominio", "banco", "origen")}
    vista["posiciones"] = len(p["correctas"]) if p["tipo"] == "ordering" else 0  # solo el nº de huecos, no la solución
    return vista


def leer_respuesta(p: dict, form) -> list:
    """Convierte el formulario en respuesta validada. Lanza ValueError si es incompleta o inválida."""
    opciones = {o["id"] for o in p["opciones"]}
    tipo = p["tipo"]
    if tipo == "multiple_choice":
        r = form.getlist("r")
        if len(r) != 1 or r[0] not in opciones:
            raise ValueError("Elige una opción.")
        return r
    if tipo == "multiple_response":
        r = form.getlist("r")
        if not r or not set(r) <= opciones:
            raise ValueError("Elige al menos una opción.")
        return sorted(set(r))
    if tipo == "ordering":
        r = [form.get(f"o{k}") for k in range(1, len(p["correctas"]) + 1)]
        if None in r or "" in r or not set(r) <= opciones or len(set(r)) != len(r):
            raise ValueError("Indica un elemento distinto en cada posición.")
        return r
    prompts = {x["id"] for x in p["prompts"]}
    pares = [[pid, form.get(f"m_{pid}")] for pid in sorted(prompts)]
    if any(o not in opciones for _, o in pares):
        raise ValueError("Empareja todos los elementos.")
    return pares
