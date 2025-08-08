from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.customer import Customer


class ICustomerRepository(ABC):
    @abstractmethod
    async def create(self, customer: dict, user_id: int) -> Customer:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        pass

    @abstractmethod
    async def get_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    async def update(self, customer_id: int, customer: dict, user_id: int) -> Customer:
        pass

    @abstractmethod
    async def delete(self, customer_id: int, user_id: int) -> bool:
        pass
