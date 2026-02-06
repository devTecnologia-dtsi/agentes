from langchain.tools import tool
from .service import ResponsableService

responsable_service = ResponsableService()

@tool
def listar_responsables():
    """Lista todos los responsables registrados en el sistema de presupuesto."""
    return responsable_service.listar_responsables()

@tool
def obtener_responsable_por_id(id: int):
    """Obtiene los detalles de un responsable específico por su ID."""
    return responsable_service.obtener_responsable(id)

@tool
def crear_responsable(responsable: str, cargo: str, area: str, correo: str):
    """Crea un nuevo responsable en el sistema de presupuesto."""
    return responsable_service.crear_responsable(responsable, cargo, area, correo)

@tool
def actualizar_responsable(id: int, responsable: str | None = None, cargo: str | None = None, area: str | None = None, correo: str | None = None):
    """Actualiza los detalles de un responsable existente."""
    return responsable_service.actualizar_responsable(id, responsable, cargo, area, correo)

@tool
def eliminar_responsable(id: int):
    """Elimina un responsable del sistema de presupuesto por su ID."""
    return responsable_service.eliminar_responsable(id)