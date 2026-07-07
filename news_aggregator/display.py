"""
display.py
----------
Terminal formatting helpers, kept separate from business logic
so the "look" of the app can change without touching the CLI flow.
"""

from typing import List
from colorama import Fore, Style, init as colorama_init
from models import Article

colorama_init(autoreset=True)

WIDTH = 78


def header(text: str) -> None:
    print("\n" + Fore.CYAN + "=" * WIDTH)
    print(Fore.CYAN + Style.BRIGHT + text.center(WIDTH))
    print(Fore.CYAN + "=" * WIDTH)


def divider() -> None:
    print(Fore.LIGHTBLACK_EX + "-" * WIDTH)


def print_article(article: Article, index: int) -> None:
    print(f"{Fore.YELLOW}{Style.BRIGHT}{index}. {article.title}")
    print(f"   {Fore.GREEN}Source: {article.source}   "
          f"{Fore.MAGENTA}Published: {article.published_at}")
    desc = article.description
    if len(desc) > 220:
        desc = desc[:217] + "..."
    print(f"   {desc}")
    print(f"   {Fore.BLUE}{article.url}")
    divider()


def print_articles(articles: List[Article]) -> None:
    if not articles:
        print(Fore.RED + "No articles found.")
        return
    for i, article in enumerate(articles, start=1):
        print_article(article, i)
    print(Fore.CYAN + f"Total: {len(articles)} article(s)")


def print_menu() -> None:
    header("MULTI-SOURCE NEWS AGGREGATOR")
    print("""
  1. View Latest News (all categories)
  2. Select Category
  3. Search News
  4. Save Last Results (TXT/CSV)
  5. Exit
""")


def print_categories(categories: List[str]) -> None:
    header("SELECT A CATEGORY")
    for i, cat in enumerate(categories, start=1):
        print(f"  {i}. {cat.title()}")


def error(message: str) -> None:
    print(Fore.RED + Style.BRIGHT + f"Error: {message}")


def info(message: str) -> None:
    print(Fore.CYAN + message)


def success(message: str) -> None:
    print(Fore.GREEN + message)
