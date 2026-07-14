import sqlite3
import hashlib
import os
from datetime import datetime
from getpass import getpass

DB_NAME = "user_system.db"

# ==========================================
# 1. DATABASE LAYER
# ==========================================
class DatabaseManager:
    def __init__(self, db_path=DB_NAME):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initializes the database and seeds a default administrator account."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    phone TEXT,
                    role TEXT DEFAULT 'User',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        self._seed_admin()

    def _seed_admin(self):
        """Seeds a default admin if the system is fresh."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Admin'")
            if cursor.fetchone()[0] == 0:
                admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
                cursor.execute("""
                    INSERT INTO users (username, email, password, phone, role)
                    VALUES (?, ?, ?, ?, ?)
                """, ("admin", "admin@system.com", admin_pass, "000-000-0000", "Admin"))
                conn.commit()


# ==========================================
# 2. AUTHENTICATION & BUSINESS LOGIC LAYER
# ==========================================
class UserService:
    def __init__(self, db_manager):
        self.db = db_manager
        self.current_user = None  # Tracks logged-in user session

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, email, password, phone, role="User"):
        hashed_pw = self.hash_password(password)
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, email, password, phone, role)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, email, hashed_pw, phone, role))
                conn.commit()
                return True, "Registration successful!"
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return False, "Username already exists."
            elif "email" in str(e):
                return False, "Email already registered."
            return False, "Database integrity error."
        except Exception as e:
            return False, f"An error occurred: {e}"

    def login(self, username_or_email, password):
        hashed_pw = self.hash_password(password)
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users 
                WHERE (username = ? OR email = ?) AND password = ?
            """, (username_or_email, username_or_email, hashed_pw))
            user = cursor.fetchone()
            
            if user:
                self.current_user = dict(user)
                return True, f"Welcome back, {self.current_user['username']}!"
            return False, "Invalid username/email or password."

    def logout(self):
        self.current_user = None

    def update_profile(self, new_email, new_phone, new_password=None):
        if not self.current_user:
            return False, "No active session."

        query = "UPDATE users SET email = ?, phone = ?"
        params = [new_email, new_phone]

        if new_password:
            query += ", password = ?"
            params.append(self.hash_password(new_password))

        query += " WHERE id = ?"
        params.append(self.current_user['id'])

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, tuple(params))
                conn.commit()
                
                # Update local session state
                self.current_user['email'] = new_email
                self.current_user['phone'] = new_phone
                return True, "Profile updated successfully!"
        except sqlite3.IntegrityError:
            return False, "Email already in use by another account."
        except Exception as e:
            return False, f"Update failed: {e}"

    def delete_self_account(self):
        if not self.current_user:
            return False, "No active session."
        
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (self.current_user['id'],))
                conn.commit()
                self.logout()
                return True, "Your account has been deleted permanently."
        except Exception as e:
            return False, f"Error deleting account: {e}"

    # --- Admin Protected Methods ---
    def is_admin(self):
        return self.current_user and self.current_user['role'] == 'Admin'

    def admin_get_all_users(self):
        if not self.is_admin():
            return []
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, phone, role, created_at FROM users")
            return [dict(row) for row in cursor.fetchall()]

    def admin_search_users(self, keyword):
        if not self.is_admin():
            return []
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            search_term = f"%{keyword}%"
            cursor.execute("""
                SELECT id, username, email, phone, role, created_at FROM users
                WHERE username LIKE ? OR email LIKE ?
            """, (search_term, search_term))
            return [dict(row) for row in cursor.fetchall()]

    def admin_filter_by_role(self, role):
        if not self.is_admin():
            return []
        with self.db.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, phone, role, created_at FROM users WHERE role = ?", (role,))
            return [dict(row) for row in cursor.fetchall()]

    def admin_delete_user(self, user_id):
        if not self.is_admin():
            return False, "Unauthorized."
        if user_id == self.current_user['id']:
            return False, "You cannot delete your own admin account through the admin panel."
            
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                return True, f"User ID {user_id} deleted successfully."
        except Exception as e:
            return False, f"Error deleting user: {e}"


