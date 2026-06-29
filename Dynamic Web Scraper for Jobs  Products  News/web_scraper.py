"""
Dynamic Web Scraper - Jobs / Products / News
Task 9 - Python Developer Internship
Hasnain Karimain Educational Academy

Categories:
  1. Trending Repos  - github.com/trending  (acts as "Jobs/Projects")
  2. Topic Explorer  - github.com/topics     (acts as "Products/Listings")
  3. GitHub Releases - github.com/trending   (acts as "News/Updates")

All three use GitHub which is publicly accessible without login.
"""

import os
import sys
import json
import csv
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    os.system("chcp 65001 > nul")


# ─────────────────────────── Globals ────────────────────────────
scraped_data = []
current_category = None

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

LANGUAGES = ["", "python", "javascript", "typescript", "java", "c++", "go", "rust"]
TOPICS    = ["artificial-intelligence", "machine-learning", "web-scraping",
             "data-science", "automation", "cybersecurity", "django", "fastapi"]


# ═══════════════════════════════════════════════════════════════
#  UTILITY
# ═══════════════════════════════════════════════════════════════

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def separator(char="=", width=62):
    print(char * width)

def header(title):
    separator()
    print(f"  {title}")
    separator()

def pause():
    input("\n  Press Enter to continue...")

def fetch(url, retries=3, delay=2):
    """GET with retry logic and User-Agent spoofing."""
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code == 200:
                return r
            print(f"  [WARN] HTTP {r.status_code} on attempt {attempt}")
        except requests.exceptions.ConnectionError:
            print(f"  [ERR] Connection failed (attempt {attempt})")
        except requests.exceptions.Timeout:
            print(f"  [ERR] Request timed out (attempt {attempt})")
        except Exception as e:
            print(f"  [ERR] {e} (attempt {attempt})")
        if attempt < retries:
            time.sleep(delay)
    return None


# ═══════════════════════════════════════════════════════════════
#  CATEGORY 1 - TRENDING REPOS  (like "Jobs")
# ═══════════════════════════════════════════════════════════════

