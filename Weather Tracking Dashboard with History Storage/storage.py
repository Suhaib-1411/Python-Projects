import json
import os
from datetime import datetime
from config import DATA_FILE

def load_history() -> list:
    """Loads historical records from the JSON history store."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("\nWarning: History file corrupted. Initializing new records file.")
        return []

def save_record(weather_data: dict) -> bool:
    """Appends a new weather record along with a timestamp to the JSON data file."""
    if not weather_data:
        return False
        
    history = load_history()
    
    record = weather_data.copy()
    record["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(record)
    
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(history, file, indent=4)
        return True
    except IOError:
        print("\nFile Error: Unable to write data to storage.")
        return False