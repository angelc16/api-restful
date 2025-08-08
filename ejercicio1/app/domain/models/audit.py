from sqlalchemy import Column, String, Integer, Text
from .base import BaseModel

class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    entity_id = Column(Integer, nullable=False)
    entity_type = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    previous_state = Column(Text, nullable=True)
    current_state = Column(Text, nullable=True)
