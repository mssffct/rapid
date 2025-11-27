from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core_types.states import UserStates
from app.database import get_db_session
from app.models import User as DBUser
from app.users.schemas import UserCreate, UserResponse
from app.auth.security import get_password_hash  # Для хеширования пароля

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
        user: UserCreate,
        db_session: AsyncSession = Depends(get_db_session)
):
    """
    Эндпоинт для создания нового пользователя.
    """
    # Проверяем, существует ли пользователь с таким именем
    existing_user = await db_session.execute(
        select(DBUser).filter(DBUser.name == user.name)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # Хешируем пароль
    hashed_password = get_password_hash(user.password)

    # Создаем нового пользователя
    db_user = DBUser(
        name=user.name,
        real_name=user.real_name,
        password=hashed_password,
        role=user.role,
        state=UserStates.ACTIVE
    )

    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)  # Обновляем объект, чтобы получить id из БД

    return db_user