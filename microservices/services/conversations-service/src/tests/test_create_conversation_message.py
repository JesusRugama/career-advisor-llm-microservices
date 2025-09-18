import pytest
from uuid import uuid4
import sys
import os

# Add paths for microservices setup
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../shared"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from models import Conversation, Message
from dependencies import get_users_client, get_ai_service
from tests.fake_services import FakeUsersClient, FakeAIService
from main import app

# Fixtures are automatically discovered from conftest.py
# No need to import client, db_session - pytest will find them


class TestCreateConversationMessage:
    """Integration tests for the POST /users/{user_id}/messages endpoint that creates conversations and messages."""

    def setup_method(self):
        """Set up fake services for all tests in this class."""
        self.user_id = uuid4()
        
        # Create default fake services
        self.fake_users_client = FakeUsersClient()
        self.fake_ai_service = FakeAIService({
            "success": True,
            "response": "This is a helpful AI response for your career question."
        })
        
        # Create default user profile
        self.default_user_profile = {
            "skills": ["Python", "FastAPI", "PostgreSQL"],
            "years_experience": "3",
            "career_goals": ["Senior Engineer", "Tech Lead"]
        }
        
        # Set up default user profile
        self.setup_user_profile(self.user_id)

        # Override dependencies for all tests in this class
        app.dependency_overrides[get_users_client] = lambda: self.fake_users_client
        app.dependency_overrides[get_ai_service] = lambda: self.fake_ai_service

    def setup_user_profile(self, user_id: uuid4, profile: dict = None):
        """Helper method to set up user profile for a test."""
        profile_to_use = profile or self.default_user_profile
        self.fake_users_client.set_user_profile(user_id, profile_to_use)

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_success(self, client):
        """Test POST /users/{user_id}/messages creates new conversation and message."""
        message_content = "Hello, I need career advice for transitioning to tech!"

        response = await client.post(
            f"/api/users/{self.user_id}/messages", json={"message": message_content}
        )

        assert response.status_code == 200
        data = response.json()

        # Validate response structure
        assert data["success"] is True
        assert "message" in data
        assert "conversation" in data

        # Validate AI response message (not the user message)
        message = data["message"]
        assert message["is_human"] is False  # This should be the AI response
        assert message["content"] == "This is a helpful AI response for your career question."
        assert "id" in message
        assert "created_at" in message
        assert "conversation_id" in message

        # Validate conversation data
        conversation = data["conversation"]
        assert "id" in conversation
        assert "title" in conversation
        assert "created_at" in conversation
        assert conversation["user_id"] == str(self.user_id)
        assert conversation["title"] == "New Conversation"

        # Ensure message belongs to the created conversation
        assert message["conversation_id"] == conversation["id"]

        # Validate that AI service was called with correct data
        last_ai_call = self.fake_ai_service.get_last_call()
        assert last_ai_call is not None
        assert last_ai_call["user_profile"] == self.default_user_profile
        assert last_ai_call["question"] == message_content

        # Validate UUID formats
        import uuid
        uuid.UUID(message["id"])
        uuid.UUID(message["conversation_id"])
        uuid.UUID(conversation["id"])

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_user_profile_not_found(self, client):
        """Test POST /users/{user_id}/messages when user profile doesn't exist."""
        # Create a different user ID for this test (one without a profile)
        user_without_profile = uuid4()
        
        # Don't set up user profile - fake client will return None
        
        response = await client.post(
            f"/api/users/{user_without_profile}/messages", 
            json={"message": "This should fail due to missing profile"}
        )

        assert response.status_code == 404
        data = response.json()
        assert "User profile not found" in data["detail"]
        assert "complete your profile first" in data["detail"]

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_ai_service_failure(self, client):
        """Test POST /users/{user_id}/messages when AI service fails."""
        # Configure AI service to return failure
        self.fake_ai_service.set_response({
            "success": False,
            "response": "Sorry, I couldn't generate a response at this time.",
            "error": "API timeout"
        })

        response = await client.post(
            f"/api/users/{self.user_id}/messages", 
            json={"message": "What should I learn next?"}
        )

        assert response.status_code == 200
        data = response.json()

        # Should return error message but still succeed
        assert data["success"] is False
        message = data["message"]
        assert message["is_human"] is False
        assert "having trouble generating a response" in message["content"]

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_empty_content(self, client):
        """Test POST /users/{user_id}/messages with empty message content."""
        response = await client.post(
            f"/api/users/{self.user_id}/messages", json={"message": ""}
        )

        # Should still create conversation and get AI response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # The returned message should be the AI response, not the empty user message
        message = data["message"]
        assert message["is_human"] is False
        assert message["content"] == "This is a helpful AI response for your career question."
        
        # Verify AI service was called with empty question
        last_ai_call = self.fake_ai_service.get_last_call()
        assert last_ai_call["question"] == ""

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_missing_message_field(self, client):
        """Test POST /users/{user_id}/messages with missing message field."""
        response = await client.post(f"/api/users/{self.user_id}/messages", json={})

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_invalid_user_id(self, client):
        """Test POST /users/{user_id}/messages with invalid user_id format."""
        response = await client.post(
            "/api/users/invalid-uuid/messages", json={"message": "Test message"}
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_multiple_calls(self, client):
        """Test multiple calls to POST /users/{user_id}/messages create separate conversations."""
        # First message
        response1 = await client.post(
            f"/api/users/{self.user_id}/messages",
            json={"message": "First conversation message"},
        )

        # Second message
        response2 = await client.post(
            f"/api/users/{self.user_id}/messages",
            json={"message": "Second conversation message"},
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = response1.json()
        data2 = response2.json()

        # Should create different conversations
        assert data1["conversation"]["id"] != data2["conversation"]["id"]
        assert (
            data1["message"]["conversation_id"] != data2["message"]["conversation_id"]
        )

        # Both should belong to same user
        assert data1["conversation"]["user_id"] == str(self.user_id)
        assert data2["conversation"]["user_id"] == str(self.user_id)

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_long_content(self, client):
        """Test POST /users/{user_id}/messages with long message content."""
        long_message = "A" * 5000  # 5000 character message

        response = await client.post(
            f"/api/users/{self.user_id}/messages", json={"message": long_message}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_response_schema(self, client):
        """Test that POST /users/{user_id}/messages response matches MessageWithConversationResponse schema."""

        response = await client.post(
            f"/api/users/{self.user_id}/messages", json={"message": "Schema validation test"}
        )

        assert response.status_code == 200
        data = response.json()

        # Test MessageWithConversationResponse structure
        required_fields = ["success", "message", "conversation"]
        for field in required_fields:
            assert field in data

        # Test MessageBase structure
        message = data["message"]
        message_fields = ["id", "is_human", "content", "created_at", "conversation_id"]
        for field in message_fields:
            assert field in message

        # Test ConversationBase structure (as dict)
        conversation = data["conversation"]
        conversation_fields = ["id", "title", "created_at", "user_id"]
        for field in conversation_fields:
            assert field in conversation
