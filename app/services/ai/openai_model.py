"""Inicializador simple de agente OpenAI."""

from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def inicializar_agente_openai(herramientas, prompt, agent_type=None, **kwargs):
    """Crea un agente OpenAI con las herramientas y prompt dados.

    Args:
        herramientas: Lista de herramientas de LangChain.
        prompt: Prompt base para orientar al agente.
        agent_type: Tipo de agente (default: STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION).
        **kwargs: Argumentos adicionales para initialize_agent.

    Returns:
        Agente configurado o None si hay error.
    """
    try:
        if agent_type is None:
            agent_type = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
        
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=2048,
            api_key=settings.OPENAI_API_KEY
        )

        # Configurar kwargs del agente para incluir el prompt de sistema y soporte de memoria
        agent_kwargs = {
            "prefix": prompt, # En Structured Chat, 'prefix' suele ser donde va el System Prompt
            "memory_prompts": [MessagesPlaceholder(variable_name="chat_history")],
            "input_variables": ["input", "agent_scratchpad", "chat_history"]
        }
        
        # Si se pasan kwargs adicionales, mezclarlos
        if "agent_kwargs" in kwargs:
            agent_kwargs.update(kwargs.pop("agent_kwargs"))

        return initialize_agent(
            herramientas,
            llm,
            agent=agent_type,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
            max_execution_time=60,
            early_stopping_method="force",
            agent_kwargs=agent_kwargs,
            **kwargs
        )

    except Exception as e:
        logger.error(f"Error al inicializar agente OpenAI: {e}")
        raise e
