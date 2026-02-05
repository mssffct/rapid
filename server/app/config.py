import os
import typing

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SECRET_KEY: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )
    ALGORITHM: str = "HS256"
    ENCRYPTION_KEY: str | None = None

    @field_validator("POSTGRES_HOST", mode="before")
    @classmethod
    def get_postgres_host(cls, val: str) -> str:
        return "db" if os.getenv("DOCKERIZED") else val


settings = Settings()


def get_db_url(database: typing.Optional[str] = None):
    return (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{database or settings.POSTGRES_DB}"
    )
