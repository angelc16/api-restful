from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.domain.models.base import BaseModel


class Audit(BaseModel):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, nullable=False)
    entity_type = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    previous_state = Column(Text, nullable=True)
    current_state = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
