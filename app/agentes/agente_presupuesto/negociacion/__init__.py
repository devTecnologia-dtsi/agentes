from .tools import ( 
    listar_negociaciones, obtener_negociacion_por_id,
    crear_negociacion, actualizar_negociacion,
    eliminar_negociacion
    
    )

def get_tools():
    return [
        listar_negociaciones,
        obtener_negociacion_por_id,
        crear_negociacion,
        actualizar_negociacion,
        eliminar_negociacion
    ]