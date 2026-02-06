from .tools import ( 
    listar_ordenes, obtener_orden, 
    crear_orden, actualizar_orden, 
    eliminar_orden
    
    )

def get_tools():
    return [
        listar_ordenes,
        obtener_orden,
        crear_orden,
        actualizar_orden,
        eliminar_orden
    ]