from typing import List  # Add this import
from fastapi import HTTPException, status
import httpx
from admin_api.models.news import NewsRequest, NewsResponse
from admin_api.utils import http_client
from typing import Optional

DJANGO_API_URL = "http://django:8000/api/"


async def create_news_service(news: dict) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f'{DJANGO_API_URL}news_create/',
                json=news  # Убедитесь, что данные корректно отформатированы в JSON
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

async def get_news_service(news_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_API_URL}news/{news_id}/")
        if response.status_code == 404:
            return None
        if response.status_code == 200:
            return response.json()

async def list_news_service(
    limit: int,
    offset: int,
    is_published: Optional[bool],
    order_by: Optional[str]  # Добавьте параметр для сортировки
):
    """
    Запрос к Django API для получения списка новостей.

    - **limit**: Максимальное количество новостей, которое будет возвращено.
    - **offset**: Смещение от начала списка.
    - **is_published**: Фильтрация новостей по статусу публикации.
    - **order_by**: Параметр для сортировки новостей.
    """
    params = {"limit": limit, "offset": offset}

    if is_published is not None:
        params["is_published"] = is_published

    if order_by:
        params["order_by"] = order_by

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DJANGO_API_URL}news/", params=params)

    if response.status_code == 200:
        return response.json()

    raise HTTPException(status_code=response.status_code, detail=response.text)

async def update_news_service(news_id: int, news: dict):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{DJANGO_API_URL}news_create/{news_id}/", json=news)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

async def delete_news_service(news_id):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{DJANGO_API_URL}news_create/{news_id}/")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True
