from langchain.tools import tool
from .service import TipoService

tipo_service = TipoService()

@tool
def listar_tipo():
    """
    Obtiene la lista completa de todos los tipos de presupuesto disponibles.
    Devuelve: Lista de tipos con ID, código y tipo.
    """
    return tipo_service.listar_tipos()

@tool
def obtener_tipo_por_id(id: int):
    """
    Obtiene los detalles de un tipo específico por su ID.
    
    Parámetros:
        id: ID numérico único del tipo
        
    Devuelve: Detalles completos del tipo (ID, código, tipo) o error si no existe.
    """
    return tipo_service.obtener_tipo(id)

@tool
def crear_tipo(cod: str, tipo: str):
    """
    Crea un nuevo tipo de presupuesto.
    
    Parámetros:
        cod: Código único del tipo (ej: 'T100', 'T200')
        tipo: Nombre descriptivo del tipo (ej: 'Operativo', 'Capital')
        
    Devuelve: Los datos del tipo creado incluyendo su nuevo ID.
    """
    return tipo_service.crear_tipo(cod, tipo)


@tool
def actualizar_tipo(id: int, cod: str | None = None, tipo: str | None = None):
    """
     Actualiza el código y/o el nombre de un tipo existente.

    Parámetros:
        id: ID del tipo a actualizar
        cod: Nuevo código del tipo (opcional)
        tipo: Nuevo nombre del tipo (opcional)

    Devuelve:
        Datos actualizados del tipo o mensaje de error.
    """
    return tipo_service.actualizar_tipo(id=id, cod=cod, tipo=tipo)

@tool
def eliminar_tipo(id: int):
    """
    Elimina un tipo de presupuesto por su ID.

    Parámetros:
        id: ID del tipo a eliminar

    Devuelve:
        Mensaje de éxito o error.
    """
    return tipo_service.eliminar_tipo(id)