
"""Configuración e inicialización del agente de aulas virtuales.

El agente se inicializa dinámicamente según el modelo especificado.
No hardcodea ningún modelo.
"""

from app.services.ai import instanciar_agente
from .prompts import PROMPT_AULAS_VIRTUALES
from .tools import (
    obtener_cursos_usuario,
    obtener_eventos_curso,
    obtener_tiempo_actual,
)

herramientas = [
    obtener_cursos_usuario,
    obtener_eventos_curso,
    obtener_tiempo_actual,
]


def construir_agente_aulas_virtuales(modelo_ia: str = "gemini"):
    """Construye el agente de aulas virtuales y lo instancia con el modelo especificado.
    
    Parámetros:
        modelo_ia: Nombre del modelo ("gemini", "openai")
    
    Retorna:
        Agente de aulas virtuales inicializado
    """
    return instanciar_agente(herramientas, PROMPT_AULAS_VIRTUALES, modelo_ia)
