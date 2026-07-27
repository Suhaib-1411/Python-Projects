# Role-Based Access Control (RBAC) System

A Python CLI application implementing Role-Based Access Control (RBAC) with secure password hashing (PBKDF2-HMAC-SHA256), permission validation, activity audit logging, and SQLite database storage.

## Roles & Permissions Matrix

| Permission | User | Manager | Admin |
| :--- | :---: | :---: | :---: |
| `view_data` | ✓ | ✓ | ✓ |
| `add_data` | ✗ | ✓ | ✓ |
| `edit_data` | ✗ | ✓ | ✓ |
| `delete_data` | ✗ | ✗ | ✓ |
| `manage_roles` | ✗ | ✗ | ✓ |
| `view_logs` | ✗ | ✗ | ✓ |
| `export_report` | ✗ | ✗ | ✓ |

## Prerequisites

* Python 3.8 or higher
* Standard Library modules: `sqlite3`, `hashlib`, `os`, `csv`, `getpass`, `sys`

## Application Setup & Execution

1. Run the main script:
   ```bash
   python main.py