import sys
import inventory
import database
import reports

def print_menu():
    print("\n--- INVENTORY MANAGEMENT SYSTEM ---")
    print("1. Add Product")
    print("2. Update Stock Quantity")
    print("3. Record Product Sale")
    print("4. View All Inventory")
    print("5. Search Product by Name")
    print("6. Delete Product")
    print("7. Generate & Export Report")
    print("8. Exit")

def handle_add_product():
    print("\n--- ADD NEW PRODUCT ---")
    name = input("Enter Product Name: ").strip()
    category = input("Enter Category: ").strip()
    
    try:
        price = float(input("Enter Unit Price ($): "))
        quantity = int(input("Enter Starting Quantity: "))
    except ValueError:
        print("\nError: Invalid numerical input for Price or Quantity.")
        return

    supplier = input("Enter Supplier Name: ").strip()
    inventory.create_product(name, category, price, quantity, supplier)

def handle_update_stock():
    print("\n--- UPDATE STOCK ---")
    try:
        product_id = int(input("Enter Product ID: "))
        new_quantity = int(input("Enter New Total Stock Quantity: "))
    except ValueError:
        print("\nError: Product ID and Quantity must be integers.")
        return

    inventory.adjust_stock(product_id, new_quantity)

def handle_sell_product():
    print("\n--- SELL PRODUCT ---")
    try:
        product_id = int(input("Enter Product ID: "))
        quantity = int(input("Enter Quantity to Sell: "))
    except ValueError:
        print("\nError: Product ID and Quantity must be integers.")
        return

    inventory.process_sale(product_id, quantity)

def handle_view_inventory():
    products = database.get_all_products()
    if not products:
        print("\nInformation: Inventory is currently empty.")
        return

    print("\n--- CURRENT INVENTORY ---")
    print(f"{'ID':<5} | {'Name':<20} | {'Category':<12} | {'Price':<8} | {'Qty':<5} | {'Supplier':<12}")
    print("-" * 75)
    for p in products:
        print(f"{p['id']:<5} | {p['name']:<20} | {p['category']:<12} | ${p['price']:<7.2f} | {p['quantity']:<5} | {p['supplier']:<12}")

def handle_search_product():
    query = input("\nEnter Product Name to Search: ").strip()
    if not query:
        print("\nError: Search query cannot be empty.")
        return

    results = database.search_products_by_name(query)
    if not results:
        print(f"\nNo products found matching '{query}'.")
        return

    print(f"\n--- SEARCH RESULTS FOR '{query}' ---")
    print(f"{'ID':<5} | {'Name':<20} | {'Category':<12} | {'Price':<8} | {'Qty':<5} | {'Supplier':<12}")
    print("-" * 75)
    for p in results:
        print(f"{p['id']:<5} | {p['name']:<20} | {p['category']:<12} | ${p['price']:<7.2f} | {p['quantity']:<5} | {p['supplier']:<12}")

def handle_delete_product():
    print("\n--- DELETE PRODUCT ---")
    try:
        product_id = int(input("Enter Product ID to delete: "))
    except ValueError:
        print("\nError: Product ID must be an integer.")
        return

    confirm = input(f"Are you sure you want to delete product ID {product_id}? (y/n): ").strip().lower()
    if confirm == 'y':
        inventory.remove_product(product_id)

def handle_reports():
    print("\n--- GENERATE REPORTS ---")
    print(reports.generate_full_report_text(threshold=5))
    
    export_choice = input("\nSave this report to 'inventory_report.txt'? (y/n): ").strip().lower()
    if export_choice == 'y':
        reports.export_report_file("inventory_report.txt", threshold=5)

def run_application():
    inventory.initialize_system()
    
    while True:
        print_menu()
        choice = input("\nSelect an option (1-8): ").strip()

        if choice == "1":
            handle_add_product()
        elif choice == "2":
            handle_update_stock()
        elif choice == "3":
            handle_sell_product()
        elif choice == "4":
            handle_view_inventory()
        elif choice == "5":
            handle_search_product()
        elif choice == "6":
            handle_delete_product()
        elif choice == "7":
            handle_reports()
        elif choice == "8":
            print("\nExiting Inventory Management System.")
            sys.exit()
        else:
            print("\nInvalid choice. Select an option between 1 and 8.")

if __name__ == "__main__":
    run_application()