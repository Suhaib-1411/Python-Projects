import csv
import database

# Mapping of normalized Roles to Permission sets
ROLE_PERMISSIONS = {
    "ADMIN": {"view_data", "add_data", "edit_data", "delete_data", "manage_roles", "view_logs", "export_report"},
    "MANAGER": {"view_data", "add_data", "edit_data"},
    "USER": {"view_data"}
}

def check_permission(user_role: str, required_permission: str) -> bool:
    """Checks whether a user role possesses a required permission."""
    role_clean = user_role.strip().upper()
    allowed_permissions = ROLE_PERMISSIONS.get(role_clean, set())
    return required_permission in allowed_permissions

def log_activity(username: str, action: str, status: str):
    """Records user actions and authorization status into the audit log."""
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO activity_logs (username, action, status)
            VALUES (?, ?, ?);
        """, (username, action, status))
        conn.commit()

def update_user_role(admin_username: str, target_username: str, new_role: str) -> bool:
    """Updates the assigned role of a target user (Admin privilege required)."""
    new_role_clean = new_role.strip().upper()
    if new_role_clean not in ROLE_PERMISSIONS:
        print(f"\nError: Invalid role '{new_role}'. Allowed: {list(ROLE_PERMISSIONS.keys())}")
        return False

    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE username = ?;", (new_role_clean, target_username.strip()))
        conn.commit()
        if cursor.rowcount > 0:
            log_activity(admin_username, f"Assigned role '{new_role_clean}' to '{target_username}'", "SUCCESS")
            print(f"\nSuccess: Updated role for user '{target_username}' to '{new_role_clean}'.")
            return True
        else:
            print(f"\nError: User '{target_username}' not found.")
            return False

def get_activity_logs() -> list:
    """Retrieves past activity audit logs."""
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT 50;")
        return cursor.fetchall()

def export_roles_report(filename: str = "user_roles_report.csv") -> bool:
    """Exports user account role listings to a CSV report file."""
    try:
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY id ASC;")
            users = cursor.fetchall()

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["User_ID", "Username", "Assigned_Role", "Created_At"])
            for u in users:
                writer.writerow([u["id"], u["username"], u["role"], u["created_at"]])
        print(f"\nSuccess: User roles report exported to '{filename}'.")
        return True
    except Exception as e:
        print(f"\nError exporting report: {e}")
        return False