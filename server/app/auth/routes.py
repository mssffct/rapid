from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.auth.schemas import Token, User as PydanticUser
from app.auth.security import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.dependencies import get_current_user, get_current_active_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_db_session) # Добавляем зависимость от сессии БД
):
    """
    Эндпоинт для входа пользователя и получения JWT токена.
    """
    user = await authenticate_user(db_session, form_data.username, form_data.password) # Передаем db_session
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=PydanticUser)
async def read_users_me(current_user: PydanticUser = Depends(get_current_user)):
    """
    Защищенный эндпоинт для получения информации о текущем пользователе.
    """
    return current_user

@router.get("/users/me/active/", response_model=PydanticUser)
async def read_users_me_active(current_active_user: PydanticUser = Depends(get_current_active_user)):
    """
    Защищенный эндпоинт для получения информации о текущем активном пользователе.
    """
    return current_active_user