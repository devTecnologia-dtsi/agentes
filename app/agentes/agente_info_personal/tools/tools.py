
"""Herramientas del agente de información personal."""

import json
from contextvars import ContextVar

from langchain.tools import tool
from app.core.logging import get_logger
from ..services.informacion_personal import cargar_datos_info_personal

logger = get_logger(__name__)

# Contexto por request (thread-safe / async-safe)
_usuario_id_ctx: ContextVar = ContextVar("usuario_id_info", default=None)


def set_usuario_id_info(usuario_id: str) -> None:
    """Guarda el ID de usuario en el contexto actual."""
    _usuario_id_ctx.set(usuario_id)


@tool
async def obtener_datos_info_personal() -> str:
    """Consulta los datos personales del usuario bajo demanda."""

    usuario_id = _usuario_id_ctx.get()
    if usuario_id is None:
        logger.warning("No hay ID de usuario en el contexto")
        return "Error: No se ha establecido el ID del usuario."

    datos = await cargar_datos_info_personal(usuario_id)
    if datos is None:
        return "Error al consultar servicio de información personal."

    try:
        # Extraer solo el objeto Estudiante
        estudiante = datos.get('Estudiante', datos)
        
        # Log para depuración de respuesta de servicio
        # logger.info(f"Datos recibidos de API para {usuario_id}: {json.dumps(estudiante, ensure_ascii=False)}")

        resultado = json.dumps(estudiante, indent=2, ensure_ascii=False)
        return resultado
    except Exception as e:
        error_msg = f"Error al procesar los datos: {str(e)}"
        return str(error_msg)
