
"""Rutas compatibles con la API de OpenAI para integrar agentes locales.

Este módulo expone endpoints que emulan `/v1/models` y
`/v1/chat/completions` para que Open-WebUI pueda comunicarse con los
agentes implementados en esta aplicación.
"""

from fastapi import APIRouter, Request
import httpx
from app.core.config import settings

router = APIRouter()

# Mapeo de nombres de modelos a endpoints
MODEL_TO_ENDPOINT = {
    "agente-horarios": "agente-horarios",
    "agente-info-personal": "agente-info-personal",
    "agente-aulas-virtuales": "agente-aulas-virtuales",
    "agente-notas": "agente-notas",
    "agente-presupuesto": "agente-presupuesto",
}


# === ENDPOINT: /models ===
@router.get("/models")
def listar_modelos():
    """Endpoint compatible con OpenAI API.

    Devuelve agentes como si fueran 'modelos'.
    """
    return {
        "object": "list",
        "data": [
            {"id": model_id, "object": "model"} 
            for model_id in MODEL_TO_ENDPOINT.keys()
        ],
    }


# === ENDPOINT: /chat/completions ===
@router.post("/chat/completions")
async def chat_completions(request: Request):
    """Recibe prompts desde Open-WebUI.

    Redirige la solicitud al agente correspondiente.
    """
    data = await request.json()
    model = data.get("model")
    messages = data.get("messages", [])
    prompt = messages[-1]["content"] if messages else ""

    # * Datos de ejemplo que Open-WebUI enviará de Usuario y Rol
    # TODO: En producción, estos datos deberían venir de la autenticación o headers
    body = {
        "prompt": prompt, 
        "id_usuario": "000837050", 
        "rol": "estudiante",
        "uuid": "1165a682-45fb-4bb9-875c-c65f3d46c14p",
        "email_usuario": "juan.garzon-m@uniminuto.edu.co",
        "programa": "ingenieria",
        "modelo_ia": "openai"
    }

    # Validar si el modelo existe
    endpoint_suffix = MODEL_TO_ENDPOINT.get(model)
    if not endpoint_suffix:
        return {"error": f"Modelo no reconocido: {model}"}

    # Determinar la URL base usando la configuración
    # Si el host es 0.0.0.0, usamos localhost para la petición interna
    host = "127.0.0.1" if settings.SERVER_HOST == "0.0.0.0" else settings.SERVER_HOST
    base_url = f"http://{host}:{settings.SERVER_PORT}"

    async with httpx.AsyncClient() as client:
        # Timeout aumentado porque algunos agentes (como Aulas) pueden tardar en warm-up
        response = await client.post(
            f"{base_url}/api/{endpoint_suffix}", 
            json=body,
            timeout=60.0 
        )

    # La respuesta de tu agente
    if response.status_code != 200:
         return {
            "error": f"Error en el agente {model}: {response.text}",
            "status_code": response.status_code
        }

    agent_response = response.json()
    answer = agent_response.get("respuesta", str(agent_response))

    return {
        "id": "chatcmpl-1",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": answer},
                "finish_reason": "stop",
            }
        ],
    }
