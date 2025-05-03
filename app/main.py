from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import FoodTruck
from app.routers import foodtrucks

app = FastAPI(title="SF Food Trucks API", version="0.0.1")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

# Add a middleware to handle CORS headers for all responses
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

app.include_router(foodtrucks.router) # register router

# Basic route to check if the app is running
@app.get("/ping")
async def ping() -> dict[str, str]:
    """
    Liveness probe.
    Returns 'pong!' to confirm the app is responsive.
    """
    return {"message": "pong!"}

# Route to check if the database connection works
@app.get("/db-health")
async def db_health(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Simple query to confirm we can talk to Postgres."""
    async with db as session:
        # Run a simple SQL query to make sure the DB is reachable
        result = await session.execute(text("SELECT 'ok'"))
        return {"db": result.scalar_one()} # Should return: {"db": "ok"}

# Route to count the number of rows in the FoodTruck table
@app.get("/count")
async def count(db: AsyncSession = Depends(get_db)) -> dict[str, int]:
    """Count the number of rows in the food_trucks table."""
    async with db as session:
        result = await session.execute(select(func.count()).select_from(FoodTruck))
        return {"rows": result.scalar_one()} # Should return: {"rows": 488}