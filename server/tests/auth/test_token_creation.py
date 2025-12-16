import pytest
import typing
from datetime import datetime, timedelta, timezone
from fastapi import status
from app.config import settings
from app.auth.security import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.types.auth import UserRole
from tests.conftest import API_URL
from tests.fixtures.auth import create_user, PASSWD
from jose import jwt


if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from httpx import AsyncClient

URL = "/auth"
ADMIN = {"username": "admin1", "password": "Qgt^75"}


@pytest.mark.asyncio
async def test_login(client: "AsyncClient", test_session: "AsyncSession"):
    empty_base_response = await client.post(
        f"{API_URL}{URL}/login",
        data={"username": ADMIN.get("username"), "password": ADMIN.get("password")},
    )
    assert empty_base_response.status_code == status.HTTP_401_UNAUTHORIZED
    # creating user
    user = await create_user(test_session, UserRole.PLAIN_USER)
    # corrupted login
    corrupted_login_data = await client.post(
        f"{API_URL}{URL}/login",
        data={"username": user.name, "password": "corrupted_password"},
    )
    assert corrupted_login_data.status_code == status.HTTP_401_UNAUTHORIZED
    # creds are correct
    login_result = await client.post(
        f"{API_URL}{URL}/login", data={"username": user.name, "password": PASSWD}
    )
    data = login_result.json()
    token = data.get("access_token")
    assert login_result.status_code == status.HTTP_200_OK
    assert "access_token" in data
    token_payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    # data set to token correctly
    assert user.name == token_payload.get("sub")
    expected_expiry = (
        datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    ).timestamp()
    assert token_payload.get("exp") == pytest.approx(expected_expiry)
    # routes are available
    response = await client.get(
        f"{API_URL}/routes_available", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    # change expiry
    expired = datetime.now(timezone.utc) - timedelta(minutes=3)
    expired_token = jwt.encode(
        {"sub": user.name, "exp": expired},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    # routes are unavailable
    response = await client.get(
        f"{API_URL}/routes_available",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "Signature has expired."
