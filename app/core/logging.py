
import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# Constantes de configuración
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"

class ColoredFormatter(logging.Formatter):
    """Formateador personalizado para agregar colores a los logs en consola."""
    
    # Códigos ANSI para colores
    cyan = "\x1b[36;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.cyan + self.fmt + self.reset,
            logging.INFO: self.green + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def _setup_log_directory(file_path: str):
    """Asegura que el directorio de logs exista."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    Configura y devuelve un logger para el módulo especificado.
    Implementa el patrón Singleton para la configuración de handlers por logger.
    
    Args:
        name (str): Nombre del módulo (usualmente __name__).
        
    Returns:
        logging.Logger: Logger configurado.
    """
    logger = logging.getLogger(name)
    
    # Si el logger ya tiene handlers, asumimos que ya está configurado
    if logger.handlers:
        return logger
        
    logger.setLevel(settings.LOG_LEVEL)
    
    # Formateador para archivo (sin colores)
    file_formatter = logging.Formatter(LOG_FORMAT)
    
    # 1. Handler de Consola (StreamHandler) con colores
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter(LOG_FORMAT))
    logger.addHandler(console_handler)
    
    # 2. Handler de Archivo Rotativo (sin colores)
    try:
        _setup_log_directory(settings.LOG_FILE_PATH)
        file_handler = RotatingFileHandler(
            settings.LOG_FILE_PATH, 
            maxBytes=10*1024*1024, # 10 MB
            backupCount=5, 
            encoding="utf-8"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        # Fallback seguro a stderr si falla el archivo
        sys.stderr.write(f"Error crítico configurando logger de archivo: {e}\n")

    # Evitar que los logs se propaguen al root logger si este también tiene handlers
    # para evitar duplicados, ya que estamos configurando handlers por logger.
    logger.propagate = False
    
    return logger
