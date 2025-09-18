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


class TestAddMessageToConversation:
    """Integration tests for the POST /users/{user_id}/conversations/{conversation_id}/message endpoint."""

    @pytest.mark.asyncio
    async def test_add_message_to_conversation_success(self, client, db_session):
        """Test successful message addition with AI response."""
        user_id = uuid4()

        # Create conversation directly using model
        conversation = Conversation(user_id=user_id, title="Test Conversation")
        db_session.add(conversation)
        await db_session.commit()
        await db_session.refresh(conversation)
        conversation_id = conversation.id

        # Create fake services with test data
        fake_user_profile = {
            "skills": ["Python", "FastAPI", "PostgreSQL"],
            "years_experience": "3",
            "career_goals": ["Senior Engineer", "Tech Lead"],
        }

        fake_ai_response = {
            "success": True,
            "response": "Based on your 3 years of experience with Python and FastAPI, I recommend focusing on system design and leadership skills to reach your goal of becoming a Tech Lead.",
        }

        # Create fake service instances
        fake_users_client = FakeUsersClient()
        fake_users_client.set_user_profile(user_id, fake_user_profile)

        fake_ai_service = FakeAIService(fake_ai_response)

        # Override dependencies with fakes
        app.dependency_overrides[get_users_client] = lambda: fake_users_client
        app.dependency_overrides[get_ai_service] = lambda: fake_ai_service

        # Add message to existing conversation
        response = await client.post(
            f"/api/users/{user_id}/conversations/{conversation_id}/message",
            json={"message": "How can I become a tech lead?"},
        )

        assert response.status_code == 200
        data = response.json()

        # Validate response structure
        assert data["success"] is True
        assert "message" in data

        # Validate AI response message
        message = data["message"]
        assert message["is_human"] is False  # AI response
        assert message["content"] == fake_ai_response["response"]
        assert message["conversation_id"] == str(conversation_id)
        assert "id" in message
        assert "created_at" in message

        # Verify fake services were called correctly
        last_ai_call = fake_ai_service.get_last_call()
        assert last_ai_call is not None
        assert last_ai_call["user_profile"] == fake_user_profile
        assert last_ai_call["question"] == "How can I become a tech lead?"

    @pytest.mark.asyncio
    async def test_add_message_conversation_not_found(self, client):
        """Test adding message to non-existent conversation."""
        user_id = uuid4()
        fake_conversation_id = uuid4()

        response = await client.post(
            f"/api/users/{user_id}/conversations/{fake_conversation_id}/message",
            json={"message": "This should fail"},
        )

        assert response.status_code == 404
        data = response.json()
        assert "Conversation not found" in data["detail"]

    @pytest.mark.asyncio
    async def test_add_message_user_profile_not_found(self, client, db_session):
        """Test adding message when user profile doesn't exist."""
        user_id = uuid4()

        # Create conversation directly using model
        conversation = Conversation(user_id=user_id, title="Test Conversation")
        db_session.add(conversation)
        await db_session.commit()
        await db_session.refresh(conversation)
        conversation_id = conversation.id

        # Create fake service instances
        fake_users_client = FakeUsersClient()
        app.dependency_overrides[get_users_client] = lambda: fake_users_client

        response = await client.post(
            f"/api/users/{user_id}/conversations/{conversation_id}/message",
            json={"message": "This should fail due to missing profile"},
        )

        assert response.status_code == 404
        data = response.json()
        assert "User profile not found" in data["detail"]
        assert "complete your profile first" in data["detail"]

    @pytest.mark.asyncio
    async def test_add_message_ai_service_failure(self, client, db_session):
        """Test handling AI service failure gracefully."""
        user_id = uuid4()

        # Create conversation directly using model
        conversation = Conversation(user_id=user_id, title="Test Conversation")
        db_session.add(conversation)
        await db_session.commit()
        await db_session.refresh(conversation)
        conversation_id = conversation.id

        # Mock user profile response
        mock_user_profile = {
            "skills": ["Python"],
            "years_experience": "2",
            "career_goals": ["Senior Engineer"],
        }

        # Mock AI service failure
        mock_ai_failure = {
            "success": False,
            "response": "Sorry, I couldn't generate a response at this time.",
            "error": "API timeout",
        }

        fake_users_client = FakeUsersClient()
        fake_users_client.set_user_profile(user_id, mock_user_profile)

        fake_ai_service = FakeAIService(mock_ai_failure)

        app.dependency_overrides[get_users_client] = lambda: fake_users_client
        app.dependency_overrides[get_ai_service] = lambda: fake_ai_service

        response = await client.post(
            f"/api/users/{user_id}/conversations/{conversation_id}/message",
            json={"message": "What should I learn next?"},
        )

        assert response.status_code == 200
        data = response.json()

        # Should return error message but still succeed
        assert data["success"] is False
        message = data["message"]
        assert message["is_human"] is False
        assert "having trouble generating a response" in message["content"]
        assert message["conversation_id"] == str(conversation_id)

    @pytest.mark.asyncio
    async def test_add_message_invalid_conversation_id(self, client):
        """Test adding message with invalid conversation ID format."""
        user_id = uuid4()

        response = await client.post(
            f"/api/users/{user_id}/conversations/invalid-uuid/message",
            json={"message": "This should fail"},
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_add_message_invalid_user_id(self, client):
        """Test adding message with invalid user ID format."""
        conversation_id = uuid4()

        response = await client.post(
            f"/api/users/invalid-uuid/conversations/{conversation_id}/message",
            json={"message": "This should fail"},
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_add_message_missing_message_field(self, client):
        """Test adding message with missing message field."""
        user_id = uuid4()
        conversation_id = uuid4()

        response = await client.post(
            f"/api/users/{user_id}/conversations/{conversation_id}/message", json={}
        )

        assert response.status_code == 422  # Validation error

    # @pytest.mark.asyncio
    # async def test_add_message_empty_content(self, client, db_session):
    #     """Test adding message with empty content."""
    #     user_id = uuid4()

    #     # Create conversation directly using model
    #     conversation = Conversation(user_id=user_id, title="Test Conversation")
    #     db_session.add(conversation)
    #     await db_session.commit()
    #     await db_session.refresh(conversation)
    #     conversation_id = conversation.id

    #     # Mock user profile and AI response
    #     mock_user_profile = {
    #         "skills": ["Python"],
    #         "years_experience": "1",
    #         "career_goals": [],
    #     }
    #     mock_ai_response = {
    #         "success": True,
    #         "response": "I understand you have a question. Could you please provide more details?",
    #     }

    #     with patch(
    #         "feign_clients.users_client.UsersClient.get_user_profile",
    #         new_callable=AsyncMock,
    #     ) as mock_get_profile, patch(
    #         "services.ai_service.AIService.get_career_advice", new_callable=AsyncMock
    #     ) as mock_get_advice:

    #         mock_get_profile.return_value = mock_user_profile
    #         mock_get_advice.return_value = mock_ai_response

    #         response = await client.post(
    #             f"/api/users/{user_id}/conversations/{conversation_id}/message",
    #             json={"message": ""},
    #         )

    #         assert response.status_code == 200
    #         data = response.json()
    #         assert data["success"] is True

    #         # Verify AI service was called with empty question
    #         mock_get_advice.assert_called_once_with(
    #             user_profile=mock_user_profile, question=""
    #         )

    # @pytest.mark.asyncio
    # async def test_add_message_long_content(self, client, db_session):
    #     """Test adding message with long content."""
    #     user_id = uuid4()

    #     # Create conversation directly using model
    #     conversation = Conversation(user_id=user_id, title="Test Conversation")
    #     db_session.add(conversation)
    #     await db_session.commit()
    #     await db_session.refresh(conversation)
    #     conversation_id = conversation.id

    #     long_message = "A" * 2000  # 2000 character message

    #     # Mock user profile and AI response
    #     mock_user_profile = {
    #         "skills": ["Python"],
    #         "years_experience": "5",
    #         "career_goals": ["Architect"],
    #     }
    #     mock_ai_response = {
    #         "success": True,
    #         "response": "Thank you for the detailed question. Here's my advice...",
    #     }

    #     with patch(
    #         "feign_clients.users_client.UsersClient.get_user_profile",
    #         new_callable=AsyncMock,
    #     ) as mock_get_profile, patch(
    #         "services.ai_service.AIService.get_career_advice", new_callable=AsyncMock
    #     ) as mock_get_advice:

    #         mock_get_profile.return_value = mock_user_profile
    #         mock_get_advice.return_value = mock_ai_response

    #         response = await client.post(
    #             f"/api/users/{user_id}/conversations/{conversation_id}/message",
    #             json={"message": long_message},
    #         )

    #         assert response.status_code == 200
    #         data = response.json()
    #         assert data["success"] is True

    #         # Verify AI service was called with long message
    #         mock_get_advice.assert_called_once_with(
    #             user_profile=mock_user_profile, question=long_message
    #         )

    # @pytest.mark.asyncio
    # async def test_add_message_special_characters(self, client, db_session):
    #     """Test adding message with special characters and unicode."""
    #     user_id = uuid4()

    #     # Create conversation directly using model
    #     conversation = Conversation(user_id=user_id, title="Test Conversation")
    #     db_session.add(conversation)
    #     await db_session.commit()
    #     await db_session.refresh(conversation)
    #     conversation_id = conversation.id

    #     special_message = "How do I transition from Python to Go? 🚀 What about C++/C#? 日本語でも大丈夫？"

    #     # Mock user profile and AI response
    #     mock_user_profile = {
    #         "skills": ["Python"],
    #         "years_experience": "3",
    #         "career_goals": ["Backend Engineer"],
    #     }
    #     mock_ai_response = {
    #         "success": True,
    #         "response": "Great question about language transitions! 🎯",
    #     }

    #     with patch(
    #         "feign_clients.users_client.UsersClient.get_user_profile",
    #         new_callable=AsyncMock,
    #     ) as mock_get_profile, patch(
    #         "services.ai_service.AIService.get_career_advice", new_callable=AsyncMock
    #     ) as mock_get_advice:

    #         mock_get_profile.return_value = mock_user_profile
    #         mock_get_advice.return_value = mock_ai_response

    #         response = await client.post(
    #             f"/api/users/{user_id}/conversations/{conversation_id}/message",
    #             json={"message": special_message},
    #         )

    #         assert response.status_code == 200
    #         data = response.json()
    #         assert data["success"] is True
    #         assert data["message"]["content"] == mock_ai_response["response"]

    # @pytest.mark.asyncio
    # async def test_add_message_users_client_exception(self, client, db_session):
    #     """Test handling UsersClient exceptions."""
    #     user_id = uuid4()

    #     # Create conversation directly using model
    #     conversation = Conversation(user_id=user_id, title="Test Conversation")
    #     db_session.add(conversation)
    #     await db_session.commit()
    #     await db_session.refresh(conversation)
    #     conversation_id = conversation.id

    #     # Mock UsersClient to raise an exception
    #     with patch(
    #         "feign_clients.users_client.UsersClient.get_user_profile",
    #         new_callable=AsyncMock,
    #     ) as mock_get_profile:
    #         mock_get_profile.side_effect = Exception("Network error")

    #         response = await client.post(
    #             f"/api/users/{user_id}/conversations/{conversation_id}/message",
    #             json={"message": "This should handle the exception"},
    #         )

    #         assert response.status_code == 500
    #         data = response.json()
    #         assert "Error processing message" in data["detail"]

    # @pytest.mark.asyncio
    # async def test_add_message_response_schema(self, client, db_session):
    #     """Test that response matches MessageResponse schema."""
    #     user_id = uuid4()

    #     # Create conversation directly using model
    #     conversation = Conversation(user_id=user_id, title="Test Conversation")
    #     db_session.add(conversation)
    #     await db_session.commit()
    #     await db_session.refresh(conversation)
    #     conversation_id = conversation.id

    #     # Mock user profile and AI response
    #     mock_user_profile = {
    #         "skills": ["JavaScript"],
    #         "years_experience": "2",
    #         "career_goals": ["Full Stack"],
    #     }
    #     mock_ai_response = {
    #         "success": True,
    #         "response": "Here's my advice for full stack development...",
    #     }

    #     with patch(
    #         "feign_clients.users_client.UsersClient.get_user_profile",
    #         new_callable=AsyncMock,
    #     ) as mock_get_profile, patch(
    #         "services.ai_service.AIService.get_career_advice", new_callable=AsyncMock
    #     ) as mock_get_advice:

    #         mock_get_profile.return_value = mock_user_profile
    #         mock_get_advice.return_value = mock_ai_response

    #         response = await client.post(
    #             f"/api/users/{user_id}/conversations/{conversation_id}/message",
    #             json={"message": "Schema validation test"},
    #         )

    #         assert response.status_code == 200
    #         data = response.json()

    #         # Test MessageResponse structure
    #         required_fields = ["success", "message"]
    #         for field in required_fields:
    #             assert field in data

    #         # Test MessageBase structure
    #         message = data["message"]
    #         message_fields = [
    #             "id",
    #             "is_human",
    #             "content",
    #             "created_at",
    #             "conversation_id",
    #         ]
    #         for field in message_fields:
    #             assert field in message

    #         # Validate UUID formats
    #         import uuid

    #         uuid.UUID(message["id"])
    #         uuid.UUID(message["conversation_id"])

    #         # Validate message belongs to correct conversation
    #         assert message["conversation_id"] == conversation_id
