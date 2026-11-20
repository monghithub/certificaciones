"""Listas oficiales de servicios dentro y fuera de alcance (fuentes/servicios-alcance.md), agrupadas por categoría."""
import re

CATEGORIAS_ES = {
    "Analytics": "Análisis de datos", "Application Integration": "Integración de aplicaciones",
    "Business Applications": "Aplicaciones empresariales", "Cloud Financial Management": "Gestión financiera de la nube",
    "Compute": "Cómputo", "Containers": "Contenedores", "Customer Enablement": "Soporte al cliente",
    "Database": "Bases de datos", "Developer Tools": "Herramientas para desarrolladores",
    "End User Computing": "Informática para usuarios finales", "Frontend Web and Mobile": "Web y móvil",
    "Internet of Things (IoT)": "Internet de las cosas", "Machine Learning": "Aprendizaje automático e IA",
    "Management and Governance": "Administración y gobierno", "Media": "Multimedia",
    "Migration and Transfer": "Migración y transferencia", "Networking and Content Delivery": "Redes y entrega de contenido",
    "Security, Identity, and Compliance": "Seguridad, identidad y cumplimiento", "Storage": "Almacenamiento",
}


def listas(texto: str) -> dict[str, list[tuple[str, str]]]:
    """{"dentro": [(categoría, servicio)], "fuera": [...]} a partir de las secciones «dentro» y «fuera de alcance»."""
    resultado: dict[str, list[tuple[str, str]]] = {"dentro": [], "fuera": []}
    actual, categoria = None, None
    for linea in texto.splitlines():
        if linea.startswith("## "):
            t = linea.lower()
            actual = "dentro" if "dentro de alcance" in t else "fuera" if "fuera de alcance" in t else None
            categoria = None
        elif linea.startswith("### "):
            categoria = linea[4:].strip()
        elif actual and categoria and linea.startswith("- ") and not linea.startswith("- **"):
            resultado[actual].append((categoria, linea[2:].strip()))
    return resultado


def sin_parentesis(nombre: str) -> str:
    return re.sub(r"\s*\([^)]*\)", "", nombre).strip()
