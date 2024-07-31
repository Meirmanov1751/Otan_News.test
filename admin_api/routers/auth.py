from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from admin_api.utils import OAuth2PasswordBearer
from typing import List, Dict
import httpx

# URL for Django authentication endpoint
DJANGO_API_URL = "http://django:8000/"

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/login", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{DJANGO_API_URL}api/token/',
                                     data={"email": form_data.username, "password": form_data.password})

        if response.status_code == 200:
            return response.json()
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


@router.post("/reset_password", response_model=dict)
async def reset_password(data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{DJANGO_API_URL}auth/users/reset_password/', data=data.dict())

        if response.status_code == 204:
            return {"detail": "Password reset e-mail has been sent."}
        raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))


@router.post("/reset_password_confirm", response_model=dict)
async def reset_password_confirm(data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{DJANGO_API_URL}auth/users/reset_password_confirm/', data=data.dict())

        if response.status_code == 204:
            return {"detail": "Password has been reset successfully."}
        raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error"))
