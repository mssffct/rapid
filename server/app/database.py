import json

from uuid import uuid4, UUID
from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.types import TypeDecorator, TEXT
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncAttrs,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from app.config import get_db_url
from app.core.managers.crypto import CryptoManager

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# настройка аннотаций
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)
]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class EncryptedJSONType(TypeDecorator):
    impl = TEXT
    cache_ok = True

    async def process_bind_param(self, value, dialect):
        """
        Обрабатывает значение перед сохранением в БД (шифрует).
        """
        if value is None:
            return None
        if not isinstance(value, dict):
            raise TypeError("EncryptedJSONType ожидает словарь.")

        # encrypt_data возвращает bytes, TEXT поле ожидает str
        return CryptoManager.manager().encrypt_data(value).decode("utf-8")

    async def process_result_value(self, value, dialect):
        """
        Обрабатывает значение после извлечения из БД (дешифрует).
        """
        if value is None:
            return None

        try:
            # value будет строкой из БД, но decrypt_data ожидает bytes
            return await CryptoManager.manager().decrypt_data(value.encode("utf-8"))
        except Exception as e:
            # Логирование ошибки или поднятие кастомной ошибки
            print(f"Ошибка дешифрования данных из БД: {e}")
            return None  # Или поднять исключение HTTPException

    async def copy_value(self, value):
        # Глубокая копия для изменяемых объектов (словарей)
        if value is not None:
            return json.loads(
                json.dumps(value)
            )  # Простой способ глубокой копии для JSON
        return value


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class ManagedDBModel(Base):
    __abstract__ = True

    data: Mapped[str] = mapped_column(EncryptedJSONType, nullable=True)


async def get_db_session():
    """FastAPI dependency to get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Creates database tables for app and testing"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
