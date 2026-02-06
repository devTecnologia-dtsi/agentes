from .tools import (
    listar_clases, obtener_clase_por_id, 
    crear_clase, actualizar_clase, 
    eliminar_clase
    )


def get_tools():
    
    return [
        listar_clases,
        obtener_clase_por_id,
        crear_clase,
        actualizar_clase,
        eliminar_clase
    ]