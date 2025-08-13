from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FoodBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str

class FoodCreate(FoodBase):
    pass

class FoodUpdate(FoodBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

class FoodResponse(FoodBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
