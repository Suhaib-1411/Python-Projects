# CLI Contact Management System

A professional, modular Command-Line Interface (CLI) application for contact management. This application functions as a lightweight Customer Relationship Management (CRM) tool, allowing users to efficiently store, update, search, and maintain contact records.

## Features

- **Add Contacts:** Create new contact entries with enforced input validation for required fields, phone numbers, and email addresses.
- **View Contacts:** Display all stored records in a structured, responsive ASCII table format.
- **Search:** Perform case-insensitive, partial-match queries based on Name, Phone Number, or Email Address.
- **Filter:** Isolate specific groups of contacts by performing exact-match queries on City or Company fields.
- **Update:** Modify existing records by referencing their unique 6-character alphanumeric ID. Fields can be selectively updated without overwriting existing data.
- **Delete:** Safely remove records from the database by specifying either the Contact ID or the exact Full Name.
- **Data Persistence:** Automated reading and writing to a local `contacts.json` file ensures data is preserved between sessions.
- **Exception Handling:** Comprehensive try-except blocks prevent application termination due to invalid user input or missing files.


## Execution Instructions

1. Save the source code file as `CMS.py`.
2. Open a terminal or command prompt environment.
3. Navigate to the directory containing the script:
   ```bash
   cd path/to/directory

## Usage Guide

Upon executing the script, the main navigation menu will be displayed in the console.
   - **1** Enter 1 to append a new contact. Ensure your inputs conform to standard email and phone number formats, as validation is enforced.

   - **2**  Enter 2 to view the master list of contacts. Take note of the unique ID column, which is required for updates and specific deletions.

   - **3**  Enter 3 to search the database. This function supports partial string matching.

   - **4**  Enter 5 to update a record. You will be prompted for the Contact ID. During the update process, pressing Enter without typing a new value will preserve the existing data for that specific field.

   - **5**  Enter 7 to exit the program. All modifications are immediately committed to the JSON file upon completion of each action, ensuring no data loss.