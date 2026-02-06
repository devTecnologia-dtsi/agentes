from langchain.tools import tool
from datetime import date
from .service import NegociacionService

negociacion_service = NegociacionService()

@tool
def listar_negociaciones():
    """
    Obtiene la lista completa de todas las negociaciones de presupuesto disponibles.
    Devuelve: Lista de negociaciones con ID, fechas y contrato asociado
    """
    return negociacion_service.listar_negociaciones()

@tool
def obtener_negociacion_por_id(id: int):
    """
    Obtiene los detalles de una negociación específicada por su ID.
    
    Parámetros:
        id: ID numérico único de la negociación
        
    Devuelve: Detalles completos de la negociación (ID, fechas, contrato) o error si no existe.
    """
    return negociacion_service.obtener_negociacion(id)

@tool
def crear_negociacion(fecha_inicio: date, fecha_fin: date, id_contrato:int):
    """
    Crea una nueva negociación de presupuesto.
    
    Parámetros:
        fecha_inicio: Fecha de inicio de la negociación (YYYY-MM-DD)
        fecha_fin: Fecha de fin de la negociación (YYYY-MM-DD)
        id_contrato: ID del contrato asociado
        
    Devuelve: Los datos de la negociación creada incluyendo su nuevo ID.
    """
    return negociacion_service.crear_negociacion(fecha_inicio, fecha_fin, id_contrato)

@tool
def actualizar_negociacion(id: int, fecha_inicio: date | None = None, fecha_fin: date | None = None, id_contrato: int | None = None):
    """
     Actualiza los detalles de una negociación existente.

    Parámetros:
        id: ID de la negociación a actualizar
        fecha_inicio: Nueva fecha de inicio de la negociación (YYYY-MM-DD) (opcional)
        fecha_fin: Nueva fecha de fin de la negociación (YYYY-MM-DD) (opcional)
        id_contrato: Nuevo ID del contrato asociado (opcional)

    Devuelve:
        Datos actualizados de la negociación o mensaje de error.
    """
    return negociacion_service.actualizar_negociacion(id, fecha_inicio, fecha_fin, id_contrato) 

@tool
def eliminar_negociacion(id: int):
    """
    Elimina una negociación de presupuesto por su ID.

    Parámetros:
        id: ID de la negociación a eliminar
        
    Devuelve: Mensaje de éxito o error.
    """
    return negociacion_service.eliminar_negociacion(id)