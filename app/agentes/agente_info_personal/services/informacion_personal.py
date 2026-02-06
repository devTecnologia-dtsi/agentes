
"""Servicios para manejo de datos y APIs."""

import httpx
from typing import Optional, Dict
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


async def cargar_datos_info_personal(usuario_id: str) -> Optional[Dict]:
    """Carga datos de información personal del usuario desde la API.

    Args:
        usuario_id: ID del usuario para consultar.

    Returns:
        Diccionario con datos personales si se cargaron exitosamente,
        None si hubo error de conexión o en la API
    """
    logger.info(f"Consultando API para usuario {usuario_id}")
    url = f"{settings.API_INFORMACION_PERSONAL}/banner.php?fn=datosPersonales&id={usuario_id}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=20.0)

        if response.status_code == 200:
            datos_informacion_personal = response.json()
            
            # Validar que haya datos válidos
            if datos_informacion_personal is None:
                logger.warning(f"API retornó None para usuario {usuario_id}")
                return None
            
            logger.info(f"Datos cargados exitosamente para usuario {usuario_id}")
            return datos_informacion_personal
        else:
            logger.error(
                "Error en la respuesta: "
                f"{response.status_code} - {response.text}"
            )
            logger.error("Error al cargar datos de información personal")
            return None

    except httpx.RequestError as e:
        logger.error(f"Error de conexión al cargar información personal: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Error inesperado al cargar información personal: {e}", exc_info=True)
        return None
