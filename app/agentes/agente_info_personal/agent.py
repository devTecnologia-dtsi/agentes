
"""Configuración e inicialización del agente de información personal.

El agente se inicializa dinámicamente según el modelo especificado.
No hardcodea ningún modelo.
"""

from app.services.ai import instanciar_agente
from .prompts import PROMPT_PERSONAL
from .tools import obtener_datos_info_personal

# Herramientas del agente
herramientas = [
    obtener_datos_info_personal,
]


def construir_agente_info_personal(modelo_ia: str = "gemini"):
    """Construye el agente de información personal y lo instancia con el modelo especificado.
    
    Parámetros:
        modelo_ia: Nombre del modelo ("gemini", "openai")
    
    Retorna:
        Agente de información personal inicializado
    """
    return instanciar_agente(herramientas, PROMPT_PERSONAL, modelo_ia)
