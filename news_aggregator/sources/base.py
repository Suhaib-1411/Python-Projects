"""
sources/base.py
----------------
Abstract base class that all news sources must implement.
Keeping a common interface makes it trivial to add new sources
(e.g. a new API or a different feed protocol) without touching
the aggregation logic.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from models import Article


class NewsSource(ABC):
    """Common interface for any news provider (API, RSS, scraper, etc.)."""

    name: str = "BaseSource"

    @abstractmethod
    def fetch_by_category(self, category: str) -> List[Article]:
        """Return a list of Articles for a given category."""
        raise NotImplementedError

    @abstractmethod
    def search(self, keyword: str) -> List[Article]:
        """Return a list of Articles matching a keyword search."""
        raise NotImplementedError

    def is_available(self) -> bool:
        """Whether this source is usable (e.g. has a valid API key)."""
        return True
