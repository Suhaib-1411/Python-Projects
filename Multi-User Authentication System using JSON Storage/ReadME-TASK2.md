# Secure Multi-User Authentication System

A command-line based multi-user authentication system built in Python. This system simulates a standard registration and login workflow, managing user state and data securely via JSON storage.

## Features

### Core Functionality
* **User Registration:** Create an account with a unique username, email address, and strong password.
* **User Login:** Authenticate using either a username or registered email alongside the corresponding password.
* **JSON Persistence:** Automatically serializes and stores user data to `users.json`.
* **Secure Input:** Utilizes Python's `getpass` module to obscure passwords during terminal input.

### Security Enhancements
* **Cryptographic Hashing:** Passwords are hashed using the `SHA-256` algorithm prior to storage. Plaintext passwords are never saved.
* **Input Validation:** * Emails are validated against standard regular expression patterns.
    * Passwords enforce a minimum length of 8 characters, requiring at least one uppercase letter and one numeric digit.
* **Anti-Duplication Logic:** Registration actively prevents duplicate usernames and emails (case-insensitive evaluation).
* **Brute-Force Mitigation:** Accounts lock automatically following 3 consecutive failed login attempts.
* **Role-Based Access Control:** The first user to register is granted an `Admin` role; subsequent users default to `User`.
* **Account Lifecycle Management:** Users can reset passwords using registered email verification or permanently delete their accounts from the authenticated dashboard.

## Execution Guide

### Prerequisites
* Python 3.x environment.
* Standard built-in libraries (`json`, `os`, `hashlib`, `re`, `getpass`). No external dependencies are required.

### Running the Application
1. Save the source code block to a local file named `auth_system.py`.
2. Open a terminal or command prompt instance.
3. Navigate to the working directory where the file is stored.
4. Execute the script via the command line:
   ```bash
   python auth_system.py