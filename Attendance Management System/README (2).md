# Attendance Management System (CSV + Database)

A Python CLI application designed to track and calculate daily attendance records for students or employees. Utilizes dual persistence through SQLite and CSV flat files to maintain data synchronization across both storage types.

## Prerequisites

* Python 3.8 or higher
* Built-in modules: `sqlite3`, `csv`, `datetime`, `sys`

## System Architecture

* `database.py`: Handles SQLite schema initialization, database queries, constraint enforcement, and record modifications.
* `csv_sync.py`: Synchronizes database contents into `attendance_records.csv` and handles summary report exports.
* `attendance.py`: Validates user input formats, date standards, and computes attendance metrics.
* `main.py`: Command Line Interface loop and menu handlers.

## Usage Guide

1. Clone or download the repository files into your working directory.
2. Run the application:
   ```bash
   python main.py