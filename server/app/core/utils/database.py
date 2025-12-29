from typing import TYPE_CHECKING, Any
from fastapi import HTTPException, status
from sqlalchemy.future import select


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlmodel import SQLModel


async def check_exists(
    session: "AsyncSession", model: "SQLModel", field: str, value: Any
):
    existing = await session.execute(
        select(model).filter(getattr(model, field) == value)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
