import sqlite3
from typing import List, Optional
from database import get_connection

def get_all_products() -> List[sqlite3.Row]:
    """Retrieves all available products from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products ORDER BY id ASC;")
        return cursor.fetchall()

def get_product_by_id(product_id: int) -> Optional[sqlite3.Row]:
    """Retrieves a single product by its unique ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?;", (product_id,))
        return cursor.fetchone()

def search_products_by_name(query: str) -> List[sqlite3.Row]:
    """Performs a case-insensitive search for products by name."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE name LIKE ? ORDER BY name ASC;", (f"%{query}%",))
        return cursor.fetchall()