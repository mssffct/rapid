import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.auth.schemas import TokenData, User as PydanticUser # Pydantic User
from app.models import User as DBUser # SQLAlchemy User


ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Конфигурация хеширования паролей ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Хеширует пароль."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие открытого пароля хешированному."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT токен доступа."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_user(db_session: AsyncSession, name: str) -> Optional[DBUser]:
    """Получает пользователя из базы данных."""
    result = await db_session.execute(select(DBUser).filter(DBUser.name == name))
    return result.scalar_one_or_none()

async def authenticate_user(db_session: AsyncSession, username: str, password: str) -> Optional[PydanticUser]:
    """Аутентифицирует пользователя по имени и паролю."""
    user = await get_user(db_session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return PydanticUser(**user.__dict__)