import sqlite3

DB_NAME = "rbac_system.db"

def get_connection():
    """Establishes and returns a database connection with dictionary-like row factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite database schema for users, roles, data items, and activity logs."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'USER' COLLATE NOCASE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Shared Data Resource Table (to demonstrate View, Add, Edit, Delete)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_by TEXT NOT NULL
            );
        """)

        # Activity Audit Logs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()