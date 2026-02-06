"""Servicios para manejo de datos y APIs."""

import requests
import os
from typing import Optional, List, Dict
from app.core.logging import get_logger
from app.core.config import settings

logger = get_logger(__name__)

def cargar_datos_horario(usuario_id: str) -> Optional[List[Dict]]:
    """Carga datos de horarios del usuario desde la API.

    Args:
        usuario_id: ID del usuario para consultar.

    Returns:
        Lista de horarios si se carga exitosamente (puede estar vacía),
        None si hubo error de conexión o en la API
    """
    logger.info(f"Consultando API para nuevo usuario {usuario_id}")
    url = (f"{settings.API_HORARIO_ACTUAL}?cn={usuario_id}")

    try:
        response = requests.get(url, timeout=20)

        if response.status_code == 200:
            datos_horario = response.json()
            # Eliminar duplicados usando set comprehension
            datos_horario = [
                dict(t)
                for t in {tuple(sorted(d.items())) for d in datos_horario}
            ]
            logger.debug(f"Datos crudos de API: {len(datos_horario)} registros")
            logger.debug(f"Primeros 2 registros: {datos_horario[:2]}")
            return datos_horario
        else:
            logger.error(
                "Error en la respuesta: "
                f"{response.status_code} - {response.text}"
            )
            logger.error("Error al cargar datos de horarios")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión al cargar horarios: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Error inesperado al cargar horarios: {e}", exc_info=True)
        return None

