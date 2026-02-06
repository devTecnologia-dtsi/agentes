
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class RolUsuario(str, Enum):
    """Roles de usuario soportados por la aplicación."""
    ESTUDIANTE = "estudiante"
    DOCENTE = "docente"
    ADMINISTRATIVO = "administrativo"

class ModeloIA(str, Enum):
    """Modelos de IA disponibles (string-based)."""
    GEMINI = "gemini"
    OPENAI = "openai"
    OLLAMA = "ollama"

class RequestAgentes(BaseModel):
    """Modelo de entrada para solicitudes a los agentes.

    Attributes:
        uuid: Identificador único de sesión/chat (request uuid).
        prompt: Pregunta o instrucción del usuario.
        id_usuario: Identificador único del usuario (opcional segun el agente).
        email_usuario: Correo del usuario (opcional segun el agente).
        rol: Rol del usuario que realiza la consulta.
        modelo_ia: Modelo de IA a usar (gemini, openai).
        programa: Código del programa académico.
    """
    uuid: str
    prompt: str
    id_usuario: Optional[str] = None
    email_usuario: Optional[str] = None
    rol: RolUsuario
    modelo_ia: ModeloIA
    programa: str
