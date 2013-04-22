import os
from _pbkdf2 import pbkdf2_hex


def _salt(len=16):
    return os.urandom(len).encode('base_64')


def pbkdf2(key, key_len=12, salt=None):
    key = key.encode('ascii', 'ignore')
    salt = salt or _salt(64)
    dkey = pbkdf2_hex(key, salt, iterations=10000, keylen=key_len)
    return dkey, salt
