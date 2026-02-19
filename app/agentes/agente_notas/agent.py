from app.services.ai import instanciar_agente
from .prompts import SYSTEM_PROMPT

from .tools import (
    nota_parcial_materia,
    nota_examen_materia,
    fechas_materia,
    consultar_cursos,
    consultar_informacion_estudiante,
    consultar_creditos,
    materias_cursadas,
    materias_pendientes,
    materias_perdidas,
    creditos_materia,
    nota_materia,
    semestre_materia,
    veces_cursada_materia,
    promedio_estudiante
    )

herramientas = [
    nota_parcial_materia,
    nota_examen_materia,
    fechas_materia,
    consultar_cursos,
    consultar_informacion_estudiante,
    consultar_creditos,
    materias_cursadas,
    materias_pendientes,
    materias_perdidas,
    creditos_materia,
    nota_materia,
    semestre_materia,
    veces_cursada_materia,
    promedio_estudiante
]
 
 
def construir_agente_notas(modelo_ia: str = "gemini"):
    """Construye el agente de notas académicas y lo instancia con el modelo especificado.
   
    Parámetros:
        modelo_ia: Nombre del modelo ("gemini", "openai")
   
    Retorna:
        Agente de notas académicas inicializado
    """
    return instanciar_agente(herramientas, SYSTEM_PROMPT, modelo_ia)
