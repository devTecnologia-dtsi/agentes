
"""Tools relacionadas con cursos del usuario en Moodle."""

import json
from langchain.tools import tool
from app.core.logging import get_logger

from ..services import moodle_cursos
from .context import email_usuario_context, set_datos_cursos

logger = get_logger(__name__)


@tool
def obtener_cursos_usuario() -> str:
    """Obtiene los cursos en los que está inscrito el usuario desde Moodle.

    Returns:
        JSON con lista de cursos con id, nombre, código, fechas y último acceso.
    """
    logger.info("Consultando cursos del usuario")

    email = email_usuario_context.get()
    if email is None:
        return "Error: No se ha establecido el email del usuario."

    cursos = moodle_cursos.obtener_cursos_usuario(email)

    if cursos is None:
        return "Error al consultar cursos en Moodle."

    if len(cursos) == 0:
        return "No estás inscrito en ningún curso actualmente."

    # Guardar en contexto para que obtener_eventos_curso pueda usarlos
    set_datos_cursos(cursos)

    try:
        return json.dumps(cursos, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error al procesar cursos: {str(e)}"
