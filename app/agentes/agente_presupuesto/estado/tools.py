from langchain.tools import tool
from .service import EstadoService

estado_service = EstadoService()

@tool
def listar_estados():
    """
    Obtiene la lista completa de todos los estados de presupuesto disponibles.
    Devuelve: Lista de estados con ID, código y estado
    """
    return estado_service.listar_estados()

@tool
def obtener_estado_por_id(id: int):
    """
    Obtiene los detalles de un estado específicado por su ID.
    
    Parámetros:
        id: ID numérico único del estado
        
    Devuelve: Detalles completos del estado (ID, código, estado) o error si no existe.
    """
    return estado_service.obtener_estado(id)

@tool
def crear_estado(cod: str, estado:str):
    """
    Crea un nuevo estado de presupuesto.
    
    Parámetros:
        cod: Código del estado
        estado: Descripción del estado
        
    Devuelve: Los datos del estado creado incluyendo su nuevo ID.
    """
    return estado_service.crear_estado(cod, estado)

@tool
def actualizar_estado(id: int, cod: str | None = None, estado: str | None = None):
    """
     Actualiza los detalles de un estado existente.

    Parámetros:
        id: ID del estado a actualizar
        cod: Nuevo código del estado (opcional)
        estado: Nueva descripción del estado (opcional)

    Devuelve:
        Datos actualizados del estado o mensaje de error.
    """
    return estado_service.actualizar_estado(id, cod, estado)

@tool
def eliminar_estado(id: int):
    """
    Elimina un estado de presupuesto por su ID.

    Parámetros:
        id: ID del estado a eliminar

    Devuelve:
        Mensaje de éxito o error.
    """
    return estado_service.eliminar_estado(id)