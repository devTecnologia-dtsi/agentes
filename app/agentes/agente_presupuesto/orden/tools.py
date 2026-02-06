from langchain.tools import tool
from datetime import date
from decimal import Decimal
from .service import OrdenService

orden_service = OrdenService()


@tool
def listar_ordenes():
    """
    Obtiene la lista completa de todas las órdenes de presupuesto disponibles.
    Devuelve: Lista de órdenes con ID, valor, fechas y proveedor
    """
    return orden_service.listar_ordenes()

@tool
def obtener_orden(id: int):
    """
    Obtiene los detalles de una orden específicada por su ID.
    
    Parámetros:
        id: ID numérico único de la orden
        
    Devuelve: Detalles completos de la orden (ID, valor, fechas, proveedor) o error si no existe.
    """
    return orden_service.obtener_orden(id)

@tool
def crear_orden(valor: Decimal, iva: Decimal, fecha_inicio: date, fecha_fin: date, id_presupuesto:int, id_proveedor:int):
    """
    Crea una nueva orden de presupuesto.
    
    Parámetros:
        valor: Valor total de la orden
        iva: Valor del IVA aplicado
        fecha_inicio: Fecha de inicio de la orden (YYYY-MM-DD)
        fecha_fin: Fecha de fin de la orden (YYYY-MM-DD)
        id_presupuesto: ID del presupuesto asociado
        id_proveedor: ID del proveedor asociado
        
    Devuelve: Los datos de la orden creada incluyendo su nuevo ID.
    """
    return orden_service.crear_orden(valor, iva, fecha_inicio, fecha_fin, id_presupuesto, id_proveedor)

@tool
def actualizar_orden(id: int, valor: Decimal | None = None, iva: Decimal | None = None, fecha_inicio: date | None = None, fecha_fin: date | None = None, id_presupuesto:int | None = None, id_proveedor:int | None = None):
    """
     Actualiza los detalles de una orden existente.

    Parámetros:
        id: ID de la orden a actualizar
        valor: Nuevo valor total de la orden (opcional)
        iva: Nuevo valor del IVA aplicado (opcional)
        fecha_inicio: Nueva fecha de inicio de la orden (YYYY-MM-DD) (opcional)
        fecha_fin: Nueva fecha de fin de la orden (YYYY-MM-DD) (opcional)
        id_presupuesto: Nuevo ID del presupuesto asociado (opcional)
        id_proveedor: Nuevo ID del proveedor asociado (opcional)

    Devuelve:
        Datos actualizados de la orden o mensaje de error.
    """
    return orden_service.actualizar_orden(id, valor, iva, fecha_inicio, fecha_fin, id_presupuesto, id_proveedor)

@tool
def eliminar_orden(id: int):
    """
    Elimina una orden de presupuesto existente.

    Parámetros:
        id: ID de la orden a eliminar

    Devuelve:
        Mensaje de éxito o error.
    """
    return orden_service.eliminar_orden(id)