#from typing import Optional
from langchain.tools import tool
from ..services.CalificacionesService import CalificacionesService
from .context import get_id_estudiante

notas_service = CalificacionesService()

def normalizar(texto: str) -> str:
    return texto.lower().strip()

@tool
def nota_parcial_materia(materia: str, parcial: int):
    """
    Devuelve la nota de un parcial específico de una materia.
    El parcial debe ser 1 o 2.
    """
    if parcial not in (1, 2):
        return {"error": "El parcial debe ser 1 o 2"}

    id_estudiante = get_id_estudiante()
    if not id_estudiante:
        return {"error": "Estudiante no identificado"}

    for periodo in notas_service.lista_periodos():
        data = notas_service.consultar_periodo(id_estudiante, periodo)
        if not data:
            continue

        materias = notas_service.extraer_calificaciones(data)

        for m in materias:
            if normalizar(materia) in normalizar(m["materia"]):
                nota = m.get(f"parcial{parcial}")

                return {
                    "materia": m["materia"],
                    "parcial": parcial,
                    "nota": nota,
                    "periodo": periodo
                }

    return {"error": f"No se encontró la materia {materia}"}

@tool
def nota_examen_materia(materia: str):
    """
    Devuelve la nota del examen final y la nota definitiva de una materia.
    Úsala cuando el estudiante pregunte por el examen de una materia.
    """
    id_estudiante = get_id_estudiante()
    if not id_estudiante:
        return {"error": "Estudiante no identificado"}

    for periodo in notas_service.lista_periodos():
        data = notas_service.consultar_periodo(id_estudiante, periodo)
        if not data:
            continue

        for m in notas_service.extraer_calificaciones(data):
            if normalizar(materia) in normalizar(m["materia"]):
                return {
                    "materia": m["materia"],
                    "examen": m["examen"],
                    "definitiva": m["definitiva"],
                    "periodo": periodo
                }

    return {"error": f"No se encontró examen para {materia}"}


