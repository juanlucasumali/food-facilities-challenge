import os, pytest_asyncio, pytest
import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from httpx import AsyncClient
from httpx import ASGITransport
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, get_db
from app.models import FoodTruck

DATABASE_URL = os.getenv("DATABASE_URL")

# Create a new engine for each test
@pytest_asyncio.fixture
async def engine():
    eng = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)

    # Create the extensions and tables
    async with eng.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()

# Create a new DB session for each test
@pytest_asyncio.fixture
async def db_session(engine) -> AsyncSession:
    connection = await engine.connect()
    await connection.begin()
    
    # Create a session bound to this connection
    Session = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
    session = Session()
    
    # Begin a nested transaction
    trans = await connection.begin_nested()
    
    # Yield the session
    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.rollback()
        await connection.close()

# Create a new FastAPI test client for each test
@pytest_asyncio.fixture
async def client(db_session):
    async def _override():
        yield db_session

    # Override the get_db dependency to use the new DB session
    app.dependency_overrides[get_db] = _override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac:
        yield ac
    app.dependency_overrides.clear()
