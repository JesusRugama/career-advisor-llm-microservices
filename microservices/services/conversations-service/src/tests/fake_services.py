"""
Fake implementations for testing using dependency overrides.
"""

from uuid import UUID
from typing import Dict, Optional


class FakeUsersClient:
    """Fake UsersClient for testing."""

    def __init__(self, user_profiles: Optional[Dict[str, dict]] = None):
        # Store user profiles by user_id (as string)
        self.user_profiles = user_profiles or {}

    async def get_user_profile(self, user_id: UUID) -> Optional[dict]:
        """Return fake user profile or None if not found."""
        return self.user_profiles.get(str(user_id))

    def set_user_profile(self, user_id: UUID, profile: dict):
        """Set a user profile for testing."""
        self.user_profiles[str(user_id)] = profile


class FakeAIService:
    """Fake AIService for testing."""

    def __init__(self, default_response: Optional[dict] = None):
        self.default_response = default_response or {
            "success": True,
            "response": "This is a fake AI response for testing.",
        }
        # Track calls for verification
        self.calls = []

    async def get_career_advice(self, user_profile: dict, question: str) -> dict:
        """Return fake AI response."""
        # Record the call for test verification
        self.calls.append({"user_profile": user_profile, "question": question})
        return self.default_response

    def set_response(self, response: dict):
        """Set the response for testing."""
        self.default_response = response

    def get_last_call(self) -> Optional[dict]:
        """Get the last call made to this service."""
        return self.calls[-1] if self.calls else None

    def reset_calls(self):
        """Reset call history."""
        self.calls = []
