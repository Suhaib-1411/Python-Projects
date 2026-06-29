import json
import os
import hashlib
import re
import getpass

# --- Configuration Constants ---
DB_FILE = 'users.json'
MAX_LOGIN_ATTEMPTS = 3

# --- File Operations ---
def load_data():
    """
    Loads user data from the JSON file. 
    Returns an empty dictionary if the file does not exist or is corrupted.
    """
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    """
    Serializes and saves user data securely to the JSON file.
    """
    with open(DB_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# --- Security & Validation ---
def hash_password(password):
    """
    Hashes a plaintext password using SHA-256 for secure storage.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    """
    Validates email format using a standard regular expression.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def is_strong_password(password):
    """
    Checks if the password meets minimum complexity requirements:
    - Minimum 8 characters
    - At least one numeric digit
    - At least one uppercase letter
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    return True, "Valid"

# --- Core Functionality ---
def register(db):
    """Handles new user registration and validation."""
    print("\n--- User Registration ---")
    username = input("Enter a username: ").strip()
    
    if any(user.lower() == username.lower() for user in db):
        print("Error: Username already exists.")
        return

    email = input("Enter your email: ").strip()
    if not is_valid_email(email):
        print("Error: Invalid email format.")
        return
        
    if any(info['email'].lower() == email.lower() for info in db.values()):
        print("Error: Email is already registered.")
        return

    password = getpass.getpass("Enter a secure password: ")
    is_strong, msg = is_strong_password(password)
    if not is_strong:
        print(f"Error: {msg}")
        return

    confirm_password = getpass.getpass("Confirm password: ")
    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    # Role assignment: First registered user receives Admin privileges
    role = "Admin" if not db else "User"

    db[username] = {
        "email": email,
        "password_hash": hash_password(password),
        "role": role,
        "failed_attempts": 0,
        "locked": False
    }
    
    save_data(db)
    print(f"Success: Account '{username}' registered successfully as {role}.")

def login(db):
    """Authenticates a user based on credentials and checks account lock status."""
    print("\n--- User Login ---")
    identifier = input("Enter username or email: ").strip()
    password = getpass.getpass("Enter password: ")

    # Lookup user by either username or email
    username = None
    for user, info in db.items():
        if user.lower() == identifier.lower() or info['email'].lower() == identifier.lower():
            username = user
            break

    if not username:
        print("Error: Account not found.")
        return

    user_info = db[username]

    # Enforce account lockout policy
    if user_info.get('locked', False):
        print("Error: Account is locked due to too many failed attempts. Please reset your password.")
        return

    # Verify credentials
    if user_info['password_hash'] == hash_password(password):
        print(f"\nSuccess: Login successful. Welcome back, {username} ({user_info['role']}).")
        user_info['failed_attempts'] = 0  
        save_data(db)
        user_dashboard(db, username)
    else:
        user_info['failed_attempts'] += 1
        attempts_left = MAX_LOGIN_ATTEMPTS - user_info['failed_attempts']
        
        if attempts_left <= 0:
            user_info['locked'] = True
            print("Error: Maximum login attempts reached. Account locked.")
        else:
            print(f"Error: Incorrect password. {attempts_left} attempts remaining.")
        save_data(db)

def reset_password(db):
    """Allows a user to reset their password and unlock their account via email verification."""
    print("\n--- Reset Password ---")
    username = input("Enter your username: ").strip()
    
    if username not in db:
        print("Error: Username not found.")
        return
        
    email = input("Enter your registered email: ").strip()
    if db[username]['email'].lower() != email.lower():
        print("Error: Email does not match our records.")
        return
        
    new_password = getpass.getpass("Enter new secure password: ")
    is_strong, msg = is_strong_password(new_password)
    if not is_strong:
        print(f"Error: {msg}")
        return
        
    db[username]['password_hash'] = hash_password(new_password)
    db[username]['failed_attempts'] = 0
    db[username]['locked'] = False
    save_data(db)
    print("Success: Password reset successfully. Account unlocked.")

def delete_account(db, current_user):
    """Processes secure account deletion with secondary password confirmation."""
    print("\n--- Delete Account ---")
    confirm = input(f"Are you sure you want to delete '{current_user}'? (yes/no): ").lower()
    if confirm == 'yes':
        password = getpass.getpass("Enter password to confirm deletion: ")
        if db[current_user]['password_hash'] == hash_password(password):
            del db[current_user]
            save_data(db)
            print("Success: Account deleted successfully.")
            return True
        else:
            print("Error: Incorrect password. Deletion cancelled.")
    return False

def user_dashboard(db, username):
    """Provides a restricted menu accessible only to authenticated users."""
    while True:
        print(f"\n--- Dashboard: {username} ---")
        print("1. View Profile")
        print("2. Delete Account")
        print("3. Logout")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            info = db[username]
            print("\n--- Profile Data ---")
            print(f"Username: {username}")
            print(f"Email: {info['email']}")
            print(f"Role: {info['role']}")
        elif choice == '2':
            if delete_account(db, username):
                break 
        elif choice == '3':
            print("Logging out...")
            break
        else:
            print("Error: Invalid option.")

# --- Application Entry Point ---
def main():
    print("Welcome to the Secure Authentication System")
    while True:
        db = load_data()
        print("\n--- Main Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            register(db)
        elif choice == '2':
            login(db)
        elif choice == '3':
            reset_password(db)
        elif choice == '4':
            print("Exiting application.")
            break
        else:
            print("Error: Invalid option. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()