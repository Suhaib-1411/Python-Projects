"""
config.py
---------
Central configuration for the News Aggregator app.
Loads settings from environment variables (via a .env file if present).
"""

import os
from dotenv import load_dotenv

# Load variables from a .env file in the project root, if it exists.
load_dotenv()

# ---- API Keys ----
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

# ---- NewsAPI Settings ----
NEWSAPI_BASE_URL = "https://newsapi.org/v2"
NEWSAPI_DEFAULT_COUNTRY = "us"
NEWSAPI_PAGE_SIZE = 20  # max articles to request per call

# ---- Supported Categories ----
CATEGORIES = ["technology", "sports", "business", "entertainment", "health", "science", "general"]

# ---- RSS Feed Sources (used regardless of NewsAPI key availability) ----
# Feeds are grouped by category so category filtering works even
# without a NewsAPI key.
RSS_FEEDS = {
    "technology": [
        ("The Verge", "https://www.theverge.com/rss/index.xml"),
        ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ],
    "sports": [
        ("BBC Sport", "http://feeds.bbci.co.uk/sport/rss.xml"),
        ("ESPN", "https://www.espn.com/espn/rss/news"),
    ],
    "business": [
        ("BBC Business", "http://feeds.bbci.co.uk/news/business/rss.xml"),
        ("CNBC", "https://www.cnbc.com/id/10001147/device/rss/rss.html"),
    ],
    "entertainment": [
        ("BBC Entertainment", "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml"),
        ("Variety", "https://variety.com/feed/"),
    ],
    "health": [
        ("BBC Health", "http://feeds.bbci.co.uk/news/health/rss.xml"),
    ],
    "science": [
        ("BBC Science", "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml"),
    ],
    "general": [
        ("BBC News", "http://feeds.bbci.co.uk/news/rss.xml"),
        ("Reuters World", "https://www.reutersagency.com/feed/?best-topics=top-news&post_type=best"),
    ],
}

# ---- Output Settings ----
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---- Network Settings ----
REQUEST_TIMEOUT = 10  # seconds
