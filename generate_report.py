"""
generate_report.py
Queries quotes.db and generates a 1-page HTML report summarizing the data.
"""

import sqlite3
from datetime import datetime

DB_FILE = "quotes.db"
OUTPUT_FILE = "report.html"


def get_summary(conn):
    """Run a few summary queries and return their results."""
    total = conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]

    by_author = conn.execute("""
        SELECT author, COUNT(*) AS total
        FROM quotes
        GROUP BY author
        ORDER BY total DESC
    """).fetchall()

    by_category = conn.execute("""
        SELECT categories.name, COUNT(*) AS total
        FROM quotes
        JOIN categories ON quotes.category_id = categories.id
        GROUP BY categories.name
        ORDER BY total DESC
    """).fetchall()

    longest = conn.execute("""
        SELECT quote, author, LENGTH(quote) AS len
        FROM quotes
        ORDER BY len DESC
        LIMIT 3
    """).fetchall()

    return total, by_author, by_category, longest


def build_html(total, by_author, by_category, longest):
    """Turn query results into a simple HTML report."""
    author_rows = "".join(
        f"<tr><td>{author}</td><td>{count}</td></tr>"
        for author, count in by_author
    )
    category_rows = "".join(
        f"<tr><td>{name}</td><td>{count}</td></tr>"
        for name, count in by_category
    )
    longest_items = "".join(
        f"<li>&ldquo;{quote}&rdquo; &mdash; {author} ({length} chars)</li>"
        for quote, author, length in longest
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Data Monitor Report</title>
<style>
  body {{ font-family: -apple-system, Arial, sans-serif; max-width: 700px;
          margin: 40px auto; color: #1a1a1a; line-height: 1.5; }}
  h1 {{ font-size: 22px; margin-bottom: 4px; }}
  .meta {{ color: #666; font-size: 13px; margin-bottom: 32px; }}
  h2 {{ font-size: 16px; margin-top: 32px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
  th, td {{ text-align: left; padding: 6px 10px; border-bottom: 1px solid #eee; font-size: 14px; }}
  th {{ color: #666; font-weight: 500; }}
  .stat {{ font-size: 28px; font-weight: 600; }}
  ul {{ padding-left: 20px; font-size: 14px; }}
  li {{ margin-bottom: 8px; }}
</style>
</head>
<body>
  <h1>Data Monitor Report</h1>
  <div class="meta">Generated {timestamp}</div>

  <div class="stat">{total}</div>
  <div>total records tracked</div>

  <h2>Records by author</h2>
  <table>
    <tr><th>Author</th><th>Count</th></tr>
    {author_rows}
  </table>

  <h2>Records by category</h2>
  <table>
    <tr><th>Category</th><th>Count</th></tr>
    {category_rows}
  </table>

  <h2>Longest entries</h2>
  <ul>
    {longest_items}
  </ul>
</body>
</html>
"""


def main():
    conn = sqlite3.connect(DB_FILE)
    total, by_author, by_category, longest = get_summary(conn)
    conn.close()

    html = build_html(total, by_author, by_category, longest)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()