
"""Agente especializado en operaciones CRUD de presupuesto."""

from app.core.logging import get_logger

logger = get_logger(__name__)

try:
    from .agent import construir_agente_presupuesto

    AGENTE_PRESUPUESTO_DISPONIBLE = True
except ImportError as e:
    logger.error(f"Error al cargar Agente de Presupuesto: {e}")
    construir_agente_presupuesto = None
    AGENTE_PRESUPUESTO_DISPONIBLE = False
