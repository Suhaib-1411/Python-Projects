import importlib.util
import os
import sys
from typing import Dict
from core.base_plugin import BasePlugin
from core.logger import logger

class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, BasePlugin] = {}
        self.disabled_plugins: set = set()

    def discover_and_load(self):
        """Scans the plugin directory and dynamically imports valid BasePlugin subclasses."""
        self.plugins.clear()
        
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)

        sys.path.insert(0, self.plugin_dir)

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                file_path = os.path.join(self.plugin_dir, filename)

                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        # Look for classes inheriting from BasePlugin
                        for attribute_name in dir(module):
                            attribute = getattr(module, attribute_name)
                            if (
                                isinstance(attribute, type)
                                and issubclass(attribute, BasePlugin)
                                and attribute is not BasePlugin
                            ):
                                plugin_instance = attribute()
                                self.plugins[plugin_instance.name] = plugin_instance
                                logger.info(f"Successfully loaded plugin: {plugin_instance.name} v{plugin_instance.version}")
                except Exception as e:
                    logger.error(f"Failed to load plugin from {filename}: {e}")
                    print(f" Warning: Faulty plugin detected in '{filename}' - skipped.")

    def enable_plugin(self, name: str):
        if name in self.disabled_plugins:
            self.disabled_plugins.remove(name)
            logger.info(f"Enabled plugin: {name}")

    def disable_plugin(self, name: str):
        if name in self.plugins:
            self.disabled_plugins.add(name)
            logger.info(f"Disabled plugin: {name}")

    def run_plugin(self, name: str):
        if name not in self.plugins:
            print(f" Plugin '{name}' not found.")
            return

        if name in self.disabled_plugins:
            print(f" Plugin '{name}' is currently disabled.")
            return

        try:
            logger.info(f"Executing plugin: {name}")
            print(f"\n--- Running: {name} ---")
            self.plugins[name].execute()
            print("--- Execution Completed ---\n")
        except Exception as e:
            logger.error(f"Error during runtime execution of '{name}': {e}")
            print(f" Error: Plugin '{name}' crashed unexpectedly during execution.")