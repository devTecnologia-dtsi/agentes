"""Inicializador de agente Gemini usando LangChain moderno (create_tool_calling_agent)."""

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

def inicializar_agente_gemini(herramientas, prompt, **kwargs):
    """Crea un agente Gemini con las herramientas y prompt dados.

    Args:
        herramientas: Lista de herramientas de LangChain.
        prompt: Prompt base (system prompt) para orientar al agente.
        **kwargs: Argumentos adicionales (ignorados por compatibilidad).

    Returns:
        AgentExecutor configurado con herramientas y memoria automática.
    """
    try:
        # Crear modelo con configuración explícita
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_output_tokens=2048,
            google_api_key=settings.GOOGLE_API_KEY
        )

        # Crear template de prompt con soporte de historial de conversación
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Crear agente con herramientas (create_tool_calling_agent es moderno y compatible)
        agent = create_tool_calling_agent(
            llm=llm,
            tools=herramientas,
            prompt=prompt_template
        )

        # Envolver en AgentExecutor para manejo automático de memoria y ejecución
        agente_executor = AgentExecutor(
            agent=agent,
            tools=herramientas,
            verbose=True,
            max_iterations=15,  # Gemini puede necesitar más iteraciones
            max_execution_time=60,
            handle_parsing_errors=True,
            return_intermediate_steps=False
        )

        logger.info("Agente Gemini inicializado correctamente con create_tool_calling_agent")
        return agente_executor

    except Exception as e:
        logger.error(f"Error al inicializar agente Gemini: {e}", exc_info=True)
        raise e