
"""Agente especializado en consultas de notas académicas."""

from app.core.logging import get_logger

logger = get_logger(__name__)

try:
    from .agent import construir_agente_notas

    AGENTE_NOTAS_DISPONIBLE = True
except ImportError as e:
    logger.error(f"Error al cargar Agente de Notas Académicas: {e}")
    construir_agente_notas = None
    AGENTE_NOTAS_DISPONIBLE = False
