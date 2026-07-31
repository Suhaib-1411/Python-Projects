# Plugin-Driven Modular Python Application

## Project Overview

This project is a CLI-based modular Python application built on a dynamic plugin architecture. Features and functionality can be added, updated, or disabled at runtime without modifying the core system codebase.

The architecture strictly separates the core framework (responsible for plugin discovery, lifecycle management, error handling, and logging) from individual plugins (which contain domain-specific logic).

---

## Folder Structure

```text
modular_app/
│
├── core/
│   ├── __init__.py
│   ├── base_plugin.py      # Abstract Base Class defining the plugin contract
│   ├── plugin_manager.py   # Dynamic loader and runtime lifecycle manager
│   └── logger.py           # Centralized logging configuration
│
├── plugins/
│   ├── calculator_plugin.py    # Example: Basic arithmetic evaluation
│   ├── systeminfo_plugin.py    # Example: System hardware and OS info
│   └── textutility_plugin.py   # Example: Text transformations
│
├── logs/                       # Automatically created runtime log directory
├── main.py                     # Primary Application Entry Point
└── README.md                   # System Documentation and Plugin Guide
```

---

## Key Features

- **Dynamic Plugin Discovery**: Automatically scans the `plugins/` directory and loads valid modules at startup or during runtime.
- **Strict Interface Contract**: Utilizes Python's `abc` module to enforce uniform structures across all plugins.
- **Runtime Hot-Reloading**: Reloads plugins from disk without requiring an application restart.
- **Plugin Management**: Enables users to view, run, enable, or disable specific plugins interactively.
- **Fault Tolerance**: Isolated execution blocks ensure that faulty or crashing plugins do not crash the core application.
- **Structured Logging**: Tracks plugin loading, execution events, and error traces in `logs/app.log`.

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher installed on your system.

### Running the Application

1. Open a terminal or command prompt.
2. Navigate to the project directory:

```bash
cd Task_23/modular_app
```

3. Launch the application:

```bash
python main.py
```

---

## Interactive Menu Options

When launched, the application presents the following menu:

1. **View Available Plugins**: Displays all loaded plugins, their version, author, and current status (ACTIVE / DISABLED).
2. **Run Plugin**: Prompt for a plugin name and execute its primary function.
3. **Enable/Disable Plugin**: Toggles a plugin's execution state.
4. **Reload Plugins**: Re-scans the `plugins/` folder to load new plugins or reflect changes without restarting.
5. **Exit**: Gracefully terminates the application.

---

## Plugin Development Guide

You can easily extend this system by creating new plugins inside the `plugins/` directory.

### Step-by-Step Implementation

1. Create a new Python file inside `plugins/` (e.g., `plugins/my_custom_plugin.py`).
2. Import `BasePlugin` from `core.base_plugin`.
3. Create a class that inherits from `BasePlugin`.
4. Implement the required properties (`name`, `version`, `author`) and the `execute()` method.

### Sample Code Structure

```python
from core.base_plugin import BasePlugin

class MyCustomPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "Custom Tool"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def author(self) -> str:
        return "Developer Name"

    def execute(self) -> None:
        print("Custom plugin is executing successfully.")
```

### Loading Your Plugin

Once your file is saved in `plugins/`:
- If the application is running, select **Option 4 (Reload Plugins)** in the menu.
- If starting fresh, run `python main.py`, and the manager will auto-discover your new plugin.

---

## Error Handling and Logging

- All activity, including plugin discovery, success logs, and runtime exceptions, is written to `logs/app.log`.
- If a plugin contains a syntax error or fails during execution, the exception is caught, logged, and presented clearly to the user without interrupting main application flow.