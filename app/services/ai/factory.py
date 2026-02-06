
"""Factory para instanciar agentes de IA."""

from app.core.config import settings
from .gemini_model import inicializar_agente_gemini
from .openai_model import inicializar_agente_openai
from .hf_model import inicializar_agente_huggingface
from .ollama_model import inicializar_agente_ollama

def instanciar_agente(tools, prompt, modelo_ia: str = "gemini"):
    """Instancia un agente según el modelo especificado.
    
    Parámetros:
        tools: Lista de herramientas del agente
        prompt: Prompt del sistema para el agente
        modelo_ia: Nombre del modelo ("gemini", "openai", "huggingface", "ollama")
    
    Retorna:
        Agente inicializado con el modelo especificado
        
    Raises:
        ValueError: Si el modelo no existe o la API key no está configurada
    """
    
    # Mapeo de modelos disponibles
    # (función_inicializadora, nombre_variable_settings)
    MODELOS = {
        "gemini": (inicializar_agente_gemini, "GOOGLE_API_KEY"),
        "openai": (inicializar_agente_openai, "OPENAI_API_KEY"),
        "huggingface": (inicializar_agente_huggingface, "HUGGINGFACEHUB_API_TOKEN"),
        "ollama": (inicializar_agente_ollama, "OLLAMA_API_KEY"),
    }
    
    if modelo_ia not in MODELOS:
        raise ValueError(
            f"Modelo de IA inválido: {modelo_ia}. "
            f"Modelos disponibles: {list(MODELOS.keys())}"
        )
    
    init_func, api_key_name = MODELOS[modelo_ia]
    
    # Verificar que la API key esté configurada
    # Usamos getattr para obtener el valor dinámicamente desde settings
    api_key_value = getattr(settings, api_key_name)
    
    if not api_key_value:
        raise ValueError(
            f"{api_key_name} no está configurada en el archivo .env o settings. "
            f"No se puede inicializar el modelo {modelo_ia}."
        )
    
    # Inicializar y retornar el agente
    agente = init_func(tools, prompt)
    
    if agente is None:
        raise ValueError(
            f"El inicializador del modelo {modelo_ia} falló y retornó None. "
            f"Revise los logs para más detalles sobre el error interno del modelo."
        )
        
    return agente
