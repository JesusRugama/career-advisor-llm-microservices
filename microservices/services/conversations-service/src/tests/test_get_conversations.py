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

class TestGetConversations:
    """Integration tests for the conversations service using real database."""

    @pytest.mark.asyncio
    async def test_get_conversations_empty_list(self, client):
        """Test GET /users/{user_id}/conversations with no conversations."""
        user_id = uuid4()
        response = await client.get(f"/api/users/{user_id}/conversations")
        
        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["conversations"] == []

    @pytest.mark.asyncio
    async def test_get_conversations_with_data(self, client, db_session):
        """Test GET /users/{user_id}/conversations with existing conversations."""
        user_id = uuid4()
        other_user_id = uuid4()
        
        # Create test conversations for the user
        conversation1 = Conversation(
            id=uuid4(),
            user_id=user_id,
            title="Career Planning Discussion"
        )
        conversation2 = Conversation(
            id=uuid4(),
            user_id=user_id,
            title="Skills Development Chat"
        )
        # Create conversation for different user (should not appear in results)
        conversation3 = Conversation(
            id=uuid4(),
            user_id=other_user_id,
            title="Other User's Conversation"
        )

        # Add to database
        db_session.add(conversation1)
        db_session.add(conversation2)
        db_session.add(conversation3)
        await db_session.flush()  # Use flush instead of commit to avoid transaction conflicts

        # Test the endpoint
        response = await client.get(f"/api/users/{user_id}/conversations")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert len(data["conversations"]) == 2

        # Check conversation structure
        for conversation in data["conversations"]:
            assert "id" in conversation
            assert "title" in conversation
            assert "user_id" in conversation
            assert "created_at" in conversation
            assert isinstance(conversation["title"], str)
            assert conversation["user_id"] == str(user_id)

        # Check specific conversations are returned (order might vary due to created_at)
        titles = [c["title"] for c in data["conversations"]]
        assert "Career Planning Discussion" in titles
        assert "Skills Development Chat" in titles
        assert "Other User's Conversation" not in titles

    @pytest.mark.asyncio
    async def test_get_conversations_user_isolation(self, client, db_session):
        """Test that users only see their own conversations."""
        user1_id = uuid4()
        user2_id = uuid4()
        
        # Create conversations for different users
        conversation1 = Conversation(
            id=uuid4(),
            user_id=user1_id,
            title="User 1 Conversation"
        )
        conversation2 = Conversation(
            id=uuid4(),
            user_id=user2_id,
            title="User 2 Conversation"
        )

        db_session.add(conversation1)
        db_session.add(conversation2)
        await db_session.flush()

        # Test user1 only sees their conversation
        response1 = await client.get(f"/api/users/{user1_id}/conversations")
        assert response1.status_code == 200
        data1 = response1.json()
        assert len(data1["conversations"]) == 1
        assert data1["conversations"][0]["title"] == "User 1 Conversation"

        # Test user2 only sees their conversation
        response2 = await client.get(f"/api/users/{user2_id}/conversations")
        assert response2.status_code == 200
        data2 = response2.json()
        assert len(data2["conversations"]) == 1
        assert data2["conversations"][0]["title"] == "User 2 Conversation"

    @pytest.mark.asyncio
    async def test_get_conversations_http_methods(self, client):
        """Test that only GET method is allowed."""
        user_id = uuid4()
        
        # Test POST method (should fail)
        response = await client.post(f"/api/users/{user_id}/conversations")
        assert response.status_code == 405  # Method Not Allowed

        # Test PUT method (should fail)
        response = await client.put(f"/api/users/{user_id}/conversations")
        assert response.status_code == 405  # Method Not Allowed

        # Test DELETE method (should fail)
        response = await client.delete(f"/api/users/{user_id}/conversations")
        assert response.status_code == 405  # Method Not Allowed

    @pytest.mark.asyncio
    async def test_get_conversations_response_structure(self, client, db_session):
        """Test that response matches expected Pydantic schema structure."""
        user_id = uuid4()
        
        # Create a test conversation
        conversation = Conversation(
            id=uuid4(),
            user_id=user_id,
            title="Test Structure Validation"
        )

        db_session.add(conversation)
        await db_session.flush()

        response = await client.get(f"/api/users/{user_id}/conversations")

        assert response.status_code == 200
        data = response.json()

        # Test ConversationListResponse structure
        assert isinstance(data, dict)
        assert "success" in data
        assert "conversations" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["conversations"], list)
        assert len(data["conversations"]) == 1

        # Test ConversationBase structure
        conversation_data = data["conversations"][0]
        assert "id" in conversation_data
        assert "title" in conversation_data
        assert "user_id" in conversation_data
        assert "created_at" in conversation_data
        assert conversation_data["title"] == "Test Structure Validation"
        assert conversation_data["user_id"] == str(user_id)

        # Validate UUID format
        import uuid
        uuid.UUID(conversation_data["id"])  # Should not raise exception
        uuid.UUID(conversation_data["user_id"])  # Should not raise exception

    @pytest.mark.asyncio
    async def test_get_conversations_invalid_user_id(self, client):
        """Test GET /users/{user_id}/conversations with invalid user_id format."""
        # Test with invalid UUID format
        response = await client.get("/api/users/invalid-uuid/conversations")
        assert response.status_code == 422  # Validation Error

