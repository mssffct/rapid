from typing import Any, TYPE_CHECKING

from datetime import datetime, timezone, timedelta

from app.core.utils.database import atomic_op, Ops
from app.models import Cache as DBCache
from sqlalchemy.future import select

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class CacheManager:
    """Caching implementation for db-cache or Redis cache"""

    def __init__(self, db_session: "AsyncSession | None" = None):
        self.db_session = db_session

    @staticmethod
    def manager(**kwargs) -> "CacheManager":
        return CacheManager(**kwargs)

    async def get(self, owner: str, delete_after: bool = False) -> DBCache | None:
        if self.db_session:
            query = await self.db_session.execute(
                select(DBCache).filter_by(owner=owner)
            )
            cached_ins = query.scalar_one_or_none()
            if cached_ins:
                valid = await self.validate(cached_ins)
                if not valid or delete_after:
                    await atomic_op(self.db_session, Ops.DEL, cached_ins)
                    return cached_ins
            return cached_ins
        return None

    async def pop(self, owner: str):
        return await self.get(owner, delete_after=True)

    async def put(self, owner: str, data: Any, validity: int) -> bool:
        if self.db_session:
            cache_ins = DBCache(owner=owner, data=data, validity=validity)
            result = await atomic_op(self.db_session, op=Ops.ADD, ins=cache_ins)
            return result
        return False

    @staticmethod
    async def validate(ins: "DBCache") -> bool:
        now = datetime.now(timezone.utc)
        return False if now > ins.created_at + timedelta(seconds=ins.validity) else True
