from .tools import (
    listar_otro_si, obtener_otro_si_por_id,
    crear_otro_si, actualizar_otro_si,
    eliminar_otro_si
    )

def get_tools():
    return [
        listar_otro_si,
        obtener_otro_si_por_id,
        crear_otro_si,
        actualizar_otro_si,
        eliminar_otro_si
    ]