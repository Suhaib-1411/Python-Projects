import json
import os
import sys
from datetime import datetime

# Path fix for root directory resolution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apscheduler.schedulers.background import BackgroundScheduler
from core.task_actions import run_python_script, open_application, log_custom_message
from core.logger import logger
DATA_FILE = "data/tasks.json"

class TaskSchedulerManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.tasks = {}
        self.load_tasks()

    def start(self):
        self.scheduler.start()
        self._reschedule_all()

    def stop(self):
        self.scheduler.shutdown()

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    self.tasks = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load tasks.json: {e}")
                self.tasks = {}

    def save_tasks(self):
        os.makedirs("data", exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def _get_target_func(self, action_type, payload):
        if action_type == "script":
            return run_python_script, [payload]
        elif action_type == "open":
            return open_application, [payload]
        elif action_type == "message":
            return log_custom_message, [payload]
        return None, []

    def _reschedule_all(self):
        for task_id, task in self.tasks.items():
            if task.get("enabled", True):
                self._add_to_apscheduler(task_id, task)

    def _add_to_apscheduler(self, task_id, task):
        func, args = self._get_target_func(task["action_type"], task["payload"])
        if not func:
            return

        try:
            if task["schedule_type"] == "interval":
                minutes = int(task["value"])
                self.scheduler.add_job(
                    func, 'interval', minutes=minutes, args=args, id=task_id, replace_existing=True
                )
            elif task["schedule_type"] == "date":
                run_time = datetime.strptime(task["value"], "%Y-%m-%d %H:%M:%S")
                self.scheduler.add_job(
                    func, 'date', run_date=run_time, args=args, id=task_id, replace_existing=True
                )
        except Exception as e:
            logger.error(f"Failed to schedule job {task_id}: {e}")

    def add_task(self, name, action_type, payload, schedule_type, value):
        task_id = str(int(datetime.now().timestamp()))
        task = {
            "name": name,
            "action_type": action_type,
            "payload": payload,
            "schedule_type": schedule_type,
            "value": str(value),
            "enabled": True
        }
        self.tasks[task_id] = task
        self.save_tasks()
        self._add_to_apscheduler(task_id, task)
        logger.info(f"Task '{name}' added successfully.")

    def delete_task(self, task_id):
        if task_id in self.tasks:
            if self.scheduler.get_job(task_id):
                self.scheduler.remove_job(task_id)
            del self.tasks[task_id]
            self.save_tasks()
            logger.info(f"Task ID {task_id} deleted.")
            return True
        return False

    def toggle_task(self, task_id):
        if task_id in self.tasks:
            current_state = self.tasks[task_id].get("enabled", True)
            new_state = not current_state
            self.tasks[task_id]["enabled"] = new_state
            self.save_tasks()

            if new_state:
                self._add_to_apscheduler(task_id, self.tasks[task_id])
            else:
                if self.scheduler.get_job(task_id):
                    self.scheduler.remove_job(task_id)
            return new_state
        return None