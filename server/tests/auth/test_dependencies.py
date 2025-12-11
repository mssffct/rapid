import typing
import pytest
from fastapi import status
from tests.conftest import API_URL

from app.core.consts import NOT_AUTHENTICATED

if typing.TYPE_CHECKING:
    from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user_dependency(client: "AsyncClient"):
    # default app route gives result
    result = await client.get(f"{API_URL}")
    assert result.status_code == status.HTTP_200_OK
    assert "message" in result.json()
    # any protected route gives 401
    fail = await client.get(f"{API_URL}/admin_routes/")
    assert fail.status_code == status.HTTP_401_UNAUTHORIZED
    assert fail.json().get("detail") == NOT_AUTHENTICATED
