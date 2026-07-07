"""
storage.py
----------
Handles persisting fetched articles to disk (bonus feature: TXT/CSV export).
"""

import csv
import os
from datetime import datetime
from typing import List

import config
from models import Article


def _timestamped_filename(prefix: str, extension: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(config.OUTPUT_DIR, f"{prefix}_{stamp}.{extension}")


def save_as_txt(articles: List[Article], prefix: str = "news") -> str:
    filepath = _timestamped_filename(prefix, "txt")
    with open(filepath, "w", encoding="utf-8") as f:
        for i, article in enumerate(articles, start=1):
            f.write(f"{i}. {article.title}\n")
            f.write(f"   Source: {article.source}\n")
            f.write(f"   Published: {article.published_at}\n")
            f.write(f"   Category: {article.category}\n")
            f.write(f"   {article.description}\n")
            f.write(f"   URL: {article.url}\n")
            f.write("-" * 70 + "\n")
    return filepath


def save_as_csv(articles: List[Article], prefix: str = "news") -> str:
    filepath = _timestamped_filename(prefix, "csv")
    fieldnames = ["title", "source", "published_at", "category", "description", "url", "origin"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles:
            writer.writerow(article.to_dict())
    return filepath
