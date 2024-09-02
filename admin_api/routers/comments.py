from typing import List  # Import the List type

from fastapi import APIRouter, HTTPException
from admin_api.models.comments import CommentRequest, CommentResponse
from admin_api.services.comments_service import (
    create_comment_service,
    get_comment_service,
    delete_comment_service,
)

router = APIRouter()


@router.post("/", response_model=CommentResponse)
async def create_comment(comment: CommentRequest) -> CommentResponse:
    return await create_comment_service(comment)


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int) -> CommentResponse:
    comment = await get_comment_service(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.delete("/{comment_id}", response_model=dict)
async def delete_comment(comment_id: int) -> dict:
    if not await delete_comment_service(comment_id):
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"detail": "Comment deleted"}
