
"""Agente especializado en consultas de aulas virtuales de Moodle."""

from app.core.logging import get_logger

logger = get_logger(__name__)

try:
    from .agent import construir_agente_aulas_virtuales

    AGENTE_AULAS_VIRTUALES_DISPONIBLE = True
except ImportError as e:
    logger.error(f"Error al cargar Agente de Aulas Virtuales: {e}")
    construir_agente_aulas_virtuales = None
    AGENTE_AULAS_VIRTUALES_DISPONIBLE = False
