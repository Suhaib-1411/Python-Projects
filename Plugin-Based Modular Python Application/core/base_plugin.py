from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """Abstract base class that all plugins must inherit from."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the plugin."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the plugin."""
        pass

    @property
    @abstractmethod
    def author(self) -> str:
        """Author of the plugin."""
        pass

    @abstractmethod
    def execute(self) -> None:
        """Main execution entry point for the plugin logic."""
        pass