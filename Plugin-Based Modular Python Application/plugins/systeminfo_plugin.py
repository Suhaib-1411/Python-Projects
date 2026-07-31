import platform

from core.base_plugin import BasePlugin

class SystemInfoPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "System Info"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def author(self) -> str:
        return "SysAdmin"

    def execute(self) -> None:
        print(f"OS: {platform.system()} {platform.release()}")
        print(f"Python Version: {platform.python_version()}")
        print(f"Architecture: {platform.machine()}")