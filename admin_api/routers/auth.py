# fastapi_app/routers/auth.py
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from admin_api.services.auth_service import authenticate_user, create_access_token, get_current_user, get_users_list
from admin_api.utils import SECRET_KEY, ALGORITHM, jwt, OAuth2PasswordBearer
from typing import List, Dict
from enum import Enum

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
# Login endpoint for user authentication
@router.post("/login", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Вызываем функцию для аутентификации пользователя и получения токена
    auth_token = await authenticate_user(form_data.username, form_data.password)

    # Если токен получен успешно, создаем и возвращаем токен доступа
    if auth_token:

        # Возвращаем токен и тип токена
        return auth_token

    # Возвращаем ошибку, если аутентификация не удалась
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )

# Endpoint to retrieve the current user's information
@router.get("/user", response_model=dict)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/users", response_model=List)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return await get_users_list(token)



class UserRole:
    GUEST = 'guest'
    JOURNALIST = 'journalist'
    SUPER_ADMIN = 'super_admin'

    ROLE_CHOICES = (
        (GUEST, 'Guest'),
        (JOURNALIST, 'Journalist'),
        (SUPER_ADMIN, 'Super Admin'),
    )



@router.get("/roles", response_model=List)
async def list_categories():
    # Формируем список категорий с их идентификаторами и названиями
    roles = [{"id": index + 1, "name": cat[0]} for index, cat in enumerate(UserRole.ROLE_CHOICES)]
    return roles