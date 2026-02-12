from app.users.models import User as DBUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_user(db_session: AsyncSession, name: str) -> DBUser | None:
    """Get user from db"""
    result = await db_session.execute(select(DBUser).filter(DBUser.name == name))
    return result.scalar_one_or_none()
