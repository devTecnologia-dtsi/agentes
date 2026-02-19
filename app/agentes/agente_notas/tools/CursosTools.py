from langchain.tools import tool
from ..services.CursosService import CursosService
from .context import get_id_estudiante

cursos_service = CursosService()


@tool
def consultar_cursos():
    """
    Obtiene la lista de cursos actuales que está viendo el estudiante.
    Devuelve código, nombre, fechas y periodo.
    """
    id_final = get_id_estudiante()
    
    if not id_final:
        return {"error": True, "message": "No se identificó al estudiante en el contexto."}

    
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

@tool
def fechas_materia(nombre_materia: str):
    """
    Devuelve la fecha de inicio y fin de una materia específica
    junto con formato en español y contexto temporal.
    """

    id_final = get_id_estudiante()

    if not id_final:
        return {"error": True, "message": "No se identificó al estudiante."}

    resultado = cursos_service.obtener_cursos(id_final)

    if resultado.get("error"):
        return resultado

    nombre_normalizado = cursos_service._normalizar_texto(nombre_materia)

    for curso in resultado.get("cursos", []):
        materia_norm = curso.get("materia_normalizada", "")

        if nombre_normalizado in materia_norm or materia_norm in nombre_normalizado:

            inicio_raw = curso.get("inicio")
            fin_raw = curso.get("fin")

            inicio_formateado = cursos_service.formatear_fecha_es(inicio_raw) if inicio_raw else ""
            fin_formateado = cursos_service.formatear_fecha_es(fin_raw) if fin_raw else ""

            contexto_inicio = cursos_service.calcular_contexto_fecha(inicio_raw) if inicio_raw else ""
            contexto_fin = cursos_service.calcular_contexto_fecha(fin_raw) if fin_raw else ""

            return {
                "materia": curso.get("materia"),
                "inicio": inicio_formateado,
                "inicio_contexto": contexto_inicio,
                "fin": fin_formateado,
                "fin_contexto": contexto_fin,
                "periodo": curso.get("periodo")
            }

    return {"error": True, "message": "No se encontró la materia."}
