from typing import List  # Add this import
from fastapi import HTTPException, status
import httpx
from admin_api.utils import http_client
from typing import Optional

DJANGO_API_URL = "http://django:8000/api/"


async def create_quote_service(quote: dict) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f'{DJANGO_API_URL}quote_create/',
                json=quote  # Убедитесь, что данные корректно отформатированы в JSON
            )
            response.raise_for_status()  # Вызовет исключение для HTTP ошибок

            response_data = response.json()

            # Логирование ответа для отладки
            print("Ответ от Django API:", response_data)

            return response_data

        except httpx.HTTPStatusError as http_error:
            print(f"Произошла ошибка HTTP: {http_error.response.text}")  # Логирование ошибки
            raise HTTPException(status_code=http_error.response.status_code, detail=http_error.response.json())

        except Exception as e:
            # Обработка неожиданных ошибок
            print(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(status_code=500, detail="Произошла ошибка при обработке запроса")

async def get_quote_service(quote_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_API_URL}quote/{quote_id}/")
        if response.status_code == 404:
            return None
        if response.status_code == 200:
            return response.json()

async def list_quote_service(limit: int, offset: int, is_published: Optional[bool]):
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
        response = await client.get(f"{DJANGO_API_URL}quote/", params=params)

    # Проверка ответа
    if response.status_code == 200:
        return response.json()

    # Обработка ошибок
    raise HTTPException(status_code=response.status_code, detail=response.text)

async def update_quote_service(quote_id: int, quote: dict) -> dict:
    async with http_client as client:
        response = await client.put(f"{DJANGO_API_URL}quote_create/{quote_id}/", json=quote)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

async def delete_quote_service(quote_id):
    async with http_client as client:
        response = await client.delete(f"{DJANGO_API_URL}quote_create/{quote_id}/")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True
