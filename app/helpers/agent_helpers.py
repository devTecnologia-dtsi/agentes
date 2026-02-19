
import time
import asyncio
import httpx
from typing import Callable, Any, Awaitable, Dict
from fastapi import HTTPException
from langchain_core.messages import HumanMessage, AIMessage

from app.core.logging import get_logger
from app.schemas.requests import RequestAgentes
from app.schemas.responses import ResponseAgentes
from app.services.history import PostgresTurnBasedHistory

logger = get_logger(__name__)

# Diccionario para rastrear la última interacción con cada servicio (URL)
_last_service_interactions: dict[str, float] = {}

async def realizar_warmup_servicio(
    url: str, 
    headers: dict | None = None, 
    timeout: float = 30.0, 
    wait_time: float = 35.0, 
    cooldown: float = 50.0
) -> None:
    """
    Realiza un warm-up de un servicio externo
    """
    if not url:
        logger.warning("URL no proporcionada para warm-up. Omitiendo.")
        return

    now = time.time()
    last_interaction = _last_service_interactions.get(url, 0.0)

    # Si la última interacción fue reciente, el servicio está caliente
    if now - last_interaction < cooldown:
        logger.info(f"Servicio {url} activo (warm). Omitiendo warm-up.")
        return

    logger.info(f"Iniciando warm-up de {url} (Cold Start). Espera: {wait_time}s")
    
    async def _make_request():
        try:
            async with httpx.AsyncClient() as client:
                await client.get(url, headers=headers, timeout=timeout)
        except Exception as e:
            # Es esperado que falle o timeoutee durante el warm-up
            logger.debug(f"Warm-up request a {url} finalizado: {str(e)}")

    # Ejecutamos petición y sleep en paralelo
    start_time = time.time()
    await asyncio.gather(_make_request(), asyncio.sleep(wait_time))
    
    elapsed = time.time() - start_time
    logger.info(f"Warm-up de {url} completado en {elapsed:.2f}s.")
    
    # Actualizamos el timestamp de la última interacción
    _last_service_interactions[url] = time.time()


def actualizar_tiempo_interaccion_servicio(url: str) -> None:
    """
    Actualiza el timestamp de interacción para mantener el servicio 'caliente'.
    """
    if url:
        _last_service_interactions[url] = time.time()


def validar_y_obtener_prompt(prompt_entrada: str) -> str:
    """
    Valida que el prompt no esté vacío.
    """
    prompt_validado = prompt_entrada.strip()
    if not prompt_validado:
        raise HTTPException(
            status_code=400,
            detail="El prompt no puede estar vacío"
        )
    return prompt_validado


# =================================================================================================
# Funciones Helpers para procesar_solicitud_agente
# =================================================================================================

def verificar_disponibilidad_agente(nombre_agente: str, disponible: bool):
    """Verifica si el agente está habilitado globalmente."""
    if not disponible:
        raise HTTPException(
            status_code=503,
            detail=f"El {nombre_agente} está deshabilitado temporalmente."
        )

def validar_y_obtener_email(email: str | None) -> str:
    """Valida que el email esté presente si es requerido."""
    if not email:
        raise HTTPException(
            status_code=400,
            detail="Se requiere el email del usuario para este agente."
        )
    return email

def validar_y_obtener_id_usuario(id_usuario: str | None) -> str:
    """Valida que el id_usuario esté presente si es requerido."""
    if not id_usuario:
        raise HTTPException(
            status_code=400,
            detail="Se requiere el ID del usuario para este agente."
        )
    return id_usuario

def registrar_llamada_agente(nombre: str, usuario_id: str, rol: str, modelo: str, prompt: str):
    """Registra en logs la llamada al agente."""
    logger.info(f"Solicitud a {nombre} | Usuario: {usuario_id} | Rol: {rol} | Modelo: {modelo}")
    logger.info(f"Prompt: {prompt}")

def ejecutar_construccion_agente(funcion_construir: Callable, modelo: str) -> Any:
    """Ejecuta la función factory del agente y maneja errores de inicialización."""
    try:
        agente = funcion_construir(modelo_ia=modelo)
        if not agente:
            raise ValueError("La función constructora retornó None")
        return agente
    except Exception as e:
        logger.error(f"Error construyendo agente: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al inicializar el agente. Detalle: {str(e)}"
        )

def inicializar_historial(uuid: str, id_usuario: str | None, email_usuario: str | None) -> PostgresTurnBasedHistory:
    """Inicializa el historial basado en PostgreSQL."""
    return PostgresTurnBasedHistory(
        session_id=uuid,
        student_id=str(id_usuario) if id_usuario is not None else None,
        email_usuario=email_usuario
    )

def guardar_interaccion_historial(
    history: PostgresTurnBasedHistory, 
    prompt: str, 
    respuesta: str,
    system_prompt: str | None = None,
    agent_name: str | None = None
):
    """Guarda el prompt del usuario, la respuesta del agente y metadatos en el historial."""
    # Usamos el método unificado add_interaction para guardar todo el contexto
    history.add_interaction(
        human_msg=prompt,
        ai_msg=respuesta,
        system_msg=system_prompt,
        agent_name=agent_name
    )

def construir_respuesta_agente(
    respuesta_agente: dict,
    nombre_agente: str,
    id_usuario: str,
    email_usuario: str | None,
    rol: str
) -> ResponseAgentes:
    """Construye el objeto de respuesta estandarizado."""
    output = respuesta_agente.get("output", "Sin respuesta")

    return ResponseAgentes(
        agente=nombre_agente,
        respuesta=output,
        id_usuario=id_usuario,
        email_usuario=email_usuario,
        rol=rol
    )

