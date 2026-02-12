import typing

from pydantic import BaseModel
from uuid import UUID
from typing_extensions import Annotated, Doc
from fastapi.param_functions import Form

from app.core.types.auth import UserRole, AuthType
from app.core.types.states import AvailabilityState


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


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    result: str


class TokenData(BaseModel):
    name: typing.Optional[str] = None
    exp: typing.Optional[int] = None


class AuthenticatorBase(BaseModel):
    name: str
    auth_type: AuthType


class AuthenticatorResponse(AuthenticatorBase):
    uuid: UUID


class AuthenticatorCreate(AuthenticatorBase):
    state: AvailabilityState
    priority: int
    mfa: typing.Optional[UUID]


class LoginForm:
    def __init__(
        self,
        *,
        username: Annotated[
            str,
            Form(),
            Doc(
                """
                `username` string. The OAuth2 spec requires the exact field name
                `username`.
                """
            ),
        ],
        password: Annotated[
            str,
            Form(json_schema_extra={"format": "password"}),
            Doc(
                """
                `password` string. The OAuth2 spec requires the exact field name
                `password`.
                """
            ),
        ],
        # TODO add empty value
        authenticator: Annotated[
            str,
            Form(),
            Doc(
                """
                authenticator uuid
                """
            ),
        ],
    ):
        self.username = username
        self.password = password
        self.authenticator = authenticator
