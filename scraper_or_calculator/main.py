import argparse
import csv
import json
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"

def scrape_quotes(max_pages: int = 10, delay: float = 1.0) -> list[dict]:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (KwameScraper/1.0)"})

    quotes = []
    url = f"{BASE_URL}/page/1/"
    page = 1

    while url and page <= max_pages:
        r = session.get(url, timeout=15)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        blocks = soup.select(".quote")

        for b in blocks:
            text = b.select_one(".text").get_text(strip=True)
            author = b.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in b.select(".tags .tag")]
            quotes.append({"text": text, "author": author, "tags": tags})

        next_link = soup.select_one("li.next a")
        url = f"{BASE_URL}{next_link['href']}" if next_link else None

        print(f"✅ Scraped page {page} | total quotes: {len(quotes)}")
        page += 1
        time.sleep(delay)

    return quotes

def save_csv(quotes: list[dict], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        for q in quotes:
            writer.writerow({"text": q["text"], "author": q["author"], "tags": "|".join(q["tags"])})

def save_json(quotes: list[dict], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(quotes, indent=2, ensure_ascii=False), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Scrape quotes and export CSV/JSON.")
    parser.add_argument("--pages", type=int, default=5, help="Max pages to scrape (default: 5)")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between pages (default: 1.0)")
    parser.add_argument("--outdir", type=str, default="scraper_or_calculator/output", help="Output directory")
    args = parser.parse_args()

    quotes = scrape_quotes(max_pages=args.pages, delay=args.delay)

    outdir = Path(args.outdir).expanduser().resolve()
    save_csv(quotes, outdir / "quotes.csv")
    save_json(quotes, outdir / "quotes.json")

    print("\n--- Done ---")
    print(f"Saved: {outdir / 'quotes.csv'}")
    print(f"Saved: {outdir / 'quotes.json'}")
    print(f"Total quotes: {len(quotes)}")

if __name__ == "__main__":
    main()
