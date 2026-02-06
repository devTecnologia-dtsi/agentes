from langchain.tools import tool
from .service import ProveedorService

proveedor_service = ProveedorService()

@tool
def listar_proveedores():
    """
    Obtiene la lista completa de todos los proveedores de presupuesto disponibles.
    Devuelve: Lista de proveedores con ID y nombre
    """
    return proveedor_service.listar_proveedores()

@tool
def obtener_proveedor_por_id(id: int):
    """
    Obtiene los detalles de un proveedor específicado por su ID.
    
    Parámetros:
        id: ID numérico único del proveedor
        
    Devuelve: Detalles completos del proveedor (ID, nombre) o error si no existe.
    """
    return proveedor_service.obtener_proveedor(id)

@tool
def crear_proveedor(nombre: str):
    """
    Crea un nuevo proveedor de presupuesto.
    
    Parámetros:
        nombre: Nombre del proveedor
        
    Devuelve: Los datos del proveedor creado incluyendo su nuevo ID.
    """
    return proveedor_service.crear_proveedor(nombre)

@tool
def actualizar_proveedor(id: int, nombre: str | None = None):
    """
     Actualiza los detalles de un proveedor existente.

    Parámetros:
        id: ID del proveedor a actualizar
        nombre: Nuevo nombre del proveedor (opcional)

    Devuelve:
        Datos actualizados del proveedor o mensaje de error.
    """
    return proveedor_service.actualizar_proveedor(id, nombre)

@tool
def eliminar_proveedor(id: int):
    """
    Elimina un proveedor de presupuesto por su ID.

    Parámetros:
        id: ID del proveedor a eliminar

    Devuelve:
        Mensaje de éxito o error.
    """
    return proveedor_service.eliminar_proveedor(id)