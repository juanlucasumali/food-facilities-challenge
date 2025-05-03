import asyncio, sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.models import Base
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an async database engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Async function to initialize the database
async def run():
    async with engine.begin() as conn:
        # 1) Enable required Postgres extensions
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))  # For spatial/geographic features
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))  # For trigram indexing (fuzzy text search)

        # 2) Create tables and indexes defined in the SQLAlchemy models
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run())
