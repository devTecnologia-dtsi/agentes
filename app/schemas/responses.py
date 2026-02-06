
"""Esquemas de respuesta estandarizados."""

from pydantic import BaseModel
from app.schemas.requests import RolUsuario

class ResponseAgentes(BaseModel):
    """Modelo de salida estandarizado para respuestas de agentes.

    Attributes:
        agente: Nombre del agente que generó la respuesta.
        respuesta: Texto de la respuesta generada.
        id_usuario: Identificador del usuario (opcional).
        email_usuario: Email del usuario (opcional).
        rol: Rol del usuario (opcional).
    """
    agente: str
    respuesta: str
    id_usuario: str | None = None
    email_usuario: str | None = None
    rol: RolUsuario | None = None
