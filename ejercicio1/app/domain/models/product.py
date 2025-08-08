from sqlalchemy import Column, Integer, String, Float
from .base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String(255), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    sku = Column(String(50), unique=True)
    stock = Column(Integer, default=0)
