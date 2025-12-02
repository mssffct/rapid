# users/schemas.py
from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    name: str
    real_name: str | None = None
    role: str | None = None
    state: str | None = None
    password: str

class UserResponse(BaseModel):
    uuid: UUID
    name: str
    real_name: str | None = None
    state: str | None = None
    role: str | None = None

    class Config:
        from_attributes = True # Для SQLAlchemy 1.4: orm_mode = True