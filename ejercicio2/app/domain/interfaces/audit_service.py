from typing import Protocol, Optional

class IAuditService(Protocol):
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
        ...
