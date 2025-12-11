import random
import string
import typing

from app.core.types.auth import UserRole
from app.core.types.states import UserState
from app.models import User
from app.auth.security import get_password_hash


USERNAMES = [f"user_{index}" for index in range(10)]
PASSWD = "A8s*^ThYq1"


async def create_user(test_session, role: UserRole) -> typing.Optional[User]:
    name = random.choice(USERNAMES)
    real_name = f"{name} {random.choice(string.ascii_letters)}"
    user = User(
        name=name,
        real_name=real_name,
        password=get_password_hash(PASSWD),
        role=role,
        state=UserState.ACTIVE,
    )
    try:
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        return user
    except Exception as e:
        print(e)
