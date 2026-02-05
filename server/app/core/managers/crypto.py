import bcrypt
import json

from cryptography.fernet import Fernet

from app.core.utils import singleton
from app.config import settings
from app.core.exceptions import NoEncryptionKey


class CryptoManager(metaclass=singleton.Singleton):
    _fernet_ins: "Fernet"

    def __init__(self):
        # from cryptography.fernet import Fernet
        # fernet_key = Fernet.generate_key()
        # print(fernet_key.decode()) -> .env
        self.get_fernet_ins()

    @staticmethod
    def manager() -> 'CryptoManager':
        return CryptoManager()

    def get_fernet_ins(self) -> None:
        key = settings.ENCRYPTION_KEY
        if key:
            if isinstance(key, str):
                key = key.encode('utf-8')
            self._fernet_ins = Fernet(key)
        else:
            raise NoEncryptionKey


    def encrypt_data(self, data: dict) -> bytes:
        """Encrypt data"""
        json_data = json.dumps(data)
        encrypted_bytes = self._fernet_ins.encrypt(json_data.encode('utf-8'))
        return encrypted_bytes

    def decrypt_data(self, encrypted_bytes: bytes) -> dict:
        """Дешифрует байты в словарь данных."""
        decrypted_bytes = self._fernet_ins.decrypt(encrypted_bytes)
        json_data = decrypted_bytes.decode('utf-8')
        data = json.loads(json_data)
        return data

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