
from typing import List, Optional
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from sqlalchemy.orm import Session
from .connection import SessionLocal
from .models import ChatHistory
from app.core.logging import get_logger

logger = get_logger(__name__)

class PostgresTurnBasedHistory(BaseChatMessageHistory):
    def __init__(
        self,
        session_id: str,
        student_id: Optional[str] = None,
        email_usuario: Optional[str] = None,
        messages_limit: int = 10,
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
                rows = list(reversed(rows))
                
                messages = []
                for row in rows:
                    if row.system_prompt:
                        messages.append(SystemMessage(content=row.system_prompt))
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

    def add_message(self, message: BaseMessage) -> None:
        """Agrega un mensaje a la base de datos."""
        try:
            with SessionLocal() as db:
                try:
                    if isinstance(message, HumanMessage):
                        self._add_human_message(db, message)
                    elif isinstance(message, AIMessage):
                        self._add_ai_message(db, message)
                    elif isinstance(message, SystemMessage):
                        self._add_system_message(db, message)
                    else:
                        logger.warning(f"Tipo de mensaje no soportado explícitamente: {type(message)}")
                    
                    db.commit()
                except Exception as e:
                    db.rollback()
                    logger.error(f"Error guardando mensaje en historial: {e}")
        except Exception as e:
             logger.error(f"Error de conexión al guardar mensaje en historial: {e}")

    def _add_human_message(self, db: Session, message: HumanMessage):
        # Crear nueva fila para el turno
        chat_entry = ChatHistory(
            session_id=self.session_id,
            human_prompt=message.content,
            student_id=self.student_id,
            email_usuario=self.email_usuario,
        )
        db.add(chat_entry)

    def _add_ai_message(self, db: Session, message: AIMessage):
        # Buscar la última entrada de esta sesión que tenga human_prompt y le falte ai_response
        last_entry = (
            db.query(ChatHistory)
            .filter(ChatHistory.session_id == self.session_id)
            .order_by(ChatHistory.created_at.desc())
            .first()
        )

        if last_entry and last_entry.human_prompt and not last_entry.ai_response:
            # Completar el turno
            last_entry.ai_response = message.content
        else:
            # Caso raro AI habla primero o múltiples respuestas. Crear nueva fila.
            chat_entry = ChatHistory(
                session_id=self.session_id,
                ai_response=message.content,
                student_id=self.student_id,
                email_usuario=self.email_usuario,
            )
            db.add(chat_entry)

    def _add_system_message(self, db: Session, message: SystemMessage):
        # System message suele ir al principio o solo.
        chat_entry = ChatHistory(
            session_id=self.session_id,
            system_prompt=message.content,
            student_id=self.student_id,
            email_usuario=self.email_usuario,
        )
        db.add(chat_entry)

    def clear(self) -> None:
        """Borra el historial de la sesión."""
        with SessionLocal() as db:
            db.query(ChatHistory).filter(ChatHistory.session_id == self.session_id).delete()
            db.commit()
