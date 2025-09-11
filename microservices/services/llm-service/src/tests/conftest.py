import sys
import os

# Add shared directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../shared"))
# Add current directory to path for local imports (src directory)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import pool
from httpx import AsyncClient, ASGITransport
from alembic import command, config, context  # Import Alembic for programmatic runs
from main import app  # Import your FastAPI app
from database import Base, get_db  # Import your DB base and dependency

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/career_advisor_test",
)

engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,  # echo for debugging
    poolclass=pool.NullPool,  # Disable connection pooling to avoid conflicts
    future=True,
)
TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


def run_migrations_sync(alembic_cfg):
    """Run Alembic migrations using standard sync approach."""
    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Migration error: {e}")
        raise


# Helper to get Alembic config for llm service
def get_alembic_config():
    # Path to alembic.ini in the llm service root directory
    # Go up from tests -> src -> llm-service root
    alembic_ini_path = os.path.join(os.path.dirname(__file__), "../../alembic.ini")
    alembic_cfg = config.Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    return alembic_cfg


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    alembic_cfg = get_alembic_config()
    run_migrations_sync(alembic_cfg)
    yield engine
    command.downgrade(alembic_cfg, "base")


# Function-scoped fixture: Provide session with fresh connection per test
@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    # Create a fresh connection for each test to avoid AsyncPG conflicts
    async with db_engine.connect() as conn:
        # Create session bound to this specific connection
        session_maker = async_sessionmaker(
            bind=conn, class_=AsyncSession, expire_on_commit=False
        )
        async with session_maker() as session:
            try:
                yield session
            finally:
                await session.rollback()  # Rollback any uncommitted changes


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()
