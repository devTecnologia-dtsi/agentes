from app.services.ai import instanciar_agente
from .prompts import SYSTEM_PROMPT

from .tools import (
    consultar_notas,
    consultar_cursos,
    consultar_informacion_estudiante,
    consultar_creditos,
    consultar_materias_por_estado,
    consultar_historial
    )

herramientas = [
    consultar_notas,
    consultar_cursos,
    consultar_informacion_estudiante,
    consultar_creditos,
    consultar_materias_por_estado,
    consultar_historial
]
 
 
def construir_agente_notas(modelo_ia: str = "gemini"):
    """Construye el agente de notas académicas y lo instancia con el modelo especificado.
   
    Parámetros:
        modelo_ia: Nombre del modelo ("gemini", "openai")
   
    Retorna:
        Agente de notas académicas inicializado
    """
    return instanciar_agente(herramientas, SYSTEM_PROMPT, modelo_ia)
