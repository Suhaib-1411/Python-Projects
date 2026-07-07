# 🖥️ System Resource Monitoring & Alert Script

A lightweight, CLI-based Python tool that monitors **CPU**, **RAM**, and **Disk**
usage in real time, raises alerts when user-defined thresholds are exceeded,
and logs performance data to a CSV file for later review.

This project simulates the core functionality of real-world IT monitoring
tools (like a mini Nagios / Zabbix / htop combo) using only `psutil` and the
Python standard library.

---

## ✨ Features

- **Real-time monitoring** — live CPU / RAM / Disk usage with a text progress bar
- **Custom alert thresholds** — set your own limits for each resource
- **Alerts** — console warning, terminal bell sound, and optional desktop
  pop-up notification (via `plyer`, if installed)
- **CSV logging** — every reading is timestamped and saved to `system_log.csv`
- **Log viewer** — view the most recent log entries directly from the menu
- **Modular code** — monitoring, alerting, and logging are separate,
  independently testable functions
- **Robust error handling** — the app won't crash if a sensor read fails,
  the log file can't be written, or a notification library is missing

---

## 📦 Requirements

- Python 3.7+
- [`psutil`](https://pypi.org/project/psutil/) (required)
- [`plyer`](https://pypi.org/project/plyer/) (optional — enables desktop
  notifications; the app works fine without it)

## 🔧 Installation

```bash
# 1. Clone or download this repository
git clone <your-repo-url>
cd resource_monitor

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## ▶️ Usage

Run the script:

```bash
python3 resource_monitor.py
```

You'll see a main menu:

```
========================================
 SYSTEM RESOURCE MONITOR - MAIN MENU
========================================
 1. Start Monitoring
 2. Set Thresholds
 3. View Logs
 4. Exit
========================================
```

### 1. Start Monitoring
Displays a live-updating dashboard with CPU, RAM, and Disk usage bars.
Every reading is written to `system_log.csv`. If any resource crosses its
threshold, you'll see an on-screen alert, hear a terminal bell, and (if
`plyer` is installed) get a desktop notification. Stop monitoring anytime
with `Ctrl+C`.

### 2. Set Thresholds
Update the alert limits for CPU, RAM, and Disk (as a percentage, 0–100).
Press Enter on any prompt to keep the current value.

### 3. View Logs
Prints the most recent entries from `system_log.csv` in a readable table.

### 4. Exit
Closes the application.

---

## 📁 Log File Format

`system_log.csv` — a sample is included in this repository:

| Timestamp           | CPU (%) | RAM (%) | Disk (%) | Alert                                  |
|----------------------|---------|---------|----------|-----------------------------------------|
| 2026-07-05 04:28:03  | 0.0     | 6.5     | 46.1     | OK                                       |
| 2026-07-05 04:28:11  | 92.3    | 75.2    | 60.1     | CPU usage is 92.3% (threshold: 80.0%)    |

---

## 🗂️ Project Structure

```
resource_monitor/
├── resource_monitor.py   # Main application (all logic, modular functions)
├── requirements.txt      # Python dependencies
├── system_log.csv        # Sample log file (generated automatically)
└── README.md             # This file
```

## 🧩 Code Design (Modularity)

| Function              | Responsibility                                   |
|-----------------------|---------------------------------------------------|
| `get_system_stats()`  | Reads CPU/RAM/Disk usage via `psutil`             |
| `check_alerts()`      | Compares readings against thresholds               |
| `trigger_alert()`     | Displays/sounds/notifies on threshold breach       |
| `log_data()`          | Appends a row to the CSV log                       |
| `view_logs()`         | Reads and pretty-prints recent log entries         |
| `print_dashboard()`   | Renders the live CLI dashboard                      |
| `start_monitoring()`  | Main real-time monitoring loop                      |
| `set_thresholds()`    | Interactive threshold configuration                 |
| `main()`              | Menu loop tying everything together                |

---

## 🌟 Bonus Features Implemented

- ✅ **Desktop notifications** via `plyer` (optional dependency, graceful
  fallback if not installed)
- ✅ **Sound alert** via terminal bell (`\a`), no extra dependency needed,
  cross-platform

### Not implemented (left as an exercise / future work)
- Email alert system (would require SMTP credentials — see note below)
- Auto-start on system boot (OS-specific: systemd unit on Linux, Task
  Scheduler on Windows, LaunchAgent on macOS)

> 💡 **Extending to email alerts:** add a `send_email_alert(alerts)` function
> using Python's built-in `smtplib` + `email.message.EmailMessage`, and call
> it from inside `trigger_alert()`. Store credentials in environment
> variables — never hard-code them.

> 💡 **Auto-start on boot (Linux example):** create a systemd service file
> pointing at `resource_monitor.py` and enable it with
> `systemctl enable resource_monitor.service`.

---

## ⚠️ Notes

- Disk usage is measured for the root path (`/` on Linux/macOS, `C:\` on
  Windows).
- CPU usage is sampled with a short blocking interval (`psutil.cpu_percent(interval=0.5)`)
  to get an accurate reading rather than an instantaneous (often misleading) value.
- All file I/O and sensor reads are wrapped in error handling so a transient
  failure won't crash the whole application.

---

## 📄 License

Free to use and modify for learning and portfolio purposes.
