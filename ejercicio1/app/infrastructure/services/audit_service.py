from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.audit import AuditLog

from ...domain.interfaces.audit_service import IAuditService


class SQLAuditService(IAuditService):
    def __init__(self, session: AsyncSession):
        self.session = session

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
        audit = AuditLog(
            entity_id=entity_id,
            entity_type=entity_type,
            user_id=user_id,
            action=action,
            description=description,
            previous_state=previous_state,
            current_state=current_state
        )
        self.session.add(audit)
        await self.session.commit()
