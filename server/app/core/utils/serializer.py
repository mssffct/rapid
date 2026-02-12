from typing import Any
from app.core.managers.crypto import CryptoManager


async def serialize(obj: Any) -> bytes:
    data = await CryptoManager.manager().encrypt_data(obj)
    return data