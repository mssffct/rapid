from app.core.managers.crypto import CryptoManager
from app.core.utils.singleton import Singleton


cm = CryptoManager.manager()

def test_cm_init():
    cm2 = CryptoManager.manager()
    assert isinstance(CryptoManager, Singleton)
    assert id(cm) == id(cm2)

def test_cm_pass_hash():
    passwd = "SUPERSECRET"
    hashed = cm.get_password_hash(passwd)
    assert cm.verify_password(passwd, hashed)

def test_cm_encrypt_decrypt():
    data = {"key1": "value1", "key2": {"key_inner": "value_inner"}}
    encrypted = cm.encrypt_data(data)
    assert isinstance(encrypted, bytes)
    decrypted = cm.decrypt_data(encrypted)
    assert isinstance(decrypted, dict)
    assert decrypted == data
