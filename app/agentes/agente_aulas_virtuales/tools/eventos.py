
"""Tools relacionadas con eventos/actividades de cursos en Moodle."""

import json
from langchain.tools import tool
from app.core.logging import get_logger

from ..services import moodle_eventos_curso
from .context import datos_cursos_context

logger = get_logger(__name__)


@tool
def obtener_eventos_curso(id_curso: int, instancia: str) -> str:
    """Obtiene los eventos y actividades de un curso específico desde Moodle.
    
    Requiere el ID del curso y su modalidad (instancia), ambos obtenidos de obtener_cursos_usuario.

    Args:
        id_curso: ID numérico del curso.
        instancia: Modalidad del curso (campo 'modalidad' de obtener_cursos_usuario) como moocs o cuatrimestral.
    """
    logger.info(f"Consultando eventos del curso: {id_curso}, Instancia: {instancia}")

    eventos = moodle_eventos_curso.obtener_eventos_curso(id_curso, instancia)

    if eventos is None:
        return "Error al cargar los eventos del curso."

    if len(eventos) == 0:
        return f"No hay eventos programados en el curso {id_curso}."

    return json.dumps(eventos, indent=2, ensure_ascii=False)
