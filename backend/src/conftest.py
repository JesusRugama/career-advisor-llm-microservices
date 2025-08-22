import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from httpx import AsyncClient
from alembic.config import Config
from alembic import command
import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from main import app  # Import your FastAPI app
from database import get_db  # Import your DB dependency
from models.base import Base  # Import your DB base

# Use PostgreSQL for testing - same as production
# Allow override via environment variable
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/career_advisor_test"
)

# For migrations (sync)
sync_engine = create_engine(TEST_DATABASE_URL)

# For async operations (app and tests)
async_engine = create_async_engine(TEST_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))

# Use async sessions for testing
TestingSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Session-scoped fixture: Run migrations once, drop at end
@pytest.fixture(scope="session")
def db_engine():
    # Set up Alembic configuration for test database
    # Get the absolute path to the backend directory (where alembic.ini is located)
    backend_dir = os.path.dirname(os.path.dirname(__file__))  # Go up from src/ to backend/
    alembic_ini_path = os.path.join(backend_dir, "alembic.ini")

    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    # Set the correct path to the migrations folder
    migrations_dir = os.path.join(backend_dir, "migrations")
    alembic_cfg.set_main_option("script_location", migrations_dir)

    try:
        # Check current migration state
        from alembic.runtime import migration
        with sync_engine.connect() as conn:
            context = migration.MigrationContext.configure(conn)
            current_rev = context.get_current_revision()
            print(f"DEBUG: Current migration revision: {current_rev}")

        # If there's a migration state but no tables, reset and start fresh
        if current_rev is not None:
            print("DEBUG: Found existing migration state, dropping all tables and resetting...")
            Base.metadata.drop_all(bind=sync_engine)
            # Reset migration state to start from scratch
            command.stamp(alembic_cfg, "base")

        # Run migrations to create schema
        print(f"DEBUG: Running migrations to: {TEST_DATABASE_URL}")
        command.upgrade(alembic_cfg, "head")
        print("DEBUG: Migrations completed successfully")

        # Check final migration state
        with sync_engine.connect() as conn:
            context = migration.MigrationContext.configure(conn)
            final_rev = context.get_current_revision()
            print(f"DEBUG: Final migration revision: {final_rev}")

    except Exception as e:
        print(f"DEBUG: Migration failed with error: {e}")
        raise

    yield async_engine

    # Clean up after all tests - drop all tables
    Base.metadata.drop_all(bind=sync_engine)


# Function-scoped fixture: Provide async session with rollback for isolation
@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    # Create a fresh session for each test
    async with TestingSessionLocal() as session:
        yield session
        # Session cleanup happens automatically with context manager


# Fixture for AsyncClient with DB override
@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    from httpx import ASGITransport

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
