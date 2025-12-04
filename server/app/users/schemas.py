# users/schemas.py
from pydantic import BaseModel
from uuid import UUID


class UserCreate(BaseModel):
    name: str
    real_name: str | None = None
    role: str | None = None
    state: str | None = None
    password: str


class UserUpdate(BaseModel):
    uuid: UUID
    name: str
    real_name: str | None = None
    state: str | None = None
    role: str | None = None


class UserResponse(BaseModel):
    uuid: UUID
    name: str
    real_name: str | None = None
    state: str | None = None
    role: str | None = None

    class ConfigDict:
        from_attributes = True