def scrape_trending():
    global scraped_data, current_category

    header("SCRAPE - Trending GitHub Repositories")
    print("  Choose language filter:\n")
    for i, lang in enumerate(LANGUAGES):
        label = lang if lang else "All Languages"
        print(f"  {i}. {label}")

    choice = input("\n  Choice [0]: ").strip()
    try:
        lang = LANGUAGES[int(choice)]
    except (ValueError, IndexError):
        lang = ""

    pages = input("  Pages to scrape [1-3, default 1]: ").strip()
    try:
        pages = max(1, min(3, int(pages)))
    except ValueError:
        pages = 1

    lang_label = lang if lang else "all"
    print(f"\n  Scraping GitHub Trending ({lang_label}, {pages} page(s))...")

    results = []
    url = f"https://github.com/trending/{lang}" if lang else "https://github.com/trending"

    for page in range(1, pages + 1):
        page_url = url + (f"?since=daily&page={page}" if page > 1 else "?since=daily")
        print(f"  Fetching page {page}: {page_url}")
        r = fetch(page_url)
        if not r:
            print(f"  [ERR] Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        repos = soup.select("article.Box-row")

        for repo in repos:
            try:
                title_tag = repo.select_one("h2 a")
                title     = title_tag.get_text(strip=True).replace(" ", "").replace("\n", "") if title_tag else "N/A"
                link      = "https://github.com" + title_tag["href"] if title_tag else "N/A"
                desc_tag  = repo.select_one("p")
                desc      = desc_tag.get_text(strip=True) if desc_tag else "No description"
                lang_tag  = repo.select_one("[itemprop=programmingLanguage]")
                language  = lang_tag.get_text(strip=True) if lang_tag else "N/A"
                stars_tag = repo.select_one("a[href*=stargazers]")
                stars     = stars_tag.get_text(strip=True) if stars_tag else "0"
                forks_tag = repo.select_one("a[href*=forks]")
                forks     = forks_tag.get_text(strip=True) if forks_tag else "0"
                today_tag = repo.select_one(".float-sm-right")
                today     = today_tag.get_text(strip=True) if today_tag else "N/A"

                results.append({
                    "category":  "Trending",
                    "title":     title,
                    "language":  language,
                    "stars":     stars,
                    "forks":     forks,
                    "stars_today": today,
                    "description": desc,
                    "link":      link,
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
            except Exception as e:
                print(f"  [WARN] Parse error: {e}")

        time.sleep(1)

    scraped_data = results
    current_category = "Trending"
    print(f"\n  [OK] Scraped {len(results)} trending repos.")
    pause()


# ═══════════════════════════════════════════════════════════════
#  CATEGORY 2 - TOPIC EXPLORER  (like "Products/Listings")
# ═══════════════════════════════════════════════════════════════

def scrape_topics():
    global scraped_data, current_category

    header("SCRAPE - GitHub Topic Explorer")
    print("  Choose a topic:\n")
    for i, t in enumerate(TOPICS):
        print(f"  {i}. {t}")
    print(f"  {len(TOPICS)}. Custom topic")

    choice = input("\n  Choice [0]: ").strip()
    try:
        idx = int(choice)
        if idx == len(TOPICS):
            topic = input("  Enter topic name: ").strip().lower().replace(" ", "-")
        else:
            topic = TOPICS[idx]
    except (ValueError, IndexError):
        topic = TOPICS[0]

    pages = input("  Pages to scrape [1-3, default 1]: ").strip()
    try:
        pages = max(1, min(3, int(pages)))
    except ValueError:
        pages = 1

    print(f"\n  Scraping GitHub Topic: {topic} ({pages} page(s))...")

    results = []
    for page in range(1, pages + 1):
        url = f"https://github.com/topics/{topic}?page={page}"
        print(f"  Fetching page {page}: {url}")
        r = fetch(url)
        if not r:
            print(f"  [ERR] Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        articles = soup.select("article.border")

        for article in articles:
            try:
                title_tag = article.select_one("h3 a:last-child")
                title     = title_tag.get_text(strip=True) if title_tag else "N/A"
                href      = title_tag["href"] if title_tag else ""
                link      = "https://github.com" + href if href else "N/A"
                desc_tag  = article.select_one("p.color-fg-muted")
                desc      = desc_tag.get_text(strip=True) if desc_tag else "No description"
                lang_tag  = article.select_one("[itemprop=programmingLanguage]")
                language  = lang_tag.get_text(strip=True) if lang_tag else "N/A"
                stars_tag = article.select_one("#repo-stars-counter-star")
                stars     = stars_tag["title"] if stars_tag and stars_tag.has_attr("title") else (stars_tag.get_text(strip=True) if stars_tag else "0")
                updated_tag = article.select_one("relative-time")
                updated   = updated_tag["datetime"][:10] if updated_tag and updated_tag.has_attr("datetime") else "N/A"

                results.append({
                    "category":    "Topic",
                    "topic":       topic,
                    "title":       title,
                    "language":    language,
                    "stars":       stars,
                    "description": desc,
                    "last_updated": updated,
                    "link":        link,
                    "scraped_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
            except Exception as e:
                print(f"  [WARN] Parse error: {e}")

        time.sleep(1)

    scraped_data = results
    current_category = f"Topic:{topic}"
    print(f"\n  [OK] Scraped {len(results)} repos from topic '{topic}'.")
    pause()


# ═══════════════════════════════════════════════════════════════
#  CATEGORY 3 - GITHUB NEWS  (Recently released / starred repos)
# ═══════════════════════════════════════════════════════════════

def scrape_news():
    global scraped_data, current_category

    header("SCRAPE - GitHub Trending News (Weekly / Monthly)")
    print("  Time range:\n")
    print("  1. Daily   (hottest today)")
    print("  2. Weekly  (this week's top)")
    print("  3. Monthly (this month's top)")

    choice = input("\n  Choice [1]: ").strip()
    period_map = {"1": "daily", "2": "weekly", "3": "monthly"}
    period = period_map.get(choice, "daily")

    lang_choice = input("  Language filter (e.g. python, or leave blank for all): ").strip().lower()
    lang_path = f"/{lang_choice}" if lang_choice else ""

    url = f"https://github.com/trending{lang_path}?since={period}"
    print(f"\n  Scraping: {url}")

    r = fetch(url)
    if not r:
        print("  [ERR] Failed to fetch data.")
        pause()
        return

    soup = BeautifulSoup(r.text, "html.parser")
    repos = soup.select("article.Box-row")
    results = []

    for rank, repo in enumerate(repos, start=1):
        try:
            title_tag = repo.select_one("h2 a")
            title     = title_tag.get_text(strip=True).replace(" ", "").replace("\n", "") if title_tag else "N/A"
            link      = "https://github.com" + title_tag["href"] if title_tag else "N/A"
            desc_tag  = repo.select_one("p")
            desc      = desc_tag.get_text(strip=True) if desc_tag else "No description"
            lang_tag  = repo.select_one("[itemprop=programmingLanguage]")
            language  = lang_tag.get_text(strip=True) if lang_tag else "N/A"
            stars_tag = repo.select_one("a[href*=stargazers]")
            stars     = stars_tag.get_text(strip=True) if stars_tag else "0"
            today_tag = repo.select_one(".float-sm-right")
            gained    = today_tag.get_text(strip=True) if today_tag else "N/A"

            results.append({
                "category":    "News",
                "rank":        rank,
                "period":      period,
                "title":       title,
                "language":    language,
                "stars":       stars,
                "stars_gained": gained,
                "description": desc,
                "link":        link,
                "scraped_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
        except Exception as e:
            print(f"  [WARN] Parse error: {e}")

    scraped_data = results
    current_category = f"News:{period}"
    print(f"\n  [OK] Scraped {len(results)} trending repos ({period}).")
    pause()


# ═══════════════════════════════════════════════════════════════
#  SEARCH / FILTER
# ═══════════════════════════════════════════════════════════════

def search_filter():
    if not scraped_data:
        print("\n  [WARN] No data scraped yet. Please scrape first.")
        pause()
        return

    header("SEARCH / FILTER")
    print("  1. Search by keyword (title or description)")
    print("  2. Filter by language")
    print("  3. Filter by minimum stars")
    print("  0. Back")

    choice = input("\n  Choice: ").strip()

    if choice == "1":
        kw = input("  Keyword: ").strip().lower()
        results = [
            d for d in scraped_data
            if kw in d.get("title", "").lower() or kw in d.get("description", "").lower()
        ]
        _display_results(results, f"Keyword: '{kw}'")

    elif choice == "2":
        lang = input("  Language (e.g. Python): ").strip().lower()
        results = [d for d in scraped_data if d.get("language", "").lower() == lang]
        _display_results(results, f"Language: {lang}")

    elif choice == "3":
        try:
            min_stars = int(input("  Minimum stars (numeric only, e.g. 1000): ").strip().replace(",", ""))
            results = []
            for d in scraped_data:
                try:
                    s = int(d.get("stars", "0").replace(",", "").split()[0])
                    if s >= min_stars:
                        results.append(d)
                except Exception:
                    pass
            _display_results(results, f"Stars >= {min_stars}")
        except ValueError:
            print("  [ERR] Invalid number.")
            pause()

    elif choice == "0":
        return
    else:
        print("  [ERR] Invalid choice.")
        pause()


def _display_results(results, label):
    separator("-")
    print(f"  Results for [{label}]  ->  {len(results)} item(s)\n")
    if not results:
        print("  No matching records.")
    else:
        for i, d in enumerate(results, 1):
            print(f"  {i}. {d.get('title', 'N/A')}")
            print(f"     Language : {d.get('language', 'N/A')}")
            print(f"     Stars    : {d.get('stars', 'N/A')}")
            print(f"     Desc     : {d.get('description', 'N/A')[:80]}")
            print(f"     Link     : {d.get('link', 'N/A')}")
            print()
    pause()


# ═══════════════════════════════════════════════════════════════
#  SAVE DATA
# ═══════════════════════════════════════════════════════════════

def save_data():
    if not scraped_data:
        print("\n  [WARN] No data to save. Please scrape first.")
        pause()
        return

    header("SAVE DATA")
    print("  1. Save as JSON")
    print("  2. Save as CSV")
    print("  3. Save both")
    print("  0. Back")

    choice = input("\n  Choice: ").strip()
    if choice == "0":
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    cat = (current_category or "data").replace(":", "_").replace("/", "_")
    base = f"scraped_{cat}_{ts}"

    if choice in ("1", "3"):
        fname = base + ".json"
        try:
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(scraped_data, f, indent=2, ensure_ascii=False)
            print(f"\n  [OK] Saved JSON: {fname}")
        except Exception as e:
            print(f"  [ERR] {e}")

    if choice in ("2", "3"):
        fname = base + ".csv"
        try:
            keys = list(scraped_data[0].keys())
            with open(fname, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(scraped_data)
            print(f"  [OK] Saved CSV : {fname}")
        except Exception as e:
            print(f"  [ERR] {e}")

    pause()


# ═══════════════════════════════════════════════════════════════
#  VIEW CURRENT DATA
# ═══════════════════════════════════════════════════════════════

def view_data():
    if not scraped_data:
        print("\n  [WARN] No data scraped yet.")
        pause()
        return

    header(f"CURRENT DATA  [{current_category}]  -  {len(scraped_data)} records")

    limit = input("  How many records to display? [10]: ").strip()
    try:
        limit = int(limit)
    except ValueError:
        limit = 10

    for i, d in enumerate(scraped_data[:limit], 1):
        separator("-")
        print(f"  [{i}] {d.get('title', 'N/A')}")
        for k, v in d.items():
            if k not in ("title", "category"):
                val = str(v)
                if len(val) > 90:
                    val = val[:87] + "..."
                print(f"       {k:<15}: {val}")
    separator("-")
    print(f"  Showing {min(limit, len(scraped_data))} of {len(scraped_data)} records.")
    pause()


# ═══════════════════════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════════════════════

def main():
    while True:
        clear()
        header("Dynamic Web Scraper  |  Task 9")
        count = f"{len(scraped_data)} records [{current_category}]" if scraped_data else "No data scraped"
        print(f"  Status: {count}\n")
        print("  --- Select Category to Scrape ---")
        print("  1. Trending Repos   (github.com/trending)")
        print("  2. Topic Explorer   (github.com/topics)")
        print("  3. News / Updates   (trending by period)")
        print("")
        print("  --- Actions ---")
        print("  4. View Current Data")
        print("  5. Search / Filter")
        print("  6. Save Data (JSON / CSV)")
        print("  0. Exit")
        separator()

        choice = input("  Select option: ").strip()

        if choice == "1":
            scrape_trending()
        elif choice == "2":
            scrape_topics()
        elif choice == "3":
            scrape_news()
        elif choice == "4":
            view_data()
        elif choice == "5":
            search_filter()
        elif choice == "6":
            save_data()
        elif choice == "0":
            print("\n  Goodbye!\n")
            sys.exit(0)
        else:
            print("  [ERR] Invalid option.")
            input("  Press Enter...")


if __name__ == "__main__":
    main()
