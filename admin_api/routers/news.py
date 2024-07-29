from typing import List  # Import the List type
from typing import Optional
from fastapi import APIRouter, HTTPException
from admin_api.models.news import NewsRequest, NewsResponse
from admin_api.services.news_service import (
    create_news_service,
    get_news_service,
    list_news_service,
    update_news_service,
    delete_news_service,
)

router = APIRouter()

@router.post("/", response_model=NewsResponse)
async def create_news(news: NewsRequest) -> NewsResponse:
    return await create_news_service(news)

@router.get("/{news_id}", response_model=dict)
async def get_news(news_id):
    news = await get_news_service(news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@router.get("/", response_model=dict)
async def list_news(limit: int = 10, offset: int = 0, is_published: Optional[bool] = None):
    """
    Получить список новостей с возможностью фильтрации по статусу публикации.

    - **limit**: Максимальное количество новостей, которое будет возвращено.
    - **offset**: Смещение от начала списка.
    - **is_published**: Фильтрация новостей по статусу публикации.
    """
    return await list_news_service(limit, offset, is_published)

@router.put("/{news_id}", response_model=NewsResponse)
async def update_news(news_id: int, news: NewsRequest) -> NewsResponse:
    updated_news = await update_news_service(news_id, news)
    if not updated_news:
        raise HTTPException(status_code=404, detail="News not found")
    return updated_news

@router.delete("/{news_id}", response_model=dict)
async def delete_news(news_id: int) -> dict:
    if not await delete_news_service(news_id):
        raise HTTPException(status_code=404, detail="News not found")
    return {"detail": "News deleted"}
