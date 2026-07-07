"""
sources/rss_source.py
----------------------
Integration with RSS feeds via the `feedparser` library.

This source works with no API key at all, so the app remains
functional even if the user hasn't set up a NewsAPI key.
"""

from typing import List
import feedparser

import config
from models import Article
from sources.base import NewsSource


class RSSSource(NewsSource):
    name = "RSS Feeds"

    def __init__(self, feeds: dict = None):
        # feeds: {category: [(source_name, url), ...]}
        self.feeds = feeds or config.RSS_FEEDS

    def is_available(self) -> bool:
        return bool(self.feeds)

    def _parse_feed(self, source_name: str, url: str, category: str) -> List[Article]:
        articles = []
        try:
            parsed = feedparser.parse(url)
        except Exception as exc:  # feedparser rarely raises, but be defensive
            print(f"[RSS] Failed to fetch {source_name}: {exc}")
            return articles

        if parsed.bozo and not parsed.entries:
            print(f"[RSS] Could not parse feed from {source_name} ({url}).")
            return articles

        for entry in parsed.entries[: config.NEWSAPI_PAGE_SIZE]:
            articles.append(
                Article(
                    title=entry.get("title"),
                    source=source_name,
                    url=entry.get("link", ""),
                    published_at=entry.get("published", entry.get("updated")),
                    description=entry.get("summary", entry.get("description")),
                    category=category,
                    origin="rss",
                )
            )
        return articles

    def fetch_by_category(self, category: str) -> List[Article]:
        feeds_for_category = self.feeds.get(category, [])
        if not feeds_for_category:
            return []

        articles = []
        for source_name, url in feeds_for_category:
            articles.extend(self._parse_feed(source_name, url, category))
        return articles

    def search(self, keyword: str) -> List[Article]:
        """RSS feeds don't support server-side search, so we fetch across
        all categories and filter client-side by keyword."""
        keyword_lower = keyword.lower()
        matches = []

        for category, feed_list in self.feeds.items():
            for source_name, url in feed_list:
                for article in self._parse_feed(source_name, url, category):
                    haystack = f"{article.title} {article.description}".lower()
                    if keyword_lower in haystack:
                        matches.append(article)
        return matches
