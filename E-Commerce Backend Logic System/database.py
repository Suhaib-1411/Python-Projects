import sqlite3

DB_NAME = "ecommerce.db"

def get_connection():
    """Establishes and returns a database connection with dictionary-like row factory."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite database tables for products, orders, and order items."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Enable foreign key support
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Products Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                price REAL NOT NULL CHECK(price >= 0),
                category TEXT NOT NULL,
                stock INTEGER NOT NULL CHECK(stock >= 0)
            );
        """)

        # Orders Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_amount REAL NOT NULL CHECK(total_amount >= 0),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Order Items Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_price REAL NOT NULL CHECK(unit_price >= 0),
                FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products (id)
            );
        """)
        conn.commit()

def seed_products():
    """Populates the database with initial sample products if empty."""
    sample_products = [
        ("Laptop Pro 15", 1299.99, "Electronics", 10),
        ("Wireless Headphones", 199.50, "Electronics", 25),
        ("Mechanical Keyboard", 89.99, "Accessories", 15),
        ("Ergonomic Gaming Mouse", 49.99, "Accessories", 30),
        ("USB-C Docking Station", 75.00, "Accessories", 20)
    ]

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM products;")
        if cursor.fetchone()["count"] == 0:
            cursor.executemany("""
                INSERT INTO products (name, price, category, stock)
                VALUES (?, ?, ?, ?);
            """, sample_products)
            conn.commit()