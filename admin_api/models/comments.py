from pydantic import BaseModel, Field
from typing import Optional


class CommentRequest(BaseModel):
    comment: str = Field(..., title="Comment text")
    news_id: int = Field(..., title="ID of the related news article")
    user_id: int = Field(..., title="ID of the user making the comment")


class CommentResponse(BaseModel):
    id: int
    comment: str
    news_id: int
    user_id: int
    created_at: str
