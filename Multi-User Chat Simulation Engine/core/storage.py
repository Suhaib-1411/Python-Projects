import json
import os
from typing import List, Dict

HISTORY_FILE = "logs/chat_history.json"

class StorageManager:
    def __init__(self, filepath: str = HISTORY_FILE):
        self.filepath = filepath
        self._ensure_storage()

    def _ensure_storage(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save_message(self, message: Dict):
        history = self.load_history()
        history.append(message)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

    def load_history(self) -> List[Dict]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []