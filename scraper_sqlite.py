"""
scraper_sqlite.py
Scrapes quotes from https://quotes.toscrape.com and saves them to a SQLite database.
"""

import json
import sqlite3
import requests
from bs4 import BeautifulSoup

with open("config.json") as f:
    config = json.load(f)

URL = config["target_url"]
DB_FILE = config["output_db"]
HEADERS = {"User-Agent": config["user_agent"]}


def fetch_page(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_quotes(soup):
    quotes = []
    for block in soup.select(".quote"):
        text = block.select_one(".text").get_text(strip=True)
        author = block.select_one(".author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in block.select(".tag")]
        quotes.append((text, author, ", ".join(tags)))
    return quotes


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT NOT NULL,
            tags TEXT
        )
    """)
    conn.commit()


def save_to_db(quotes, conn):
    conn.executemany(
        "INSERT INTO quotes (quote, author, tags) VALUES (?, ?, ?)",
        quotes
    )
    conn.commit()


def main():
    soup = fetch_page(URL)
    quotes = parse_quotes(soup)

    conn = sqlite3.connect(DB_FILE)
    init_db(conn)
    save_to_db(quotes, conn)
    conn.close()

    print(f"Saved {len(quotes)} quotes to {DB_FILE}")


if __name__ == "__main__":
    main()