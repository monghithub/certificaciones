#!/usr/bin/env python3
"""Journal de preguntas y respuestas: caché local para reutilizar respuestas similares

Almacena preguntas y respuestas en JSON para:
1. Buscar si una pregunta similar ya tiene respuesta
2. Acelerar búsquedas (no hay que llamar a Claude)
3. Mantener un inventario de QA para referencia
4. Detectar patrones de preguntas frecuentes
"""
import json
import os
from pathlib import Path
from typing import Optional, List, Tuple
from datetime import datetime

class JournalConsultas:
    """Gestor del journal de preguntas y respuestas."""

    def __init__(self, ruta: Optional[str] = None):
        """
        Inicializa el journal.

        Args:
            ruta: Ruta al archivo journal.json.
                  Default: ~/.local/share/consultas-claude/journal.json
        """
        if ruta is None:
            base = Path.home() / '.local' / 'share' / 'consultas-claude'
            base.mkdir(parents=True, exist_ok=True)
            ruta = str(base / 'journal.json')

        self.ruta = Path(ruta)
        self.datos = self._cargar()

    def _cargar(self) -> dict:
        """Carga el journal desde disco. Si no existe, inicia vacío."""
        if self.ruta.exists():
            try:
                with open(self.ruta, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {'version': 1, 'preguntas': [], 'estadisticas': {}}

        return {'version': 1, 'preguntas': [], 'estadisticas': {}}

    def _guardar(self):
        """Guarda el journal a disco."""
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ruta, 'w', encoding='utf-8') as f:
            json.dump(self.datos, f, indent=2, ensure_ascii=False)

    def buscar_similar(self, pregunta: str, umbral: float = 0.7) -> Optional[dict]:
        """
        Busca si existe una pregunta similar en el journal.

        Args:
            pregunta: La pregunta a buscar
            umbral: Mínimo de similitud (0.0 a 1.0). Default 0.7 (70%)

        Returns:
            Dict con la pregunta/respuesta similar, o None si no hay
        """
        from validador_scope import detectar_similitud_simple

        mejor_match = None
        mejor_similitud = 0.0

        for item in self.datos.get('preguntas', []):
            similitud = detectar_similitud_simple(pregunta, item['pregunta'])

            if similitud >= umbral and similitud > mejor_similitud:
                mejor_similitud = similitud
                mejor_match = item

        return mejor_match

    def agregar(self, pregunta: str, respuesta: str, usuario: str, curso: str, objetivo: Optional[str] = None):
        """
        Agrega una pregunta y respuesta al journal.

        Args:
            pregunta: La pregunta hecha
            respuesta: La respuesta de Claude
            usuario: ID/nombre del usuario
            curso: Slug del curso (ej: aif-c01)
            objetivo: Objetivo oficial relacionado (ej: 1.2.3), opcional
        """
        item = {
            'id': len(self.datos['preguntas']) + 1,
            'fecha': datetime.now().isoformat(),
            'usuario': usuario,
            'curso': curso,
            'objetivo': objetivo,
            'pregunta': pregunta,
            'respuesta': respuesta,
            'accesos': 1,  # contabilizar reutilizaciones
        }

        self.datos['preguntas'].append(item)

        # Actualizar estadísticas
        stats = self.datos.get('estadisticas', {})
        stats['total_preguntas'] = len(self.datos['preguntas'])
        stats['ultima_actualizacion'] = datetime.now().isoformat()
        self.datos['estadisticas'] = stats

        self._guardar()
        return item

    def reutilizar(self, item_id: int):
        """Registra que una respuesta se reutilizó."""
        for item in self.datos.get('preguntas', []):
            if item['id'] == item_id:
                item['accesos'] = item.get('accesos', 1) + 1
                self._guardar()
                return

    def listar_por_objetivo(self, objetivo: str) -> List[dict]:
        """Lista todas las preguntas relacionadas con un objetivo."""
        return [
            p for p in self.datos.get('preguntas', [])
            if p.get('objetivo') == objetivo
        ]

    def listar_por_usuario(self, usuario: str) -> List[dict]:
        """Lista todas las preguntas de un usuario."""
        return [
            p for p in self.datos.get('preguntas', [])
            if p.get('usuario') == usuario
        ]

    def buscar_por_palabras(self, palabras: List[str]) -> List[dict]:
        """Busca preguntas que contengan las palabras clave."""
        resultados = []
        palabras_lower = [p.lower() for p in palabras]

        for item in self.datos.get('preguntas', []):
            pregunta_lower = item['pregunta'].lower()
            if any(palabra in pregunta_lower for palabra in palabras_lower):
                resultados.append(item)

        return resultados

    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas del journal."""
        preguntas = self.datos.get('preguntas', [])

        if not preguntas:
            return {
                'total_preguntas': 0,
                'preguntas_reutilizadas': 0,
                'tasa_reutilizacion': 0.0,
                'usuarios_unicos': 0,
                'cursos': [],
            }

        # Contar reutilizaciones (accesos > 1)
        reutilizadas = sum(1 for p in preguntas if p.get('accesos', 1) > 1)

        # Usuarios únicos
        usuarios = set(p['usuario'] for p in preguntas)

        # Cursos
        cursos = set(p['curso'] for p in preguntas)

        return {
            'total_preguntas': len(preguntas),
            'preguntas_reutilizadas': reutilizadas,
            'tasa_reutilizacion': reutilizadas / len(preguntas) if preguntas else 0.0,
            'usuarios_unicos': len(usuarios),
            'cursos': sorted(list(cursos)),
            'accesos_total': sum(p.get('accesos', 1) for p in preguntas),
        }

    def exportar_csv(self, ruta: Optional[str] = None) -> str:
        """Exporta el journal a CSV para análisis."""
        import csv

        if ruta is None:
            ruta = str(self.ruta.parent / f'journal-export-{datetime.now().strftime("%Y%m%d")}.csv')

        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'fecha', 'usuario', 'curso', 'objetivo', 'pregunta', 'accesos'
            ])
            writer.writeheader()

            for item in self.datos.get('preguntas', []):
                writer.writerow({
                    'id': item['id'],
                    'fecha': item['fecha'],
                    'usuario': item['usuario'],
                    'curso': item['curso'],
                    'objetivo': item.get('objetivo', '—'),
                    'pregunta': item['pregunta'],
                    'accesos': item.get('accesos', 1),
                })

        return ruta

if __name__ == '__main__':
    # Ejemplo de uso
    journal = JournalConsultas()

    # Agregar una pregunta de ejemplo
    print("Agregando preguntas de ejemplo...")
    journal.agregar(
        pregunta="¿Qué es RAG en Amazon Bedrock?",
        respuesta="RAG (Retrieval-Augmented Generation) permite que el modelo acceda a documentos externos...",
        usuario="admin",
        curso="aif-c01",
        objetivo="3.1.3"
    )

    journal.agregar(
        pregunta="¿Cuál es la diferencia entre Model Monitor y Clarify?",
        respuesta="Model Monitor detecta cambios en datos y predicciones (deriva)...",
        usuario="admin",
        curso="aif-c01",
        objetivo="4.1.7"
    )

    # Buscar similares
    print("\nBuscando preguntas similares...")
    similar = journal.buscar_similar("¿Qué es RAG en Bedrock?")
    if similar:
        print(f"✓ Encontrada: {similar['pregunta']}")
        print(f"  Accesos previos: {similar['accesos']}")

    # Estadísticas
    print("\nEstadísticas del journal:")
    stats = journal.obtener_estadisticas()
    for clave, valor in stats.items():
        print(f"  {clave}: {valor}")

    # Listar por objetivo
    print("\nPreguntas del objetivo 3.1.3:")
    para_objetivo = journal.listar_por_objetivo("3.1.3")
    for p in para_objetivo:
        print(f"  - {p['pregunta']}")
