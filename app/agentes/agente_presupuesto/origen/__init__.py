from .tools import (
    listar_origenes, obtener_origen_por_id,
    crear_origen, actualizar_origen,
    eliminar_origen
    )

def get_tools():
    return [
        listar_origenes,
        obtener_origen_por_id,
        crear_origen,
        actualizar_origen,
        eliminar_origen
    ]