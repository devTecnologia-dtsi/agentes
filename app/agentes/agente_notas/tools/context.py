from contextvars import ContextVar
from typing import Dict, Any, Optional

# ContextVars
id_estudiante_context: ContextVar[Optional[str]] = ContextVar("id_estudiante_context", default=None)
programa_context: ContextVar[Optional[str]] = ContextVar("programa_context", default=None)
datos_cursos_context: ContextVar[Optional[Dict[str, Any]]] = ContextVar("datos_cursos_context", default=None)

def set_id_estudiante(id_estudiante: str):
    """
    Establece el ID del estudiante en el contexto actual.
    También reinicia cualquier otro contexto residual para evitar contaminación cruzada.
    """
    reset_context()
    id_estudiante_context.set(id_estudiante)

def get_id_estudiante() -> Optional[str]:
    return id_estudiante_context.get()

def set_programa(programa: str):
    programa_context.set(programa)

def get_programa() -> Optional[str]:
    return programa_context.get()

def set_datos_cursos(datos: Dict[str, Any]):
    datos_cursos_context.set(datos)

def get_datos_cursos() -> Optional[Dict[str, Any]]:
    return datos_cursos_context.get()

def reset_context():
    id_estudiante_context.set(None)
    programa_context.set(None)
    datos_cursos_context.set(None)
