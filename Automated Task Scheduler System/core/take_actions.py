import os
import subprocess
from core.logger import logger

def run_python_script(script_path: str):
    """Executes an external Python script."""
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True, check=True)
        msg = f"SUCCESS: Script '{script_path}' executed. Output: {result.stdout.strip()}"
        logger.info(msg)
        print(f"\n[TASK EXECUTED] {msg}")
    except Exception as e:
        msg = f"FAILED: Script '{script_path}' failed. Error: {e}"
        logger.error(msg)
        print(f"\n[TASK FAILED] {msg}")

def open_application(app_path: str):
    """Opens a file or application."""
    try:
        os.startfile(app_path)
        msg = f"SUCCESS: Opened application/file '{app_path}'"
        logger.info(msg)
        print(f"\n[TASK EXECUTED] {msg}")
    except Exception as e:
        msg = f"FAILED: Could not open '{app_path}'. Error: {e}"
        logger.error(msg)
        print(f"\n[TASK FAILED] {msg}")

def log_custom_message(message: str):
    """Logs a custom user message."""
    msg = f"SUCCESS: Message Logged -> {message}"
    logger.info(msg)
    print(f"\n[TASK EXECUTED] {msg}")