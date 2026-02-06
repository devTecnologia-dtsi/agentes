from langchain.tools import tool
from.service import CuentaService

cuenta_service = CuentaService()

@tool
def listar_cuentas():
    """
    Obtiene la lista completa de todas las cuentas de presupuesto disponibles.
    Devuelve: Lista de cuentas con ID, número y descripción
    """
    return cuenta_service.listar_cuentas()

@tool
def obtener_cuenta_por_id(id: int):
    """
    Obtiene los detalles de una cuenta específicada por su ID.
    
    Parámetros:
        id: ID numérico único de la cuenta
        
    Devuelve: Detalles completos de la cuenta (ID, número, descripción) o error si no existe.
    """
    return cuenta_service.obtener_cuenta(id)

@tool
def crear_cuenta(numero: int, cuenta: str, id_dtsi:int, id_tipo:int, id_componente: int):
    """
    Crea una nueva cuenta de presupuesto.
    
    Parámetros:
        numero: Número de la cuenta
        cuenta: Descripción de la cuenta
        id_dtsi: ID del DTSI asociado
        id_tipo: ID del tipo de cuenta
        id_componente: ID del componente asociado
        
    Devuelve: Los datos de la cuenta creada incluyendo su nuevo ID.
    """
    return cuenta_service.crear_cuenta(numero, cuenta, id_dtsi, id_tipo, id_componente)     

@tool
def actualizar_cuenta(id: int, numero: int | None = None, cuenta: str | None = None, id_dtsi:int | None = None, id_tipo:int | None = None, id_componente: int | None = None):
    """
     Actualiza los detalles de una cuenta existente.

    Parámetros:
        id: ID de la cuenta a actualizar
        numero: Nuevo número de la cuenta (opcional)
        cuenta: Nueva descripción de la cuenta (opcional)
        id_dtsi: Nuevo ID del DTSI asociado (opcional)
        id_tipo: Nuevo ID del tipo de cuenta (opcional)
        id_componente: Nuevo ID del componente asociado (opcional)

    Devuelve:
        Datos actualizados de la cuenta o mensaje de error.
    """
    return cuenta_service.actualizar_cuenta(id, numero, cuenta, id_dtsi, id_tipo, id_componente)

@tool
def eliminar_cuenta(id: int):
    """
    Elimina una cuenta de presupuesto especificada por su ID.

    Parámetros:
        id: ID numérico único de la cuenta a eliminar

    Devuelve:
        Mensaje de éxito o error.
    """
    return cuenta_service.eliminar_cuenta(id)