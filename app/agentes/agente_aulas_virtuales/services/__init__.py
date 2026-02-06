"""Servicios de acceso a las APIs de Moodle."""

from . import moodle_cursos
from . import moodle_eventos_curso

__all__ = [
    'moodle_cursos',
    'moodle_eventos_curso'
]
