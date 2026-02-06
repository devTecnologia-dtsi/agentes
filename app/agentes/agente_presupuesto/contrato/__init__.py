from .tools import (
    listar_contratos,
    obtener_contrato_por_id,
    crear_contrato,
    actualizar_contrato,
    eliminar_contrato
)

def get_tools():
    return [
        listar_contratos,
        obtener_contrato_por_id,
        crear_contrato,
        actualizar_contrato,
        eliminar_contrato
    ]