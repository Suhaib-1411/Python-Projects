import os
from cryptography.fernet import Fernet, InvalidToken

KEY_FILE = "secret.key"

def generate_or_load_key() -> bytes:
    """
    Generates a new 256-bit key for Fernet symmetric encryption if missing, 
    or loads the existing key from the key file.
    """
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key
    else:
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()

def encrypt_password(plain_password: str) -> str:
    """Encrypts a plain text password using Fernet symmetric encryption."""
    key = generate_or_load_key()
    fernet = Fernet(key)
    encrypted_bytes = fernet.encrypt(plain_password.encode("utf-8"))
    return encrypted_bytes.decode("utf-8")

def decrypt_password(encrypted_password: str) -> str:
    """Decrypts a Fernet cipher text string back to plain text."""
    try:
        key = generate_or_load_key()
        fernet = Fernet(key)
        decrypted_bytes = fernet.decrypt(encrypted_password.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")
    except InvalidToken:
        print("\nSecurity Error: Invalid encryption key or corrupted data string.")
        return "[Decryption Failed]"