import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the async SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create a session factory that makes async sessions from the engine
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    """Base class for ORM models."""
    pass

# This function is used in FastAPI to get a database session
@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI that provides a database session.
    It opens a session and automatically closes it when done.
    """
    async with AsyncSessionLocal() as session:
        yield session
