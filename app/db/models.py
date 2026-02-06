from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.connection import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)  # uuid_request
    human_prompt = Column(Text, nullable=True)
    ai_response = Column(Text, nullable=True)
    system_prompt = Column(Text, nullable=True)
    student_id = Column(String, nullable=True)
    email_usuario = Column(String, nullable=True)
    agent = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
