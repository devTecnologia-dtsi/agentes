
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

def obtener_cursos_usuario(correo_institucional: str) -> Optional[List[Dict]]:
    """Obtiene los cursos del usuario desde Moodle.

    Args:
        correo_institucional: Correo institucional del usuario.

    Returns:
        Lista de cursos si se carga exitosamente (puede estar vacía),
        None si hubo error de conexión o en la API
    """
    logger.info(f"Consultando API de cursos para {correo_institucional}")
    
    url = f"{get_base_url()}/getUserCourses?correoInstitucional={correo_institucional}"
    headers = get_headers()
    
    # Realizar la solicitud a la API de Moodle
    try:
        response = requests.get(url, headers=headers, timeout=40)
        if response.status_code == 200:
            # Procesar la respuesta JSON
            data = response.json()
            
            # Iterar por cada modalidad (executionId)
            if isinstance(data, list):
                datos_cursos_usuario: List[Dict] = []
                for modalidad in data:
                    execution_id = modalidad.get('executionId', 'desconocido')
                    cursos = modalidad.get('result', {}).get('body', [])
                    
                    # Procesar cada curso
                    for curso in cursos:
                        curso_simple = {
                            'id': curso.get('id'),
                            'modalidad': execution_id,
                            'nombre': curso.get('fullname'),
                            'codigo': curso.get('shortname'),
                            'fecha_inicio': convertir_timestamp_unix(curso.get('startdate')),
                            'fecha_fin': convertir_timestamp_unix(curso.get('enddate')),
                            'ultimo_acceso': convertir_timestamp_unix(curso.get('lastaccess')),
                            'formato': curso.get('format')
                        }
                        datos_cursos_usuario.append(curso_simple)
                
                logger.info(f"Cursos cargados exitosamente para {correo_institucional}")
                return datos_cursos_usuario
            
            return []
        else:
            logger.error(f"Error de conexión al cargar cursos: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error inesperado al cargar cursos: {e}", exc_info=True)
        return None
