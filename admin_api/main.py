from fastapi import FastAPI
from admin_api.routers import news, comments, auth, categories

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="FastAPI News Service",
    description="API for managing news articles and related content",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(auth.router, prefix="/", tags=["auth"])
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI News Service!"}
