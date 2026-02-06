from langchain.tools import tool
from .service import DtsiService

dtsi_service = DtsiService()

@tool
def listar_dtsi():
    """
    Obtiene la lista completa de todos los DTSI disponibles.
    Devuelve: Lista de DTSI con ID, clase, tipo y responsable.
    """
    return dtsi_service.listar_dtsi()

@tool
def obtener_dtsi_por_id(id: int):
    """
    Obtiene los detalles de un DTSI específico por su ID.
    
    Parámetros:
        id: ID numérico único del DTSI
        
    Devuelve: Detalles completos del DTSI (ID, clase, tipo, responsable) o error si no existe.
    """
    return dtsi_service.obtener_dtsi(id)

@tool
def crear_dtsi(id_clase: int, id_tipo: int, id_responsble: int):
    """
    Crea un nuevo DTSI.
    
    Parámetros:
        id_clase: ID de la clase asociada al DTSI
        id_tipo: ID del tipo de DTSI
        id_responsble: ID del responsable del DTSI
        
    Devuelve: Los datos del DTSI creado incluyendo su nuevo ID.
    """
    return dtsi_service.crear_dtsi(id_clase, id_tipo, id_responsble)

@tool
def actualizar_dtsi(id: int, id_clase: int | None = None, id_tipo: int | None = None, id_responsble: int | None = None):
    """
     Actualiza la clase, tipo y/o responsable de un DTSI existente.

    Parámetros:
        id: ID del DTSI a actualizar
        id_clase: Nuevo ID de la clase (opcional)
        id_tipo: Nuevo ID del tipo (opcional)
        id_responsble: Nuevo ID del responsable (opcional)

    Devuelve:
        Datos actualizados del DTSI o mensaje de error.
    """
    return dtsi_service.actualizar_dtsi(id=id, id_clase=id_clase, id_tipo=id_tipo, id_responsble=id_responsble)

@tool
def eliminar_dtsi(id: int):
    """
    Elimina un DTSI específico por su ID.

    Parámetros:
        id: ID del DTSI a eliminar

    Devuelve:
        Mensaje de éxito o error.
    """
    return dtsi_service.eliminar_dtsi(id)