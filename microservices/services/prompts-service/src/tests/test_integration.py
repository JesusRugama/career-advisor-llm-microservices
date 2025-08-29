import pytest
import pytest_asyncio
from uuid import uuid4
import sys
import os

# Add paths for microservices setup
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models import Prompt

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
    async def test_get_prompts_with_additional_data(self, client, db_session):
        """Test GET /api/prompts with additional prompts beyond seed data."""
        # Get baseline count from seed data
        initial_response = await client.get("/api/prompts")
        initial_count = len(initial_response.json()["prompts"])
        
        # Create additional test prompts with unique titles
        prompt1 = Prompt(
            id=uuid4(),
            title="Test Career Guidance",
            prompt_text="What are the best career paths for someone with my skills?",
            category="career",
            is_active=True
        )
        prompt2 = Prompt(
            id=uuid4(),
            title="Test Skill Development",
            prompt_text="What skills should I focus on developing next?",
            category="skills",
            is_active=True
        )
        prompt3 = Prompt(
            id=uuid4(),
            title="Test Inactive Prompt",
            prompt_text="This should not appear",
            category="test",
            is_active=False
        )

        # Add to database
        db_session.add(prompt1)
        db_session.add(prompt2)
        db_session.add(prompt3)
        await db_session.flush()  # Use flush instead of commit to avoid transaction conflicts

        # Test the endpoint
        response = await client.get("/api/prompts")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        # Should have seed data + 2 new active prompts
        assert len(data["prompts"]) == initial_count + 2

        # Check prompt structure
        for prompt in data["prompts"]:
            assert "id" in prompt
            assert "title" in prompt
            assert "prompt_text" in prompt
            assert isinstance(prompt["title"], str)
            assert isinstance(prompt["prompt_text"], str)

        # Check specific test prompts are returned
        titles = [p["title"] for p in data["prompts"]]
        assert "Test Career Guidance" in titles
        assert "Test Skill Development" in titles
        assert "Test Inactive Prompt" not in titles

    @pytest.mark.asyncio
    async def test_get_prompts_only_active(self, client, db_session):
        """Test that only active prompts are returned."""
        # Get baseline count (all seed data should be active)
        initial_response = await client.get("/api/prompts")
        initial_count = len(initial_response.json()["prompts"])
        
        # Create mix of active and inactive prompts
        active_prompt = Prompt(
            id=uuid4(),
            title="Test Active Prompt",
            prompt_text="This should appear",
            category="test",
            is_active=True
        )
        inactive_prompt = Prompt(
            id=uuid4(),
            title="Test Inactive Prompt",
            prompt_text="This should not appear",
            category="test",
            is_active=False
        )

        db_session.add(active_prompt)
        db_session.add(inactive_prompt)
        await db_session.flush()  # Use flush instead of commit to avoid transaction conflicts

        response = await client.get("/api/prompts")

        assert response.status_code == 200
        data = response.json()

        # Should have seed data + 1 new active prompt (inactive not included)
        assert len(data["prompts"]) == initial_count + 1
        
        # Verify our test active prompt is included
        titles = [p["title"] for p in data["prompts"]]
        assert "Test Active Prompt" in titles
        assert "Test Inactive Prompt" not in titles
        
        # Verify all returned prompts are active
        for prompt in data["prompts"]:
            # Note: We can't directly check is_active from API response
            # but the endpoint should only return active prompts
            assert prompt["title"] != "Test Inactive Prompt"

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
        # Create a test prompt with unique title
        prompt = Prompt(
            id=uuid4(),
            title="Test Structure Validation Prompt",
            prompt_text="Test prompt text for validation",
            category="test",
            is_active=True
        )

        db_session.add(prompt)
        await db_session.flush()  # Use flush instead of commit to avoid transaction conflicts

        response = await client.get("/api/prompts")

        assert response.status_code == 200
        data = response.json()

        # Test PromptListResponse structure
        assert isinstance(data, dict)
        assert "success" in data
        assert "prompts" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["prompts"], list)
        assert len(data["prompts"]) > 0  # Should have at least seed data + our test prompt

        # Test PromptBase structure - find our test prompt
        test_prompt = None
        for prompt_data in data["prompts"]:
            if prompt_data["title"] == "Test Structure Validation Prompt":
                test_prompt = prompt_data
                break
        
        assert test_prompt is not None, "Test prompt not found in response"
        assert "id" in test_prompt
        assert "title" in test_prompt
        assert "prompt_text" in test_prompt
        assert test_prompt["title"] == "Test Structure Validation Prompt"
        assert test_prompt["prompt_text"] == "Test prompt text for validation"

        # Validate UUID format
        import uuid
        uuid.UUID(test_prompt["id"])  # Should not raise exception
