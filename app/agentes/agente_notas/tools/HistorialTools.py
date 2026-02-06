"""Tools relacionadas con historial académico del estudiante."""
 
from langchain.tools import tool
from ..services.HistorialService import HistorialService
from .context import get_id_estudiante
 
historial_service = HistorialService()
 
@tool
def consultar_historial(id_estudiante: str = None, filtro_nota: str = None, operador: str = "==") -> dict:
    """
    Obtiene el historial académico completo del estudiante.
    Devuelve lista de cursos con código, nombre, nota y periodo.
   
    Parámetros:
    - id_estudiante: ID del estudiante (obtenido del contexto si no se proporciona)
    - filtro_nota: (Opcional) Nota específica o rango a filtrar (ej: "3", "4.5")
    - operador: (Opcional) Tipo de comparación: "==" (exacta), "<", ">", "<=", ">=" (default: "==")
   
    Ejemplos:
    - consultar_historial() → Historial completo
    - consultar_historial(filtro_nota="5", operador="==") → Materias con nota exacta 5
    - consultar_historial(filtro_nota="3", operador="<") → Materias con nota < 3
    - consultar_historial(filtro_nota="4", operador=">=") → Materias con nota >= 4
    """
    # Si no se proporciona ID, usar del contexto
    if id_estudiante is None:
        id_estudiante = get_id_estudiante()
   
    if id_estudiante is None:
        return {"error": True, "message": "No se proporcionó ID de estudiante"}
   
    # Si se solicita filtrado, usar el método específico
    if filtro_nota:
        resultado = historial_service.obtener_historial_por_nota(
            id_estudiante,
            nota_buscada=filtro_nota,
            operador=operador
        )
    else:
        # Usamos el método que ya limpia y transforma el historial
        resultado = historial_service.obtener_historial(id_estudiante)
 
    # Validación de error
    if isinstance(resultado, dict) and resultado.get("error"):
        return {
            "error": True,
            "message": resultado.get("message", "No se pudo obtener el historial académico.")
        }
 
    # Estructura final limpia
    return {
        "error": False,
        "historial": resultado.get("historial", []),
        "filtro_aplicado": {
            "nota": filtro_nota,
            "operador": operador
        } if filtro_nota else None
    }