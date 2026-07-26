# E-Commerce Backend Logic System

A Python CLI application simulating e-commerce backend operations including product catalog querying, shopping cart management, stock-checked checkout processing, and historical order logging.

## Prerequisites

* Python 3.8+
* Built-in standard library modules: `sqlite3`, `typing`, `json`, `sys`

## File Overview

* `database.py`: Handles SQLite database initialization, relational schema creation, and product catalog seeding.
* `products.py`: Manages product lookup operations and case-insensitive catalog searching.
* `cart.py`: Implements in-memory shopping cart operations, stock limit verification, and bill total calculation.
* `orders.py`: Executes checkout transactions, deducts product inventory stock atomically, and records orders with line item details.
* `main.py`: Command Line Interface loop handling menu choices and user prompt validations.

## Setup & Execution

1. Clone or extract source files into a project directory.
2. Launch the application:
   ```bash
   python main.py