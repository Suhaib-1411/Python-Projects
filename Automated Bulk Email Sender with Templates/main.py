import os
import csv
import smtplib
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Global variables
contacts = []
template_content = ""
history_file = "email_history.json"

def load_contacts():
    """Menu 1: Loads recipient data from a CSV file"""
    global contacts
    filename = input("\nEnter CSV file name (e.g., contacts.csv): ").strip()
    
    if not os.path.exists(filename):
        print(" Error: CSV file not found!")
        return

    contacts = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Basic cleaning of data
                contacts.append({
                    "name": row.get("name", "").strip(),
                    "email": row.get("email", "").strip(),
                    "company": row.get("company", "").strip()
                })
        print(f" Success! Loaded {len(contacts)} contact(s) from '{filename}'.")
    except Exception as e:
        print(f" Error reading CSV: {e}")

def load_template():
    """Menu 2: Reads the text template containing placeholders"""
    global template_content
    filename = input("\nEnter template text file name (e.g., template.txt): ").strip()
    
    if not os.path.exists(filename):
        print(" Error: Template file not found!")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            template_content = file.read()
        print(" Template loaded successfully! Preview:")
        print("-" * 30)
        print(template_content)
        print("-" * 30)
    except Exception as e:
        print(f" Error reading template file: {e}")

def log_history(email, subject, status):
    """Helper: Appends email outcomes to a local JSON tracking history file"""
    history_data = []
    if os.path.exists(history_file) and os.path.getsize(history_file) > 0:
        try:
            with open(history_file, 'r', encoding='utf-8') as file:
                history_data = json.load(file)
        except json.JSONDecodeError:
            history_data = []

    log_entry = {
        "email": email,
        "subject": subject,
        "status": status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    history_data.append(log_entry)

    with open(history_file, 'w', encoding='utf-8') as file:
        json.dump(history_data, file, indent=4)

def send_bulk_emails():
    """Menu 3: Iterates through contacts, personalizes text templates, and transmits via SMTP"""
    global contacts, template_content
    if not contacts:
        print(" No contacts loaded. Run Option 1 first.")
        return
    if not template_content:
        print(" No template loaded. Run Option 2 first.")
        return

    print("\n --- SMTP Configuration ---")
    sender_email = input("Enter your email address: ").strip()
    # It is recommended to use a Gmail App Password rather than a main account password
    password = input("Enter your App Password: ").strip()
    subject = input("Enter email subject line: ").strip()

    print("\n Initiating bulk delivery process...")
    
    # Setting up standard SMTP connection rules (using Gmail as standard default baseline example)
    smtp_server = "smtp.gmail.com"
    port = 587

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Secure connection upgrade step
        server.login(sender_email, password)
    except Exception as e:
        print(f" Authentication or connection failed: {e}")
        return

    for contact in contacts:
        # Prevent blanks or poorly formed values breaking loop iterations
        if not contact["email"]:
            continue
            
        try:
            # Personalizing placeholders dynamically
            personalized_body = template_content.format(
                name=contact["name"],
                company=contact["company"]
            )
            
            # Constructing email package structures
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = contact["email"]
            msg['Subject'] = subject
            msg.attach(MIMEText(personalized_body, 'plain'))
            
            # Fire transmission
            server.sendmail(sender_email, contact["email"], msg.as_string())
            print(f" Email successfully transmitted to: {contact['email']}")
            log_history(contact["email"], subject, "Sent")
            
        except Exception as err:
            print(f" Delivery failure to {contact['email']}: {err}")
            log_history(contact["email"], subject, f"Failed: {str(err)}")

    server.quit()
    print("\n🏁 Bulk processing cycle completed.")

def view_history():
    """Menu 4: Reads and outputs the logged history file results cleanly to console"""
    if not os.path.exists(history_file) or os.path.getsize(history_file) == 0:
        print("\n No email records found in history registry logs.")
        return

    try:
        with open(history_file, 'r', encoding='utf-8') as file:
            logs = json.load(file)
            print("\n --- SENT EMAIL HISTORY ---")
            print(f"{'Timestamp':<20} | {'Recipient Email':<25} | {'Status':<10}")
            print("-" * 65)
            for item in logs:
                print(f"{item['timestamp']:<20} | {item['email']:<25} | {item['status']:<10}")
    except Exception as e:
        print(f" Error displaying telemetry log history: {e}")

def main():
    """Main application loop controlling interface mechanics"""
    while True:
        print("\n=========================================")
        print("     BULK EMAIL SENDER APPLICATION     ")
        print("=========================================")
        print("1. Load Contacts (CSV)")
        print("2. Load Email Template")
        print("3. Send Bulk Emails")
        print("4. View Delivery History")
        print("5. Exit")
        print("=========================================")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            load_contacts()
        elif choice == '2':
            load_template()
        elif choice == '3':
            send_bulk_emails()
        elif choice == '4':
            view_history()
        elif choice == '5':
            print("\n Exiting App. Have a productive day!")
            break
        else:
            print(" Invalid menu assignment entry selection.")

if __name__ == "__main__":
    main()