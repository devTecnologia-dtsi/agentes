
from app.core.logging import get_logger

logger = get_logger(__name__)

try:
    from .agent import construir_agente_info_personal
    from .services.informacion_personal import cargar_datos_info_personal

    AGENTE_INFO_PERSONAL_DISPONIBLE = True
except ImportError as e:
    logger.error(f"Error al cargar Agente de Información Personal: {e}")
    construir_agente_info_personal = None
    cargar_datos_info_personal = None
    AGENTE_INFO_PERSONAL_DISPONIBLE = False
