from .tools import ( listar_cuentas, obtener_cuenta_por_id,
    crear_cuenta, actualizar_cuenta, eliminar_cuenta
    )

def get_tools():
    return [
        listar_cuentas,
        obtener_cuenta_por_id,
        crear_cuenta,
        actualizar_cuenta,
        eliminar_cuenta
    ]