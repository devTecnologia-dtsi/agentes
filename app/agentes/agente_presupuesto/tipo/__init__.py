from .tools import ( 
    listar_tipo, obtener_tipo_por_id,
    crear_tipo, actualizar_tipo,
    eliminar_tipo
)

def get_tools():
    return [
        listar_tipo,
        obtener_tipo_por_id,
        crear_tipo,
        actualizar_tipo,
        eliminar_tipo
    ]