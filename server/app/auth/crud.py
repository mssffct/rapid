from typing import TYPE_CHECKING
from sqlalchemy.future import select
from app.auth.models import Authenticator
from app.core.types.states import AvailabilityState


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_authenticator(
    db_session: "AsyncSession", auth_id: str | None
) -> Authenticator | None:
    """
    Checks if authenticator exists and not disabled
    Returns valid authenticator
    """
    query = await db_session.execute(
        select(Authenticator).filter(Authenticator.uuid == auth_id)
    )
    auth = query.scalar_one_or_none()
    if not auth:
        raise ValueError("Authenticator not exists")
    if auth.state == AvailabilityState.DISABLED:
        raise ValueError("Authenticator is disabled")
    return auth
