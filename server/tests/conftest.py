import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from app.main import app
from app.config import get_db_url
from app.database import Base, get_db_session

API_URL = "/api/v1"

TEST_DATABASE_URL = get_db_url("test")

test_engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession
)


@pytest_asyncio.fixture(scope="function", name="test_session", autouse=True)
async def test_session():
    async with test_engine.begin() as conn:
        # TODO think about cleaning db
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture(scope="function", name="client", autouse=True)
async def client(test_session):
    app.dependency_overrides[get_db_session] = lambda: test_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function", autouse=True)
async def close_engine():
    yield
    await test_engine.dispose()
