from .tools import (
    listar_presupuestos, obtener_presupuesto_por_id,
    crear_presupuesto, actualizar_presupuesto, eliminar_presupuesto
)

def get_tools():
    return [
        listar_presupuestos,
        obtener_presupuesto_por_id,
        crear_presupuesto,
        actualizar_presupuesto,
        eliminar_presupuesto
    ]