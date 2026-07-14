# Secure Python-SQLite User Management System

An advanced Command Line Interface (CLI) application developed in Python utilizing an SQLite database to securely store and manage user profiles. Featuring cryptographic password hashing, parameterized SQL queries for defense against injection attacks, session tracking, and a fully functional Role-Based Access Control (RBAC) Admin dashboard.

##  Key Features

* **Robust Security:** High-strength SHA-256 password hashing ensures credentials are never stored in plaintext.
* **SQL Injection Defense:** Built completely on parameterized queries using standard database drivers.
* **Session Management:** Keeps track of login state in-memory during application runtime.
* **Role-Based Access Control (RBAC):** Restricts admin management tools exclusively to users flagged as administrators.
* **Full CRUD Operations:** * **C**reate: Register new profile with unique validations.
    * **R**ead: Dynamic CLI profiling showing customized details.
    * **U**pdate: Dynamic schema update routines safely changing operational data.
    * **D**elete: Cascaded account self-removal system.
* **Modular Architecture:** Separation of database management (`DatabaseManager`), controller/business logic (`UserService`), and UI logic (`CLI`).

---

##  Tech Stack
* **Language:** Python 3.x
* **Database Engine:** SQLite3 (standard library)
* **Crypto Engine:** Hashlib SHA-256 (standard library)

---

##  Getting Started

### Prerequisites
* Python 3.6 or higher installed on your system. No third-party modules required!

### Setup Instructions
1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/your-repo-name.git](https://github.com/YOUR_USERNAME/your-repo-name.git)
    cd your-repo-name
    ```
2.  **Execute the Script**
    ```bash
    python app.py
    ```

###  Default Credentials
To help evaluate the Admin features instantly, the database auto-seeds a default admin account on its first run:
* **Username:** `admin`
* **Password:** `admin123`

---

##  Database Schema Details

The database table `users` is dynamically configured with the following properties:

| Column Name | Data Type | Constraints |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key, Auto-Increment |
| `username` | TEXT | UNIQUE, NOT NULL |
| `email` | TEXT | UNIQUE, NOT NULL |
| `password` | TEXT | Hashed SHA-256 String, NOT NULL |
| `phone` | TEXT | Nullable |
| `role` | TEXT | Default 'User' |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |