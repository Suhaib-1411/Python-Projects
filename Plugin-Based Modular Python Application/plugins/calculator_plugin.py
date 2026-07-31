from core.base_plugin import BasePlugin

class CalculatorPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "Calculator"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def author(self) -> str:
        return "Dev Team"

    def execute(self) -> None:
        try:
            expr = input("Enter a simple math expression (e.g., 12 * 4): ")
            # Safe evaluation for demo purposes
            result = eval(expr, {"__builtins__": None}, {})
            print(f"Result: {result}")
        except Exception as e:
            print(f"Invalid math expression: {e}")