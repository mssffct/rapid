from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.future import select
from typing import TYPE_CHECKING
from datetime import datetime, timezone, timedelta
from app.database import Base


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class Cache(Base):
    __tablename__ = "cache_table"

    owner: Mapped[str] = mapped_column(String(128), default="unknown")
    key: Mapped[str] = mapped_column(String(128))
    value: Mapped[str]

    validity: Mapped[int]  # validity in seconds

    @staticmethod
    async def purge(db_session: "AsyncSession") -> None:
        try:
            now = datetime.now(timezone.utc)
            result = await db_session.execute(select(Cache))
            for item in result.all():
                if now > item.created_at + timedelta(seconds=item.validity):
                    await db_session.delete(item)
                    await db_session.commit()
        except Exception:
            await db_session.rollback()
