from langchain.tools import tool
from datetime import date
from .service import OtroSIService

otro_si_service = OtroSIService()

@tool
def listar_otro_si():
    """
    Obtiene la lista completa de todos los otros sí de presupuesto disponibles.
    Devuelve: Lista de otros sí con ID, fechas, estado y contrato asociado
    """
    return otro_si_service.listar_otro_si()

@tool
def obtener_otro_si_por_id(id: int):
    """
    Obtiene los detalles de un otro sí específicado por su ID.
    
    Parámetros:
        id: ID numérico único del otro sí
        
    Devuelve: Detalles completos del otro sí (ID, fechas, estado, contrato) o error si no existe.
    """
    return otro_si_service.obtener_otro_si(id)

@tool
def crear_otro_si(fecha_inicio: date, fecha_fin: date,id_estado:int, id_contrato:int):
    """
    Crea un nuevo otro sí de presupuesto.
    
    Parámetros:
        fecha_inicio: Fecha de inicio del otro sí (YYYY-MM-DD)
        fecha_fin: Fecha de fin del otro sí (YYYY-MM-DD)
        id_estado: ID del estado del otro sí
        id_contrato: ID del contrato asociado
        
    Devuelve: Los datos del otro sí creado incluyendo su nuevo ID.
    """
    return otro_si_service.crear_otro_si(fecha_inicio, fecha_fin,id_estado, id_contrato)

@tool
def actualizar_otro_si(id: int, fecha_inicio: date | None = None, fecha_fin: date | None = None, id_estado: int | None = None, id_contrato: int | None = None):
    """
     Actualiza los detalles de un otro sí existente.

    Parámetros:
        id: ID del otro sí a actualizar
        fecha_inicio: Nueva fecha de inicio del otro sí (YYYY-MM-DD) (opcional)
        fecha_fin: Nueva fecha de fin del otro sí (YYYY-MM-DD) (opcional)
        id_estado: Nuevo ID del estado del otro sí (opcional)
        id_contrato: Nuevo ID del contrato asociado (opcional)

    Devuelve:
        Datos actualizados del otro sí o mensaje de error.
    """
    return otro_si_service.actualizar_otro_si(id, fecha_inicio, fecha_fin, id_estado, id_contrato)

@tool
def eliminar_otro_si(id: int):
    """
    Elimina un otro sí de presupuesto por su ID.
    """
    return otro_si_service.eliminar_otro_si(id)