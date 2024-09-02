from pydantic import BaseSettings


class Settings(BaseSettings):
    django_api_url: str = "http://django:8000/api"

    class Config:
        env_file = ".env"


settings = Settings()
