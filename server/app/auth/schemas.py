import typing

from pydantic import BaseModel
from uuid import UUID

from app.core.types.auth import UserRole


class UserBase(BaseModel):
    name: str
    real_name: str | None = None
    state: str | None = None
    role: str | None = None

    def is_admin(self):
        """Check if user has admin rights"""
        return self.role in (UserRole.STAFF_ADMIN, UserRole.LICENSE_ADMIN)


class UserCreate(UserBase):
    password: str


class User(UserBase):
    uuid: UUID
    state: str

    class ConfigDict:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: typing.Optional[str] = None
    exp: typing.Optional[int] = None
