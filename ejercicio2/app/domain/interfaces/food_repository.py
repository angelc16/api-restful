from typing import Protocol, List, Optional
from app.domain.models.food import Food

class IFoodRepository(Protocol):
    async def create(self, food: dict, user_id: int) -> Food:
        ...

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Food]:
        ...

    async def get_by_id(self, food_id: int) -> Optional[Food]:
        ...

    async def update(self, food_id: int, food_data: dict, user_id: int) -> Food:
        ...

    async def delete(self, food_id: int, user_id: int) -> bool:
        ...
