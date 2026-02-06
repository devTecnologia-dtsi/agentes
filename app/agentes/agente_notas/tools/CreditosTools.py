from langchain.tools import tool
from ..services.CreditosService import CreditosService
from .context import get_id_estudiante

service = CreditosService()

@tool
def consultar_creditos():
    """
    Consulta el resumen de créditos académicos del estudiante.
    Devuelve:
    - créditos aprobados
    - créditos perdidos
    - créditos pendientes
    """
    id_final = get_id_estudiante()

    if not id_final:
        return {
            "error": True,
            "message": "No se identificó al estudiante en el contexto."
        }

    return service.obtener_resumen_creditos(id_final)

@tool
def consultar_materias_por_estado():
    """
    Consulta el detalle de materias del estudiante:
    - cursadas
    - perdidas
    - pendientes
    """
    id_final = get_id_estudiante()

    if not id_final:
        return {
            "error": True,
            "message": "No se identificó al estudiante en el contexto."
        }

    return service.obtener_detalle_materias(id_final)
