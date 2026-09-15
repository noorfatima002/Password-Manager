from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"


def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as file:
            file.write(key)


def load_key():
    with open(KEY_FILE, "rb") as file:
        return file.read()


def encrypt_password(password):
    key = load_key()
    cipher = Fernet(key)
    return cipher.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    key = load_key()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_password.encode()).decode()