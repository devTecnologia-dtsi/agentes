
"""Rutas informativas y de estado de la API."""

from fastapi import APIRouter
from app.schemas.requests import RolUsuario
from app.services.agents_loader import (
    ACCESO_AGENTES,
    AGENTE_HORARIOS_DISPONIBLE,
    AGENTE_INFO_PERSONAL_DISPONIBLE,
    AGENTE_AULAS_VIRTUALES_DISPONIBLE,
    AGENTE_NOTAS_DISPONIBLE,
    AGENTE_PRESUPUESTO_DISPONIBLE,
)

router = APIRouter()


# ======================
# Ruta principal (documentación de la API)
# ======================
@router.get("/")
def root():
    """Información sobre los endpoints disponibles."""
    return {
        "mensaje": "API de Microservicios de Agentes Educativos",
        "version": "1.0.0",
        "endpoints": {
            "agente_horarios": "POST /api/agente-horarios",
            "agente_info_personal": "POST /api/agente-info-personal",
            "agente_aulas_virtuales": "POST /api/agente-aulas-virtuales",
            "agente_notas": "POST /api/agente-notas",
            "agente_presupuesto": "POST /api/agente-presupuesto",
            "status": "GET /api/status",
            "accesos": "GET /api/accesos",
            "documentacion": "GET /docs",
        },
        "ejemplo_request": {
            "prompt": "¿Cuáles son mis horarios?",
            "id_usuario": "estudiante123",
            "rol": "estudiante",
            "programa": "ingenieria",
        },
    }


# ======================
# API de estado y información
# ======================
@router.get("/status")
def api_status():
    """Estado general de la aplicación y agentes disponibles."""
    return {
        "agentes_disponibles": {
            "horarios": AGENTE_HORARIOS_DISPONIBLE,
            "info_personal": AGENTE_INFO_PERSONAL_DISPONIBLE,
            "aulas_virtuales": AGENTE_AULAS_VIRTUALES_DISPONIBLE,
            "notas": AGENTE_NOTAS_DISPONIBLE,
            "presupuesto": AGENTE_PRESUPUESTO_DISPONIBLE,
        },
        "endpoints": {
            "agente_horarios": "/api/agente-horarios",
            "agente_info_personal": "/api/agente-info-personal",
            "agente_aulas_virtuales": "/api/agente-aulas-virtuales",
            "agente_notas": "/api/agente-notas",
            "agente_presupuesto": "/api/agente-presupuesto",
        },
    }


@router.get("/accesos")
def info_accesos():
    """Información sobre qué roles pueden acceder a cada agente."""
    return {
        "control_acceso": ACCESO_AGENTES,
        "roles_disponibles": [rol.value for rol in RolUsuario],
        "descripcion": {
            "aulas_virtuales": "Agente de Aulas Virtuales - Consultas sobre cursos y eventos en Moodle",
            "horarios": "Agente de Horarios - Consultas sobre horarios de clases",
            "info_personal": "Agente de Información Personal - Datos personales del estudiante",
            "notas": "Agente de Notas - Consultas sobre calificaciones y créditos",
            "presupuesto": "Agente de Presupuesto - Gestión de presupuestos",
        },
    }

@router.get("/modelos_ai")
def modelos_ai_info():
    """Información sobre los modelos de IA disponibles."""
    return {
        "modelos_disponibles": {
            "openai": "gpt-4o-mini",
            "gemini": "gemini-2.5-flash-lite",
            "ollama": "gemma3:1b (local)",
            "huggingface": "google/flan-t5-large",
        }
    }
