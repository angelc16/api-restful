from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy import select
from ...domain.interfaces.product_repository import IProductRepository
from ...domain.interfaces.audit_service import IAuditService
from app.domain.models.product import Product

class SQLProductRepository(IProductRepository):
    def __init__(self, session: AsyncSession, audit_service: IAuditService):
        self.session = session
        self.audit_service = audit_service

    async def create(self, product: dict, user_id: int) -> Product:
        db_product = Product(**product)
        self.session.add(db_product)
        await self.session.flush()
        await self.audit_service.log_action(
            entity_id=db_product.id,
            entity_type="Product",
            user_id=user_id,
            action="CREATE",
            description=f"Created product {db_product.name}",
            current_state=str(product),
        )

        await self.session.commit()
        await self.session.refresh(db_product)
        return db_product

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        result = await self.session.execute(
            select(Product).filter(Product.is_active).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.session.execute(
            select(Product).filter(Product.id == product_id, Product.is_active)
        )
        return result.scalar_one_or_none()

    async def update(
        self, product_id: int, product_data: dict, user_id: int
    ) -> Product:
        db_product = await self.get_by_id(product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        previous_state = str(db_product.__dict__)

        for key, value in product_data.items():
            setattr(db_product, key, value)

        await self.audit_service.log_action(
            entity_id=product_id,
            entity_type="Product",
            user_id=user_id,
            action="UPDATE",
            description=f"Updated product {db_product.name}",
            previous_state=previous_state,
            current_state=str(db_product.__dict__),
        )

        await self.session.commit()
        await self.session.refresh(db_product)
        return db_product

    async def delete(self, product_id: int, user_id: int) -> bool:
        db_product = await self.get_by_id(product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        previous_state = str(db_product.__dict__)
        db_product.is_active = False

        await self.audit_service.log_action(
            entity_id=product_id,
            entity_type="Product",
            user_id=user_id,
            action="DELETE",
            description=f"Deleted product {db_product.name}",
            previous_state=previous_state,
            current_state=str(db_product.__dict__),
        )

        await self.session.commit()
        return True
