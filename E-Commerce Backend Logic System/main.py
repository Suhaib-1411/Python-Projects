import sys
import database
import products
from cart import ShoppingCart
import orders

user_cart = ShoppingCart()

def print_menu():
    print("\n--- E-COMMERCE BACKEND SYSTEM ---")
    print("1. View Products")
    print("2. Search Products")
    print("3. Add Product to Cart")
    print("4. View / Manage Cart")
    print("5. Place Order")
    print("6. View Order History")
    print("7. Exit")

def handle_view_products():
    prod_list = products.get_all_products()
    if not prod_list:
        print("\nInformation: Product catalog is empty.")
        return

    print("\n" + "="*65)
    print(" PRODUCT CATALOG")
    print("="*65)
    print(f"{'ID':<5} | {'Product Name':<25} | {'Category':<12} | {'Price':<8} | {'Stock':<5}")
    print("-" * 65)
    for p in prod_list:
        print(f"{p['id']:<5} | {p['name']:<25} | {p['category']:<12} | ${p['price']:<7.2f} | {p['stock']:<5}")
    print("="*65)

def handle_search_products():
    query = input("\nEnter product name to search: ").strip()
    if not query:
        print("\nError: Search query cannot be blank.")
        return

    results = products.search_products_by_name(query)
    if not results:
        print(f"\nInformation: No products found matching '{query}'.")
        return

    print("\n" + "="*65)
    print(f" SEARCH RESULTS FOR '{query}'")
    print("="*65)
    print(f"{'ID':<5} | {'Product Name':<25} | {'Category':<12} | {'Price':<8} | {'Stock':<5}")
    print("-" * 65)
    for p in results:
        print(f"{p['id']:<5} | {p['name']:<25} | {p['category']:<12} | ${p['price']:<7.2f} | {p['stock']:<5}")
    print("="*65)

def handle_add_to_cart():
    try:
        product_id = int(input("\nEnter Product ID to add: "))
        quantity = int(input("Enter Quantity: "))
    except ValueError:
        print("\nError: Product ID and Quantity must be valid integers.")
        return

    prod = products.get_product_by_id(product_id)
    if not prod:
        print(f"\nError: Product ID {product_id} does not exist.")
        return

    user_cart.add_item(prod["id"], prod["name"], prod["price"], quantity, prod["stock"])

def handle_view_cart():
    if user_cart.is_empty():
        print("\nInformation: Your shopping cart is empty.")
        return

    print("\n" + "="*65)
    print(" SHOPPING CART")
    print("="*65)
    print(f"{'ID':<5} | {'Product Name':<25} | {'Price':<8} | {'Qty':<5} | {'Subtotal':<8}")
    print("-" * 65)
    for item_id, item in user_cart.items.items():
        subtotal = item["price"] * item["quantity"]
        print(f"{item['id']:<5} | {item['name']:<25} | ${item['price']:<7.2f} | {item['quantity']:<5} | ${subtotal:<7.2f}")
    print("-" * 65)
    print(f" TOTAL BILL: ${user_cart.calculate_total():.2f}")
    print("="*65)

    print("\nCart Actions:")
    print("1. Update Item Quantity")
    print("2. Remove Item from Cart")
    print("3. Return to Main Menu")
    action = input("Select action (1-3): ").strip()

    if action == "1":
        try:
            pid = int(input("Enter Product ID to update: "))
            new_qty = int(input("Enter new quantity: "))
            user_cart.update_quantity(pid, new_qty)
        except ValueError:
            print("\nError: Input must be a valid integer.")
    elif action == "2":
        try:
            pid = int(input("Enter Product ID to remove: "))
            user_cart.remove_item(pid)
        except ValueError:
            print("\nError: Input must be a valid integer.")

def handle_place_order():
    if user_cart.is_empty():
        print("\nError: Your cart is empty. Add items before placing an order.")
        return

    handle_view_cart()
    confirm = input("\nConfirm placement of this order? (y/n): ").strip().lower()
    if confirm == 'y':
        orders.place_order(user_cart)

def handle_view_orders():
    order_history = orders.get_all_orders()
    if not order_history:
        print("\nInformation: No orders have been placed yet.")
        return

    print("\n" + "="*65)
    print(" ORDER HISTORY")
    print("="*65)
    for o in order_history:
        print(f" Order ID: #{o['order_id']} | Date: {o['created_at']} | Total: ${o['total_amount']:.2f}")
        print(" Items Purchased:")
        for item in o["items"]:
            subtotal = item["unit_price"] * item["quantity"]
            print(f"   - {item['product_name']} (x{item['quantity']}) @ ${item['unit_price']:.2f} = ${subtotal:.2f}")
        print("-" * 65)

def run_app():
    database.init_db()
    database.seed_products()

    while True:
        print_menu()
        choice = input("\nSelect option (1-7): ").strip()

        if choice == "1":
            handle_view_products()
        elif choice == "2":
            handle_search_products()
        elif choice == "3":
            handle_add_to_cart()
        elif choice == "4":
            handle_view_cart()
        elif choice == "5":
            handle_place_order()
        elif choice == "6":
            handle_view_orders()
        elif choice == "7":
            print("\nExiting E-Commerce System.")
            sys.exit()
        else:
            print("\nInvalid selection. Choose an option between 1 and 7.")

if __name__ == "__main__":
    run_app()