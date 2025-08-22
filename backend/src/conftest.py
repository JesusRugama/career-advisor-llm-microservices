import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
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

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Session-scoped fixture: Run migrations once, drop at end
@pytest.fixture(scope="session")
def db_engine():
    # Set up Alembic configuration for test database
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    
    # Run migrations to create schema
    command.upgrade(alembic_cfg, "head")
    
    yield engine
    
    # Clean up after all tests - drop all tables
    Base.metadata.drop_all(bind=engine)


# Function-scoped fixture: Provide session with rollback for isolation
@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    # Rollback changes to ensure test isolation
    session.close()
    transaction.rollback()
    connection.close()


# Fixture for TestClient with DB override
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Session cleanup handled by db_session fixture

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
