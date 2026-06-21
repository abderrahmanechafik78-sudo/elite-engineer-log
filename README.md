# Elite Engineer Log — Price/Stock Monitor (v1: Quotes Demo)

## Problem

Manually checking a website for changes (prices, stock, listings, or in this
first version, content) is slow, easy to forget, and doesn't scale past one
or two sources. This project automates that check: scrape a target page on a
schedule, store every result, and query the history later instead of relying
on memory or manual spot-checks.

This first version targets `quotes.toscrape.com`, a site built for scraping
practice, to prove out the full pipeline — scraping, storage, scheduling,
and querying — before pointing it at a real price/stock source.

## Approach

1. **Scrape** — `requests` fetches the page HTML; `BeautifulSoup` parses out
   structured fields (quote text, author, tags) using CSS selectors.
2. **Store** — two storage backends were built to compare tradeoffs:
   - `scraper_csv.py` writes to `quotes.csv` (simple, human-readable, but
     overwritten on every run — no history).
   - `scraper_sqlite.py` writes to `quotes.db` using SQLite (queryable,
     supports relations via a `categories` table and `JOIN`, and can be
     extended to append timestamped history instead of overwriting).
3. **Query** — practiced core SQL directly against `quotes.db`: `SELECT`,
   `WHERE`, `GROUP BY`, `ORDER BY`, and a `JOIN` against a second
   `categories` table to tag and count quotes by category.
4. **Schedule** — a `cron` job runs `scraper_sqlite.py` daily at 9:00 AM
   using the project's virtual environment, so the database stays current
   without any manual step.

**Stack:** Python 3, `requests`, `beautifulsoup4`, `sqlite3`, `cron`, `git`.

## Next improvements

- Switch from overwriting rows to timestamped inserts, enabling real
  price-over-time queries instead of only a snapshot.
- Move hardcoded values (target URL, output paths, schedule) into a
  `config.json` so the same script works for any client/site without
  editing code.
- Add error handling and retry logic for failed requests (network errors,
  site structure changes, rate limiting).
- Add basic alerting (e.g. email or message) when a tracked value changes
  beyond a threshold, instead of requiring a manual query to notice.
- Build a simple HTML or PDF report summarizing recent changes, generated
  automatically after each scheduled run.
- Point the pipeline at a real target site (e.g. a competitor's product
  page) as the actual Price/Stock Monitor offer.

## Setup

```bash
git clone https://github.com/abderrahmanechafik78-sudo/elite-engineer-log.git
cd elite-engineer-log
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 scraper_sqlite.py
```
