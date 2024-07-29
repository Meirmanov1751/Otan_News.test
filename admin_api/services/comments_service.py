from typing import List  # Import the List type

import httpx
from admin_api.models.comments import CommentRequest, CommentResponse
from admin_api.utils import http_client

DJANGO_API_URL = "http://django:8000/api/comments/"

async def create_comment_service(comment: CommentRequest) -> CommentResponse:
    async with http_client as client:
        response = await client.post(f"{DJANGO_API_URL}", json=comment.dict())
        response.raise_for_status()
        return CommentResponse(**response.json())

async def get_comment_service(comment_id: int) -> CommentResponse:
    async with http_client as client:
        response = await client.get(f"{DJANGO_API_URL}{comment_id}/")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return CommentResponse(**response.json())

async def delete_comment_service(comment_id: int) -> bool:
    async with http_client as client:
        response = await client.delete(f"{DJANGO_API_URL}{comment_id}/")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True
