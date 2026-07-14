import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTACTS_FILE = os.path.join(BASE_DIR, "contacts.json")
TEMPLATES_FILE = os.path.join(BASE_DIR, "templates.json")
LOG_FILE = os.path.join(BASE_DIR, "whatsapp_log.csv")

# Selenium Settings
CHROME_PROFILE_DIR = os.path.join(BASE_DIR, "selenium_profile")