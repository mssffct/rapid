from fastapi import status
from tests.conftest import client, test_db, API_URL

URL = "/auth"
ADMIN = {
    "username": "admin1",
    "password": "Qgt^75"
}


def test_obtain_token(test_db):
    empty_base_response = client.post(
        f'{API_URL}{URL}/obtain_token',
        data={"username": ADMIN.get("username"), "password": ADMIN.get("password")}
    )
    assert empty_base_response.status_code == status.HTTP_401_UNAUTHORIZED