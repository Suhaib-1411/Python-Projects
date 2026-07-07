# 📰 Multi-Source News Aggregator

A modular, CLI-based Python application that aggregates news from multiple
sources — **NewsAPI** and **RSS feeds** — into one unified, deduplicated
reading experience.

---

## ✨ Features

- **Multi-source fetching** — pulls from NewsAPI and several RSS feeds
  *simultaneously* (threaded), and merges the results.
- **Category filtering** — Technology, Sports, Business, Entertainment,
  Health, Science, General.
- **Keyword search** — searches NewsAPI's `/everything` endpoint and
  filters RSS feeds client-side.
- **Duplicate removal** — articles with the same headline (from different
  outlets) are merged into a single entry.
- **Clean CLI output** — colorized headlines, source, date, and description.
- **Export results** — save your last set of results to `.txt` or `.csv`.
- **Graceful degradation** — if you don't have a NewsAPI key, the app still
  works fully using RSS feeds only.
- **Robust error handling** — handles missing API keys, rate limits,
  network failures, and empty results without crashing.

---

## 📁 Project Structure

```
news_aggregator/
├── main.py                 # Entry point
├── cli.py                  # Menu system / user interaction loop
├── aggregator.py            # Combines + deduplicates results from all sources
├── models.py                # Article data model
├── display.py                # Terminal output formatting
├── storage.py                # Save results to TXT/CSV
├── config.py                  # Settings, API keys, RSS feed list
├── sources/
│   ├── base.py                # Abstract NewsSource interface
│   ├── newsapi_source.py       # NewsAPI.org integration
│   └── rss_source.py            # RSS feed integration (feedparser)
├── data/                        # Saved TXT/CSV exports land here
├── requirements.txt
├── .env.example
└── README.md
```

The code is intentionally modular: every source implements the same
`NewsSource` interface (`fetch_by_category`, `search`), so adding a new
provider (e.g. a different news API) only requires creating one new file
in `sources/` and registering it in `cli.py`.

---

## 🚀 Setup

### 1. Clone / copy the project and install dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional but recommended) Get a free NewsAPI key

1. Register at [https://newsapi.org/register](https://newsapi.org/register)
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Paste your key into `.env`:
   ```
   NEWSAPI_KEY=your_actual_key_here
   ```

> **No API key?** No problem — the app will automatically fall back to
> RSS-only mode and tell you which sources are active on startup.

### 3. Run the app

```bash
python main.py
```

---

## 🖥 Usage

On launch you'll see:

```
1. View Latest News (all categories)
2. Select Category
3. Search News
4. Save Last Results (TXT/CSV)
5. Exit
```

- **View Latest News** — fetches top general headlines from every active source.
- **Select Category** — pick from Technology, Sports, Business, Entertainment, Health, Science, General.
- **Search News** — enter any keyword; searches NewsAPI's full article index plus RSS feeds.
- **Save Last Results** — export whatever you last viewed/searched to a timestamped `.txt` or `.csv` file inside `data/`.

Each article displayed shows:
- Headline
- Source name
- Publication date
- Short description
- Article URL

---

## 🔌 API / Source Details

### NewsAPI (`sources/newsapi_source.py`)
- Uses `GET /v2/top-headlines` for category browsing (country defaults to `us`, configurable in `config.py`).
- Uses `GET /v2/everything` for keyword search, sorted by publish date.
- Handles: missing/invalid key (401), rate limiting (429), and other HTTP errors — logs a friendly message and returns an empty list rather than crashing.
- Free tier limits: 100 requests/day, developer-tier only (no production `everything` search on very old free-tier keys) — see NewsAPI's own docs for current limits.

### RSS Feeds (`sources/rss_source.py`)
- Uses `feedparser` to pull from a curated list of public RSS feeds per category (BBC, The Verge, Ars Technica, ESPN, CNBC, Variety, Reuters).
- Since RSS has no server-side search, keyword search fetches all configured feeds and filters titles/descriptions client-side.
- You can add or change feeds by editing the `RSS_FEEDS` dictionary in `config.py` — just add a `(SourceName, feed_url)` tuple under the relevant category.

---

## 🛡 Error Handling Highlights

- **No API key** → app runs in RSS-only mode with a startup notice.
- **Network failure** → per-source errors are caught and logged; other sources still return results.
- **API rate limit hit** → clear message shown, app keeps running.
- **No results found** → "No articles found." message instead of a crash.
- **Invalid menu input** → re-prompts instead of exiting.
- **Duplicate articles** (same headline across sources) → automatically merged.

---

## 🧩 Extending the App

To add a new source:
1. Create `sources/my_source.py` implementing `NewsSource` (`fetch_by_category`, `search`, optionally `is_available`).
2. Import and add an instance of it to the `self.sources` list in `cli.py`.

That's it — the aggregator, deduplication, and display logic all work automatically with any number of sources.

---

## 📦 Deliverables Checklist

- ✅ Modular source code (`main.py`, `cli.py`, `aggregator.py`, `models.py`, `display.py`, `storage.py`, `config.py`, `sources/`)
- ✅ API integration code (NewsAPI + RSS)
- ✅ README.md (this file)
- ✅ Bonus: Save to TXT/CSV
