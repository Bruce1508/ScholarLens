"""
API Log model
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from config.database import Base


class APILog(Base):
    """
    API request/response logs
    Tracks Claude API calls for debugging and analytics
    """
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(100))
    prompt_type = Column(String(50))  # 'persona_builder', 'essay_generator', etc.
    request_payload = Column(JSONB)
    response_payload = Column(JSONB)
    tokens_used = Column(Integer)
    latency_ms = Column(Integer)
    status = Column(String(20))  # 'success', 'error', 'timeout'
    error_message = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<APILog(id={self.id}, prompt_type='{self.prompt_type}', status='{self.status}')>"
