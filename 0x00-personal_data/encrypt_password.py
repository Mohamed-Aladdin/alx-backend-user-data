#!/usr/bin/env python3
"""Task 5, 6 Module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string
    """
    hash = password.encode()
    hashed = bcrypt.hashpw(hash, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """returns a boolean
    """
    hash = password.encode()

    if bcrypt.checkpw(hash, hashed_password):
        return True
    return False
