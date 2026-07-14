import json
import csv
import os
from datetime import datetime
from config import CONTACTS_FILE, TEMPLATES_FILE, LOG_FILE

def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        dummy = [
            {"phone": "+1234567890", "name": "Alice", "course": "Python Core"},
            {"phone": "+1987654321", "name": "Bob", "course": "Data Science"}
        ]
        with open(CONTACTS_FILE, 'w') as f:
            json.dump(dummy, f, indent=4)
        return dummy
    with open(CONTACTS_FILE, 'r') as f:
        return json.load(f)

def load_templates():
    if not os.path.exists(TEMPLATES_FILE):
        dummy = {
            "reminder": "Hello {name}, this is a reminder for your {course} class today!",
            "welcome": "Welcome {name}! Glad to have you in the {course} program."
        }
        with open(TEMPLATES_FILE, 'w') as f:
            json.dump(dummy, f, indent=4)
        return dummy
    with open(TEMPLATES_FILE, 'r') as f:
        return json.load(f)

def log_message(phone, message, status):
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Phone Number", "Message", "Status"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), phone, message, status])

def view_logs():
    if not os.path.exists(LOG_FILE):
        print("\n[!] No logs found yet.")
        return
    print("\n" + "="*40 + " MESSAGE LOGS " + "="*40)
    with open(LOG_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(f"{row[0]:<20} | {row[1]:<15} | {row[3]:<8} | {row[2][:30]}...")
    print("="*94)