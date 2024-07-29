# fastapi_app/services/auth_service.py
from fastapi import APIRouter, HTTPException, Depends
import httpx
from typing import List, Dict
from fastapi import HTTPException, status
from admin_api.utils import SECRET_KEY, ALGORITHM, jwt, OAuth2PasswordBearer
from datetime import datetime, timedelta

# URL for Django authentication endpoint
DJANGO_API_URL = "http://django:8000/"

# OAuth2 scheme for bearer tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def authenticate_user(email: str, password: str):
    async with httpx.AsyncClient() as client:
        # Отправляем POST-запрос с email и паролем
        response = await client.post(f'{DJANGO_API_URL}api/token/', data={"email": email, "password": password})

        # Проверяем успешность ответа
        if response.status_code == 200:
            # Возвращаем токен из ответа
            return response.json()
        raise HTTPException(status_code=401, detail="Invalid credentials")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token for the authenticated user.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=30))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Retrieve current user information from Django API using JWT token.
    """
    # Установите заголовок авторизации с токеном
    headers = {"Authorization": f"Bearer {token}"}

    # Посылаем запрос к Django API
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{DJANGO_API_URL}auth/users/me/', headers=headers)

    # Если Django не смог аутентифицировать пользователя, возвращаем 401 ошибку
    if response.status_code != 200:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Получаем данные пользователя из ответа Django API
    user_data = response.json()
    return user_data


async def get_users_list(token: str) -> List:
    # Установите заголовок авторизации с токеном
    headers = {"Authorization": f"Bearer {token}"}
    print(headers)
    # Посылаем запрос к Django API
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{DJANGO_API_URL}auth/users/', headers=headers)

    # Если Django не смог аутентифицировать пользователя, возвращаем 401 ошибку
    if response.status_code != 200:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(response.json())
    # Получаем данные пользователя из ответа Django API
    user_data = response.json()
    return user_data