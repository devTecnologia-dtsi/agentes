
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

engine = None
SessionLocal = None
Base = declarative_base()

if not settings.POSTGRES_CONNECTION_STRING:
    logger.warning(
        "POSTGRES_CONNECTION_STRING no está configurada. "
        "El historial en PostgreSQL estará desactivado."
    )
else:
    try:
        engine = create_engine(settings.POSTGRES_CONNECTION_STRING)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as e:
        logger.error(f"Error creando el engine de base de datos: {e}")
        engine = None
        SessionLocal = None


def get_db():
    """
    Generador de dependencias para obtener una sesión de base de datos.
    Maneja el ciclo de vida de la sesión (crear, usar, cerrar).
    """
    if SessionLocal is None:
        logger.warning("SessionLocal no está inicializado; get_db devuelve None.")
        db = None
        try:
            yield db
        finally:
            pass
    else:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


def init_db():
    """
    Inicializa las tablas de la base de datos definidas en los modelos.
    Requiere que el engine esté configurado correctamente.
    """
    global engine
    if engine is None:
        logger.warning(
            "Base de datos no configurada. La aplicación funcionará sin historial(memoria)"
        )
        return

    from . import models

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logger.error(f"Error inicializando la base de datos (create_all): {e}")
