import pytest
import httpx
from fastapi import status
from app.core.types.auth import UserRole
from tests.conftest import API_URL
from tests.fixtures.auth import create_user, PASSWD
from sqlalchemy.ext.asyncio import AsyncSession

URL = "/auth"
ADMIN = {"username": "admin1", "password": "Qgt^75"}


@pytest.mark.asyncio
async def test_obtain_token(client: httpx.AsyncClient, test_session: AsyncSession):
    empty_base_response = await client.post(
        f"{API_URL}{URL}/obtain_token",
        data={"username": ADMIN.get("username"), "password": ADMIN.get("password")},
    )
    assert empty_base_response.status_code == status.HTTP_401_UNAUTHORIZED
    # creating user
    user = await create_user(test_session, UserRole.PLAIN_USER)
    # corrupted login
    corrupted_login_data = await client.post(
        f"{API_URL}{URL}/obtain_token",
        data={"username": user.name, "password": "corrupted_password"},
    )
    assert corrupted_login_data.status_code == status.HTTP_401_UNAUTHORIZED
    # creds are correct
    login_result = await client.post(
        f"{API_URL}{URL}/obtain_token", data={"username": user.name, "password": PASSWD}
    )
    assert login_result.status_code == status.HTTP_200_OK
    assert "access_token" in login_result.json()
