from langchain.tools import tool
from .service import OrigenService

origen_service = OrigenService()

@tool
def listar_origenes():
    """
    Obtiene la lista completa de todos los orígenes de presupuesto disponibles.
    Devuelve: Lista de orígenes con ID, código y descripción
    """
    return origen_service.listar_origenes()

@tool
def obtener_origen_por_id(id: int):
    """
    Obtiene los detalles de un origen específicado por su ID.
    
    Parámetros:
        id: ID numérico único del origen
        
    Devuelve: Detalles completos del origen (ID, código, descripción) o error si no existe.
    """
    return origen_service.obtener_origen(id)

@tool
def crear_origen(cod: str, origen:str):
    """
    Crea un nuevo origen de presupuesto.
    
    Parámetros:
        cod: Código del origen
        origen: Descripción del origen
        
    Devuelve: Los datos del origen creado incluyendo su nuevo ID.
    """
    return origen_service.crear_origen(cod, origen)

@tool
def actualizar_origen(id: int, cod: str | None = None, origen: str | None = None):
    """
     Actualiza los detalles de un origen existente.

    Parámetros:
        id: ID del origen a actualizar
        cod: Nuevo código del origen (opcional)
        origen: Nueva descripción del origen (opcional)

    Devuelve:
        Datos actualizados del origen o mensaje de error.
    """
    return origen_service.actualizar_origen(id, cod, origen)

@tool
def eliminar_origen(id: int):
    """
    Elimina un origen de presupuesto existente.

    Parámetros:
        id: ID del origen a eliminar

    Devuelve:
        Mensaje de éxito o error.
    """
    return origen_service.eliminar_origen(id)