import hashlib
import os
import sqlite3
from typing import Optional, Dict, Any
import database

def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
    """Hashes a password using PBKDF2-HMAC-SHA256 with 100,000 iterations and a salt."""
    if salt is None:
        salt = os.urandom(16)
    
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return pwd_hash.hex(), salt.hex()

def verify_password(stored_hash: str, stored_salt: str, password_attempt: str) -> bool:
    """Verifies a password attempt against the stored hash and salt."""
    salt_bytes = bytes.fromhex(stored_salt)
    attempt_hash, _ = hash_password(password_attempt, salt_bytes)
    return attempt_hash == stored_hash

def register_user(username: str, password: str, role: str = "USER") -> bool:
    """Registers a new user with secure password hashing and normalized role handling."""
    username_clean = username.strip()
    role_clean = role.strip().upper()

    if not username_clean or not password.strip():
        print("\nError: Username and password cannot be empty.")
        return False

    valid_roles = ["ADMIN", "MANAGER", "USER"]
    if role_clean not in valid_roles:
        print(f"\nError: Invalid role '{role}'. Allowed roles: {', '.join(valid_roles)}")
        return False

    pwd_hash, salt = hash_password(password)

    try:
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, salt, role)
                VALUES (?, ?, ?, ?);
            """, (username_clean, pwd_hash, salt, role_clean))
            conn.commit()
            print(f"\nSuccess: User '{username_clean}' registered with role '{role_clean}'.")
            return True
    except sqlite3.IntegrityError:
        print(f"\nError: Username '{username_clean}' is already taken.")
        return False

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticates a user and returns their user profile dictionary if successful."""
    username_clean = username.strip()
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?;", (username_clean,))
        user_row = cursor.fetchone()

        if not user_row:
            return None

        if verify_password(user_row["password_hash"], user_row["salt"], password):
            return {
                "id": user_row["id"],
                "username": user_row["username"],
                "role": user_row["role"].upper()
            }
        return None