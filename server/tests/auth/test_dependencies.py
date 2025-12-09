from fastapi import status
from tests.conftest import client, test_db, API_URL

from app.core.consts import NOT_AUTHENTICATED


def test_get_user_dependency(test_db):
    # default app route gives result
    result = client.get(f'{API_URL}')
    assert result.status_code == status.HTTP_200_OK
    assert "message" in result.json()
    # any protected route gives 401
    fail = client.get(f"{API_URL}/admin_routes")
    assert fail.status_code == status.HTTP_401_UNAUTHORIZED
    assert fail.json().get("detail") == NOT_AUTHENTICATED