from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db_session
from app.auth.schemas import TokenData, User as PydanticUser
from app.auth.security import get_user
from app.config import settings
from app.exceptions import raise_401_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

all_roles = {"SA", "LA", "PU", "D"}

class PermissionManager:
    def __init__(self, allowed_roles: str | set[str]):
        self.allowed_roles = all_roles if allowed_roles == "ALL" else allowed_roles

    async def __call__(
        self,
        token: str = Depends(oauth2_scheme),
        db_session: AsyncSession = Depends(get_db_session),
    ) -> PydanticUser:
        """Get current user from token dependency and check if user is permitted"""
        payload: dict = {}
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            name: str = payload.get("sub")
            if name is None:
                await raise_401_exception("Could not validate credentials")
        except JWTError as e:
            await raise_401_exception(str(e))
        token_data = TokenData(name=payload.get("sub"), exp=payload.get("exp"))
        user = await get_user(db_session, token_data.name)
        if user is None:
            await raise_401_exception("Could not validate credentials")
        if user.role not in self.allowed_roles:
            await raise_401_exception("Not allowed")
        return PydanticUser(**user.__dict__)
