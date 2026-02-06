from langchain.tools import tool
from ..services.CursosService import CursosService
from .context import get_id_estudiante, get_datos_cursos

cursos_service = CursosService()


@tool
def consultar_cursos():
    """
    Obtiene la lista de cursos actuales que está viendo el estudiante.
    Devuelve código, nombre, fechas y periodo.
    """
    # 1. Obtener ID (contexto)
    id_final = get_id_estudiante()
    
    if not id_final:
        return {"error": True, "message": "No se identificó al estudiante en el contexto."}

    # 2. Consultar servicio
    resultado = cursos_service.obtener_cursos(id_final)

    if isinstance(resultado, dict) and resultado.get("error"):
        return resultado

    return resultado


@tool
def consultar_informacion_estudiante():
    """
    Obtiene la información académica del estudiante:
    - Programa
    - Facultad
    - Nivel
    - Sede
    - Modalidad
    - Periodo académico actual
    """
    id_final = get_id_estudiante()

    if not id_final:
        return {"error": True, "message": "No se identificó al estudiante en el contexto."}

    resultado = cursos_service.obtener_informacion_estudiante(id_final)

    if isinstance(resultado, dict) and resultado.get("error"):
        return resultado

    return resultado
