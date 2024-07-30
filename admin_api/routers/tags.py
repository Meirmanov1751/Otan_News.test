from typing import List  # Import the List type
from typing import Optional
from fastapi import APIRouter, HTTPException
from admin_api.services.tags_services import (
    create_tags_service,
    get_tags_service,
    list_tags_service,
    update_tags_service,
    delete_tags_service,
)

router = APIRouter()



@router.post("/", response_model=dict)
async def create_tags(tags: dict):
    try:
        return await create_tags_service(tags)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Обработка неожиданных ошибок
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tags_id}", response_model=dict)
async def get_tags(tags_id):
    tags = await get_tags_service(tags_id)
    if not tags:
        raise HTTPException(status_code=404, detail="tags not found")
    return tags


@router.get("/", response_model=dict)
async def list_tags(limit: int = 10, offset: int = 0, is_published: Optional[bool] = None):
    """
    Получить список новостей с возможностью фильтрации по статусу публикации.

    - **limit**: Максимальное количество новостей, которое будет возвращено.
    - **offset**: Смещение от начала списка.
    - **is_published**: Фильтрация новостей по статусу публикации.
    """
    return await list_tags_service(limit, offset, is_published)

@router.put("/{tags_id}", response_model=dict)
async def update_tags(tags_id: int, tags: dict) -> dict:
    updated_tags = await update_tags_service(tags_id, tags)
    if not updated_tags:
        raise HTTPException(status_code=404, detail="tags not found")
    return updated_tags

@router.delete("/{tags_id}", response_model=dict)
async def delete_tags(tags_id: int) -> dict:
    if not await delete_tags_service(tags_id):
        raise HTTPException(status_code=404, detail="tags not found")
    return {"detail": "tags deleted"}
