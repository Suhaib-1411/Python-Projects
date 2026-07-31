import asyncio
import sys
import os

# Ensure local module imports resolve cleanly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.chat_room import ChatRoom

async def display_incoming_messages(room: ChatRoom):
    """Background async worker that processes the message queue."""
    while True:
        msg = await room.message_queue.get()
        # Non-blocking console rendering for real-time updates
        print(f"\n[LIVE MSG] [{msg['timestamp']}] ({msg['type']}) {msg['sender']} -> {msg['recipient']}: {msg['content']}")
        room.message_queue.task_done()

async def main():
    room = ChatRoom()

    # Pre-populate default virtual users
    room.register_user("Alice")
    room.register_user("Bob")

    # Start the async background listener
    asyncio.create_task(display_incoming_messages(room))

    while True:
        print("\n==========================================")
        print("    MULTI-USER CHAT SIMULATION ENGINE     ")
        print("==========================================")
        print("1. Add New User")
        print("2. List Active Users & Status")
        print("3. Toggle User Online/Offline Status")
        print("4. Send Broadcast Message")
        print("5. Send Private Message (1-to-1)")
        print("6. View Chat History")
        print("7. Exit")

        choice = await asyncio.to_thread(input, "\nSelect an option (1-7): ")
        choice = choice.strip()

        if choice == "1":
            username = await asyncio.to_thread(input, "Enter new username: ")
            username = username.strip()
            if room.register_user(username):
                print(f"User '{username}' created successfully and set to ONLINE.")
            else:
                print(f"Error: Username '{username}' already exists.")

        elif choice == "2":
            print("\n--- Registered Users ---")
            for name, u in room.users.items():
                status = "ONLINE" if u.is_online else "OFFLINE"
                print(f"• {name} [{status}]")

        elif choice == "3":
            username = await asyncio.to_thread(input, "Enter username to toggle: ")
            username = username.strip()
            if username in room.users:
                curr = room.users[username].is_online
                room.toggle_user_status(username, not curr)
                print(f"User '{username}' is now {'ONLINE' if not curr else 'OFFLINE'}.")
            else:
                print("User not found.")

        elif choice == "4":
            sender = await asyncio.to_thread(input, "Enter sender username: ")
            msg = await asyncio.to_thread(input, "Enter message to broadcast: ")
            try:
                await room.send_message(sender.strip(), msg.strip())
                await asyncio.sleep(0.1) # Brief yield for background queue rendering
            except Exception as e:
                print(f"Execution Error: {e}")

        elif choice == "5":
            sender = await asyncio.to_thread(input, "Enter sender username: ")
            recipient = await asyncio.to_thread(input, "Enter recipient username: ")
            msg = await asyncio.to_thread(input, "Enter private message: ")
            try:
                await room.send_message(sender.strip(), msg.strip(), recipient=recipient.strip())
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Execution Error: {e}")

        elif choice == "6":
            print("\n--- Chat History Logs ---")
            history = room.storage.load_history()
            if not history:
                print("No message history available.")
            else:
                for entry in history:
                    print(f"[{entry['timestamp']}] ({entry['type']}) {entry['sender']} -> {entry['recipient']}: {entry['content']}")

        elif choice == "7":
            print("\nShutting down Chat Engine. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting...")