def manejar_error_en_agente(nombre_agente: str, error: Exception):
    """Maneja errores no capturados durante la ejecución del agente."""
    logger.error(f"Error crítico en {nombre_agente}: {str(error)}", exc_info=True)
    raise HTTPException(
        status_code=500,
        detail=f"Ocurrió un error interno en el {nombre_agente}. Por favor intente más tarde."
    )

# =================================================================================================
# Función Principal
# =================================================================================================

async def procesar_solicitud_agente(
    request: RequestAgentes,
    nombre_agente: str,
    agente_disponible: bool,
    funcion_construir_agente: Callable,
    funcion_configurar_contexto: Callable[[Any], None] | None = None,
    # Parámetros opcionales para flujos avanzados
    tarea_previa: Callable[[], Awaitable[None]] | None = None,
    tarea_posterior: Callable[[], Awaitable[None]] | None = None,
    usar_email_como_identificador: bool = False,
    system_prompt: str | None = None
) -> ResponseAgentes:
    """Procesa una solicitud estándar para un agente.
    
    Orquesta todo el flujo: verificación de permisos, validación, 
    tareas previas (warm-up), construcción del agente, ejecución e historial.

    Args:
        request: Objeto con los datos de la solicitud (prompt, usuario, rol, etc.).
        nombre_agente: Identificador técnico del agente (slug, ej: "agente-horarios", "agente-notas"). 
                       Se usa para permisos, BD y se formatea para logs/respuesta.
        agente_disponible: Booleano que indica si el agente está habilitado en el sistema.
        funcion_construir_agente: Función factoría que crea la instancia del agente LangChain.
        funcion_configurar_contexto: Función opcional para inyectar datos en variables de contexto (thread-safe).
        tarea_previa: Corrutina opcional a ejecutar ANTES del agente (ej: warm-up de APIs).
        tarea_posterior: Corrutina opcional a ejecutar DESPUÉS del agente (ej: actualizar métricas).
        usar_email_como_identificador: Si es True, usa el email como ID principal. Si es False (default), usa id_usuario.
        system_prompt: Texto del prompt de sistema para guardar en auditoría (opcional).
    """
    try:
        # Importación tardía para evitar ciclos
        from app.services.agents_loader import verificar_acceso_agente
        
        # 1. Verificar acceso
        # nombre_agente se usa para buscar en el diccionario de permisos (ACCESO_AGENTES)
        if not verificar_acceso_agente(nombre_agente, request.rol):
            raise HTTPException(
                status_code=403,
                detail=f"Acceso denegado: El rol {request.rol} no tiene permisos para el agente '{nombre_agente}'"
            )
            
        # 2. Verificar disponibilidad
        verificar_disponibilidad_agente(nombre_agente, agente_disponible)
        
        # 3. Tareas previas (ej: Warm-up o Carga de Datos)
        if tarea_previa:
            await tarea_previa()
        
        # 4. Validar prompt
        prompt_validado = validar_y_obtener_prompt(request.prompt)
        
        # Determinar el ID principal para logs y contexto
        if usar_email_como_identificador:
             # Si se requiere email, validarlo
            id_principal = validar_y_obtener_email(request.email_usuario)
        else:
            # Si se requiere ID de usuario, validarlo
            id_principal = validar_y_obtener_id_usuario(request.id_usuario)

        # 5. Configurar contexto (si aplica)
        if funcion_configurar_contexto:
            # Si la función acepta argumentos, pasamos el ID principal
            # Nota: Asumimos que funcion_configurar_contexto maneja su propia lógica si es compleja
            funcion_configurar_contexto(id_principal)
            
        # 6. Registrar llamada
        registrar_llamada_agente(nombre_agente, id_principal, request.rol, request.modelo_ia.value, prompt_validado)
        
        # 7. Construir agente
        agente = ejecutar_construccion_agente(funcion_construir_agente, request.modelo_ia.value)
        
        # 8. Inicializar historial
        # Nota: El historial siempre intenta usar ambos IDs si están disponibles
        history = inicializar_historial(request.uuid, request.id_usuario, request.email_usuario)
        
        # 9. Invocar agente con historial como contexto
        # El AgentExecutor maneja automáticamente la memoria y el ReAct loop
        respuesta_agente = await agente.ainvoke({
            "input": prompt_validado,
            "chat_history": history.messages  # Historial recuperado de BD
        })
        
        # 10. Extraer respuesta del agente
        respuesta_contenido = respuesta_agente.get("output", "Sin respuesta")
        
        # 11. Guardar historial
        guardar_interaccion_historial(
            history, 
            prompt_validado, 
            respuesta_contenido, 
            system_prompt=system_prompt,
            agent_name=nombre_agente
        )
        
        # 11. Tareas posteriores (ej: Actualizar timestamps)
        if tarea_posterior:
            await tarea_posterior()
        
        # 12. Retornar respuesta
        return construir_respuesta_agente(
            respuesta_agente,
            nombre_agente, # Devolvemos el nombre crudo al usuario
            id_usuario=request.id_usuario,
            email_usuario=request.email_usuario,
            rol=request.rol
        )
        
    except HTTPException as error_http:
        raise error_http
    except Exception as error_general:
        manejar_error_en_agente(nombre_agente, error_general)
