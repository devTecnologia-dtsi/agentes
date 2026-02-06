"""Paquete de tools del agente de aulas virtuales.

Expone las tools y funciones de contexto más usadas para importaciones simples:
from .tools import obtener_cursos_usuario, obtener_eventos_curso, obtener_tiempo_actual, set_email_usuario
"""

from .cursos import obtener_cursos_usuario
from .eventos import obtener_eventos_curso
from .tiempo import obtener_tiempo_actual
from .context import set_email_usuario, email_usuario_context, datos_cursos_context, set_datos_cursos

__all__ = [
    "obtener_cursos_usuario",
    "obtener_eventos_curso",
    "obtener_tiempo_actual",
    "set_email_usuario",
    "set_datos_cursos",
    "email_usuario_context",
    "datos_cursos_context",
]
