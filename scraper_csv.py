"""
scraper_csv.py
Scrapes quotes from https://quotes.toscrape.com and saves them to a CSV file.
"""

import csv
import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com"
OUTPUT_FILE = "quotes.csv"
HEADERS = {"User-Agent": "Mozilla/5.0 (educational scraping practice)"}


def fetch_page(url):
    """Download a page and return a BeautifulSoup object."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_quotes(soup):
    """Extract (text, author, tags) tuples from a parsed page."""
    quotes = []
    for block in soup.select(".quote"):
        text = block.select_one(".text").get_text(strip=True)
        author = block.select_one(".author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in block.select(".tag")]
        quotes.append((text, author, ", ".join(tags)))
    return quotes


def save_to_csv(quotes, filename):
    """Write a list of (text, author, tags) tuples to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["quote", "author", "tags"])
        writer.writerows(quotes)


def main():
    soup = fetch_page(URL)
    quotes = parse_quotes(soup)
    save_to_csv(quotes, OUTPUT_FILE)
    print(f"Saved {len(quotes)} quotes to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()