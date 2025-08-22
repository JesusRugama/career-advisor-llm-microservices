import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from main import app
from domains.prompts.models import Prompt
from uuid import uuid4


class TestPromptsEndpoint:
    """Test cases for the /prompts endpoint."""

    def test_get_prompts_success_with_mock(self):
        """Test successful retrieval of active prompts using mock."""
        
        # Create mock prompts
        mock_prompts = [
            Prompt(
                id=uuid4(),
                title="Career Path Guidance",
                prompt_text="What are the best career paths for someone with my skills?",
                category="career",
                is_active=True
            ),
            Prompt(
                id=uuid4(),
                title="Skill Development",
                prompt_text="What skills should I focus on developing next?",
                category="skills",
                is_active=True
            )
        ]
        
        # Mock the database dependency
        async def mock_get_db():
            mock_db = AsyncMock()
            mock_db.scalars.return_value = iter(mock_prompts)
            yield mock_db
        
        # Override the dependency
        from database import get_db
        app.dependency_overrides[get_db] = mock_get_db
        
        try:
            client = TestClient(app)
            response = client.get("/api/prompts")
            
            assert response.status_code == 200
            data = response.json()
            
            # Check response structure
            assert "success" in data
            assert "prompts" in data
            assert data["success"] is True
            assert len(data["prompts"]) == 2
            
            # Check prompt structure
            for prompt in data["prompts"]:
                assert "id" in prompt
                assert "title" in prompt
                assert "prompt_text" in prompt
                assert isinstance(prompt["title"], str)
                assert isinstance(prompt["prompt_text"], str)
        
        finally:
            # Clean up dependency override
            app.dependency_overrides.clear()

    def test_get_prompts_empty_database_with_mock(self):
        """Test endpoint behavior with no prompts in database using mock."""
        
        # Mock empty database
        async def mock_get_db():
            mock_db = AsyncMock()
            mock_db.scalars.return_value = iter([])
            yield mock_db
        
        from database import get_db
        app.dependency_overrides[get_db] = mock_get_db
        
        try:
            client = TestClient(app)
            response = client.get("/api/prompts")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["success"] is True
            assert data["prompts"] == []
        
        finally:
            app.dependency_overrides.clear()

    def test_get_prompts_http_methods(self):
        """Test that only GET method is allowed."""
        
        async def mock_get_db():
            mock_db = AsyncMock()
            yield mock_db
        
        from database import get_db
        app.dependency_overrides[get_db] = mock_get_db
        
        try:
            client = TestClient(app)
            
            # Test POST method (should fail)
            response = client.post("/api/prompts")
            assert response.status_code == 405  # Method Not Allowed
            
            # Test PUT method (should fail)
            response = client.put("/api/prompts")
            assert response.status_code == 405  # Method Not Allowed
            
            # Test DELETE method (should fail)
            response = client.delete("/api/prompts")
            assert response.status_code == 405  # Method Not Allowed
        
        finally:
            app.dependency_overrides.clear()

    def test_get_prompts_response_structure(self):
        """Test that response matches expected structure."""
        
        mock_prompt = Prompt(
            id=uuid4(),
            title="Test Prompt",
            prompt_text="Test prompt text",
            category="test",
            is_active=True
        )
        
        async def mock_get_db():
            mock_db = AsyncMock()
            mock_db.scalars.return_value = iter([mock_prompt])
            yield mock_db
        
        from database import get_db
        app.dependency_overrides[get_db] = mock_get_db
        
        try:
            client = TestClient(app)
            response = client.get("/api/prompts")
            
            assert response.status_code == 200
            data = response.json()
            
            # Test PromptListResponse structure
            assert isinstance(data, dict)
            assert "success" in data
            assert "prompts" in data
            assert isinstance(data["success"], bool)
            assert isinstance(data["prompts"], list)
            
            # Test PromptBase structure
            if data["prompts"]:
                prompt = data["prompts"][0]
                assert "id" in prompt
                assert "title" in prompt
                assert "prompt_text" in prompt
                assert prompt["title"] == "Test Prompt"
                assert prompt["prompt_text"] == "Test prompt text"
        
        finally:
            app.dependency_overrides.clear()

    def test_get_prompts_content_validation(self):
        """Test that returned prompts have expected content."""
        
        mock_prompts = [
            Prompt(
                id=uuid4(),
                title="Career Path Guidance",
                prompt_text="What are the best career paths for someone with my skills?",
                category="career",
                is_active=True
            ),
            Prompt(
                id=uuid4(),
                title="Skill Development",
                prompt_text="What skills should I focus on developing next?",
                category="skills",
                is_active=True
            )
        ]
        
        async def mock_get_db():
            mock_db = AsyncMock()
            mock_db.scalars.return_value = iter(mock_prompts)
            yield mock_db
        
        from database import get_db
        app.dependency_overrides[get_db] = mock_get_db
        
        try:
            client = TestClient(app)
            response = client.get("/api/prompts")
            
            assert response.status_code == 200
            data = response.json()
            
            # Find specific prompts by title
            career_prompt = next((p for p in data["prompts"] if p["title"] == "Career Path Guidance"), None)
            skill_prompt = next((p for p in data["prompts"] if p["title"] == "Skill Development"), None)
            
            assert career_prompt is not None
            assert skill_prompt is not None
            
            # Validate content
            assert "career paths" in career_prompt["prompt_text"].lower()
            assert "skills" in skill_prompt["prompt_text"].lower()
        
        finally:
            app.dependency_overrides.clear()
