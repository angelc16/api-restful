from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.audit_service import IAuditService
from app.domain.interfaces.food_repository import IFoodRepository
from app.domain.models.food import Food

class SQLFoodRepository(IFoodRepository):
    def __init__(self, session: AsyncSession, audit_service: IAuditService):
        self.session = session
        self.audit_service = audit_service

    async def create(self, food: dict, user_id: int) -> Food:
        db_food = Food(**food)
        self.session.add(db_food)
        await self.session.flush()

        await self.audit_service.log_action(
            entity_id=db_food.id,
            entity_type="Food",
            user_id=user_id,
            action="CREATE",
            description=f"Created food {db_food.name}",
            current_state=str(food)
        )

        await self.session.commit()
        await self.session.refresh(db_food)
        return db_food

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Food]:
        result = await self.session.execute(
            select(Food)
            .filter(Food.is_active)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, food_id: int) -> Optional[Food]:
        result = await self.session.execute(
            select(Food)
            .filter(Food.id == food_id, Food.is_active)
        )
        return result.scalar_one_or_none()

    async def update(self, food_id: int, food_data: dict, user_id: int) -> Food:
        db_food = await self.get_by_id(food_id)
        if not db_food:
            raise HTTPException(status_code=404, detail="Food not found")

        previous_state = str(db_food.__dict__)

        for key, value in food_data.items():
            setattr(db_food, key, value)

        await self.audit_service.log_action(
            entity_id=food_id,
            entity_type="Food",
            user_id=user_id,
            action="UPDATE",
            description=f"Updated food {db_food.name}",
            previous_state=previous_state,
            current_state=str(db_food.__dict__)
        )

        await self.session.commit()
        await self.session.refresh(db_food)
        return db_food

    async def delete(self, food_id: int, user_id: int) -> bool:
        db_food = await self.get_by_id(food_id)
        if not db_food:
            raise HTTPException(status_code=404, detail="Food not found")

        previous_state = str(db_food.__dict__)
        db_food.is_active = False

        await self.audit_service.log_action(
            entity_id=food_id,
            entity_type="Food",
            user_id=user_id,
            action="DELETE",
            description=f"Deleted food {db_food.name}",
            previous_state=previous_state,
            current_state=str(db_food.__dict__)
        )

        await self.session.commit()
        return True
