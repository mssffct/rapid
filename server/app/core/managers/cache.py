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
    def manager() -> "CacheManager":
        return CacheManager()

    async def get(self, owner: str, delete: bool = False) -> DBCache | None:
        if self.db_session:
            cached_ins = await self.db_session.get(DBCache, owner)
            if cached_ins:
                valid = await self.validate(cached_ins)
                if not valid or delete:
                    await atomic_op(self.db_session, Ops.DEL, cached_ins)
            return cached_ins
        return None

    async def pop(self):
        return await self.get(delete=True)

    async def put(self, owner: str, data: Any):
        pass

    @staticmethod
    async def validate(ins: "DBCache") -> bool:
        now = datetime.now(timezone.utc)
        return False if now > ins.created_at + timedelta(seconds=ins.validity) else True