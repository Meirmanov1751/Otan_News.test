from typing import List  # Import the List type
from typing import Optional
from fastapi import APIRouter, HTTPException
from admin_api.services.lang_services import (
    create_language_service,
    get_language_service,
    delete_language_service,
    list_language_service
)

router = APIRouter()

@router.post("/", response_model=dict)
async def create_comment(language: dict) -> dict:
    return await create_language_service(language)

@router.get("/", response_model=dict)
async def list_tags(limit: int = 10, offset: int = 0, is_published: Optional[bool] = None):
    """
    Получить список новостей с возможностью фильтрации по статусу публикации.

    - **limit**: Максимальное количество новостей, которое будет возвращено.
    - **offset**: Смещение от начала списка.
    - **is_published**: Фильтрация новостей по статусу публикации.
    """
    return await list_language_service(limit, offset, is_published)

@router.get("/{language_id}", response_model=dict)
async def get_comment(language_id: int) -> dict:
    comment = await get_language_service(language_id)
    if not comment:
        raise HTTPException(status_code=404, detail="language not found")
    return comment

@router.delete("/{language_id}", response_model=dict)
async def delete_comment(language_id: int) -> dict:
    if not await delete_language_service(language_id):
        raise HTTPException(status_code=404, detail="language not found")
    return {"detail": "language deleted"}
