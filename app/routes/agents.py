"""Rutas para invocar a los agentes."""

import os
from fastapi import APIRouter

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.requests import RequestAgentes
from app.schemas.responses import ResponseAgentes
from app.services.agents_loader import (
    AGENTE_HORARIOS_DISPONIBLE,
    AGENTE_INFO_PERSONAL_DISPONIBLE,
    AGENTE_AULAS_VIRTUALES_DISPONIBLE,
    AGENTE_NOTAS_DISPONIBLE,
    AGENTE_PRESUPUESTO_DISPONIBLE,
    construir_agente_horarios,
    construir_agente_info_personal,
    construir_agente_aulas_virtuales,
    construir_agente_notas,
    construir_agente_presupuesto,
)
from app.helpers.agent_helpers import (
    procesar_solicitud_agente,
    realizar_warmup_servicio,
    actualizar_tiempo_interaccion_servicio,
)

# Importar Prompts para Auditoría
from app.agentes.agente_horarios.prompts.system_prompt import PROMPT_HORARIO
from app.agentes.agente_info_personal.prompts.system_prompt import PROMPT_PERSONAL
from app.agentes.agente_aulas_virtuales.prompts.system_prompt import PROMPT_AULAS_VIRTUALES
from app.agentes.agente_notas.prompts.system_prompt import SYSTEM_PROMPT as PROMPT_NOTAS
from app.agentes.agente_presupuesto.prompt.system_prompt import SYSTEM_PROMPT as PROMPT_PRESUPUESTO

logger = get_logger(__name__)

router = APIRouter()

# ======================
# Endpoints de microservicios para cada agente
# ======================

@router.post("/agente-horarios", tags=["tools"])
async def agente_horarios_endpoint(request: RequestAgentes) -> ResponseAgentes:
    """Agente de Horarios."""
    # Importación de setter de contexto específico
    from app.agentes.agente_horarios.tools.tools import set_usuario_id
    
    return await procesar_solicitud_agente(
        request=request,
        nombre_agente="agente-horarios",
        agente_disponible=AGENTE_HORARIOS_DISPONIBLE,
        funcion_construir_agente=construir_agente_horarios,
        funcion_configurar_contexto=set_usuario_id,
        system_prompt=PROMPT_HORARIO
    )


@router.post("/agente-info-personal", tags=["tools"])
async def agente_info_personal_endpoint(request: RequestAgentes) -> ResponseAgentes:
    """Agente de Información Personal."""
    # Importación de setter de contexto específico
    from app.agentes.agente_info_personal.tools.tools import set_usuario_id_info
    
    return await procesar_solicitud_agente(
        request=request,
        nombre_agente="agente-info-personal",
        agente_disponible=AGENTE_INFO_PERSONAL_DISPONIBLE,
        funcion_construir_agente=construir_agente_info_personal,
        funcion_configurar_contexto=set_usuario_id_info,
        system_prompt=PROMPT_PERSONAL
    )


@router.post("/agente-aulas-virtuales", tags=["tools"])
async def agente_aulas_virtuales_endpoint(request: RequestAgentes) -> ResponseAgentes:
    """Agente de Aulas Virtuales (Moodle)."""
    # Importación de setter de contexto específico
    from app.agentes.agente_aulas_virtuales.tools.context import set_email_usuario
    
    # Lógica de Warm-up para Moodle
    async def warmup_moodle():
        moodle_url = settings.MOODLE_API_URL
        if not moodle_url:
            logger.error("MOODLE_API_URL no encontrada en variables de entorno (Settings)")
            
        api_key = settings.API_KEY_MICROSERVICIOS
        headers = {"apikey": api_key} if api_key else None
        
        logger.info(f"Verificando warm-up para URL: {moodle_url}")
        await realizar_warmup_servicio(url=moodle_url, headers=headers)

    # Lógica Post-Ejecución (Actualizar timestamp)
    async def actualizar_timestamp():
        moodle_url = settings.MOODLE_API_URL
        actualizar_tiempo_interaccion_servicio(moodle_url)

    return await procesar_solicitud_agente(
        request=request,
        nombre_agente="agente-aulas-virtuales",
        agente_disponible=AGENTE_AULAS_VIRTUALES_DISPONIBLE,
        funcion_construir_agente=construir_agente_aulas_virtuales,
        funcion_configurar_contexto=set_email_usuario,
        tarea_previa=warmup_moodle,
        tarea_posterior=actualizar_timestamp,
        usar_email_como_identificador=True,  # Importante: Aulas usa email para tracking
        system_prompt=PROMPT_AULAS_VIRTUALES
    )


@router.post("/agente-notas", tags=["tools"])
async def agente_notas_endpoint(request: RequestAgentes) -> ResponseAgentes:
    """Agente de Notas Académicas."""
    # Importación de setter de contexto específico
    from app.agentes.agente_notas.tools.context import set_id_estudiante

    # Lógica de Warm-up para Notas
    async def warmup_notas():
        import asyncio
        api_key = settings.API_KEY_MICROSERVICIOS
        headers = {"apikey": api_key} if api_key else None
        
        # Construir URLs desde API_NOTAS (base)
        base_url = settings.API_NOTAS
        urls_warmup = []
        if base_url:
            # IMPORTANTE: Apuntar a los endpoints específicos para asegurar que el pipeline se despierte
            # aunque devuelva 400 por falta de parámetros.
            urls_warmup = [
                f"{base_url}/servicios-banner-dos/cumplimientoCursos",
                f"{base_url}/servicios-banner/consultaCursos",
                f"{base_url}/servicios-banner/calificacionActual"
            ]
        
        # Filtrar URLs válidas
        urls_validas = [url for url in urls_warmup if url]
        
        if urls_validas:
            logger.info(f"Iniciando warm-up paralelo para {len(urls_validas)} servicios desde API_NOTAS...")
            # Ejecutar warm-up en paralelo
            await asyncio.gather(*(
                realizar_warmup_servicio(url=url, headers=headers) 
                for url in urls_validas
            ))

    # Lógica Post-Ejecución (Actualizar timestamp)
    async def actualizar_timestamp_notas():
        base_url = settings.API_NOTAS
        if base_url:
            urls_warmup = [
                f"{base_url}/servicios-banner-dos/cumplimientoCursos",
                f"{base_url}/servicios-banner/consultaCursos",
                f"{base_url}/servicios-banner/calificacionActual"
            ]
            for url in urls_warmup:
                actualizar_tiempo_interaccion_servicio(url)

    return await procesar_solicitud_agente(
        request=request,
        nombre_agente="notas",
        agente_disponible=AGENTE_NOTAS_DISPONIBLE,
        funcion_construir_agente=construir_agente_notas,
        funcion_configurar_contexto=set_id_estudiante,
        tarea_previa=warmup_notas,
        tarea_posterior=actualizar_timestamp_notas,
        system_prompt=PROMPT_NOTAS
    )


@router.post("/agente-presupuesto", tags=["tools"])
async def agente_presupuesto_endpoint(request: RequestAgentes) -> ResponseAgentes:
    """Agente de Presupuesto - Gestiona operaciones CRUD de presupuesto."""
    return await procesar_solicitud_agente(
        request=request,
        nombre_agente="agente-presupuesto",
        agente_disponible=AGENTE_PRESUPUESTO_DISPONIBLE,
        funcion_construir_agente=construir_agente_presupuesto,
        system_prompt=PROMPT_PRESUPUESTO
    )
