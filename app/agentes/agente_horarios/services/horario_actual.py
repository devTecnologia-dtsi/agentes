"""Servicios para manejo de datos y APIs."""

import requests
from typing import Optional, List, Dict
from app.core.logging import get_logger
from app.core.config import settings

logger = get_logger(__name__)

# Orden de días para devolver el horario organizado por semana
ORDEN_DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def cargar_datos_horario(usuario_id: str) -> Optional[List[Dict]]:
    """Carga datos de horarios del usuario desde la API.

    Devuelve la información sin duplicados y ordenada por día de la semana
    (Lunes a Domingo). La normalización de valores (ej. null) queda a cargo
    de la capa que consume (tool/agente).

    Args:
        usuario_id: ID del usuario para consultar.

    Returns:
        Lista de horarios si se carga exitosamente (puede estar vacía),
        None si hubo error de conexión o en la API.
    """
    logger.info(f"Consultando API para nuevo usuario {usuario_id}")
    url = (f"{settings.API_HORARIO_ACTUAL}?cn={usuario_id}")

    try:
        response = requests.get(url, timeout=20)

        if response.status_code == 200:
            datos_horario = response.json()
            logger.info(f"API retornó {len(datos_horario)} registros para usuario {usuario_id}")

            # Eliminar duplicados exactos (dict → tupla ordenada para hashable)
            datos_unicos = [
                dict(t)
                for t in {tuple(sorted(d.items(), key=lambda x: x[0])) for d in datos_horario}
            ]
            if len(datos_unicos) < len(datos_horario):
                logger.info(f"Se eliminaron {len(datos_horario) - len(datos_unicos)} registros duplicados")

            # Ordenar por día y luego por horaInicio dentro de cada día (sin hora → al final)
            def _clave_orden(registro: Dict) -> tuple:
                dia = (registro.get("dia") or "").strip().capitalize()
                idx_dia = ORDEN_DIAS.index(dia) if dia in ORDEN_DIAS else len(ORDEN_DIAS)
                hi = registro.get("horaInicio")
                if hi is None:
                    return (idx_dia, 9999)
                try:
                    return (idx_dia, int(hi))
                except (TypeError, ValueError):
                    return (idx_dia, 9999)

            datos_ordenados = sorted(datos_unicos, key=_clave_orden)
            logger.debug(f"Datos procesados: {len(datos_ordenados)} registros, organizados por día")
            return datos_ordenados
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

