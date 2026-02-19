
"""Configuración e inicialización del agente de horarios.

El agente se inicializa dinámicamente según el modelo especificado.
No hardcodea ningún modelo.
"""

from app.services.ai import instanciar_agente
from .prompts import PROMPT_HORARIO
from .tools import (
    calcular_diferencia_horas,
    obtener_datos_horario,
    obtener_info_profesor,
    obtener_tiempo_actual,
)

# Herramientas del agente
herramientas = [
    obtener_datos_horario,
    obtener_tiempo_actual,
    calcular_diferencia_horas,
    obtener_info_profesor,
]


def construir_agente_horarios(modelo_ia: str = "gemini"):
    """Construye el agente de horarios y lo instancia con el modelo especificado.
    
    Parámetros:
        modelo_ia: Nombre del modelo ("gemini", "openai")
    
    Retorna:
        Agente de horarios inicializado
    """
    return instanciar_agente(herramientas, PROMPT_HORARIO, modelo_ia)
