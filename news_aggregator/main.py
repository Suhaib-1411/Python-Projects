#!/usr/bin/env python3
"""
main.py
-------
Entry point for the Multi-Source News Aggregator CLI application.

Run with:
    python main.py
"""

from cli import NewsCLI


def main():
    app = NewsCLI()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")


if __name__ == "__main__":
    main()
