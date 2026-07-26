# Blog Backend Data Management System

A Python backend system managing user registration, authentication, blog post CRUD lifecycle operations, and nested thread comments backed by relational SQLite persistence.

## Prerequisites

* Python 3.8+
* Native standard library modules: `sqlite3`, `hashlib`, `os`, `sys`

## File Overview

* `database.py`: Manages SQLite engine connectivity, schema migration, and initial seeding.
* `auth.py`: Implements PBKDF2 HMAC-SHA256 password hashing with unique per-user cryptographic salts and handles user authentication.
* `blog.py`: Executes data querying logic for post lifecycle management (Create, Read, Update, Delete) and comment appending.
* `main.py`: Command Line Interface context router handling session tracking and input prompt handling.

## Installation & Running

1. Clone or extract source files into your target directory.
2. Launch the application:
   ```bash
   python main.py