from typing import List, Dict, Any, Optional
from database import get_connection
from cart import ShoppingCart

def place_order(cart: ShoppingCart) -> Optional[int]:
    """
    Processes an order from the cart, validates stock levels,
    deducts inventory, and records order details atomically.
    """
    if cart.is_empty():
        print("\nError: Cannot place an order with an empty cart.")
        return None

    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Verify stock availability for all cart items before processing
        for item in cart.items.values():
            cursor.execute("SELECT stock, name FROM products WHERE id = ?;", (item["id"],))
            db_product = cursor.fetchone()
            if not db_product:
                print(f"\nError: Product '{item['name']}' no longer exists.")
                conn.rollback()
                return None
            if db_product["stock"] < item["quantity"]:
                print(f"\nError: Insufficient stock for '{db_product['name']}'. Available: {db_product['stock']}.")
                conn.rollback()
                return None

        total_amount = round(cart.calculate_total(), 2)

        # Insert main order entry
        cursor.execute("INSERT INTO orders (total_amount) VALUES (?);", (total_amount,))
        order_id = cursor.lastrowid

        # Insert order line items and deduct product inventory stock
        for item in cart.items.values():
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price)
                VALUES (?, ?, ?, ?, ?);
            """, (order_id, item["id"], item["name"], item["quantity"], item["price"]))

            cursor.execute("""
                UPDATE products
                SET stock = stock - ?
                WHERE id = ?;
            """, (item["quantity"], item["id"]))

        conn.commit()
        cart.clear()
        print(f"\nSuccess: Order #{order_id} placed successfully! Total Paid: ${total_amount:.2f}")
        return order_id

    except Exception as e:
        conn.rollback()
        print(f"\nTransaction Error: Failed to place order. {e}")
        return None
    finally:
        conn.close()

def get_all_orders() -> List[Dict[str, Any]]:
    """Retrieves all historical orders and their associated item details."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders ORDER BY created_at DESC;")
        orders_rows = cursor.fetchall()

        orders_list = []
        for o in orders_rows:
            order_id = o["id"]
            cursor.execute("SELECT * FROM order_items WHERE order_id = ?;", (order_id,))
            items_rows = cursor.fetchall()
            
            items = [
                {
                    "product_id": item["product_id"],
                    "product_name": item["product_name"],
                    "quantity": item["quantity"],
                    "unit_price": item["unit_price"]
                }
                for item in items_rows
            ]

            orders_list.append({
                "order_id": order_id,
                "total_amount": o["total_amount"],
                "created_at": o["created_at"],
                "items": items
            })

        return orders_list