from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.audit_service import IAuditService
from app.domain.interfaces.food_repository import IFoodRepository
from app.domain.models.user import User
from app.domain.services.oauth2 import get_current_user
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.food_repository import SQLFoodRepository
from app.infrastructure.services.audit_service import SQLAuditService


# Services
def get_audit_service(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> IAuditService:
    return SQLAuditService(session)

# Repositories
def get_food_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
    audit_service: Annotated[IAuditService, Depends(get_audit_service)]
) -> IFoodRepository:
    return SQLFoodRepository(session, audit_service)

# Type hints
CurrentUser = Annotated[User, Depends(get_current_user)]
FoodRepositoryDep = Annotated[IFoodRepository, Depends(get_food_repository)]
AuditServiceDep = Annotated[IAuditService, Depends(get_audit_service)]
