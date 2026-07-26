import sqlite3
from typing import List, Tuple, Optional

DB_NAME = "inventory.db"

def get_connection():
    """Returns a database connection with dictionary-like row factories."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite database tables for products and sales history."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                category TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                quantity INTEGER NOT NULL CHECK(quantity >= 0),
                supplier TEXT NOT NULL
            )
        """)
        
        # Sales log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity_sold INTEGER NOT NULL CHECK(quantity_sold > 0),
                total_price REAL NOT NULL CHECK(total_price >= 0),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        """)
        conn.commit()

def add_product(name: str, category: str, price: float, quantity: int, supplier: str) -> Optional[int]:
    """Inserts a new product into the database."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (name, category, price, quantity, supplier)
                VALUES (?, ?, ?, ?, ?)
            """, (name, category, price, quantity, supplier))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"\nError: Product with name '{name}' already exists.")
        return None

def update_product_stock(product_id: int, new_quantity: int) -> bool:
    """Updates the stock quantity of an existing product."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products SET quantity = ? WHERE id = ?
        """, (new_quantity, product_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_product_by_id(product_id: int) -> bool:
    """Removes a product from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_all_products() -> List[sqlite3.Row]:
    """Fetches all product records."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products ORDER BY id ASC")
        return cursor.fetchall()

def get_product_by_id(product_id: int) -> Optional[sqlite3.Row]:
    """Retrieves a single product by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return cursor.fetchone()

def search_products_by_name(name_query: str) -> List[sqlite3.Row]:
    """Case-insensitive search for products by name."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{name_query}%",))
        return cursor.fetchall()

def record_sale_transaction(product_id: int, product_name: str, quantity_sold: int, total_price: float) -> bool:
    """Records a sales transaction and updates stock levels atomically."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Deduct stock
        cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity_sold, product_id))
        # Add sales log
        cursor.execute("""
            INSERT INTO sales (product_id, product_name, quantity_sold, total_price)
            VALUES (?, ?, ?, ?)
        """, (product_id, product_name, quantity_sold, total_price))
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"\nDatabase Error during transaction: {e}")
        return False
    finally:
        conn.close()

def get_all_sales() -> List[sqlite3.Row]:
    """Retrieves all historical sales records."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales ORDER BY timestamp DESC")
        return cursor.fetchall()