# fastapi_app/main.py

import os
import django
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from user.models import User
from Otan_news.models import Post, Link

app = FastAPI()

class PostCreate(BaseModel):
    author_id: int
    title: str
    short_description: str = None
    description: str

class PostRead(BaseModel):
    id: int
    author_id: int
    title: str
    short_description: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@app.post("/posts/", response_model=PostRead)
def create_post(post: PostCreate):
    author = User.objects.get(id=post.author_id)
    db_post = Post.objects.create(
        author=author,
        title=post.title,
        short_description=post.short_description,
        description=post.description,
    )
    return db_post

@app.get("/news/{news_id}", response_model=PostRead)
def read_post(news_id: int):
    try:
        db_post = Post.objects.get(id=news_id)
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
