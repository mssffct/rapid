import bcrypt

from pathlib import Path
from typing import TYPE_CHECKING, cast

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from app.core.utils import singleton

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey


class CryptoManager(metaclass=singleton.Singleton):
    _rsa: "RSAPrivateKey"

    def __init__(self):
        #  openssl genrsa -out private.pem 2048 command in server directory on app deploy
        self._rsa = cast(
            "RSAPrivateKey",
            serialization.load_pem_private_key(self.read_rsa_key(), password=None, )
        )

    @staticmethod
    def read_rsa_key():
        rsa = Path("/app/private.pem")  # change to more safe in future
        with open(rsa, "r") as file:
            res = file.read()
        return res.encode()

    @staticmethod
    def manager() -> 'CryptoManager':
        return CryptoManager()

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Хеширует пароль."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверяет соответствие открытого пароля хешированному."""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )