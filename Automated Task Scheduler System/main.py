import sys
import os
import time

# Ensure core imports work regardless of execution folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.scheduler_manager import TaskSchedulerManager

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    manager = TaskSchedulerManager()
    manager.start()
    print("Task Scheduler Service Started running in background...")

    while True:
        print("\n==========================================")
        print("    AUTOMATED TASK SCHEDULER SYSTEM      ")
        print("==========================================")
        print("1. Schedule New Task")
        print("2. View Scheduled Tasks")
        print("3. Toggle Task Status (Enable/Disable)")
        print("4. Delete Task")
        print("5. View Execution Logs")
        print("6. Exit")

        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            print("\n--- Schedule New Task ---")
            name = input("Enter Task Name: ").strip()
            
            print("\nSelect Action Type:")
            print(" 1. Run Python Script")
            print(" 2. Open Application/File")
            print(" 3. Print/Log Message")
            act_choice = input("Choice (1-3): ").strip()
            action_map = {"1": "script", "2": "open", "3": "message"}
            action_type = action_map.get(act_choice, "message")

            payload = input("Enter path or message payload: ").strip()

            print("\nSelect Schedule Type:")
            print(" 1. Time Interval (In Minutes)")
            print(" 2. Specific Date & Time (YYYY-MM-DD HH:MM:SS)")
            sched_choice = input("Choice (1-2): ").strip()

            if sched_choice == "1":
                schedule_type = "interval"
                value = input("Enter interval duration in minutes: ").strip()
            else:
                schedule_type = "date"
                value = input("Enter run time (e.g., 2026-08-01 14:30:00): ").strip()

            manager.add_task(name, action_type, payload, schedule_type, value)
            print("Task scheduled successfully!")

        elif choice == "2":
            print("\n--- Scheduled Tasks ---")
            if not manager.tasks:
                print("No tasks registered.")
            else:
                for t_id, t in manager.tasks.items():
                    status = "[ACTIVE]" if t.get("enabled", True) else "[DISABLED]"
                    print(f"ID: {t_id} | Name: {t['name']} | Type: {t['schedule_type']} ({t['value']}) | Action: {t['action_type']} | Status: {status}")

        elif choice == "3":
            t_id = input("Enter Task ID to enable/disable: ").strip()
            res = manager.toggle_task(t_id)
            if res is not None:
                print(f"Task ID {t_id} is now {'ACTIVE' if res else 'DISABLED'}.")
            else:
                print("Task ID not found.")

        elif choice == "4":
            t_id = input("Enter Task ID to delete: ").strip()
            if manager.delete_task(t_id):
                print("Task deleted successfully.")
            else:
                print("Task ID not found.")

        elif choice == "5":
            print("\n--- Execution History Logs ---")
            if os.path.exists("logs/execution.log"):
                with open("logs/execution.log", "r", encoding="utf-8") as f:
                    logs = f.readlines()
                    print("".join(logs[-15:]) if logs else "Logs are currently empty.")
            else:
                print("No log file found.")

        elif choice == "6":
            print("\nShutting down Task Scheduler service...")
            manager.stop()
            sys.exit(0)

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()