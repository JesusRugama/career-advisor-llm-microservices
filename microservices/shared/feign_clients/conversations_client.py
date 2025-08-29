import httpx
from typing import Optional, Dict, Any
from uuid import UUID
import os
from config import settings

class ConversationsClient:
    def __init__(self):
        self.base_url = settings.feign_client_url
        self.timeout = settings.feign_client_timeout
    
    async def get_conversation(self, conversation_id: UUID, user_id: UUID) -> Optional[Dict[Any, Any]]:
        """
        Get a conversation by ID and verify it belongs to the user.
        Returns the conversation data if found and belongs to user, None otherwise.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/conversations/{conversation_id}",
                    params={"user_id": str(user_id)}
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                else:
                    # Log error but don't raise exception - let caller handle
                    print(f"Error fetching conversation {conversation_id}: {response.status_code} - {response.text}")
                    return None
                    
            except httpx.RequestError as e:
                print(f"Request error when fetching conversation {conversation_id}: {e}")
                return None
            except Exception as e:
                print(f"Unexpected error when fetching conversation {conversation_id}: {e}")
                return None
    
    async def conversation_exists(self, conversation_id: UUID, user_id: UUID) -> bool:
        """
        Check if a conversation exists and belongs to the user.
        Returns True if conversation exists and belongs to user, False otherwise.
        """
        conversation = await self.get_conversation(conversation_id, user_id)
        return conversation is not None
    
    async def create_conversation(self, user_id: UUID, title: str) -> Optional[Dict[Any, Any]]:
        """
        Create a new conversation for the user.
        Returns the created conversation data if successful, None otherwise.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/conversations",
                    json={
                        "user_id": str(user_id),
                        "title": title
                    }
                )
                
                if response.status_code == 201:
                    return response.json()
                else:
                    print(f"Error creating conversation: {response.status_code} - {response.text}")
                    return None
                    
            except httpx.RequestError as e:
                print(f"Request error when creating conversation: {e}")
                return None
            except Exception as e:
                print(f"Unexpected error when creating conversation: {e}")
                return None
