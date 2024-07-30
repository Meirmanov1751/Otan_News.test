from typing import List  # Import the List type
from typing import Optional
from fastapi import APIRouter, HTTPException
from admin_api.services.quote_services import (
    create_quote_service,
    get_quote_service,
    list_quote_service,
    update_quote_service,
    delete_quote_service,
)

router = APIRouter()



@router.post("/", response_model=dict)
async def create_quote(quote: dict):
    try:
        return await create_quote_service(quote)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Обработка неожиданных ошибок
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{quote_id}", response_model=dict)
async def get_quote(quote_id):
    quote = await get_quote_service(quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="quote not found")
    return quote


@router.get("/", response_model=dict)
async def list_quote(limit: int = 10, offset: int = 0, is_published: Optional[bool] = None):
    """
    Получить список новостей с возможностью фильтрации по статусу публикации.

    - **limit**: Максимальное количество новостей, которое будет возвращено.
    - **offset**: Смещение от начала списка.
    - **is_published**: Фильтрация новостей по статусу публикации.
    """
    return await list_quote_service(limit, offset, is_published)

@router.put("/{quote_id}", response_model=dict)
async def update_quote(quote_id: int, quote: dict) -> dict:
    updated_quote = await update_quote_service(quote_id, quote)
    if not updated_quote:
        raise HTTPException(status_code=404, detail="quote not found")
    return updated_quote

@router.delete("/{quote_id}", response_model=dict)
async def delete_quote(quote_id: int) -> dict:
    if not await delete_quote_service(quote_id):
        raise HTTPException(status_code=404, detail="quote not found")
    return {"detail": "quote deleted"}
