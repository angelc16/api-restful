from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_product_repository
from ..schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()

ProductRepository = Annotated[
    type(get_product_repository),
    Depends(get_product_repository)
]

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    user_id: int = 1,
    product_repository: ProductRepository = None
):
    return await product_repository.create(product.dict(), user_id)

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    product_repository: ProductRepository = None
):
    return await product_repository.get_all(skip, limit)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    product_repository: ProductRepository = None
):
    product = await product_repository.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    user_id: int = 1,
    product_repository: ProductRepository = None
):
    return await product_repository.update(
        product_id,
        product.dict(exclude_unset=True),
        user_id
    )

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    user_id: int = 1,
    product_repository: ProductRepository = None
):
    if await product_repository.delete(product_id, user_id):
        return {"message": "Product deleted successfully"}
