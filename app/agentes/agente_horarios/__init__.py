
from app.core.logging import get_logger

logger = get_logger(__name__)

try:
    from .agent import construir_agente_horarios
    from .services.horario_actual import cargar_datos_horario

    AGENTE_HORARIOS_DISPONIBLE = True
except ImportError as e:
    logger.error(f"Error al cargar Agente de Horarios: {e}")
    construir_agente_horarios = None
    cargar_datos_horario = None
    AGENTE_HORARIOS_DISPONIBLE = False
