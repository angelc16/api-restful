from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

from api.routers import customer as customer_r, product as product_r
from app.infrastructure.database.connection import create_tables
from api.middleware.exception_handler import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(
    lifespan=lifespan,
    title="API REST Exercise 1",
    description="API REST para gestión de productos y clientes",
    version="1.0.0",
)
register_exception_handlers(app)

app.include_router(product_r.router, prefix="/api/v1/products", tags=["products"])
app.include_router(customer_r.router, prefix="/api/v1/customers", tags=["customers"])

@app.get("/health")
async def health_check(): return {"status": "healthy"}

