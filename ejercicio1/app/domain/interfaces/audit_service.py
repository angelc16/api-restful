from abc import ABC, abstractmethod
from typing import Optional

class IAuditService(ABC):
    @abstractmethod
    async def log_action(
        self,
        entity_id: int,
        entity_type: str,
        user_id: int,
        action: str,
        description: str,
        previous_state: Optional[str] = None,
        current_state: Optional[str] = None
    ) -> None:
        pass
