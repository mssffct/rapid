from fastapi import APIRouter, Depends, status, HTTPException
from typing import TYPE_CHECKING
from sqlalchemy.future import select
from uuid import UUID
from app.auth.dependencies import PermissionManager
from app.auth.schemas import User as PydanticUser
from app.core.types.states import UserState
from app.core.managers.crypto import CryptoManager
from app.database import get_db_session
from app.users.models import User as DBUser, UsersGroup
from app.users.schemas import UserCreate, UserResponse, UserUpdate


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    current_user: PydanticUser = Depends(PermissionManager({"LA", "SA"})),
    db_session: "AsyncSession" = Depends(get_db_session),
):
    """
    Create new user
    """
    existing = await db_session.execute(
        select(DBUser)
        .filter(DBUser.name == user.name)
        .filter(DBUser.groups.any(UsersGroup.uuid.in_(user.groups)))
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = CryptoManager.get_password_hash(user.password)

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
    user_id: UUID,
    user: UserUpdate,
    current_user: PydanticUser = Depends(PermissionManager({"LA", "SA"})),
    db_session: "AsyncSession" = Depends(get_db_session),
):
    """Update user data"""
    user_to_update = await db_session.execute(
        select(DBUser).filter(DBUser.uuid == user_id)
    )
    print(user_to_update.scalar())
