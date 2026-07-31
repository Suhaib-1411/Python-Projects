import asyncio
from datetime import datetime
from typing import Dict, Optional
from core.user import User
from core.storage import StorageManager

class ChatRoom:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.storage = StorageManager()
        self.message_queue = asyncio.Queue()

    def register_user(self, username: str) -> bool:
        if username in self.users:
            return False
        user = User(username)
        user.set_status(True)
        self.users[username] = user
        return True

    def toggle_user_status(self, username: str, online: bool) -> bool:
        if username in self.users:
            self.users[username].set_status(online)
            return True
        return False

    async def send_message(self, sender: str, content: str, recipient: Optional[str] = None):
        if sender not in self.users:
            raise ValueError(f"User '{sender}' does not exist.")

        if not self.users[sender].is_online:
            raise PermissionError(f"User '{sender}' is currently offline.")

        if recipient and recipient not in self.users:
            raise ValueError(f"Recipient '{recipient}' does not exist.")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg_payload = {
            "timestamp": timestamp,
            "sender": sender,
            "recipient": recipient if recipient else "ALL (Broadcast)",
            "content": content,
            "type": "PRIVATE" if recipient else "BROADCAST"
        }

        # Save to persistent storage and push to async queue
        self.storage.save_message(msg_payload)
        await self.message_queue.put(msg_payload)
        return msg_payload