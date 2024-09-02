from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Form, Depends, Request
from pydantic import BaseModel, EmailStr
from admin_api.utils import OAuth2PasswordBearer
from typing import List, Dict
from typing import Any
import httpx

# URL for Django authentication endpoint
DJANGO_API_URL = "http://django:8000/"

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class LoginRequest(BaseModel):
    username: str
    password: str


async def get_request_data(request: Request):
    content_type = request.headers.get('Content-Type', '')

    if 'application/json' in content_type:
        body = await request.json()
        return LoginRequest(**body)
    elif 'multipart/form-data' in content_type or 'application/x-www-form-urlencoded' in content_type:
        form_data = await request.form()
        return LoginRequest(username=form_data.get('username'), password=form_data.get('password'))
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported content type")


async def get_request_data_reg(request: Request):
    content_type = request.headers.get('Content-Type', '')

    if 'application/json' in content_type:
        body = await request.json()
        return {
            "email": body.get("email"),
            "password": body.get("password"),
            "role": body.get("role"),
            "first_name": body.get("first_name"),
            "last_name": body.get("last_name"),
            "phone_number": body.get("phone_number")
        }
    elif 'multipart/form-data' in content_type or 'application/x-www-form-urlencoded' in content_type:
        form_data = await request.form()
        return {
            "email": form_data.get("email"),
            "password": form_data.get("password"),
            "role": form_data.get("role"),
            "first_name": form_data.get("first_name"),
            "last_name": form_data.get("last_name"),
            "phone_number": form_data.get("phone_number")
        }
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported content type")


@router.post("/register", response_model=dict)
async def register_user(data: dict = Depends(get_request_data_reg)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{DJANGO_API_URL}auth/users/',
            data={
                "email": data.get("email"),
                "password": data.get("password"),
                "role": data.get("role"),
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "phone_number": data.get("phone_number")
            }
        )

        if response.status_code == 201:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code,
                                detail=response.json().get('detail', 'Registration failed'))


@router.post("/login", response_model=dict)
async def login_for_access_token(body: LoginRequest = Depends(get_request_data)):
    async with httpx.AsyncClient() as client:

        response = await client.post(f'{DJANGO_API_URL}api/token/',
                                     data={"email": body.username, "password": body.password})

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


@router.get("/user", response_model=dict)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{DJANGO_API_URL}auth/users/me/', headers=headers)

        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


@router.get("/users", response_model=List)
async def read_users_list(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{DJANGO_API_URL}auth/users/', headers=headers)

        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


class PasswordResetRequest(BaseModel):
    email: EmailStr  # Используем EmailStr для валидации email


class PasswordResetConfirmRequest(BaseModel):
    uid: str
    token: str
    new_password: str


@router.post("/reset_password", response_model=dict)
async def reset_password(data: PasswordResetRequest):
    """
    Эндпоинт для отправки запроса на сброс пароля.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{DJANGO_API_URL}auth/users/reset_password/',
            data=data.dict()  # Отправляем данные в формате формы
        )

        if response.status_code == 204:
            return {"detail": "Password reset e-mail has been sent."}

        try:
            error_detail = response.json().get("detail", "Error")
        except ValueError:
            error_detail = "Unexpected error"

        raise HTTPException(status_code=response.status_code, detail=error_detail)


@router.post("/reset_password_confirm", response_model=dict)
async def reset_password_confirm(data: PasswordResetConfirmRequest):
    """
    Эндпоинт для подтверждения сброса пароля.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{DJANGO_API_URL}auth/users/reset_password_confirm/',
            data=data.dict()  # Отправляем данные в формате формы
        )

        if response.status_code == 204:
            return {"detail": "Password has been reset successfully."}

        try:
            error_detail = response.json().get("detail", "Error")
        except ValueError:
            error_detail = "Unexpected error"

        raise HTTPException(status_code=response.status_code, detail=error_detail)
