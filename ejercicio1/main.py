
from fastapi import FastAPI

from api.routers import customer, product
from app.infrastructure.database.connection import Base, engine

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(
    title="API REST Exercise 1",
    description="API REST para gestión de productos y clientes",
    version="1.0.0",
)


app.include_router(product.router, prefix="/api/v1/products", tags=["products"])
app.include_router(customer.router, prefix="/api/v1/customers", tags=["customers"])

@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
