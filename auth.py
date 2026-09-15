import hashlib
import os

SALT_FILE = "master_salt.bin"
HASH_FILE = "master_hash.bin"


def create_master_password(password):
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    with open(SALT_FILE, "wb") as file:
        file.write(salt)

    with open(HASH_FILE, "wb") as file:
        file.write(password_hash)


def verify_master_password(password):
    if not os.path.exists(SALT_FILE) or not os.path.exists(HASH_FILE):
        return False

    with open(SALT_FILE, "rb") as file:
        salt = file.read()

    with open(HASH_FILE, "rb") as file:
        stored_hash = file.read()

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return password_hash == stored_hash