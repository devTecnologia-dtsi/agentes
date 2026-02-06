"""Carga y exporta los agentes disponibles y control de acceso.

Define roles, verifica acceso por agente y expone referencias a los
agentes inicializados para su uso en los endpoints.
"""

from app.schemas.requests import RolUsuario
from app.core.logging import get_logger

logger = get_logger(__name__)

# Importar desde el paquete agentes
# ======================
# Control de acceso por agente
# ======================
ACCESO_AGENTES = {
    "horarios": [RolUsuario.ESTUDIANTE, RolUsuario.DOCENTE],
    "info_personal": [RolUsuario.ESTUDIANTE, RolUsuario.ADMINISTRATIVO],
    "aulas_virtuales": [RolUsuario.ESTUDIANTE, RolUsuario.DOCENTE],
    "notas": [RolUsuario.ESTUDIANTE],
    "presupuesto": [RolUsuario.ADMINISTRATIVO],
    }

def verificar_acceso_agente(agente: str, rol: RolUsuario) -> bool:
    """Verificar si un rol tiene acceso a un agente específico."""
    return rol in ACCESO_AGENTES.get(agente, [])

logger.info("Cargando agentes...")

# ======================
# Cargar agentes
# ======================

# Cargar agente de horarios
from app.agentes.agente_horarios import (
    AGENTE_HORARIOS_DISPONIBLE,
    construir_agente_horarios,
    cargar_datos_horario,
)

# Cargar agente de información personal
from app.agentes.agente_info_personal import (
    AGENTE_INFO_PERSONAL_DISPONIBLE,
    construir_agente_info_personal,
    cargar_datos_info_personal,
)

# Cargar agente de aulas virtuales
from app.agentes.agente_aulas_virtuales import (
    AGENTE_AULAS_VIRTUALES_DISPONIBLE,
    construir_agente_aulas_virtuales,
)

# Cargar agente de notas
from app.agentes.agente_notas import (
    AGENTE_NOTAS_DISPONIBLE,
    construir_agente_notas,
)

# Cargar agente de presupuesto
from app.agentes.agente_presupuesto import (
    AGENTE_PRESUPUESTO_DISPONIBLE,
    construir_agente_presupuesto,
)

# Exportar todo
__all__ = [
    "verificar_acceso_agente",
    "ACCESO_AGENTES",
    "construir_agente_horarios",
    "AGENTE_HORARIOS_DISPONIBLE",
    "cargar_datos_horario",
    "construir_agente_info_personal",
    "AGENTE_INFO_PERSONAL_DISPONIBLE",
    "cargar_datos_info_personal",
    "construir_agente_aulas_virtuales",
    "AGENTE_AULAS_VIRTUALES_DISPONIBLE",
    "construir_agente_notas",
    "AGENTE_NOTAS_DISPONIBLE",
    "construir_agente_presupuesto",
    "AGENTE_PRESUPUESTO_DISPONIBLE",
]
