from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.auth.schemas import TokenData, User as PydanticUser # Pydantic User
from app.auth.security import get_user
from app.core_types.states import UserStates
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db_session: AsyncSession = Depends(get_db_session)
) -> PydanticUser:
    """Зависимость для получения текущего пользователя из JWT токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data = TokenData(name=name)
    except JWTError:
        raise credentials_exception
    user = await get_user(db_session, token_data.name) # Используем db_session
    if user is None:
        raise credentials_exception
    return PydanticUser(**user.__dict__) # Преобразуем объект DBUser в PydanticUser

async def get_current_active_user(current_user: PydanticUser = Depends(get_current_user)) -> PydanticUser:
    """Зависимость для получения текущего активного пользователя."""
    if current_user.state in (UserStates.INACTIVE, UserStates.BLOCKED):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive or blocked user")
    return current_user