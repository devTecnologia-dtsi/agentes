
from typing import List
import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Cargar variables de entorno explícitamente para asegurar que librerías externas (como LangChain) las vean
load_dotenv()

class Settings(BaseSettings):
    """
    Configuración global de la aplicación.

    Esta clase actúa como la configuración del sistema.
    Utiliza Pydantic para:
    - Leer y parsear variables de entorno desde el archivo .env.
    - Validar tipos de datos (asegurando que los puertos sean enteros, flags sean booleanos, etc.).
    - Establecer valores por defecto seguros para desarrollo.
    - Centralizar la gestión de secretos y claves de API.
    """
    
    # Servidor
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 3000
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Base de Datos
    POSTGRES_CONNECTION_STRING: str | None = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/app.log"
    
    # APIs Keys IA
    OPENAI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    HUGGINGFACEHUB_API_TOKEN: str | None = None
    OLLAMA_API_KEY: str | None = None

    # Endpoints de Microservicios y APIs Externas
    #Agente de Horario
    API_HORARIO_ACTUAL: str | None = None
    #Agente de Información Personal
    API_INFORMACION_PERSONAL: str | None = None
    #Agente de Historial Académico
    MOODLE_API_URL: str | None = None
    
    #Agente de Notas
    API_HISTORIAL: str | None = None
    API_CREDITOS: str | None = None
    API_CURSOS_CALIFICACIONES: str | None = None
    API_NOTAS: str | None = None
    
    #Agente de Presupuesto
    API_PRESUPUESTO: str | None = None
    # apikey digibee
    API_KEY_MICROSERVICIOS: str | None = Field(default=None, alias="apikey")

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
