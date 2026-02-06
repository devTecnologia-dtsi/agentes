
import requests
from datetime import datetime
from typing import Optional, List, Dict
from .config import get_base_url, get_headers
from app.core.logging import get_logger

logger = get_logger(__name__)

def convertir_timestamp_unix(timestamp) -> Optional[str]:
    """Convierte timestamp Unix a formato legible"""
    try:
        if not timestamp or timestamp == 0:
            return None
        return datetime.fromtimestamp(int(timestamp)).strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return None

def obtener_eventos_curso(id_curso: int, instancia: str = "moocs") -> Optional[List[Dict]]:
    """Obtiene los eventos de un curso específico desde Moodle.

    Args:
        id_curso: ID del curso.
        instancia: Instancia de Moodle (por defecto "moocs").

    Returns:
        Lista de eventos si se carga exitosamente (puede estar vacía),
        None si hubo error de conexión o en la API
    """
    logger.info(f"Consultando API de eventos para curso {id_curso}")
    
    url = f"{get_base_url()}/getEventsByCourse?idCurso={id_curso}&instancia={instancia}"
    headers = get_headers()

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            # Procesar la respuesta JSON
            data = response.json()
            
            if isinstance(data, dict) and 'results' in data:
                results = data['results']
                # results puede ser una lista o un dict
                if isinstance(results, list) and len(results) > 0:
                    eventos = results[0].get('body', {}).get('events', [])
                elif isinstance(results, dict):
                    eventos = results.get('body', {}).get('events', [])
                else:
                    eventos = []
                
                # Estructurar los eventos para LLM
                datos_eventos_curso: List[Dict] = [{
                    'id': evento.get('id'),
                    'nombre': evento.get('name'),
                    'descripcion': evento.get('description', ''),
                    'tipo_actividad': evento.get('activitystr'),
                    'tipo_evento': evento.get('eventtype'),
                    'fecha_inicio': convertir_timestamp_unix(evento.get('timestart')),
                    'duracion': evento.get('timeduration'),
                    'modulo': evento.get('modulename'),
                    'vencido': evento.get('overdue', False)
                } for evento in eventos]
                logger.info(f"Eventos cargados exitosamente para curso {id_curso} ({len(datos_eventos_curso)} eventos)")
                return datos_eventos_curso
            
            # Si llegamos aquí, no hay eventos
            logger.info(f"No hay eventos para el curso {id_curso}")
            return []
        else:
            logger.error(f"Error de conexión al cargar eventos: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión al cargar eventos: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado al cargar eventos: {e}")
        return None
