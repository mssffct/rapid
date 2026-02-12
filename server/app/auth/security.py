from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from jose import jwt

from app.config import settings
from app.auth.schemas import User as PydanticUser
from app.core.managers.crypto import CryptoManager
from app.users.crud import get_user

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создает JWT токен доступа."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(
    db_session: "AsyncSession", username: str, password: str
) -> PydanticUser | None:
    """Аутентифицирует пользователя по имени и паролю."""
    user = await get_user(db_session, username)
    if not user:
        return None
    if not CryptoManager.verify_password(password, user.password):
        return None
    return PydanticUser(**user.__dict__)
