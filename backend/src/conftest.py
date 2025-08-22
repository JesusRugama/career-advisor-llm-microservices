import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import pool
from httpx import AsyncClient, ASGITransport
from alembic import command, config, context  # Import Alembic for programmatic runs
from main import app  # Import your FastAPI app
from database import Base, get_db  # Import your DB base and dependency
import os

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/career_advisor_test"
)

engine = create_async_engine(TEST_DATABASE_URL, echo=True)  # echo for debugging
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

def run_migrations_sync(alembic_cfg):
    """Run Alembic migrations using standard sync approach."""
    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Migration error: {e}")
        raise

# Helper to get Alembic config (adapt if multi-domain; e.g., loop over domain migration paths)
def get_alembic_config():
    alembic_cfg = config.Config("alembic.ini")  # Or path to your alembic.ini
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    return alembic_cfg


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    alembic_cfg = get_alembic_config()
    run_migrations_sync(alembic_cfg)
    yield engine
    command.downgrade(alembic_cfg, "base")

# Function-scoped fixture: Provide session with nested transaction for rollback
@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    connection = await db_engine.connect()
    transaction = await connection.begin_nested()
    session = TestingSessionLocal(bind=connection)
    yield session
    await session.close()
    await transaction.rollback()
    await connection.close()

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()