from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db

app = FastAPI(title="SF Food Trucks API", version="0.0.1")

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