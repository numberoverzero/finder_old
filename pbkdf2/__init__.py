import os
from _pbkdf2 import pbkdf2_hex


def salt(len=16):
    return os.urandom(len).encode('base_64')


def derive_key(key, key_len=12):
    key = key.encode('ascii', 'ignore')
    return pbkdf2_hex(key, salt(256), iterations=10000, keylen=key_len)
