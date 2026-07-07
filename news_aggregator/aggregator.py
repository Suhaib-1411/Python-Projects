"""
aggregator.py
-------------
Orchestrates fetching from all registered news sources, merges the
results, and removes duplicate articles (same headline from
different outlets/sources).
"""

from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from models import Article
from sources.base import NewsSource


class NewsAggregator:
    def __init__(self, sources: List[NewsSource]):
        self.sources = sources

    def _run_concurrently(self, method_name: str, arg: str) -> List[Article]:
        """Call `method_name(arg)` on every source in parallel and merge results.

        Running sources concurrently means a slow/unresponsive API doesn't
        block the others -- important since we may be hitting several
        network endpoints per user action.
        """
        results: List[Article] = []
        with ThreadPoolExecutor(max_workers=max(len(self.sources), 1)) as executor:
            future_to_source = {
                executor.submit(getattr(source, method_name), arg): source
                for source in self.sources
                if source.is_available()
            }
            for future in as_completed(future_to_source):
                source = future_to_source[future]
                try:
                    results.extend(future.result())
                except Exception as exc:
                    print(f"[{source.name}] Unexpected error: {exc}")
        return results

    def get_by_category(self, category: str) -> List[Article]:
        articles = self._run_concurrently("fetch_by_category", category)
        return self._deduplicate(articles)

    def search(self, keyword: str) -> List[Article]:
        articles = self._run_concurrently("search", keyword)
        return self._deduplicate(articles)

    @staticmethod
    def _deduplicate(articles: List[Article]) -> List[Article]:
        """Remove articles with the same (normalized) headline, keeping the first seen."""
        seen = set()
        unique = []
        for article in articles:
            key = article.dedup_key()
            if key not in seen:
                seen.add(key)
                unique.append(article)
        # Sort newest-looking dates first where possible; unknown dates sink to the bottom.
        unique.sort(key=lambda a: a.published_at, reverse=True)
        return unique

    def available_sources(self) -> List[str]:
        return [s.name for s in self.sources if s.is_available()]
