#!/usr/bin/env python3
"""
System Resource Monitoring & Alert Script
==========================================
A CLI-based tool to monitor CPU, RAM, and Disk usage in real time,
raise alerts when user-defined thresholds are exceeded, and log
performance data to a CSV file.

Author : (your name)
Library: psutil
"""

import csv
import os
import sys
import time
import platform
from datetime import datetime

try:
    import psutil
except ImportError:
    print("ERROR: The 'psutil' library is required. Install it with:")
    print("    pip install psutil")
    sys.exit(1)

# Optional dependency for desktop notifications (bonus feature).
# The script works perfectly fine without it (falls back to console alerts).
try:
    from plyer import notification
    DESKTOP_NOTIFICATIONS_AVAILABLE = True
except ImportError:
    DESKTOP_NOTIFICATIONS_AVAILABLE = False


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_log.csv")
LOG_HEADERS = ["Timestamp", "CPU (%)", "RAM (%)", "Disk (%)", "Alert"]

DEFAULT_THRESHOLDS = {
    "cpu": 80.0,
    "ram": 80.0,
    "disk": 90.0,
}


# --------------------------------------------------------------------------- #
# Core monitoring logic
# --------------------------------------------------------------------------- #
def get_system_stats():
    """
    Collect current CPU, RAM, and Disk usage percentages.

    Returns:
        dict: {'cpu': float, 'ram': float, 'disk': float}
    """
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage(os.path.abspath(os.sep)).percent
        return {"cpu": cpu, "ram": ram, "disk": disk}
    except Exception as exc:
        print(f"[ERROR] Failed to read system stats: {exc}")
        return {"cpu": 0.0, "ram": 0.0, "disk": 0.0}


def check_alerts(stats, thresholds):
    """
    Compare current stats against thresholds.

    Args:
        stats (dict): current resource usage
        thresholds (dict): user-defined limits

    Returns:
        list[str]: list of human-readable alert messages (empty if none)
    """
    alerts = []
    for key, label in (("cpu", "CPU"), ("ram", "RAM"), ("disk", "Disk")):
        if stats[key] >= thresholds[key]:
            alerts.append(
                f"{label} usage is {stats[key]:.1f}% (threshold: {thresholds[key]:.1f}%)"
            )
    return alerts


def trigger_alert(alerts):
    """
    Notify the user about active alerts via console (always) and
    desktop notification / sound (if available).
    """
    if not alerts:
        return

    print("\n" + "!" * 60)
    print(" ALERT: Resource threshold exceeded!")
    for a in alerts:
        print(f"  -> {a}")
    print("!" * 60)

    # Terminal bell (cross-platform, no extra dependency)
    sys.stdout.write("\a")
    sys.stdout.flush()

    if DESKTOP_NOTIFICATIONS_AVAILABLE:
        try:
            notification.notify(
                title="System Resource Alert",
                message="\n".join(alerts),
                timeout=5,
            )
        except Exception:
            # Desktop notifications are a bonus feature; never crash on failure
            pass


# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
def init_log_file(path=LOG_FILE):
    """Create the CSV log file with headers if it doesn't already exist."""
    if not os.path.exists(path):
        try:
            with open(path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(LOG_HEADERS)
        except OSError as exc:
            print(f"[ERROR] Could not create log file: {exc}")


def log_data(stats, alerts, path=LOG_FILE):
    """Append a single row of stats + alert status to the CSV log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_text = "; ".join(alerts) if alerts else "OK"
    try:
        with open(path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [timestamp, f"{stats['cpu']:.1f}", f"{stats['ram']:.1f}",
                 f"{stats['disk']:.1f}", alert_text]
            )
    except OSError as exc:
        print(f"[ERROR] Could not write to log file: {exc}")


def view_logs(path=LOG_FILE, last_n=20):
    """Print the last N entries from the log file in a readable table."""
    if not os.path.exists(path):
        print("\nNo log file found yet. Start monitoring first to generate logs.\n")
        return

    try:
        with open(path, mode="r", newline="", encoding="utf-8") as f:
            reader = list(csv.reader(f))
    except OSError as exc:
        print(f"[ERROR] Could not read log file: {exc}")
        return

    if len(reader) <= 1:
        print("\nLog file is empty.\n")
        return

    header, rows = reader[0], reader[1:]
    rows_to_show = rows[-last_n:]

    print(f"\nShowing last {len(rows_to_show)} of {len(rows)} log entries "
          f"({path}):\n")
    col_widths = [max(len(h), 12) for h in header]
    print(" | ".join(h.ljust(w) for h, w in zip(header, col_widths)))
    print("-" * (sum(col_widths) + 3 * (len(header) - 1)))
    for row in rows_to_show:
        print(" | ".join(str(c).ljust(w) for c, w in zip(row, col_widths)))
    print()


# --------------------------------------------------------------------------- #
# CLI display helpers
# --------------------------------------------------------------------------- #
def format_bar(percent, width=30):
    """Return a simple text progress bar for a percentage value."""
    filled = int(width * percent / 100)
    filled = max(0, min(width, filled))
    bar = "#" * filled + "-" * (width - filled)
    return f"[{bar}] {percent:5.1f}%"


def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")


def print_dashboard(stats, thresholds, alerts, elapsed):
    clear_screen()
    print("=" * 60)
    print(" SYSTEM RESOURCE MONITOR ".center(60, "="))
    print("=" * 60)
    print(f" Elapsed time: {elapsed}s   |   Press Ctrl+C to stop\n")

    print(f" CPU  {format_bar(stats['cpu'])}   (threshold {thresholds['cpu']:.0f}%)")
    print(f" RAM  {format_bar(stats['ram'])}   (threshold {thresholds['ram']:.0f}%)")
    print(f" Disk {format_bar(stats['disk'])}   (threshold {thresholds['disk']:.0f}%)")

    if alerts:
        print("\n ALERTS:")
        for a in alerts:
            print(f"  ⚠️  {a}")
    else:
        print("\n Status: All resources within normal limits. ✅")
    print("\n" + "=" * 60)


# --------------------------------------------------------------------------- #
# Menu actions
# --------------------------------------------------------------------------- #
def set_thresholds(thresholds):
    """Prompt the user to update CPU/RAM/Disk thresholds."""
    print("\n--- Set Alert Thresholds ---")
    print(f"(Press Enter to keep current value)\n")
    for key, label in (("cpu", "CPU"), ("ram", "RAM"), ("disk", "Disk")):
        current = thresholds[key]
        raw = input(f"{label} threshold %% [{current:.0f}]: ").strip()
        if raw == "":
            continue
        try:
            value = float(raw)
            if 0 < value <= 100:
                thresholds[key] = value
            else:
                print("  -> Value must be between 0 and 100. Skipped.")
        except ValueError:
            print("  -> Invalid number. Skipped.")
    print("\nUpdated thresholds:")
    for key, label in (("cpu", "CPU"), ("ram", "RAM"), ("disk", "Disk")):
        print(f"  {label}: {thresholds[key]:.0f}%")
    input("\nPress Enter to return to the menu...")


def start_monitoring(thresholds, interval=2):
    """Run the real-time monitoring loop until interrupted (Ctrl+C)."""
    print(f"\nStarting monitoring (refresh every {interval}s). Press Ctrl+C to stop.\n")
    time.sleep(1)
    start_time = time.time()
    try:
        while True:
            stats = get_system_stats()
            alerts = check_alerts(stats, thresholds)
            elapsed = int(time.time() - start_time)

            print_dashboard(stats, thresholds, alerts, elapsed)
            log_data(stats, alerts)

            if alerts:
                trigger_alert(alerts)

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user. Returning to menu...\n")
        time.sleep(1)
    except Exception as exc:
        print(f"\n[ERROR] Monitoring loop crashed: {exc}")
        input("Press Enter to return to the menu...")


def print_menu():
    print("\n" + "=" * 40)
    print(" SYSTEM RESOURCE MONITOR - MAIN MENU")
    print("=" * 40)
    print(" 1. Start Monitoring")
    print(" 2. Set Thresholds")
    print(" 3. View Logs")
    print(" 4. Exit")
    print("=" * 40)


def main():
    init_log_file()
    thresholds = DEFAULT_THRESHOLDS.copy()

    while True:
        print_menu()
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            start_monitoring(thresholds)
        elif choice == "2":
            set_thresholds(thresholds)
        elif choice == "3":
            view_logs()
            input("Press Enter to return to the menu...")
        elif choice == "4":
            print("\nExiting. Goodbye!\n")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
