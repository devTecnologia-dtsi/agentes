from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from app.core.config import settings
from app.routes import agents, info, openai_api

from app.db.connection import SessionLocal, init_db

# ======================
# Lifespan Events
# ======================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación (inicio y cierre)."""
    if settings.AUTO_INIT_DB:
        init_db()  # Crea automáticamente las tablas si no existen
    yield
    # Lógica de cierre (si es necesaria)

# ======================
# FastAPI
# ======================
app = FastAPI(lifespan=lifespan)

# Configurar CORS para permitir solicitudes desde cualquier origen (WebUi)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # o  ["http://localhost:3000"]
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)
# Incluir rutas con prefijos correctos
app.include_router(agents.router, prefix="/api")  # Rutas directas para agentes
app.include_router(info.router, prefix="/api")
app.include_router(openai_api.router, prefix="/v1") # Compatibilidad OpenAI
# ======================
# Ejecutar FastAPI
# ======================
if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
