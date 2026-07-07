"""
models.py
---------
Defines the core data structure used throughout the app: Article.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    """Represents a single normalized news article, regardless of source."""

    title: str
    source: str
    url: str
    published_at: Optional[str] = None
    description: str = ""
    category: str = "general"
    origin: str = "unknown"  # "newsapi" or "rss"

    def __post_init__(self):
        # Normalize missing fields so display code never has to guard against None.
        self.title = (self.title or "Untitled").strip()
        self.description = (self.description or "No description available.").strip()
        self.source = (self.source or "Unknown Source").strip()
        self.published_at = self._normalize_date(self.published_at)

    @staticmethod
    def _normalize_date(raw_date) -> str:
        """Best-effort normalization of various date formats into 'YYYY-MM-DD HH:MM'."""
        if not raw_date:
            return "Unknown date"

        # Already a datetime object (e.g. from feedparser's parsed struct converted upstream)
        if isinstance(raw_date, datetime):
            return raw_date.strftime("%Y-%m-%d %H:%M")

        raw_date = str(raw_date)

        # Try common formats: ISO 8601 (NewsAPI) and RFC 822 (RSS)
        formats = [
            "%Y-%m-%dT%H:%M:%SZ",       # NewsAPI: 2024-05-01T12:30:00Z
            "%a, %d %b %Y %H:%M:%S %Z", # RSS: Wed, 01 May 2024 12:30:00 GMT
            "%a, %d %b %Y %H:%M:%S %z",
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(raw_date, fmt)
                return dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                continue

        # Fall back to returning the raw string trimmed to something readable
        return raw_date[:16]

    def dedup_key(self) -> str:
        """Key used to detect duplicate articles across sources."""
        return self.title.lower().strip()

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "source": self.source,
            "published_at": self.published_at,
            "description": self.description,
            "category": self.category,
            "url": self.url,
            "origin": self.origin,
        }
