"""Contexto thread-safe para las tools de aulas virtuales."""

from contextvars import ContextVar
from typing import Any, Optional

# Context variables para pasar datos por request (thread-safe / async-safe)
email_usuario_context: ContextVar[Optional[str]] = ContextVar("email_usuario", default=None)
datos_cursos_context: ContextVar[Optional[Any]] = ContextVar("datos_cursos", default=None)


def set_email_usuario(email: str) -> None:
    """Establece el email del usuario en el contexto actual."""
    email_usuario_context.set(email)


def set_datos_cursos(datos: Any) -> None:
    """Guarda los cursos del usuario en el contexto actual."""
    datos_cursos_context.set(datos)
