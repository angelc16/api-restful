from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.audit_service import IAuditService
from app.domain.interfaces.food_repository import IFoodRepository
from app.domain.models.user import User
from app.domain.services.oauth2 import SECRET_KEY, ALGORITHM
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.food_repository import SQLFoodRepository
from app.infrastructure.services.audit_service import SQLAuditService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None:
            raise credentials_exception
        # En un entorno real, aquí consultarías la base de datos
        # para obtener el usuario completo. Por ahora retornamos
        # un usuario básico con el ID del cliente
        return User(id=1, client_id=client_id)
    except JWTError:
        raise credentials_exception

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

# Type hints for cleaner router signatures
CurrentUser = Annotated[User, Depends(get_current_user)]
FoodRepositoryDep = Annotated[IFoodRepository, Depends(get_food_repository)]
AuditServiceDep = Annotated[IAuditService, Depends(get_audit_service)]
