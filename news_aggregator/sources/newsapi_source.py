"""
sources/newsapi_source.py
--------------------------
Integration with NewsAPI.org (https://newsapi.org).

Endpoints used:
  - /v2/top-headlines   -> category browsing
  - /v2/everything       -> keyword search

Requires a free API key set as NEWSAPI_KEY (see .env.example).
"""

from typing import List
import requests

import config
from models import Article
from sources.base import NewsSource


class NewsAPISource(NewsSource):
    name = "NewsAPI"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.NEWSAPI_KEY

    def is_available(self) -> bool:
        return bool(self.api_key)

    def _get(self, endpoint: str, params: dict) -> dict:
        params = {**params, "apiKey": self.api_key}
        url = f"{config.NEWSAPI_BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=config.REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as exc:
            raise ConnectionError(f"Network error contacting NewsAPI: {exc}") from exc

        if response.status_code == 401:
            raise PermissionError("NewsAPI rejected the request: invalid or missing API key.")
        if response.status_code == 429:
            raise RuntimeError("NewsAPI rate limit exceeded. Please try again later.")
        if response.status_code != 200:
            raise RuntimeError(
                f"NewsAPI returned an error ({response.status_code}): {response.text[:200]}"
            )

        data = response.json()
        if data.get("status") != "ok":
            raise RuntimeError(f"NewsAPI error: {data.get('message', 'Unknown error')}")
        return data

    def _parse_articles(self, raw_articles: list, category: str) -> List[Article]:
        articles = []
        for item in raw_articles:
            source_name = (item.get("source") or {}).get("name", "NewsAPI")
            articles.append(
                Article(
                    title=item.get("title"),
                    source=source_name,
                    url=item.get("url", ""),
                    published_at=item.get("publishedAt"),
                    description=item.get("description") or item.get("content"),
                    category=category,
                    origin="newsapi",
                )
            )
        return articles

    def fetch_by_category(self, category: str) -> List[Article]:
        if not self.is_available():
            return []

        params = {
            "category": category if category != "general" else "general",
            "country": config.NEWSAPI_DEFAULT_COUNTRY,
            "pageSize": config.NEWSAPI_PAGE_SIZE,
        }
        try:
            data = self._get("top-headlines", params)
        except (ConnectionError, PermissionError, RuntimeError) as exc:
            print(f"[NewsAPI] {exc}")
            return []

        return self._parse_articles(data.get("articles", []), category)

    def search(self, keyword: str) -> List[Article]:
        if not self.is_available():
            return []

        params = {
            "q": keyword,
            "sortBy": "publishedAt",
            "pageSize": config.NEWSAPI_PAGE_SIZE,
            "language": "en",
        }
        try:
            data = self._get("everything", params)
        except (ConnectionError, PermissionError, RuntimeError) as exc:
            print(f"[NewsAPI] {exc}")
            return []

        return self._parse_articles(data.get("articles", []), category="search")
