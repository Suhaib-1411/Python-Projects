import hashlib
import os
import sqlite3
from typing import Optional, Dict, Any
from database import get_connection

def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
    """Hashes a password using PBKDF2 with a secure salt."""
    if salt is None:
        salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return hashed.hex(), salt.hex()

def register_user(username: str, password: str, email: str) -> Optional[int]:
    """Registers a new user after validating input and hashing credentials."""
    if not username.strip() or not password.strip() or not email.strip():
        print("\nError: All registration fields are required.")
        return None

    if len(password) < 6:
        print("\nError: Password must be at least 6 characters long.")
        return None

    pwd_hash, salt_str = hash_password(password)

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, salt, email)
                VALUES (?, ?, ?, ?);
            """, (username.strip(), pwd_hash, salt_str, email.strip()))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"\nError: Username '{username}' is already taken.")
        return None

def login_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticates credentials against stored hashes."""
    if not username.strip() or not password.strip():
        print("\nError: Username and password cannot be empty.")
        return None

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?;", (username.strip(),))
        user = cursor.fetchone()

        if not user:
            print("\nError: Invalid username or password.")
            return None

        salt = bytes.fromhex(user["salt"])
        computed_hash, _ = hash_password(password, salt)

        if computed_hash == user["password_hash"]:
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "created_at": user["created_at"]
            }
        else:
            print("\nError: Invalid username or password.")
            return None