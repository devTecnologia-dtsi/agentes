from langchain.tools import tool
from datetime import date
from .service import PresupuestoService

presupuesto_service = PresupuestoService()

@tool
def listar_presupuestos():
    """
    Obtiene la lista completa de todos los presupuestos disponibles.
    Devuelve: Lista de presupuestos con ID, monto, aprobado, gasto, año y cuenta asociada
    """
    return presupuesto_service.listar_presupuestos()

@tool
def obtener_presupuesto_por_id(id: int):
    """
    Obtiene los detalles de un presupuesto específicado por su ID.
    
    Parámetros:
        id: ID numérico único del presupuesto
        
    Devuelve: Detalles completos del presupuesto (ID, monto, aprobado, gasto, año, cuenta) o error si no existe.
    """
    return presupuesto_service.obtener_presupuesto(id)

@tool
def crear_presupuesto(presupuesto: float, aprobado:float, gasto:float, anio:date, id_cuenta: int):
    """
    Crea un nuevo presupuesto.
    
    Parámetros:
        presupuesto: Monto total del presupuesto
        aprobado: Monto aprobado del presupuesto
        gasto: Monto gastado del presupuesto
        anio: Año del presupuesto (YYYY-MM-DD)
        id_cuenta: ID de la cuenta asociada
        
    Devuelve: Los datos del presupuesto creado incluyendo su nuevo ID.
    """
    return presupuesto_service.crear_presupuesto(presupuesto, aprobado, gasto, anio, id_cuenta)

@tool
def actualizar_presupuesto(id: int, presupuesto: float | None = None, aprobado:float | None = None, gasto:float | None = None, anio:date | None = None, id_cuenta: int | None = None):
    """
     Actualiza los detalles de un presupuesto existente.

    Parámetros:
        id: ID del presupuesto a actualizar
        presupuesto: Nuevo monto total del presupuesto (opcional)
        aprobado: Nuevo monto aprobado del presupuesto (opcional)
        gasto: Nuevo monto gastado del presupuesto (opcional)
        anio: Nuevo año del presupuesto (YYYY-MM-DD) (opcional)
        id_cuenta: Nuevo ID de la cuenta asociada (opcional)

    Devuelve:
        Datos actualizados del presupuesto o mensaje de error.
    """
    return presupuesto_service.actualizar_presupuesto(id, presupuesto, aprobado, gasto, anio, id_cuenta)

@tool
def eliminar_presupuesto(id: int):
    """
    Elimina un presupuesto por su ID.

    Parámetros:
        id: ID del presupuesto a eliminar

    Devuelve:
        Mensaje de éxito o error.
    """
    return presupuesto_service.eliminar_presupuesto(id)