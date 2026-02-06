"""Inicializador simple de agente Hugging Face."""

from langchain.agents import AgentType, initialize_agent
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from app.core.logging import get_logger

logger = get_logger(__name__)

def inicializar_agente_huggingface(
    herramientas,
    prompt,
    agent_type=None,
    model_id: str = "nvidia/Nemotron-Cascade-14B-Thinking",
    task: str = "conversational",
    temperature: float = 0.0,
    max_new_tokens: int = 2048,
    **kwargs,
):
    """
    Crea un agente Hugging Face con las herramientas y prompt dados.
    Usa STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION por defecto.
    """
    try:
        if agent_type is None:
            agent_type = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION

        base_llm = HuggingFaceEndpoint(
            repo_id=model_id,
            task=task,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
        )

        chat_llm = ChatHuggingFace(llm=base_llm)

        return initialize_agent(
            herramientas,
            chat_llm,
            agent=agent_type,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10,
            max_execution_time=60,
            agent_kwargs={"prompt": prompt},
            **kwargs,
        )

    except Exception as e:
        logger.error(f"Error al inicializar agente Hugging Face: {e}")
        return None
