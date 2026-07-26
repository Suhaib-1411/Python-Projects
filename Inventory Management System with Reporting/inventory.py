import database

def initialize_system():
    """Initializes the database schema."""
    database.init_db()

def create_product(name: str, category: str, price: float, quantity: int, supplier: str) -> bool:
    """Validates inputs and adds a new product."""
    if not name.strip() or not category.strip() or not supplier.strip():
        print("\nError: Product details cannot be empty.")
        return False
    if price < 0:
        print("\nError: Price cannot be negative.")
        return False
    if quantity < 0:
        print("\nError: Quantity cannot be negative.")
        return False

    product_id = database.add_product(name.strip(), category.strip(), price, quantity, supplier.strip())
    if product_id:
        print(f"\nSuccess: Product added with ID {product_id}.")
        return True
    return False

def adjust_stock(product_id: int, new_quantity: int) -> bool:
    """Validates and updates stock quantity."""
    if new_quantity < 0:
        print("\nError: Stock quantity cannot be negative.")
        return False
    
    product = database.get_product_by_id(product_id)
    if not product:
        print(f"\nError: Product ID {product_id} not found.")
        return False

    if database.update_product_stock(product_id, new_quantity):
        print(f"\nSuccess: Stock updated for '{product['name']}' to {new_quantity}.")
        return True
    return False

def process_sale(product_id: int, quantity_to_sell: int) -> bool:
    """Validates and completes a product sale."""
    if quantity_to_sell <= 0:
        print("\nError: Sale quantity must be greater than zero.")
        return False

    product = database.get_product_by_id(product_id)
    if not product:
        print(f"\nError: Product ID {product_id} not found.")
        return False

    current_stock = product['quantity']
    if quantity_to_sell > current_stock:
        print(f"\nError: Insufficient stock. Available: {current_stock}, Requested: {quantity_to_sell}.")
        return False

    total_price = round(product['price'] * quantity_to_sell, 2)
    success = database.record_sale_transaction(product_id, product['name'], quantity_to_sell, total_price)
    
    if success:
        print("\n" + "="*40)
        print(" TRANSACTION COMPLETED")
        print("="*40)
        print(f" Product      : {product['name']}")
        print(f" Quantity     : {quantity_to_sell}")
        print(f" Total Amount : ${total_price:.2f}")
        print("="*40)
        return True
    return False

def remove_product(product_id: int) -> bool:
    """Deletes a product from inventory."""
    product = database.get_product_by_id(product_id)
    if not product:
        print(f"\nError: Product ID {product_id} not found.")
        return False

    if database.delete_product_by_id(product_id):
        print(f"\nSuccess: Product '{product['name']}' removed from inventory.")
        return True
    return False