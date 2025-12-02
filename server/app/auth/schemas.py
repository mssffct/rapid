from pydantic import BaseModel
from uuid import UUID

class UserBase(BaseModel):
    name: str
    real_name: str | None = None
    state: str | None = None
    role: str | None = None

class UserCreate(UserBase):
    password: str


class User(UserBase):
    uuid: UUID
    state: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    name: str | None = None