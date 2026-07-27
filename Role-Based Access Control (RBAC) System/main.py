import sys
import getpass
import database
import auth
import rbac

current_user = None  # Active session holder: Dict[str, str] or None

def print_welcome_menu():
    print("\n--- ROLE-BASED ACCESS CONTROL (RBAC) SYSTEM ---")
    print("1. Register Account")
    print("2. Login")
    print("3. Exit")

def print_authenticated_menu():
    role = current_user['role']
    print(f"\n--- LOGGED IN AS: {current_user['username']} [{role}] ---")
    print("1. View User Dashboard")
    print("2. View Data Records")
    print("3. Add Data Record")
    print("4. Edit Data Record")
    print("5. Delete Data Record")
    if role == "ADMIN":
        print("6. Admin Panel (Manage Roles / System Logs / Export)")
    print("0. Logout")

def handle_registration():
    print("\n--- USER REGISTRATION ---")
    username = input("Enter Username: ").strip()
    try:
        password = getpass.getpass("Enter Password: ").strip()
    except Exception:
        password = input("Enter Password: ").strip()

    print("Available Roles: USER, MANAGER, ADMIN")
    role = input("Assign Initial Role [Default: USER]: ").strip()
    if not role:
        role = "USER"

    auth.register_user(username, password, role)

def handle_login():
    global current_user
    print("\n--- SYSTEM LOGIN ---")
    username = input("Username: ").strip()
    try:
        password = getpass.getpass("Password: ").strip()
    except Exception:
        password = input("Password: ").strip()

    user_profile = auth.authenticate_user(username, password)
    if user_profile:
        current_user = user_profile
        rbac.log_activity(username, "User Login", "SUCCESS")
        print(f"\nSuccess: Login successful. Welcome, {user_profile['username']}!")
    else:
        rbac.log_activity(username, "User Login Attempt", "ACCESS DENIED")
        print("\nError: Invalid credentials.")

def enforce_permission(permission: str) -> bool:
    """Middleware-style check enforcing role permissions before executing actions."""
    if not current_user:
        print("\nError: No active user session.")
        return False

    allowed = rbac.check_permission(current_user["role"], permission)
    if not allowed:
        rbac.log_activity(current_user["username"], f"Execute Action '{permission}'", "ACCESS DENIED")
        print("\n" + "!"*50)
        print(" ACCESS DENIED: You lack required permission for this action.")
        print(f" Required Permission: [{permission}] | Your Role: [{current_user['role']}]")
        print("!"*50)
        return False

    rbac.log_activity(current_user["username"], f"Execute Action '{permission}'", "SUCCESS")
    return True

def handle_view_dashboard():
    print("\n" + "="*50)
    print(f" USER DASHBOARD")
    print("="*50)
    print(f" Username: {current_user['username']}")
    print(f" Role:     {current_user['role']}")
    print("\n Authorized Capabilities:")
    permissions = rbac.ROLE_PERMISSIONS.get(current_user['role'], set())
    for p in sorted(permissions):
        print(f"  [✓] {p}")
    print("="*50)

def handle_view_data():
    if not enforce_permission("view_data"):
        return

    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM records ORDER BY id ASC;")
        records = cursor.fetchall()

    print("\n--- SHARED DATA RECORDS ---")
    if not records:
        print("Information: No data records exist.")
        return

    print(f"{'ID':<5} | {'Title':<20} | {'Content':<30} | {'Created By':<12}")
    print("-" * 75)
    for r in records:
        print(f"{r['id']:<5} | {r['title']:<20} | {r['content']:<30} | {r['created_by']:<12}")

def handle_add_data():
    if not enforce_permission("add_data"):
        return

    print("\n--- ADD DATA RECORD ---")
    title = input("Enter Record Title: ").strip()
    content = input("Enter Record Content: ").strip()

    if not title or not content:
        print("\nError: Title and Content cannot be blank.")
        return

    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO records (title, content, created_by)
            VALUES (?, ?, ?);
        """, (title, content, current_user["username"]))
        conn.commit()
        print(f"\nSuccess: Added new record '{title}'.")

def handle_edit_data():
    if not enforce_permission("edit_data"):
        return

    print("\n--- EDIT DATA RECORD ---")
    try:
        record_id = int(input("Enter Record ID to Edit: "))
    except ValueError:
        print("\nError: ID must be an integer.")
        return

    new_title = input("Enter New Title: ").strip()
    new_content = input("Enter New Content: ").strip()

    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE records
            SET title = ?, content = ?
            WHERE id = ?;
        """, (new_title, new_content, record_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"\nSuccess: Updated Record ID {record_id}.")
        else:
            print(f"\nError: Record ID {record_id} not found.")

def handle_delete_data():
    if not enforce_permission("delete_data"):
        return

    print("\n--- DELETE DATA RECORD ---")
    try:
        record_id = int(input("Enter Record ID to Delete: "))
    except ValueError:
        print("\nError: ID must be an integer.")
        return

    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records WHERE id = ?;", (record_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"\nSuccess: Record ID {record_id} deleted.")
        else:
            print(f"\nError: Record ID {record_id} not found.")

def handle_admin_panel():
    if not enforce_permission("manage_roles"):
        return

    print("\n" + "="*50)
    print(" ADMIN CONTROL PANEL")
    print("="*50)
    print("1. Modify User Role Assignment")
    print("2. View System Audit Logs")
    print("3. Export User Roles Report")
    print("4. Return to Main Menu")
    choice = input("Select Option (1-4): ").strip()

    if choice == "1":
        target_user = input("Enter Username to modify: ").strip()
        new_role = input("Enter New Role (USER / MANAGER / ADMIN): ").strip()
        rbac.update_user_role(current_user["username"], target_user, new_role)
    elif choice == "2":
        if enforce_permission("view_logs"):
            logs = rbac.get_activity_logs()
            print("\n--- SYSTEM AUDIT LOGS ---")
            print(f"{'Time':<20} | {'User':<12} | {'Action':<35} | {'Status':<15}")
            print("-" * 85)
            for l in logs:
                print(f"{l['timestamp']:<20} | {l['username']:<12} | {l['action']:<35} | {l['status']:<15}")
    elif choice == "3":
        if enforce_permission("export_report"):
            rbac.export_roles_report()

def run_app():
    global current_user
    database.init_db()

    # Seed initial default admin if database is new
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM users;")
        if cursor.fetchone()["cnt"] == 0:
            auth.register_user("admin", "Admin123!", "ADMIN")

    while True:
        if current_user is None:
            print_welcome_menu()
            choice = input("\nSelect Option (1-3): ").strip()
            if choice == "1":
                handle_registration()
            elif choice == "2":
                handle_login()
            elif choice == "3":
                print("\nExiting RBAC System.")
                sys.exit()
            else:
                print("\nInvalid choice. Select between 1 and 3.")
        else:
            print_authenticated_menu()
            choice = input("\nSelect Option: ").strip()
            if choice == "1":
                handle_dashboard() if 'handle_dashboard' in locals() else handle_view_dashboard()
            elif choice == "2":
                handle_view_data()
            elif choice == "3":
                handle_add_data()
            elif choice == "4":
                handle_edit_data()
            elif choice == "5":
                handle_delete_data()
            elif choice == "6" and current_user['role'] == "ADMIN":
                handle_admin_panel()
            elif choice == "0":
                rbac.log_activity(current_user["username"], "User Logout", "SUCCESS")
                print(f"\nUser '{current_user['username']}' logged out.")
                current_user = None
            else:
                print("\nInvalid selection.")

if __name__ == "__main__":
    run_app()