import sqlite3
import os

DB_NAME = "blog.db"

def get_connection():
    """Establishes and returns a database connection with dictionary-like row factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates tables for users, posts, and comments if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Foreign keys enabled
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)

        # Comments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                author_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
                FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)
        conn.commit()

def seed_sample_data():
    """Populates the database with sample user and post entries if empty."""
    from auth import register_user
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users;")
        if cursor.fetchone()["count"] == 0:
            # Register initial user
            user_id = register_user("admin", "AdminPass123!", "admin@example.com")
            if user_id:
                cursor.execute("""
                    INSERT INTO posts (title, content, category, author_id)
                    VALUES (?, ?, ?, ?);
                """, (
                    "Welcome to the Blog System",
                    "This is an initial sample blog post demonstrating backend data persistence.",
                    "General",
                    user_id
                ))
                conn.commit()