
 
from langchain.tools import tool
from ..services.HistorialService import HistorialService
from .context import get_id_estudiante
 
historial_service = HistorialService()

 
@tool
def nota_materia(nombre_materia: str):
    """
    Devuelve la nota obtenida en una materia específica.
    Ejemplo: ¿Cuál fue mi nota en Inglés I?
    """
    id_estudiante = get_id_estudiante()

    if not id_estudiante:
        return {"error": True, "message": "No se identificó al estudiante"}

    return historial_service.obtener_nota_materia(id_estudiante, nombre_materia)


@tool
def semestre_materia(nombre_materia: str):
    """
    Devuelve los semestres en los que el estudiante cursó la materia.
    Ejemplo: ¿En qué semestre vi Proyecto de Vida?
    """
    id_estudiante = get_id_estudiante()

    if not id_estudiante:
        return {"error": True, "message": "No se identificó al estudiante"}

    return historial_service.obtener_semestre_materia(id_estudiante, nombre_materia)

@tool
def veces_cursada_materia(nombre_materia: str):
    """
    Devuelve cuántas veces el estudiante ha cursado una materia.
    Ejemplo: ¿Cuántas veces vi Álgebra?
    """
    id_estudiante = get_id_estudiante()
    if not id_estudiante:
        return {"error": True, "message": "No se identificó al estudiante"}

    return historial_service.contar_veces_materia(id_estudiante, nombre_materia)