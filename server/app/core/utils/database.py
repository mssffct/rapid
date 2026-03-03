import enum
from typing import TYPE_CHECKING, Any
from fastapi import HTTPException, status
from sqlalchemy.future import select


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlmodel import SQLModel


class Ops(enum.StrEnum):
    DEL = "DEL"
    UPD = "UPD"
    ADD = "ADD"


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


async def atomic_op(db_session: "AsyncSession", op: Ops, ins: Any) -> bool:
    async with db_session as session:
        try:
            match op:
                case Ops.ADD:
                    session.add(ins)
                case Ops.DEL:
                    await session.delete(ins)
            await session.commit()
            return True
        except Exception as e:
            print(e)
            await session.rollback()
            return False
