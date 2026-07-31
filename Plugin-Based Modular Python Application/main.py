import sys
from core.plugin_manager import PluginManager

def main():
    manager = PluginManager()
    manager.discover_and_load()

    while True:
        print("\n==================================")
        print("   🔌 PLUG-IN MASTER SYSTEM CLI   ")
        print("==================================")
        print("1. View Available Plugins")
        print("2. Run Plugin")
        print("3. Enable/Disable Plugin")
        print("4. Reload Plugins (Hot-Reload)")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()

        if choice == "1":
            print("\nInstalled Plugins:")
            if not manager.plugins:
                print(" No plugins loaded.")
            for name, plugin in manager.plugins.items():
                status = "[DISABLED]" if name in manager.disabled_plugins else "[ACTIVE]"
                print(f" • {name} (v{plugin.version}) by {plugin.author} {status}")

        elif choice == "2":
            plugin_name = input("Enter plugin name to run: ").strip()
            manager.run_plugin(plugin_name)

        elif choice == "3":
            plugin_name = input("Enter plugin name to toggle: ").strip()
            if plugin_name in manager.disabled_plugins:
                manager.enable_plugin(plugin_name)
                print(f"Enabled {plugin_name}.")
            elif plugin_name in manager.plugins:
                manager.disable_plugin(plugin_name)
                print(f"Disabled {plugin_name}.")
            else:
                print(f"Plugin '{plugin_name}' not found.")

        elif choice == "4":
            print("\nReloading plugin directory...")
            manager.discover_and_load()
            print("Plugins reloaded successfully.")

        elif choice == "5":
            print("\nShutting down plugin system. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()