from langchain.tools import tool
from .service import ClaseService

clase_service = ClaseService()

@tool
def listar_clases():
    """
    Obtiene la lista completa de todas las clases de presupuesto disponibles.
    Devuelve: Lista de clases con ID, código y nombre.
    """
    return clase_service.listar_clases()


@tool
def obtener_clase_por_id(id: int):
    """
    Obtiene los detalles de una clase específica por su ID.
    
    Parámetros:
        id: ID numérico único de la clase
        
    Devuelve: Detalles completos de la clase (ID, código, nombre) o error si no existe.
    """
    return clase_service.obtener_clase(id)


@tool
def crear_clase(cod: str, nombre: str):
    """
    Crea una nueva clase de presupuesto.
    
    Parámetros:
        cod: Código único de la clase (ej: 'A100', 'B200')
        nombre: Nombre descriptivo de la clase (ej: 'Salarios', 'Materiales')
        
    Devuelve: Los datos de la clase creada incluyendo su nuevo ID.
    """
    return clase_service.crear_clase(cod, nombre)


@tool
def actualizar_clase(id: int, cod: str | None = None, nombre: str | None = None):
    """
     Actualiza el código y/o el nombre de una clase existente.

    Parámetros:
        id: ID de la clase a actualizar
        cod: Nuevo código de la clase (opcional)
        nuevo_nombre: Nuevo nombre de la clase (opcional)

    Devuelve:
        Datos actualizados de la clase o mensaje de error.
    """
    return clase_service.actualizar_clase(id=id, cod=cod, clase=nombre)


@tool
def eliminar_clase(id: int):
    """
    Elimina una clase de presupuesto existente.
    
    Parámetros:
        id: ID de la clase a eliminar
        
    Devuelve: Confirmación de eliminación o error si no existe.
    """
    return clase_service.eliminar_clase(id)
