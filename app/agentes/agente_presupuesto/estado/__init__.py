from .tools import ( listar_estados, obtener_estado_por_id,
    crear_estado, actualizar_estado, eliminar_estado
    )

def get_tools():
    return [
        listar_estados,
        obtener_estado_por_id,
        crear_estado,
        actualizar_estado,
        eliminar_estado
    ]