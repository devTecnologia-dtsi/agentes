from .tools import (
    listar_responsables, obtener_responsable_por_id,
    crear_responsable, actualizar_responsable,
    eliminar_responsable

)

def get_tools():
    return [
        listar_responsables,
        obtener_responsable_por_id,
        crear_responsable,
        actualizar_responsable,
        eliminar_responsable
    ]