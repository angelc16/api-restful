from typing import List
from fastapi import APIRouter, HTTPException, status

from ..dependencies import CustomerRepositoryDep
from ..schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter()


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer: CustomerCreate,
    user_id: int = 1,
    customer_repository: CustomerRepositoryDep = None,
):
    created_customer = await customer_repository.create(customer.dict(), user_id)
    return CustomerResponse.model_validate(created_customer)


@router.get("/", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = 0, limit: int = 100, customer_repository: CustomerRepositoryDep = None
):
    return await customer_repository.get_all(skip, limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int, customer_repository: CustomerRepositoryDep = None
):
    customer = await customer_repository.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    user_id: int = 1,
    customer_repository: CustomerRepositoryDep = None,
):
    return await customer_repository.update(
        customer_id, customer.dict(exclude_unset=True), user_id
    )


@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: int,
    user_id: int = 1,
    customer_repository: CustomerRepositoryDep = None,
):
    if await customer_repository.delete(customer_id, user_id):
        return {"message": "Customer deleted successfully"}
