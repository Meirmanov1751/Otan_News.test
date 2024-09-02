import httpx

http_client = httpx.AsyncClient()

# fastapi_app/utils/jwt_utils.py
from datetime import timedelta
import datetime
from pydantic import BaseModel
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Secret key for JWT signing
SECRET_KEY = "django-insecure-1leu%4qcxx^80d&&7o^*(5zw4e7al774*auu^ckn1t99m)wd!)"  # Replace with a secure key
ALGORITHM = "HS256"

# admin_api/utils.py


# Определение OAuth2 схемы
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# Модель для токена
class Token(BaseModel):
    access_token: str
    token_type: str


# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Зависимость для извлечения текущего пользователя из токена
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"email": username}
