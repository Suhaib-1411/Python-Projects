from datetime import datetime

class User:
    def __init__(self, username: str):
        self.username = username
        self.is_online = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_status(self, status: bool):
        self.is_online = status

    def to_dict(self):
        return {
            "username": self.username,
            "is_online": self.is_online,
            "created_at": self.created_at
        }