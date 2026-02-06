from .tools import (
    listar_dtsi, obtener_dtsi_por_id,
    crear_dtsi, actualizar_dtsi,
    eliminar_dtsi
)

def get_tools():
    return [
        listar_dtsi,
        obtener_dtsi_por_id,
        crear_dtsi,
        actualizar_dtsi,
        eliminar_dtsi
    ]