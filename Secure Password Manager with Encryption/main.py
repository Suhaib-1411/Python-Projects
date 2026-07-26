import sys
import getpass
import database
import manager

def print_menu():
    print("\n--- SECURE PASSWORD MANAGER ---")
    print("1. Add New Password")
    print("2. View Saved Passwords")
    print("3. Search Credentials")
    print("4. Delete Entry")
    print("5. Exit")

def handle_add_password():
    print("\n--- ADD NEW CREDENTIAL ---")
    website = input("Enter Website/Application Name: ").strip()
    username = input("Enter Username/Email: ").strip()
    
    # Mask password input in supported terminals
    try:
        plain_password = getpass.getpass("Enter Password: ").strip()
    except Exception:
        plain_password = input("Enter Password: ").strip()

    manager.add_new_credential(website, username, plain_password)

def handle_view_passwords():
    credentials = manager.get_decrypted_credentials()
    if not credentials:
        print("\nInformation: No saved credentials found.")
        return

    print("\n" + "="*70)
    print(f"{'ID':<5} | {'Website/App':<20} | {'Username/Email':<20} | {'Password':<15}")
    print("-" * 70)
    for c in credentials:
        print(f"{c['id']:<5} | {c['website']:<20} | {c['username']:<20} | {c['password']:<15}")
    print("="*70)

def handle_search_credentials():
    query = input("\nEnter Website/Application Name to Search: ").strip()
    credentials = manager.search_and_decrypt_credentials(query)

    if not credentials:
        print(f"\nInformation: No credentials found matching '{query}'.")
        return

    print("\n" + "="*70)
    print(f"{'ID':<5} | {'Website/App':<20} | {'Username/Email':<20} | {'Password':<15}")
    print("-" * 70)
    for c in credentials:
        print(f"{c['id']:<5} | {c['website']:<20} | {c['username']:<20} | {c['password']:<15}")
    print("="*70)

def handle_delete_entry():
    try:
        entry_id = int(input("\nEnter Entry ID to delete: "))
    except ValueError:
        print("\nError: Entry ID must be an integer.")
        return

    confirm = input(f"Confirm deletion of Entry ID {entry_id}? (y/n): ").strip().lower()
    if confirm == 'y':
        manager.remove_credential(entry_id)

def run_app():
    database.init_db()

    while True:
        print_menu()
        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            handle_add_password()
        elif choice == "2":
            handle_view_passwords()
        elif choice == "3":
            handle_search_credentials()
        elif choice == "4":
            handle_delete_entry()
        elif choice == "5":
            print("\nExiting Password Manager.")
            sys.exit()
        else:
            print("\nInvalid selection. Choose an option between 1 and 5.")

if __name__ == "__main__":
    run_app()