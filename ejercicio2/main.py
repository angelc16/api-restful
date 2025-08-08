import os

from api.routers import auth, food
from app.infrastructure.database.connection import Base, engine
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Create database tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(
    title="Food Service API",
    description="API REST protegida con OAuth2",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(food.router, prefix="/api/v1/foods", tags=["Foods"])

@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
