from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.core.types.states import UserState
from app.database import get_db_session
from app.models import User as DBUser
from app.users.schemas import UserCreate, UserResponse, UserUpdate
from app.auth.security import get_password_hash

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, db_session: AsyncSession = Depends(get_db_session)
):
    """
    Create new user
    """
    existing_user = await db_session.execute(
        select(DBUser).filter(DBUser.name == user.name)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(user.password)

    db_user = DBUser(
        name=user.name,
        real_name=user.real_name,
        password=hashed_password,
        role=user.role,
        state=UserState.ACTIVE,
    )

    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)

    return db_user


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: UUID, user: UserUpdate, db_session: AsyncSession = Depends(get_db_session)
):
    """Update user data"""
    user_to_update = await db_session.execute(
        select(DBUser).filter(DBUser.uuid == user_id)
    )
    print(user_to_update.scalar())
