from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..dependencies import get_food_repository, get_current_user
from ..schemas.food import FoodCreate, FoodUpdate, FoodResponse

router = APIRouter()

@router.post("/", response_model=FoodResponse)
async def create_food(
    food: FoodCreate,
    food_repository = Depends(get_food_repository),
    current_user = Depends(get_current_user)
):
    return await food_repository.create(food.dict(), current_user.id)

@router.get("/", response_model=List[FoodResponse])
async def get_foods(
    skip: int = 0,
    limit: int = 100,
    food_repository = Depends(get_food_repository),
    current_user = Depends(get_current_user)
):
    return await food_repository.get_all(skip, limit)

@router.get("/{food_id}", response_model=FoodResponse)
async def get_food(
    food_id: int,
    food_repository = Depends(get_food_repository),
    current_user = Depends(get_current_user)
):
    food = await food_repository.get_by_id(food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    return food

@router.put("/{food_id}", response_model=FoodResponse)
async def update_food(
    food_id: int,
    food: FoodUpdate,
    food_repository = Depends(get_food_repository),
    current_user = Depends(get_current_user)
):
    return await food_repository.update(food_id, food.dict(), current_user.id)

@router.delete("/{food_id}")
async def delete_food(
    food_id: int,
    food_repository = Depends(get_food_repository),
    current_user = Depends(get_current_user)
):
    if await food_repository.delete(food_id, current_user.id):
        return {"message": "Food deleted successfully"}
