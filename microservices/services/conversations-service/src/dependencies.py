"""
Dependency injection functions for the conversations service.
"""

import sys
import os

# Add shared directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../shared"))

from services.ai_service import AIService
from feign_clients.users_client import UsersClient


def get_users_client() -> UsersClient:
    """Dependency to get UsersClient instance."""
    return UsersClient()


def get_ai_service() -> AIService:
    """Dependency to get AIService instance."""
    return AIService()
