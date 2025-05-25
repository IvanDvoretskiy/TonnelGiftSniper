import hashlib
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from constants import SECRET_KEY

def EVP_BytesToKey(password: str, salt: bytes, key_size: int = 32, iv_size: int = 16, iterations: int = 1) -> tuple:
    """Generate key and IV using OpenSSL's EVP_BytesToKey algorithm."""
    dtot = b''
    d = b''
    while len(dtot) < key_size + iv_size:
        d = hashlib.md5(d + password.encode() + salt).digest()
        for _ in range(1, iterations):
            d = hashlib.md5(d).digest()
        dtot += d
    return dtot[:key_size], dtot[key_size:key_size+iv_size]

def generate_wtf(timestamp: str) -> str:
    """Generate encrypted token for API requests."""
    salt = os.urandom(8)
    key, iv = EVP_BytesToKey(SECRET_KEY, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(timestamp.encode(), AES.block_size))
    return base64.b64encode(b"Salted__" + salt + encrypted).decode()