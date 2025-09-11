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


class TestGetConversationMessages:
    """Integration tests for the messages endpoints in conversations service."""

    @pytest.mark.asyncio
    async def test_get_messages_empty_conversation(self, client, db_session):
        """Test GET /users/{user_id}/conversations/{conversation_id}/messages with no messages."""
        user_id = uuid4()
        conversation_id = uuid4()
        
        # Create a conversation without messages
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
            title="Empty Conversation"
        )
        db_session.add(conversation)
        await db_session.flush()

        response = await client.get(f"/api/users/{user_id}/conversations/{conversation_id}/messages")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["messages"] == []

    @pytest.mark.asyncio
    async def test_get_messages_with_data(self, client, db_session):
        """Test GET /users/{user_id}/conversations/{conversation_id}/messages with existing messages."""
        user_id = uuid4()
        conversation_id = uuid4()
        
        # Create conversation
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
            title="Test Conversation"
        )
        db_session.add(conversation)
        await db_session.flush()

        # Create messages for the conversation
        message1 = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            is_human=True,
            content="Hello, I need career advice"
        )
        message2 = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            is_human=False,
            content="I'd be happy to help with your career questions!"
        )
        message3 = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            is_human=True,
            content="What skills should I focus on for software engineering?"
        )

        db_session.add(message1)
        db_session.add(message2)
        db_session.add(message3)
        await db_session.flush()

        response = await client.get(f"/api/users/{user_id}/conversations/{conversation_id}/messages")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["messages"]) == 3

        # Check message structure and order (should be chronological)
        messages = data["messages"]
        for message in messages:
            assert "id" in message
            assert "is_human" in message
            assert "content" in message
            assert "created_at" in message
            assert "conversation_id" in message
            assert message["conversation_id"] == str(conversation_id)

        # Check specific message content
        assert messages[0]["is_human"] == True
        assert messages[0]["content"] == "Hello, I need career advice"
        assert messages[1]["is_human"] == False
        assert messages[1]["content"] == "I'd be happy to help with your career questions!"
        assert messages[2]["is_human"] == True
        assert messages[2]["content"] == "What skills should I focus on for software engineering?"

    @pytest.mark.asyncio
    async def test_get_messages_conversation_not_found(self, client):
        """Test GET messages for non-existent conversation."""
        user_id = uuid4()
        conversation_id = uuid4()

        response = await client.get(f"/api/users/{user_id}/conversations/{conversation_id}/messages")
        
        assert response.status_code == 404
        data = response.json()
        assert "Conversation not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_get_messages_wrong_user(self, client, db_session):
        """Test GET messages for conversation belonging to different user."""
        user1_id = uuid4()
        user2_id = uuid4()
        conversation_id = uuid4()
        
        # Create conversation for user1
        conversation = Conversation(
            id=conversation_id,
            user_id=user1_id,
            title="User 1's Conversation"
        )
        db_session.add(conversation)
        await db_session.flush()

        # Try to access with user2
        response = await client.get(f"/api/users/{user2_id}/conversations/{conversation_id}/messages")
        
        assert response.status_code == 404
        data = response.json()
        assert "Conversation not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_get_messages_message_isolation(self, client, db_session):
        """Test that messages are properly isolated by conversation."""
        user_id = uuid4()
        conversation1_id = uuid4()
        conversation2_id = uuid4()
        
        # Create two conversations
        conversation1 = Conversation(
            id=conversation1_id,
            user_id=user_id,
            title="Conversation 1"
        )
        conversation2 = Conversation(
            id=conversation2_id,
            user_id=user_id,
            title="Conversation 2"
        )
        db_session.add(conversation1)
        db_session.add(conversation2)
        await db_session.flush()

        # Create messages for each conversation
        message1_conv1 = Message(
            id=uuid4(),
            conversation_id=conversation1_id,
            is_human=True,
            content="Message in conversation 1"
        )
        message2_conv1 = Message(
            id=uuid4(),
            conversation_id=conversation1_id,
            is_human=False,
            content="Response in conversation 1"
        )
        message1_conv2 = Message(
            id=uuid4(),
            conversation_id=conversation2_id,
            is_human=True,
            content="Message in conversation 2"
        )

        db_session.add(message1_conv1)
        db_session.add(message2_conv1)
        db_session.add(message1_conv2)
        await db_session.flush()

        # Test conversation 1 messages
        response1 = await client.get(f"/api/users/{user_id}/conversations/{conversation1_id}/messages")
        assert response1.status_code == 200
        data1 = response1.json()
        assert len(data1["messages"]) == 2
        assert all(msg["conversation_id"] == str(conversation1_id) for msg in data1["messages"])

        # Test conversation 2 messages
        response2 = await client.get(f"/api/users/{user_id}/conversations/{conversation2_id}/messages")
        assert response2.status_code == 200
        data2 = response2.json()
        assert len(data2["messages"]) == 1
        assert data2["messages"][0]["conversation_id"] == str(conversation2_id)
        assert data2["messages"][0]["content"] == "Message in conversation 2"

    @pytest.mark.asyncio
    async def test_get_messages_invalid_conversation_id(self, client):
        """Test GET messages with invalid conversation_id format."""
        user_id = uuid4()
        
        response = await client.get(f"/api/users/{user_id}/conversations/invalid-uuid/messages")
        assert response.status_code == 422  # Validation Error

    @pytest.mark.asyncio
    async def test_get_messages_response_structure(self, client, db_session):
        """Test that messages response matches expected Pydantic schema structure."""
        user_id = uuid4()
        conversation_id = uuid4()
        
        # Create conversation and message
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
            title="Schema Test Conversation"
        )
        message = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            is_human=True,
            content="Test message for schema validation"
        )

        db_session.add(conversation)
        db_session.add(message)
        await db_session.flush()

        response = await client.get(f"/api/users/{user_id}/conversations/{conversation_id}/messages")

        assert response.status_code == 200
        data = response.json()

        # Test MessageListResponse structure
        assert isinstance(data, dict)
        assert "success" in data
        assert "messages" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["messages"], list)
        assert len(data["messages"]) == 1

        # Test MessageBase structure
        message_data = data["messages"][0]
        assert "id" in message_data
        assert "is_human" in message_data
        assert "content" in message_data
        assert "created_at" in message_data
        assert "conversation_id" in message_data
        assert message_data["is_human"] == True
        assert message_data["content"] == "Test message for schema validation"
        assert message_data["conversation_id"] == str(conversation_id)

        # Validate UUID format
        import uuid
        uuid.UUID(message_data["id"])  # Should not raise exception
        uuid.UUID(message_data["conversation_id"])  # Should not raise exception
