from sqlalchemy import Column, String
from .base import BaseModel

class Customer(BaseModel):
    __tablename__ = "customers"

    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    address = Column(String(500))
    tax_id = Column(String(50), unique=True)
