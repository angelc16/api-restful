from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.infrastructure.database.connection import Base

class Audit(Base):
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
