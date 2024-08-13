from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Form, Depends, Request
from admin_api.models.news import NewsRequest
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional
from admin_api.utils import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

from admin_api.services.news_service import (
    create_news_service,
    get_news_service,
    list_news_service,
    update_news_service,
    delete_news_service,
)

router = APIRouter()


@router.post("/", response_model=dict)
async def create_news(
    request: Request,
    image: Optional[UploadFile] = File(None)
):
    try:
        form_data = await request.form()
        news = {key: form_data[key] for key in form_data if key != 'image'}
        image_data = await image.read() if image else None

        return await create_news_service(news, image_data)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Обработка неожиданных ошибок
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{news_id}", response_model=dict)
async def get_news(news_id):
    news = await get_news_service(news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@router.get("/", response_model=dict)
async def list_news(limit: int = 10, offset: int = 0, is_published: Optional[bool] = None,
    order_by: Optional[str] = None, token: str = Depends(oauth2_scheme),):
    """
    Получить список новостей с возможностью фильтрации по статусу публикации.

    - **limit**: Максимальное количество новостей, которое будет возвращено.
    - **offset**: Смещение от начала списка.
    - **is_published**: Фильтрация новостей по статусу публикации.
    """
    return await list_news_service(limit, offset, is_published, order_by, token)

@router.put("/{news_id}", response_model=dict)
async def update_news(news_id: int, news: dict) -> dict:
    updated_news = await update_news_service(news_id, news)
    if not updated_news:
        raise HTTPException(status_code=404, detail="News not found")
    return updated_news

@router.delete("/{news_id}", response_model=dict)
async def delete_news(news_id: int) -> dict:
    if not await delete_news_service(news_id):
        raise HTTPException(status_code=404, detail="News not found")
    return {"detail": "News deleted"}
