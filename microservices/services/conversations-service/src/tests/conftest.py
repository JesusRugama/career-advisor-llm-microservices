import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
import sys
import os

# Add paths for microservices setup
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from main import app
from database import AsyncSessionLocal, engine, create_tables
from sqlalchemy.ext.asyncio import AsyncSession

@pytest_asyncio.fixture
async def client():
    """Create an async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac

@pytest_asyncio.fixture
async def db_session():
    """Create a database session for testing."""
    # Ensure tables exist
    await create_tables()
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Set up test database tables."""
    await create_tables()
    yield
    # Cleanup after all tests
    await engine.dispose()
