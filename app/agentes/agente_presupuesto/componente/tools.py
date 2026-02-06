from langchain.tools import tool
from .service import ComponenteService

componente_service = ComponenteService()

@tool
def listar_componentes():
    """
    Obtiene la lista completa de todos los componentes de presupuesto disponibles.
    Devuelve: Lista de componentes con ID, nombre y tipo
    """
    return componente_service.listar_componentes()


@tool
def obtener_componente_por_id(id: int):
    """
    Obtiene los detalles de un componente específicado por su ID.
    
    Parámetros:
        id: ID numérico único del componente
        
    Devuelve: Detalles completos del componente (ID, nombre, tipo) o error si no existe.
    """
    return componente_service.obtener_componente(id)


@tool
def crear_componente(tipo: str, nombre: str):
    """
    Crea una nueva componente de presupuesto.
    
    Parámetros:
        tipo: Tipo de componente (ej: 'Material', 'Mano de Obra')
        nombre: Nombre descriptivo del componente (ej: 'Salarios', 'Materiales')
        
    Devuelve: Los datos de la componente creada incluyendo su nuevo ID.
    """
    return componente_service.crear_componente(tipo, nombre)


@tool
def actualizar_componente(id: int, tipo: str | None = None, nombre: str | None = None):
    """
     Actualiza el tipo y/o el nombre de un componente existente.

    Parámetros:
        id: ID del componente a actualizar
        tipo: Nuevo tipo del componente (opcional)
        nombre: Nuevo nombre del componente (opcional)

    Devuelve:
        Datos actualizados del componente o mensaje de error.
    """
    return componente_service.actualizar_componente(id=id, tipo=tipo, nombre=nombre)


@tool
def eliminar_componente(id: int):
    """
    Elimina un componente de presupuesto existente.
    
    Parámetros:
        id: ID del componente a eliminar
        
    Devuelve: Confirmación de eliminación o error si no existe.
    """
    return componente_service.eliminar_componente(id)