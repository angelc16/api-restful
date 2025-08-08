from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.product import Product



class IProductRepository(ABC):
    @abstractmethod
    async def create(self, product: dict, user_id: int) -> Product:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    async def update(self, product_id: int, product: dict, user_id: int) -> Product:
        pass

    @abstractmethod
    async def delete(self, product_id: int, user_id: int) -> bool:
        pass
