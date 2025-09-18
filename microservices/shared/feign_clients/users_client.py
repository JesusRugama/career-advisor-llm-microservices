import httpx
from typing import Optional, Dict, Any
from uuid import UUID
import os
from config import settings


class UsersClient:
    def __init__(self):
        self.base_url = settings.feign_client_url
        self.timeout = settings.feign_client_timeout

    async def get_user_profile(self, user_id: UUID) -> Optional[Dict[Any, Any]]:
        """
        Get user profile by user ID from the Users Service.
        Returns the user profile data if found, None otherwise.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/users/{user_id}/profile"
                )

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                else:
                    # Log error but don't raise exception - let caller handle
                    print(
                        f"Error fetching user profile {user_id}: {response.status_code} - {response.text}"
                    )
                    return None

            except httpx.RequestError as e:
                print(f"Request error when fetching user profile {user_id}: {e}")
                return None
            except Exception as e:
                print(f"Unexpected error when fetching user profile {user_id}: {e}")
                return None
