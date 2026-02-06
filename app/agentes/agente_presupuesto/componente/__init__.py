from .tools import (
    listar_componentes, obtener_componente_por_id,
    crear_componente, actualizar_componente,
    eliminar_componente
    )

def get_tools():
    return [
        listar_componentes,
        obtener_componente_por_id,
        crear_componente,
        actualizar_componente,
        eliminar_componente
    ]