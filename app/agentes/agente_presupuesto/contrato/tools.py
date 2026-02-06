from langchain.tools import tool
from datetime import date
from decimal import Decimal
from .service import ContratoService

contrato_service = ContratoService()

@tool
def listar_contratos():
    """
    Obtiene la lista completa de todos los contratos de presupuesto disponibles.
    Devuelve: Lista de contratos con ID, proveedor y fechas
    """
    return contrato_service.listar_Contratos()

@tool
def obtener_contrato_por_id(id: int):
    """
    Obtiene los detalles de un contrato específicado por su ID.
    
    Parámetros:
        id: ID numérico único del contrato
        
    Devuelve: Detalles completos del contrato (ID, proveedor, fechas, valor) o error si no existe.
    """
    return contrato_service.obtener_Contrato(id)

@tool
def crear_contrato(id_origen: int, id_proveedor: int, fecha_inicio: date, fecha_fin: date, valor_real: Decimal, negociado: Decimal):
    """
    Crea un nuevo contrato de presupuesto.
    
    Parámetros:
        id_origen: ID del origen del contrato
        id_proveedor: ID del proveedor asociado
        fecha_inicio: Fecha de inicio del contrato (YYYY-MM-DD)
        fecha_fin: Fecha de fin del contrato (YYYY-MM-DD)
        valor_real: Valor real del contrato
        negociado: Valor negociado del contrato
        
    Devuelve: Los datos del contrato creado incluyendo su nuevo ID.
    """
    return contrato_service.crear_Contrato(id_origen, id_proveedor, fecha_inicio, fecha_fin, valor_real, negociado)

@tool
def actualizar_contrato(id: int, id_origen: int | None = None, id_proveedor: int | None = None, fecha_inicio: date | None = None, fecha_fin: date | None = None, valor_real: Decimal | None = None, negociado: Decimal| None = None):
    """
     Actualiza los detalles de un contrato existente.

    Parámetros:
        id: ID del contrato a actualizar
        id_origen: Nuevo ID del origen del contrato (opcional)
        id_proveedor: Nuevo ID del proveedor asociado (opcional)
        fecha_inicio: Nueva fecha de inicio del contrato (YYYY-MM-DD) (opcional)
        fecha_fin: Nueva fecha de fin del contrato (YYYY-MM-DD) (opcional)
        valor_real: Nuevo valor real del contrato (opcional)
        negociado: Nuevo valor negociado del contrato (opcional)

    Devuelve:
        Datos actualizados del contrato o mensaje de error.
    """
    return contrato_service.actualizar_Contrato(id=id, id_origen=id_origen, id_proveedor=id_proveedor, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, valor_real=valor_real, negociado=negociado)

@tool
def eliminar_contrato(id: int):
    """
    Elimina un contrato de presupuesto existente.
    
    Parámetros:
        id: ID del contrato a eliminar
        
    Devuelve: Mensaje de éxito o error.
    """
    return contrato_service.eliminar_Contrato(id)