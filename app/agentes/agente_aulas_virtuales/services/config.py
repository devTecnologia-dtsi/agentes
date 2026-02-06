"""Configuración compartida para servicios de Moodle."""

from typing import Dict
from app.core.config import settings

def get_base_url() -> str:
    """
    Obtiene la URL base de la API de Moodle desde la configuración global.
    
    Returns:
        str: La URL base configurada (MOODLE_API_URL).
        
    Raises:
        ValueError: Si la URL no está configurada.
    """
    if not settings.MOODLE_API_URL:
        raise ValueError("La variable MOODLE_API_URL no está configurada.")
    return settings.MOODLE_API_URL

def get_headers() -> Dict[str, str]:
    """
    Retorna los headers para las peticiones a la API de Moodle.
    Usa la API Key global definida en API_KEY_MICROSERVICIOS (alias 'apikey').
    
    Returns:
        Dict[str, str]: Diccionario con los headers de autenticación.
        
    Raises:
        ValueError: Si la API Key no está configurada.
    """
    api_key = settings.API_KEY_MICROSERVICIOS
    if not api_key:
        raise ValueError("Falta la variable de entorno 'apikey' (configurada como API_KEY_MICROSERVICIOS).")
    return {'apikey': api_key}
