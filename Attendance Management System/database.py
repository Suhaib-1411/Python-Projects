import sqlite3
from typing import List, Optional

DB_NAME = "attendance.db"

def get_connection():
    """Establishes and returns a database connection with dictionary-like row factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database schema for tracking attendance."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id TEXT NOT NULL,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Present', 'Absent', 'Late')),
                UNIQUE(person_id, date)
            );
        """)
        conn.commit()

def insert_attendance(person_id: str, name: str, date_str: str, status: str) -> bool:
    """Inserts a new attendance record while preventing duplicate entries per date."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attendance (person_id, name, date, status)
                VALUES (?, ?, ?, ?);
            """, (person_id.upper(), name.strip(), date_str, status.title()))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print(f"\nError: Attendance record already exists for ID '{person_id}' on date '{date_str}'.")
        return False

def get_all_records() -> List[sqlite3.Row]:
    """Retrieves all attendance records sorted by date descending."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT person_id, name, date, status FROM attendance ORDER BY date DESC, person_id ASC;")
        return cursor.fetchall()

def get_records_by_date(date_str: str) -> List[sqlite3.Row]:
    """Retrieves attendance records for a specific date."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT person_id, name, date, status FROM attendance WHERE date = ? ORDER BY person_id ASC;", (date_str,))
        return cursor.fetchall()

def get_records_by_person(person_id: str) -> List[sqlite3.Row]:
    """Retrieves attendance history for a specific individual (case-insensitive)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT person_id, name, date, status FROM attendance WHERE person_id = ? ORDER BY date DESC;", (person_id.upper(),))
        return cursor.fetchall()

def update_attendance_status(person_id: str, date_str: str, new_status: str) -> bool:
    """Updates an existing attendance status."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE attendance
            SET status = ?
            WHERE person_id = ? AND date = ?;
        """, (new_status.title(), person_id.upper(), date_str))
        conn.commit()
        return cursor.rowcount > 0

def delete_attendance_record(person_id: str, date_str: str) -> bool:
    """Deletes an attendance entry from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM attendance WHERE person_id = ? AND date = ?;", (person_id.upper(), date_str))
        conn.commit()
        return cursor.rowcount > 0