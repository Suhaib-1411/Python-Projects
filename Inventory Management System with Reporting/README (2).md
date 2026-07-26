# Inventory Management System

A Python CLI application designed for retail and warehouse operations to track stock, execute sales, enforce data constraints, and output analytical inventory reports.

## Prerequisites

* Python 3.x
* Built-in `sqlite3` library (included standard with Python installations)

## File Structure

* `database.py`: Direct SQLite interaction layer, query management, schema definitions.
* `inventory.py`: Core business logic, validation rules (non-negative price/stock enforcement).
* `reports.py`: Analytics generation and file exporter functionality.
* `main.py`: Command Line Interface loop and menu handlers.

## Setup & Running

1. Clone or download the source files into a project directory.
2. Execute the application:
   ```bash
   python main.py