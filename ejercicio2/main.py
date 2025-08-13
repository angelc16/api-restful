from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from api.routers import auth, food
from app.infrastructure.database.connection import create_tables

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(
    title="Food Service API",
    lifespan=lifespan,
    description="API REST protegida con OAuth2",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(food.router, prefix="/api/v1/foods", tags=["Foods"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