# ==========================================
# 3. PRESENTATION LAYER (CLI)
# ==========================================
class CLI:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.user_service = UserService(self.db_manager)

    def print_header(self, title):
        print(f"\n{'='*40}")
        print(f"  {title.upper()}")
        print(f"{'='*40}")

    def run(self):
        while True:
            if not self.user_service.current_user:
                self.show_logged_out_menu()
            else:
                self.show_logged_in_menu()

    def show_logged_out_menu(self):
        self.print_header("User Management System")
        print("1. Register Account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        if choice == '1':
            self.register_flow()
        elif choice == '2':
            self.login_flow()
        elif choice == '3':
            print("\nGoodbye!")
            exit()
        else:
            print("[!] Invalid choice. Please try again.")

    def show_logged_in_menu(self):
        user = self.user_service.current_user
        role_badge = f"[{user['role']}]"
        self.print_header(f"Dashboard - {user['username']} {role_badge}")
        
        print("1. View My Profile")
        print("2. Update My Profile")
        print("3. Delete My Account")
        if self.user_service.is_admin():
            print("4. Admin Panel")
            print("5. Logout")
        else:
            print("4. Logout")

        choice = input("\nSelect an option: ").strip()
        
        if choice == '1':
            self.view_profile_flow()
        elif choice == '2':
            self.update_profile_flow()
        elif choice == '3':
            self.delete_self_flow()
        elif choice == '4':
            if self.user_service.is_admin():
                self.show_admin_panel()
            else:
                self.user_service.logout()
                print("[*] Logged out successfully.")
        elif choice == '5' and self.user_service.is_admin():
            self.user_service.logout()
            print("[*] Logged out successfully.")
        else:
            print("[!] Invalid option.")

    def show_admin_panel(self):
        while True:
            self.print_header("Admin Control Panel")
            print("1. View All Users")
            print("2. Search Users by Name/Email")
            print("3. Filter Users by Role")
            print("4. Delete a User Account")
            print("5. Return to Main Dashboard")
            
            choice = input("\nAdmin Action (1-5): ").strip()
            
            if choice == '1':
                users = self.user_service.admin_get_all_users()
                self.display_users_table(users)
            elif choice == '2':
                kw = input("Enter search keyword (Username/Email): ").strip()
                users = self.user_service.admin_search_users(kw)
                self.display_users_table(users)
            elif choice == '3':
                role = input("Enter role to filter (Admin/User): ").strip()
                users = self.user_service.admin_filter_by_role(role)
                self.display_users_table(users)
            elif choice == '4':
                try:
                    uid = int(input("Enter User ID to delete: "))
                    confirm = input(f"Are you sure you want to delete user ID {uid}? (y/N): ")
                    if confirm.lower() == 'y':
                        success, msg = self.user_service.admin_delete_user(uid)
                        print(f"[*] {msg}")
                except ValueError:
                    print("[!] Please enter a valid numeric ID.")
            elif choice == '5':
                break
            else:
                print("[!] Invalid admin selection.")

    # Flow Helpers
    def register_flow(self):
        self.print_header("Registration")
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = getpass("Password: ")
        phone = input("Phone Number: ").strip()
        
        # Admin setup override helper for testing
        role = "User"
        if username.lower().endswith("_admin"):
            role = "Admin"
            
        if not username or not email or not password:
            print("[!] Username, Email, and Password cannot be blank.")
            return

        success, msg = self.user_service.register_user(username, email, password, phone, role)
        if success:
            print(f"[✓] {msg}")
        else:
            print(f"[!] Registration failed: {msg}")

    def login_flow(self):
        self.print_header("Secure Sign-In")
        username_or_email = input("Username or Email: ").strip()
        password = getpass("Password: ")
        
        success, msg = self.user_service.login(username_or_email, password)
        if success:
            print(f"[✓] {msg}")
        else:
            print(f"[!] Login failed: {msg}")

    def view_profile_flow(self):
        user = self.user_service.current_user
        self.print_header("My Account Details")
        print(f"ID:         {user['id']}")
        print(f"Username:   {user['username']}")
        print(f"Email:      {user['email']}")
        print(f"Phone:      {user['phone']}")
        print(f"Role:       {user['role']}")
        print(f"Created At: {user['created_at']}")
        input("\nPress Enter to return...")

    def update_profile_flow(self):
        self.print_header("Update Profile Information")
        user = self.user_service.current_user
        
        new_email = input(f"New Email [{user['email']}]: ").strip() or user['email']
        new_phone = input(f"New Phone [{user['phone']}]: ").strip() or user['phone']
        
        change_pw = input("Do you want to change your password? (y/N): ").strip().lower()
        new_pw = None
        if change_pw == 'y':
            new_pw = getpass("New Password: ")
            confirm_pw = getpass("Confirm New Password: ")
            if new_pw != confirm_pw:
                print("[!] Passwords do not match. Aborting update.")
                return
        
        success, msg = self.user_service.update_profile(new_email, new_phone, new_pw)
        if success:
            print(f"[✓] {msg}")
        else:
            print(f"[!] Update failed: {msg}")

    def delete_self_flow(self):
        self.print_header("Account Deletion Warning")
        print("This action is IRREVERSIBLE. Your account data will be permanently wiped.")
        confirm = input("Are you absolutely sure you want to delete your account? (type 'DELETE'): ").strip()
        if confirm == 'DELETE':
            success, msg = self.user_service.delete_self_account()
            if success:
                print(f"[✓] {msg}")
            else:
                print(f"[!] Deletion Failed: {msg}")
        else:
            print("[*] Aborted deletion.")

    def display_users_table(self, users):
        if not users:
            print("\n--- No records found ---")
            return
        
        # Simple formatted terminal table
        print(f"\n{'ID':<5} | {'Username':<15} | {'Email':<25} | {'Phone':<15} | {'Role':<8}")
        print("-" * 78)
        for u in users:
            phone = u['phone'] if u['phone'] else "N/A"
            print(f"{u['id']:<5} | {u['username']:<15} | {u['email']:<25} | {phone:<15} | {u['role']:<8}")
        print("-" * 78)
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    app = CLI()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated safely. Goodbye!")