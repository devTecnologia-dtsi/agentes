#from typing import Optional
from langchain.tools import tool
from ..services.CalificacionesService import CalificacionesService
from .context import get_id_estudiante

notas_service = CalificacionesService()

@tool
def consultar_notas():
    """
    Consulta todas las calificaciones del estudiante.
    Recorre todos los periodos disponibles del año actual y devuelve
    un listado normalizado para que el agente pueda procesarlo fácilmente.
    """
    id_final = get_id_estudiante()

    if not id_final:
        return {"error": True, "message": "No se identificó al estudiante en el contexto."}

    resultados = notas_service.fetch_notas(id_final)

    if isinstance(resultados, dict) and "error" in resultados:
        return resultados

    # Normalizar la estructura: extraer materias por cada periodo
    respuesta = []

    for periodo in resultados:
        materias = notas_service.extraer_calificaciones(periodo)

        respuesta.append({
            "periodo": periodo["periodo"],
            "materias": materias
        })

    return respuesta
