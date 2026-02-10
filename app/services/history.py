"""
Servicio de Historial de Chat (PostgreSQL)

Responsabilidad:
    Actuar como adaptador entre la interfaz de historial de LangChain (BaseChatMessageHistory)
    y la persistencia en base de datos PostgreSQL de la aplicación.
    Gestiona la recuperación y almacenamiento de mensajes de chat (Human, AI, System)
    respetando el modelo de datos definido en app.db.models.

Uso:
    Este servicio es consumido principalmente por los agentes para mantener el contexto de la conversación.
"""

from typing import List, Optional
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from sqlalchemy.orm import Session
from app.db.connection import SessionLocal
from app.db.models import ChatHistory
from app.core.logging import get_logger

logger = get_logger(__name__)

# Clase base de LangChain que define cómo deben comportarse todos los historiales
class PostgresTurnBasedHistory(BaseChatMessageHistory):
    def __init__(
        self,
        session_id: str,
        student_id: Optional[str] = None,
        email_usuario: Optional[str] = None,
        messages_limit: int = 10, # Límite de mensajes a recuperar
    ):
        self.session_id = session_id
        self.student_id = student_id
        self.email_usuario = email_usuario
        self.messages_limit = messages_limit

    @property
    def messages(self) -> List[BaseMessage]:
        """Retorna la lista de mensajes (System, Human, AI) reconstruida desde la DB."""
        try:
            with SessionLocal() as db:
                # Obtener los últimos N registros ordenados por fecha descendente
                rows = (
                    db.query(ChatHistory)
                    .filter(ChatHistory.session_id == self.session_id)
                    .order_by(ChatHistory.created_at.desc())
                    .limit(self.messages_limit)
                    .all()
                )
                
                # Invertir para tener orden cronológico (antiguo -> nuevo)
                # rows es una lista, así que reversed devuelve un iterador, se convierte en lista y se itera directo
                rows = list(reversed(rows))
                
                messages = []
                for row in rows:
                    # System prompt se ignora al recuperar para no duplicar contexto
                    # if row.system_prompt:
                    #     messages.append(SystemMessage(content=row.system_prompt))
                    if row.human_prompt:
                        messages.append(HumanMessage(content=row.human_prompt))
                    if row.ai_response:
                        messages.append(AIMessage(content=row.ai_response))
                
                # Loguear el historial recuperado
                logger.info(f"--- HISTORIAL DE SESION {self.session_id} ---")
                logger.info(f"Se recuperaron {len(messages)} mensajes (Límite: {self.messages_limit}).")
                for i, msg in enumerate(messages):
                    content_preview = msg.content
                    logger.info(f"[{i}] {msg.type}: {content_preview}")
                logger.info("---------------------------------------------")

                return messages
        except Exception as e:
            logger.error(f"Error recuperando historial (continuando sin historial): {e}")
            return []

    def clear(self) -> None:
        """Borra el historial de la sesión (Requerido por BaseChatMessageHistory)."""
        # Por seguridad y auditoría, decidimos NO borrar físicamente el historial de la BD.
        # Esta función debe existir para cumplir con la clase abstracta, pero no hace nada.
        pass

    def add_interaction(
        self,
        human_msg: str,
        ai_msg: str,
        system_msg: Optional[str] = None,
        agent_name: Optional[str] = None
    ) -> None:
        """Agrega una interacción completa a la base de datos."""
        # toma el mensaje del usuario ( human_msg ), 
        # la respuesta de la IA ( ai_msg ), 
        # el system prompt usado ( system_msg ) 
        # y el nombre del agente ( agent_name ) y crea un registro nuevo.
        try:
            with SessionLocal() as db:
                chat_entry = ChatHistory(
                    session_id=self.session_id,
                    human_prompt=human_msg,
                    ai_response=ai_msg,
                    system_prompt=system_msg,
                    student_id=self.student_id,
                    email_usuario=self.email_usuario,
                    agent=agent_name
                )
                db.add(chat_entry)
                db.commit()
        except Exception as e:
            logger.error(f"Error guardando interacción en historial: {e}")

    # Método requerido por la clase base BaseChatMessageHistory de LangChain
    # Se mantiene por compatibilidad, pero internamente redirige a add_interaction si es posible,
    # o implementa una lógica simplificada para mensajes sueltos.
    def add_message(self, message: BaseMessage) -> None:
        """Agrega un mensaje a la base de datos (Compatibilidad LangChain)."""
        # Nota: En nuestro flujo principal usamos add_interaction para guardar pares completos.
        # Este método solo se llamaría si alguna herramienta interna de LangChain intenta guardar algo.
        try:
            if isinstance(message, HumanMessage):
                # Si llega un mensaje humano suelto, lo guardamos como inicio de interacción
                self.add_interaction(human_msg=message.content, ai_msg=None)
            elif isinstance(message, AIMessage):
                # Si llega un mensaje de IA suelto, intentamos actualizar el último registro
                # (Lógica simplificada de compatibilidad)
                with SessionLocal() as db:
                    last_entry = (
                        db.query(ChatHistory)
                        .filter(
                            ChatHistory.session_id == self.session_id,
                            ChatHistory.human_prompt.isnot(None),
                            ChatHistory.ai_response.is_(None)
                        )
                        .order_by(ChatHistory.created_at.desc())
                        .first()
                    )
                    if last_entry:
                        last_entry.ai_response = message.content
                        db.commit()
                    else:
                        # Si no hay hueco, guardamos como respuesta huérfana
                        self.add_interaction(human_msg=None, ai_msg=message.content)
            elif isinstance(message, SystemMessage):
                # Guardamos system message suelto
                self.add_interaction(human_msg=None, ai_msg=None, system_msg=message.content)
            else:
                logger.warning(f"Tipo de mensaje no soportado explícitamente en add_message: {type(message)}")
        except Exception as e:
             logger.error(f"Error en add_message (compatibilidad): {e}")
