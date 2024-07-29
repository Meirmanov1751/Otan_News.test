from pydantic import BaseModel, Field
from typing import Optional, List

class NewsTranslation(BaseModel):
    lang_id: int
    title: str
    text: str

class Tag(BaseModel):
    id: int
    name: str

class NewsRequest(BaseModel):
    category: str = Field(..., title="Category of the news", max_length=100)
    subcategory: Optional[str] = Field(None, title="Subcategory of the news", max_length=100)
    author_id: int = Field(..., title="ID of the author")
    quote_id: Optional[int] = Field(None, title="ID of the quote, if any")
    exclusive: bool = Field(default=False, title="Is this news exclusive")
    translations: Optional[List[NewsTranslation]] = Field(None, title="List of translations")
    tags: Optional[List[int]] = Field(None, title="List of tag IDs")
    image: Optional[str] = Field(None, title="URL of the image")

class NewsResponse(BaseModel):
    id: int
    category: str
    subcategory: Optional[str] = None
    author_id: int
    quote_id: Optional[int] = None
    exclusive: bool
    translations: List[NewsTranslation] = []
    tags: List[Tag] = []
    image: Optional[str] = None
    views: int
    created_at: str
    updated_at: str
