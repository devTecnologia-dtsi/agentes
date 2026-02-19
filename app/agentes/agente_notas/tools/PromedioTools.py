from langchain.tools import tool
from ..services.PromedioService import PromedioService
from .context import get_id_estudiante

promedio_service = PromedioService()


@tool
def promedio_estudiante():
    """
    Devuelve únicamente el promedio acumulado o general del estudiante.
    Ejemplo: ¿Cuál es mi promedio?
    """
    id_estudiante = get_id_estudiante()

    if not id_estudiante:
        return {
            "error": True,
            "message": "No se identificó al estudiante"
        }

    return promedio_service.obtener_promedio_estudiante(id_estudiante)
