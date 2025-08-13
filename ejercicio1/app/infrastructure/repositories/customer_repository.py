from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.customer import Customer

from ...domain.interfaces.audit_service import IAuditService
from ...domain.interfaces.customer_repository import ICustomerRepository

class SQLCustomerRepository(ICustomerRepository):
    def __init__(self, session: AsyncSession, audit_service: IAuditService):
        self.session = session
        self.audit_service = audit_service

    async def create(self, customer: dict, user_id: int) -> Customer:
        db_customer = Customer(**customer)
        self.session.add(db_customer)
        await self.session.flush()

        await self.audit_service.log_action(
            entity_id=db_customer.id,
            entity_type="Customer",
            user_id=user_id,
            action="CREATE",
            description=f"Created customer {db_customer.name}",
            current_state=str(customer)
        )

        await self.session.commit()
        await self.session.refresh(db_customer)
        return db_customer

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        result = await self.session.execute(
            select(Customer)
            .filter(Customer.is_active)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, customer_id: int) -> Optional[Customer]:
        result = await self.session.execute(
            select(Customer)
            .filter(Customer.id == customer_id, Customer.is_active)
        )
        return result.scalar_one_or_none()

    async def update(
        self,
        customer_id: int,
        customer_data: dict,
        user_id: int
    ) -> Customer:
        db_customer = await self.get_by_id(customer_id)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        previous_state = str(db_customer.__dict__)

        customer_data.pop("email", None)
        for key, value in customer_data.items():
            setattr(db_customer, key, value)

        await self.audit_service.log_action(
            entity_id=customer_id,
            entity_type="Customer",
            user_id=user_id,
            action="UPDATE",
            description=f"Updated customer {db_customer.name}",
            previous_state=previous_state,
            current_state=str(db_customer.__dict__)
        )

        await self.session.commit()
        await self.session.refresh(db_customer)
        return db_customer

    async def delete(self, customer_id: int, user_id: int) -> bool:
        db_customer = await self.get_by_id(customer_id)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        previous_state = str(db_customer.__dict__)
        db_customer.is_active = False

        await self.audit_service.log_action(
            entity_id=customer_id,
            entity_type="Customer",
            user_id=user_id,
            action="DELETE",
            description=f"Deleted customer {db_customer.name}",
            previous_state=previous_state,
            current_state=str(db_customer.__dict__)
        )

        await self.session.commit()
        return True
