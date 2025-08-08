from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.audit_service import IAuditService
from app.domain.interfaces.customer_repository import ICustomerRepository
from app.domain.interfaces.product_repository import IProductRepository
# from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.customer_repository import SQLCustomerRepository
from app.infrastructure.repositories.product_repository import SQLProductRepository
from app.infrastructure.services.audit_service import SQLAuditService
from app.infrastructure.database.connection import get_db

# Services
def get_audit_service(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> IAuditService:
    return SQLAuditService(session)

# Repositories
def get_product_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
    audit_service: Annotated[IAuditService, Depends(get_audit_service)]
) -> IProductRepository:
    return SQLProductRepository(session, audit_service)

def get_customer_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
    audit_service: Annotated[IAuditService, Depends(get_audit_service)]
) -> ICustomerRepository:
    return SQLCustomerRepository(session, audit_service)

# Type hints
AuditServiceDep = Annotated[IAuditService, Depends(get_audit_service)]
ProductRepositoryDep = Annotated[IProductRepository, Depends(get_product_repository)]
CustomerRepositoryDep = Annotated[ICustomerRepository, Depends(get_customer_repository)]
