"""Configuración compartida para servicios de Notas."""

from typing import Dict
from app.core.config import settings

def get_base_url() -> str:
    """
    Obtiene la URL base de la API de Notas desde la configuración global.
    
    Returns:
        str: La URL base configurada (API_NOTAS).
        
    Raises:
        ValueError: Si la URL no está configurada.
    """
    if not settings.API_NOTAS:
        raise ValueError("La variable API_NOTAS no está configurada.")
    return settings.API_NOTAS

def get_historial_url() -> str:
    """
    Obtiene la URL de la API de Historial desde la configuración global.

    Returns:
        str: La URL configurada (API_HISTORIAL).

    Raises:
        ValueError: Si la URL no está configurada.
    """
    if not settings.API_HISTORIAL:
        raise ValueError("La variable API_HISTORIAL no está configurada.")
    return settings.API_HISTORIAL

def get_headers() -> Dict[str, str]:
    """
    Retorna los headers para las peticiones a la API de Notas.
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
