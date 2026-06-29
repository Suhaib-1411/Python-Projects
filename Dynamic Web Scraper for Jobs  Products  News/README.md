# Task 9 - Dynamic Web Scraper

**Python Developer Internship Program**
Hasnain Karimain Educational Academy - Batch 7, Shift 2

---

## Overview

A professional CLI-based Python web scraper that extracts real-time data from GitHub.
Covers three categories: Trending Repos, Topic Explorer, and News/Updates.
Data can be searched, filtered, and exported to JSON or CSV.

---

## Website Used

  https://github.com

GitHub is used because it is publicly accessible, has no login wall, and provides
rich structured data across three distinct use-cases that map to the task requirements:

  Category 1 - Trending Repos   -> like a Jobs board (active, ranked listings)
  Category 2 - Topic Explorer   -> like a Products catalog (categorized items)
  Category 3 - News / Updates   -> like a News feed (daily/weekly/monthly ranking)

---

## Features

| Feature | Details |
|---|---|
| Trending Repos | Scrape github.com/trending with language filter + pagination |
| Topic Explorer | Scrape github.com/topics for any tech topic |
| News / Updates | Scrape trending repos by daily / weekly / monthly period |
| Search | Case-insensitive keyword search across title and description |
| Filter by Language | Filter results by programming language |
| Filter by Stars | Filter results by minimum star count |
| Save JSON | Export scraped data as .json |
| Save CSV | Export scraped data as .csv |
| Retry Logic | 3 automatic retries on failed requests |
| Pagination | Scrape up to 3 pages per session |

---

## Project Structure

```
task9/
|
|-- web_scraper.py             # Main application (run this)
|-- scraped_sample_data.json   # Sample scraped output (JSON)
|-- scraped_sample_data.csv    # Sample scraped output (CSV)
|-- README.md                  # This file
```

---

## Requirements

- Python 3.8+
- requests
- beautifulsoup4

### Install dependencies

```
pip install requests beautifulsoup4
```

---

## How to Run

Open Command Prompt (not VS Code terminal):

```
cd "path\to\task9"
python web_scraper.py
```

---

## Menu

```
==============================================================
  Dynamic Web Scraper  |  Task 9
==============================================================
  Status: No data scraped

  --- Select Category to Scrape ---
  1. Trending Repos   (github.com/trending)
  2. Topic Explorer   (github.com/topics)
  3. News / Updates   (trending by period)

  --- Actions ---
  4. View Current Data
  5. Search / Filter
  6. Save Data (JSON / CSV)
  0. Exit
```

---

## Step-by-Step Demo

1. Run the tool
2. Select **1** (Trending Repos) -> choose Python (option 2) -> 1 page -> wait
3. Select **4** (View Data) -> enter 5 to see first 5 results
4. Select **5** (Search/Filter) -> option 3 -> min stars: 5000
5. Select **6** (Save Data) -> option 3 (both JSON and CSV)
6. Go back and try **2** (Topic Explorer) -> choose machine-learning

---

## Data Fields

### Trending Repos / News
| Field | Description |
|---|---|
| title | Repository name (owner/repo) |
| language | Programming language |
| stars | Total star count |
| forks | Total fork count |
| stars_today | Stars gained in the period |
| description | Short repo description |
| link | Full GitHub URL |
| scraped_at | Timestamp of scrape |

### Topic Explorer
| Field | Description |
|---|---|
| title | Repository name |
| topic | Topic searched |
| language | Programming language |
| stars | Total star count |
| last_updated | Date of last commit |
| description | Short repo description |
| link | Full GitHub URL |
| scraped_at | Timestamp of scrape |

---

## Author

Muhammad Babar
Python Developer Intern - Batch 7
Hasnain Karimain Educational Academy
