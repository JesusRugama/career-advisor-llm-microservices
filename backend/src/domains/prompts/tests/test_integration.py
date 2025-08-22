import pytest
import pytest_asyncio
from uuid import uuid4
import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from domains.prompts.models import Prompt

# Fixtures are automatically discovered from conftest.py
# No need to import client, db_session - pytest will find them

class TestPromptsIntegration:
    """Integration tests for the prompts domain using real database."""

    @pytest.mark.asyncio
    async def test_get_prompts_with_seed_data(self, client):
        """Test GET /api/prompts with seed data from migrations."""
        response = await client.get("/api/prompts")
        
        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert len(data["prompts"]) == 6  # Should have 6 seed prompts
        
        # Verify seed prompt titles are present
        titles = [p["title"] for p in data["prompts"]]
        expected_titles = [
            "Career Path Guidance",
            "Skill Development", 
            "Leadership Transition",
            "Industry Trends",
            "Salary Negotiation",
            "Work-Life Balance"
        ]
        
        for title in expected_titles:
            assert title in titles

    @pytest.mark.asyncio
    async def test_get_prompts_with_data(self, client, db_session):
        """Test GET /api/prompts with prompts in database."""
        # Create test prompts
        prompt1 = Prompt(
            id=uuid4(),
            title="Career Path Guidance",
            prompt_text="What are the best career paths for someone with my skills?",
            category="career",
            is_active=True
        )
        prompt2 = Prompt(
            id=uuid4(),
            title="Skill Development",
            prompt_text="What skills should I focus on developing next?",
            category="skills",
            is_active=True
        )
        prompt3 = Prompt(
            id=uuid4(),
            title="Inactive Prompt",
            prompt_text="This should not appear",
            category="test",
            is_active=False
        )

        # Add to database
        db_session.add(prompt1)
        db_session.add(prompt2)
        db_session.add(prompt3)
        await db_session.commit()

        # Test the endpoint
        response = await client.get("/api/prompts")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert len(data["prompts"]) == 2  # Only active prompts

        # Check prompt structure
        for prompt in data["prompts"]:
            assert "id" in prompt
            assert "title" in prompt
            assert "prompt_text" in prompt
            assert isinstance(prompt["title"], str)
            assert isinstance(prompt["prompt_text"], str)

        # Check specific prompts are returned
        titles = [p["title"] for p in data["prompts"]]
        assert "Career Path Guidance" in titles
        assert "Skill Development" in titles
        assert "Inactive Prompt" not in titles

    @pytest.mark.asyncio
    async def test_get_prompts_only_active(self, client, db_session):
        """Test that only active prompts are returned."""
        # Create mix of active and inactive prompts
        active_prompt = Prompt(
            id=uuid4(),
            title="Active Prompt",
            prompt_text="This should appear",
            category="test",
            is_active=True
        )
        inactive_prompt = Prompt(
            id=uuid4(),
            title="Inactive Prompt",
            prompt_text="This should not appear",
            category="test",
            is_active=False
        )

        db_session.add(active_prompt)
        db_session.add(inactive_prompt)
        await db_session.commit()

        response = await client.get("/api/prompts")

        assert response.status_code == 200
        data = response.json()

        assert len(data["prompts"]) == 1
        assert data["prompts"][0]["title"] == "Active Prompt"

    @pytest.mark.asyncio
    async def test_get_prompts_http_methods(self, client):
        """Test that only GET method is allowed."""
        # Test POST method (should fail)
        response = await client.post("/api/prompts")
        assert response.status_code == 405  # Method Not Allowed

        # Test PUT method (should fail)
        response = await client.put("/api/prompts")
        assert response.status_code == 405  # Method Not Allowed

        # Test DELETE method (should fail)
        response = await client.delete("/api/prompts")
        assert response.status_code == 405  # Method Not Allowed

    @pytest.mark.asyncio
    async def test_get_prompts_response_structure(self, client, db_session):
        """Test that response matches expected Pydantic schema structure."""
        # Create a test prompt
        prompt = Prompt(
            id=uuid4(),
            title="Test Prompt",
            prompt_text="Test prompt text for validation",
            category="test",
            is_active=True
        )

        db_session.add(prompt)
        await db_session.commit()

        response = await client.get("/api/prompts")

        assert response.status_code == 200
        data = response.json()

        # Test PromptListResponse structure
        assert isinstance(data, dict)
        assert "success" in data
        assert "prompts" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["prompts"], list)

        # Test PromptBase structure
        prompt_data = data["prompts"][0]
        assert "id" in prompt_data
        assert "title" in prompt_data
        assert "prompt_text" in prompt_data
        assert prompt_data["title"] == "Test Prompt"
        assert prompt_data["prompt_text"] == "Test prompt text for validation"

        # Validate UUID format
        import uuid
        uuid.UUID(prompt_data["id"])  # Should not raise exception
