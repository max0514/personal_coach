#!/usr/bin/env python3
"""
Article URL Scraper for Knowledge Coach System

Collects article URLs from a website's sitemap and saves them to a CSV file,
ready for import into Google NotebookLM.

Usage:
    python scrape_urls.py <sitemap_url> [--output OUTPUT_CSV] [--filter KEYWORD]

Examples:
    python scrape_urls.py https://example.com/sitemap.xml
    python scrape_urls.py https://example.com/sitemap.xml --output dan_koe_articles.csv
    python scrape_urls.py https://example.com/sitemap.xml --filter /blog/
"""

import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests


def fetch_sitemap(url: str) -> str:
    """Fetch sitemap XML content from URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; KnowledgeCoach/1.0)"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def parse_sitemap(xml_content: str) -> list[dict]:
    """Parse sitemap XML and extract URLs with metadata."""
    # Handle namespace
    root = ET.fromstring(xml_content)
    namespace = ""
    if root.tag.startswith("{"):
        namespace = root.tag.split("}")[0] + "}"

    urls = []

    # Check if this is a sitemap index (contains other sitemaps)
    sitemap_tags = root.findall(f"{namespace}sitemap")
    if sitemap_tags:
        print(f"Found sitemap index with {len(sitemap_tags)} sub-sitemaps")
        for sitemap in sitemap_tags:
            loc = sitemap.find(f"{namespace}loc")
            if loc is not None and loc.text:
                print(f"  Fetching sub-sitemap: {loc.text}")
                try:
                    sub_content = fetch_sitemap(loc.text)
                    urls.extend(parse_sitemap(sub_content))
                except Exception as e:
                    print(f"  Warning: Failed to fetch {loc.text}: {e}")
        return urls

    # Parse regular sitemap
    for url_element in root.findall(f"{namespace}url"):
        loc = url_element.find(f"{namespace}loc")
        lastmod = url_element.find(f"{namespace}lastmod")

        if loc is not None and loc.text:
            entry = {
                "url": loc.text.strip(),
                "lastmod": lastmod.text.strip() if lastmod is not None and lastmod.text else "",
            }
            urls.append(entry)

    return urls


def filter_urls(urls: list[dict], keyword: str | None = None) -> list[dict]:
    """Filter URLs by keyword in the path."""
    if not keyword:
        return urls
    return [u for u in urls if keyword.lower() in u["url"].lower()]


def save_to_csv(urls: list[dict], output_path: str) -> None:
    """Save URLs to CSV file."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "lastmod"])
        writer.writeheader()
        writer.writerows(urls)


def split_for_notebooklm(urls: list[dict], max_per_notebook: int = 50) -> list[list[dict]]:
    """Split URLs into chunks for NotebookLM (free: 50 sources per notebook)."""
    return [urls[i : i + max_per_notebook] for i in range(0, len(urls), max_per_notebook)]


def main():
    parser = argparse.ArgumentParser(
        description="Scrape article URLs from sitemaps for Knowledge Coach"
    )
    parser.add_argument("sitemap_url", help="URL of the sitemap.xml")
    parser.add_argument(
        "--output", "-o", default=None, help="Output CSV file path (default: auto-generated)"
    )
    parser.add_argument(
        "--filter", "-f", default=None, help="Filter URLs containing this keyword (e.g., /blog/)"
    )
    parser.add_argument(
        "--split",
        "-s",
        type=int,
        default=50,
        help="Split into multiple CSVs with this many URLs each (default: 50 for NotebookLM free tier)",
    )

    args = parser.parse_args()

    # Generate default output name from domain
    if args.output is None:
        domain = urlparse(args.sitemap_url).netloc.replace(".", "_")
        args.output = f"{domain}_articles.csv"

    print(f"Fetching sitemap: {args.sitemap_url}")
    xml_content = fetch_sitemap(args.sitemap_url)

    print("Parsing URLs...")
    urls = parse_sitemap(xml_content)
    print(f"Found {len(urls)} URLs total")

    if args.filter:
        urls = filter_urls(urls, args.filter)
        print(f"After filtering for '{args.filter}': {len(urls)} URLs")

    if not urls:
        print("No URLs found. Check the sitemap URL and filter.")
        sys.exit(1)

    # Split and save
    chunks = split_for_notebooklm(urls, args.split)

    if len(chunks) == 1:
        save_to_csv(urls, args.output)
        print(f"\nSaved {len(urls)} URLs to {args.output}")
    else:
        output_path = Path(args.output)
        for i, chunk in enumerate(chunks, 1):
            chunk_path = output_path.with_stem(f"{output_path.stem}_part{i}")
            save_to_csv(chunk, str(chunk_path))
            print(f"Saved {len(chunk)} URLs to {chunk_path}")

        print(f"\nSplit into {len(chunks)} files (for {len(chunks)} NotebookLM notebooks)")

    print(f"\nTotal articles collected: {len(urls)}")
    print("\nNext steps:")
    print("  1. Open Google NotebookLM (notebooklm.google.com)")
    print("  2. Create a new notebook")
    print("  3. Add sources -> Website URLs")
    print("  4. Paste URLs from the CSV (up to 50 per notebook)")
    print("  5. If multiple CSVs, create one notebook per file")


if __name__ == "__main__":
    main()
