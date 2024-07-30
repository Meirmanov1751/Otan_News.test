from fastapi import FastAPI
from admin_api.routers import news, comments, auth, categories, lang, tags, quote

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="FastAPI News Service",
    description="API for managing news articles and related content",
    version="1.0.0",
    docs_url="/api/admin/docs",
    redoc_url=None,
    openapi_url="/api/admin/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Register routers
app.include_router(categories.router, prefix="/api/admin/categories", tags=["categories"])
app.include_router(lang.router, prefix="/api/admin/language", tags=["language"])
app.include_router(news.router, prefix="/api/admin/news", tags=["News"])
app.include_router(tags.router, prefix="/api/admin/tags", tags=["Tags"])
app.include_router(quote.router, prefix="/api/admin/quote", tags=["Quote"])
app.include_router(comments.router, prefix="/api/admin/comments", tags=["Comments"])
app.include_router(auth.router, prefix="/api/admin/auth", tags=["auth"])
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI News Service!"}
