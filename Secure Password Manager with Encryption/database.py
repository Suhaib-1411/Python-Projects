import sqlite3
from typing import List

DB_NAME = "passwords.db"

def get_connection():
    """Establishes and returns a database connection with dictionary-like row factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database table for encrypted credential storage."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL COLLATE NOCASE,
                username TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

def insert_credential(website: str, username: str, encrypted_password: str) -> int:
    """Inserts a new encrypted credential entry into the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO credentials (website, username, encrypted_password)
            VALUES (?, ?, ?);
        """, (website.strip(), username.strip(), encrypted_password))
        conn.commit()
        return cursor.lastrowid

def fetch_all_credentials() -> List[sqlite3.Row]:
    """Retrieves all stored credential records."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM credentials ORDER BY website ASC;")
        return cursor.fetchall()

def search_credentials_by_website(query: str) -> List[sqlite3.Row]:
    """Performs a case-insensitive search for entries matching a website query."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM credentials WHERE website LIKE ? ORDER BY website ASC;", (f"%{query}%",))
        return cursor.fetchall()

def delete_credential_by_id(entry_id: int) -> bool:
    """Deletes a credential record by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM credentials WHERE id = ?;", (entry_id,))
        conn.commit()
        return cursor.rowcount > 0