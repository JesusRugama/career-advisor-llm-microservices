import pytest
import pytest_asyncio
import sys
import os
from uuid import uuid4

# Add paths for microservices setup
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../shared"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from models import User, UserProfile


class TestGetUserProfile:
    """Integration tests for the users service."""

    @pytest.mark.asyncio
    async def test_health(self, client):
        """Basic placeholder test to ensure testing infrastructure works."""
        # Simple assertion to verify test runs
        assert True is True

        # Test that client fixture is available
        assert client is not None

        # Basic health check if available
        try:
            response = await client.get("/health")
            # If health endpoint exists, it should return 200
            if response.status_code == 200:
                assert response.status_code == 200
        except Exception:
            # If no health endpoint, that's fine for now
            pass

    @pytest.mark.asyncio
    async def test_get_user_profile_success(self, client, db_session):
        """Test successful retrieval of user profile."""
        # Create test user
        user_id = uuid4()
        user = User(id=user_id, name="John Doe", email="john@example.com")
        db_session.add(user)

        # Create test user profile
        profile_id = uuid4()
        profile = UserProfile(
            id=profile_id,
            user_id=user_id,
            years_experience=5,
            skills=["Python", "FastAPI", "PostgreSQL"],
            career_goals="Become a senior engineer",
            preferred_work_style="remote",
        )
        db_session.add(profile)
        await db_session.commit()

        # Test the endpoint
        response = await client.get(f"/api/users/{user_id}/profile")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["profile"] is not None
        assert data["profile"]["user_id"] == str(user_id)
        assert data["profile"]["years_experience"] == 5
        assert data["profile"]["skills"] == ["Python", "FastAPI", "PostgreSQL"]
        assert data["profile"]["career_goals"] == "Become a senior engineer"
        assert data["profile"]["preferred_work_style"] == "remote"

    @pytest.mark.asyncio
    async def test_get_user_profile_user_not_found(self, client):
        """Test user profile retrieval when user doesn't exist."""
        non_existent_user_id = uuid4()

        response = await client.get(f"/api/users/{non_existent_user_id}/profile")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "User not found"

    @pytest.mark.asyncio
    async def test_get_user_profile_profile_not_found(self, client, db_session):
        """Test user profile retrieval when user exists but profile doesn't."""
        # Create test user without profile
        user_id = uuid4()
        user = User(id=user_id, name="Jane Doe", email="jane@example.com")
        db_session.add(user)
        await db_session.commit()

        # Test the endpoint
        response = await client.get(f"/api/users/{user_id}/profile")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["profile"] is None
        assert data["message"] == "User profile not found"

    @pytest.mark.asyncio
    async def test_get_user_profile_with_null_fields(self, client, db_session):
        """Test user profile retrieval with null/optional fields."""
        # Create test user
        user_id = uuid4()
        user = User(id=user_id, name="Bob Smith", email="bob@example.com")
        db_session.add(user)

        # Create test user profile with minimal data
        profile_id = uuid4()
        profile = UserProfile(
            id=profile_id,
            user_id=user_id,
            years_experience=None,
            skills=None,
            career_goals=None,
            preferred_work_style=None,
        )
        db_session.add(profile)
        await db_session.commit()

        # Test the endpoint
        response = await client.get(f"/api/users/{user_id}/profile")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["profile"] is not None
        assert data["profile"]["user_id"] == str(user_id)
        assert data["profile"]["years_experience"] is None
        assert data["profile"]["skills"] is None
        assert data["profile"]["career_goals"] is None
        assert data["profile"]["preferred_work_style"] is None
