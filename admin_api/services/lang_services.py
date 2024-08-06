from typing import List  # Import the List type
from fastapi import HTTPException, status
import httpx
from admin_api.utils import http_client
from typing import Optional

DJANGO_API_URL = "http://django:8000/api/language"

async def create_language_service(language: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{DJANGO_API_URL}/", json=language)
        response.raise_for_status()
        return response.json()

async def list_language_service(limit: int, offset: int, is_published: Optional[bool]):
    """
    Запрос к Django API для получения списка новостей.

    - **limit**: Максимальное количество новостей, которое будет возвращено.
    - **offset**: Смещение от начала списка.
    - **is_published**: Фильтрация новостей по статусу публикации.
    """
    # Формируем параметры запроса
    params = {"limit": limit, "offset": offset}

    # Добавляем параметр is_published, если он задан
    if is_published is not None:
        params["is_published"] = is_published

    # Запрос к Django API
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_API_URL}/", params=params)

    # Проверка ответа
    if response.status_code == 200:
        return response.json()

    # Обработка ошибок
    raise HTTPException(status_code=response.status_code, detail=response.text)

async def get_language_service(language_id: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_API_URL}/{language_id}/")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

async def delete_language_service(language_id: int) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{DJANGO_API_URL}/{language_id}/")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True
