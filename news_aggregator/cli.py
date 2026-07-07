"""
cli.py
------
Menu-driven command-line interface tying together the aggregator,
storage, and display modules.
"""

from typing import List

import config
import display
import storage
from aggregator import NewsAggregator
from models import Article
from sources.newsapi_source import NewsAPISource
from sources.rss_source import RSSSource


class NewsCLI:
    def __init__(self):
        self.sources = [NewsAPISource(), RSSSource()]
        self.aggregator = NewsAggregator(self.sources)
        self.last_results: List[Article] = []

    def run(self) -> None:
        display.header("Welcome to the Multi-Source News Aggregator")
        active = self.aggregator.available_sources()
        if active:
            display.info(f"Active sources: {', '.join(active)}")
        else:
            display.error("No sources available. Check your internet connection or API key.")

        while True:
            display.print_menu()
            choice = input("Select an option (1-5): ").strip()

            if choice == "1":
                self.view_latest_news()
            elif choice == "2":
                self.select_category()
            elif choice == "3":
                self.search_news()
            elif choice == "4":
                self.save_results()
            elif choice == "5":
                display.success("Goodbye!")
                break
            else:
                display.error("Invalid option. Please choose a number from 1 to 5.")

    def view_latest_news(self) -> None:
        display.header("LATEST NEWS - GENERAL")
        display.info("Fetching latest headlines...")
        articles = self.aggregator.get_by_category("general")
        self.last_results = articles
        display.print_articles(articles)

    def select_category(self) -> None:
        display.print_categories(config.CATEGORIES)
        raw = input(f"Select a category (1-{len(config.CATEGORIES)}): ").strip()

        if not raw.isdigit() or not (1 <= int(raw) <= len(config.CATEGORIES)):
            display.error("Invalid category selection.")
            return

        category = config.CATEGORIES[int(raw) - 1]
        display.header(f"NEWS - {category.upper()}")
        display.info(f"Fetching {category} news...")
        articles = self.aggregator.get_by_category(category)
        self.last_results = articles
        display.print_articles(articles)

    def search_news(self) -> None:
        keyword = input("Enter a keyword to search for: ").strip()
        if not keyword:
            display.error("Search keyword cannot be empty.")
            return

        display.header(f"SEARCH RESULTS FOR '{keyword}'")
        display.info("Searching across all sources...")
        articles = self.aggregator.search(keyword)
        self.last_results = articles
        display.print_articles(articles)

    def save_results(self) -> None:
        if not self.last_results:
            display.error("No results to save yet. View or search news first.")
            return

        fmt = input("Save as (1) TXT or (2) CSV? ").strip()
        try:
            if fmt == "1":
                path = storage.save_as_txt(self.last_results)
            elif fmt == "2":
                path = storage.save_as_csv(self.last_results)
            else:
                display.error("Invalid format choice.")
                return
            display.success(f"Saved {len(self.last_results)} article(s) to: {path}")
        except OSError as exc:
            display.error(f"Could not save file: {exc}")
