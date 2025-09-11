import pytest
from uuid import uuid4
import sys
import os

# Add paths for microservices setup
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models import Conversation, Message

# Fixtures are automatically discovered from conftest.py
# No need to import client, db_session - pytest will find them


class TestCreateConversationMessage:
    """Integration tests for the POST /users/{user_id}/messages endpoint that creates conversations and messages."""

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_success(self, client):
        """Test POST /users/{user_id}/messages creates new conversation and message."""
        user_id = uuid4()
        message_content = "Hello, I need career advice for transitioning to tech!"
        
        response = await client.post(
            f"/api/users/{user_id}/messages",
            json={"message": message_content}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert data["success"] is True
        assert "message" in data
        assert "conversation" in data
        
        # Validate message data
        message = data["message"]
        assert message["is_human"] == True
        assert message["content"] == message_content
        assert "id" in message
        assert "created_at" in message
        assert "conversation_id" in message
        
        # Validate conversation data
        conversation = data["conversation"]
        assert "id" in conversation
        assert "title" in conversation
        assert "created_at" in conversation
        assert conversation["user_id"] == str(user_id)
        assert conversation["title"] == "New Conversation"
        
        # Ensure message belongs to the created conversation
        assert message["conversation_id"] == conversation["id"]
        
        # Validate UUID formats
        import uuid
        uuid.UUID(message["id"])
        uuid.UUID(message["conversation_id"])
        uuid.UUID(conversation["id"])

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_empty_content(self, client):
        """Test POST /users/{user_id}/messages with empty message content."""
        user_id = uuid4()
        
        response = await client.post(
            f"/api/users/{user_id}/messages",
            json={"message": ""}
        )
        
        # Should still create conversation and message with empty content
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"]["content"] == ""
        assert data["message"]["is_human"] == True

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_missing_message_field(self, client):
        """Test POST /users/{user_id}/messages with missing message field."""
        user_id = uuid4()
        
        response = await client.post(
            f"/api/users/{user_id}/messages",
            json={}
        )
        
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_invalid_user_id(self, client):
        """Test POST /users/{user_id}/messages with invalid user_id format."""
        response = await client.post(
            "/api/users/invalid-uuid/messages",
            json={"message": "Test message"}
        )
        
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_multiple_calls(self, client):
        """Test multiple calls to POST /users/{user_id}/messages create separate conversations."""
        user_id = uuid4()
        
        # First message
        response1 = await client.post(
            f"/api/users/{user_id}/messages",
            json={"message": "First conversation message"}
        )
        
        # Second message
        response2 = await client.post(
            f"/api/users/{user_id}/messages",
            json={"message": "Second conversation message"}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Should create different conversations
        assert data1["conversation"]["id"] != data2["conversation"]["id"]
        assert data1["message"]["conversation_id"] != data2["message"]["conversation_id"]
        
        # Both should belong to same user
        assert data1["conversation"]["user_id"] == str(user_id)
        assert data2["conversation"]["user_id"] == str(user_id)

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_long_content(self, client):
        """Test POST /users/{user_id}/messages with long message content."""
        user_id = uuid4()
        long_message = "A" * 5000  # 5000 character message
        
        response = await client.post(
            f"/api/users/{user_id}/messages",
            json={"message": long_message}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"]["content"] == long_message

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_special_characters(self, client):
        """Test POST /users/{user_id}/messages with special characters and unicode."""
        user_id = uuid4()
        special_message = "Hello! 🚀 I need advice about Python & JavaScript development. What about C++/C#? 日本語 test"
        
        response = await client.post(
            f"/api/users/{user_id}/messages",
            json={"message": special_message}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"]["content"] == special_message

    @pytest.mark.asyncio
    async def test_create_conversation_and_message_response_schema(self, client):
        """Test that POST /users/{user_id}/messages response matches MessageWithConversationResponse schema."""
        user_id = uuid4()
        
        response = await client.post(
            f"/api/users/{user_id}/messages",
            json={"message": "Schema validation test"}
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
