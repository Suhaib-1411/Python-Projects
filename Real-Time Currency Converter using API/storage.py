import json
import os
from datetime import datetime
from config import DATA_FILE

def load_history() -> list:
    """Loads historical calculation data from the persistent JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("\nWarning: Log file unreadable. Initializing fresh registry configuration.")
        return []

def persist_to_disk(session_buffer: list) -> bool:
    """Writes the accumulated session conversion records out to the JSON file."""
    if not session_buffer:
        print("\nInformation: No new conversion data available to save.")
        return False
        
    current_history = load_history()
    current_history.extend(session_buffer)
    
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(current_history, file, indent=4)
        return True
    except IOError:
        print("\nFile Error: Disk write failure encountered while saving history.")
        return False