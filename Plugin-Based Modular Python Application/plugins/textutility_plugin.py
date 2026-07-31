from core.base_plugin import BasePlugin

class TextUtilityPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "Text Utility"

    @property
    def version(self) -> str:
        return "1.1.0"

    @property
    def author(self) -> str:
        return "Utility Dev"

    def execute(self) -> None:
        text = input("Enter text to transform: ")
        print(f"Uppercase: {text.upper()}")
        print(f"Word Count: {len(text.split())}")
        print(f"Reversed: {text[::-1]}")