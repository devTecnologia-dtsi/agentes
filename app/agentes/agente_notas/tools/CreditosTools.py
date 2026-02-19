from langchain.tools import tool
from ..services.CreditosService import CreditosService
from .context import get_id_estudiante

service = CreditosService()

@tool
def consultar_creditos():
    """
    Consulta el resumen de créditos académicos del estudiante, 
    Devuelve el total de:
    - créditos aprobados
    - créditos perdidos
    - creditos pendientes
    """
    id_final = get_id_estudiante()

    if not id_final:
        return {
            "error": True,
            "message": "No se identificó al estudiante en el contexto."
        }

    return service.obtener_resumen_creditos(id_final)

@tool
def materias_perdidas():
    """
    Devuelve las materias perdidas del estudiante.
    Retorna: nombre, créditos, nota y periodo.
    """
    id_final = get_id_estudiante()
    if not id_final:
        return {"error": True, "message": "No se identificó al estudiante."}

    data = service.obtener_materias_por_estado(id_final)

    if data.get("error"):
        return data

    return {"perdidas": data["perdidas"]}

@tool
def materias_pendientes():
    """
    Devuelve las materias pendientes del estudiante.
    Retorna solo el nombre de la materia.
    """
    id_final = get_id_estudiante()
    if not id_final:
        return {"error": True, "message": "No se identificó al estudiante."}

    data = service.obtener_materias_por_estado(id_final)

    if data.get("error"):
        return data

    return {"pendientes": data["pendientes"]}


@tool
def materias_cursadas():
    """
    Devuelve las materias cursadas/aprobadas.
    Retorna: nombre, créditos y semestre terminado.
    """
    id_final = get_id_estudiante()
    if not id_final:
        return {"error": True, "message": "No se identificó al estudiante."}

    data = service.obtener_materias_por_estado(id_final)

    if data.get("error"):
        return data

    return {"cursadas": data["cursadas"]}


@tool
def creditos_materia(materia: str):
    """
    Devuelve cuántos créditos tiene una materia específica.
    """
    id_final = get_id_estudiante()
    if not id_final:
        return {"error": True, "message": "No se identificó al estudiante."}

    return service.buscar_creditos_materia(id_final, materia)
