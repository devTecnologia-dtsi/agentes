"""Inicializador simple de agente Ollama."""

import os
from langchain.agents import AgentType, initialize_agent
from langchain_ollama import ChatOllama
from langchain.prompts import MessagesPlaceholder
from app.core.logging import get_logger

logger = get_logger(__name__)

def inicializar_agente_ollama(herramientas, prompt, agent_type=None, **kwargs):
    """Crea un agente Ollama con las herramientas y prompt dados.

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
        
        llm = ChatOllama(
            model="gemma3:1b", 
            temperature=0,
            base_url="http://localhost:11434"
        )
        
        # Configurar kwargs del agente para incluir el prompt de sistema y soporte de memoria
        agent_kwargs = {
            "prefix": prompt,
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
        logger.error(f"Error al inicializar agente Ollama: {e}")
        raise e
