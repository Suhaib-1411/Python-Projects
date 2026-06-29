import json
import os
import re
import uuid

# --- Configuration ---
DATA_FILE = "contacts.json"

# --- Helper Functions ---
def generate_id():
    """Generates a unique 6-character alphanumeric ID."""
    return uuid.uuid4().hex[:6].upper()

def is_valid_email(email):
    """Validates email format using regular expressions."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """Validates phone number format allowing digits, spaces, plus, and hyphens."""
    pattern = r"^[\+\d\s\-]{7,15}$"
    return re.match(pattern, phone) is not None

def get_valid_input(prompt, validation_fn=None, error_msg="Invalid input.", required=True):
    """Prompts the user for input and applies validation rules."""
    while True:
        user_input = input(prompt).strip()
        
        if not user_input and required:
            print("[ERROR] This field cannot be empty. Please provide a value.")
            continue
        
        if not user_input and not required:
            return "" 
            
        if validation_fn and not validation_fn(user_input):
            print(f"[ERROR] {error_msg}")
            continue
            
        return user_input

# --- Core Features ---
def load_contacts():
    """Loads contact data from the designated JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("[WARNING] Data file is corrupted. Initializing with an empty contact list.")
        return []
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return []

def save_contacts(contacts):
    """Writes the current contact list to the JSON file."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(contacts, file, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to save data: {e}")

def display_contacts(contacts):
    """Renders a formatted table of provided contacts."""
    if not contacts:
        print("\n[INFO] No contacts found in the system.")
        return

    print("\n" + "=" * 95)
    print(f"{'ID':<8} | {'Name':<20} | {'Phone':<15} | {'Email':<25} | {'City':<10} | {'Company':<10}")
    print("-" * 95)
    
    for c in contacts:
        name = c['name'][:17] + "..." if len(c['name']) > 20 else c['name']
        email = c['email'][:22] + "..." if len(c['email']) > 25 else c['email']
        print(f"{c['id']:<8} | {name:<20} | {c['phone']:<15} | {email:<25} | {c['city']:<10} | {c['company']:<10}")
        
    print("=" * 95)

def add_contact(contacts):
    """Collects user input to generate and store a new contact record."""
    print("\n--- Add New Contact ---")
    name = get_valid_input("Full Name: ")
    phone = get_valid_input("Phone Number: ", is_valid_phone, "Invalid phone format. Please use 7-15 digits.")
    email = get_valid_input("Email Address: ", is_valid_email, "Invalid email format.")
    city = get_valid_input("City: ")
    company = get_valid_input("Company: ")

    contact = {
        "id": generate_id(),
        "name": name,
        "phone": phone,
        "email": email,
        "city": city,
        "company": company
    }
    
    contacts.append(contact)
    save_contacts(contacts)
    print(f"\n[SUCCESS] Contact '{name}' has been added. Assigned ID: {contact['id']}")

def search_contacts(contacts):
    """Executes a case-insensitive search based on selected criteria."""
    print("\n--- Search Contacts ---")
    print("1. By Name")
    print("2. By Phone")
    print("3. By Email")
    choice = input("Select search criteria (1-3): ").strip()

    if choice not in ['1', '2', '3']:
        print("[ERROR] Invalid selection.")
        return

    query = input("Enter search term: ").strip().lower()
    
    keys = {'1': 'name', '2': 'phone', '3': 'email'}
    search_key = keys[choice]

    results = [c for c in contacts if query in c[search_key].lower()]
    print(f"\n[INFO] Search Results for '{query}' in {search_key.capitalize()}:")
    display_contacts(results)

def filter_contacts(contacts):
    """Applies exact-match filtering by City or Company."""
    print("\n--- Filter Contacts ---")
    print("1. By City")
    print("2. By Company")
    choice = input("Select filter criteria (1-2): ").strip()

    if choice not in ['1', '2']:
        print("[ERROR] Invalid selection.")
        return

    query = input("Enter exact filter term: ").strip().lower()
    
    keys = {'1': 'city', '2': 'company'}
    filter_key = keys[choice]

    results = [c for c in contacts if c[filter_key].lower() == query]
    print(f"\n[INFO] Filter Results for {filter_key.capitalize()} = '{query.title()}':")
    display_contacts(results)

def update_contact(contacts):
    """Modifies an existing contact record based on its unique ID."""
    print("\n--- Update Contact ---")
    contact_id = input("Enter the ID of the contact to update: ").strip().upper()
    
    contact = next((c for c in contacts if c['id'] == contact_id), None)
    
    if not contact:
        print(f"[ERROR] Contact with ID '{contact_id}' could not be located.")
        return

    print("\nEnter new details. Leave a field blank and press Enter to retain the current value.")
    
    name = get_valid_input(f"Name ({contact['name']}): ", required=False)
    if name: contact['name'] = name
        
    phone = get_valid_input(f"Phone ({contact['phone']}): ", is_valid_phone, "Invalid format.", required=False)
    if phone: contact['phone'] = phone
        
    email = get_valid_input(f"Email ({contact['email']}): ", is_valid_email, "Invalid format.", required=False)
    if email: contact['email'] = email
        
    city = get_valid_input(f"City ({contact['city']}): ", required=False)
    if city: contact['city'] = city
        
    company = get_valid_input(f"Company ({contact['company']}): ", required=False)
    if company: contact['company'] = company

    save_contacts(contacts)
    print(f"\n[SUCCESS] Contact ID '{contact_id}' has been updated.")

def delete_contact(contacts):
    """Removes a contact record from the system."""
    print("\n--- Delete Contact ---")
    print("1. Delete by ID")
    print("2. Delete by Exact Name")
    choice = input("Select method (1-2): ").strip()

    if choice == '1':
        identifier = input("Enter Contact ID: ").strip().upper()
        key = 'id'
    elif choice == '2':
        identifier = input("Enter Exact Name: ").strip().lower()
        key = 'name'
    else:
        print("[ERROR] Invalid selection.")
        return

    initial_count = len(contacts)
    
    if key == 'id':
        contacts[:] = [c for c in contacts if c['id'] != identifier]
    else:
        contacts[:] = [c for c in contacts if c['name'].lower() != identifier]

    if len(contacts) < initial_count:
        save_contacts(contacts)
        print("\n[SUCCESS] Contact record(s) removed successfully.")
    else:
        print(f"\n[ERROR] No contact found matching the provided {key.upper()}.")

# --- Main Interface ---
def main_menu():
    """Initializes the application and displays the primary navigation menu."""
    contacts = load_contacts()
    
    while True:
        print("\n" + "=" * 30)
        print("CONTACT MANAGEMENT SYSTEM")
        print("=" * 30)
        print("1. Add New Contact")
        print("2. View All Contacts")
        print("3. Search Contacts")
        print("4. Filter Contacts")
        print("5. Update Contact")
        print("6. Delete Contact")
        print("7. Exit Application")
        print("=" * 30)
        
        try:
            choice = input("Enter selection (1-7): ").strip()
            
            if choice == '1': add_contact(contacts)
            elif choice == '2': display_contacts(contacts)
            elif choice == '3': search_contacts(contacts)
            elif choice == '4': filter_contacts(contacts)
            elif choice == '5': update_contact(contacts)
            elif choice == '6': delete_contact(contacts)
            elif choice == '7':
                print("\n[INFO] Saving data and terminating application. Goodbye.")
                break
            else:
                print("[ERROR] Invalid selection. Please enter a number between 1 and 7.")
                
        except KeyboardInterrupt:
            print("\n\n[INFO] Manual interrupt detected. Terminating application.")
            break
        except Exception as e:
            print(f"\n[CRITICAL ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main_menu()