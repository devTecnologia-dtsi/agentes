from .tools import (
    listar_proveedores, obtener_proveedor_por_id,
    crear_proveedor, actualizar_proveedor,
    eliminar_proveedor
)

def get_tools():
    return [
        listar_proveedores,
        obtener_proveedor_por_id,
        crear_proveedor,
        actualizar_proveedor,
        eliminar_proveedor
    ]