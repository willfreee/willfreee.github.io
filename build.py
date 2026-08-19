#!/usr/bin/env python3
"""
build.py
Pre-renders index.html and sitemap.xml for willfreee from books.json.
Uses standard library only (zero external dependencies).
"""

import json
import html
from datetime import date
from pathlib import Path

# Paths & Settings
BASE_DIR = Path(__file__).parent
BOOKS_FILE = BASE_DIR / "books.json"
INDEX_FILE = BASE_DIR / "index.html"
SITEMAP_FILE = BASE_DIR / "sitemap.xml"

BASE_URL = "https://willfreee.github.io"


def load_books():
    """Load master book catalog from books.json."""
    if not BOOKS_FILE.exists():
        raise FileNotFoundError(f"Missing required data file: {BOOKS_FILE}")
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_index_html(books):
    """Generate pre-rendered static index.html with pure semantic HTML."""
    cards_html = []
    for book in books:
        slug = html.escape(book["slug"])
        title = html.escape(book["title"])
        tagline = html.escape(book["tagline"])

        card = f'''        <a href="./{slug}/" class="book-card">
          <article>
            <h2 class="book-title">{title}</h2>
            <p class="book-tagline">{tagline}</p>
          </article>
        </a>'''
        cards_html.append(card)

    rendered_cards = "\n".join(cards_html)

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>willfreee — Open Guides for Lasting Freedom</title>
  <meta name="description" content="Open-source psychological guidebooks based on Allen Carr's Easyway methodology to help people break free from behavioral dependencies.">

  <!-- OpenGraph / Social Meta Tags -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/">
  <meta property="og:title" content="willfreee — Open Guides for Lasting Freedom">
  <meta property="og:description" content="Open-source psychological guidebooks based on Allen Carr's Easyway methodology to help people break free from behavioral dependencies.">
  <meta property="og:image" content="{BASE_URL}/assets/logo.png">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="willfreee — Open Guides for Lasting Freedom">
  <meta name="twitter:description" content="Open-source psychological guidebooks based on Allen Carr's Easyway methodology to help people break free from behavioral dependencies.">
  <meta name="twitter:image" content="{BASE_URL}/assets/logo.png">

  <link rel="icon" href="./favicon.ico" type="image/x-icon">
  <link rel="manifest" href="./site.webmanifest">
  <link rel="stylesheet" href="./style.css">
  <script src="./script.js" defer></script>
</head>
<body>

  <header class="site-header">
    <div class="container header-container">
      <div class="brand">
        <img src="./assets/logo.png" alt="willfreee logo" class="brand-logo" width="40" height="40">
        <a href="./" class="brand-name">will<span>freee</span></a>
      </div>
      <div class="header-actions">
        <a href="https://github.com/willfreee" target="_blank" rel="noopener noreferrer" class="btn-github">
          GitHub
        </a>
        <button id="theme-toggle" class="theme-toggle-btn" aria-label="Toggle theme">
          <span class="theme-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></span>
        </button>
      </div>
    </div>
  </header>

  <main class="site-main">
    <section class="hero-section">
      <div class="container">
        <h1 class="hero-title">open guides - lasting freedom</h1>
        <p class="hero-description">
          willfreee produces open-source guidebooks based on Allen Carr's Easyway methodology to help people dismantle behavioral dependencies.
          All guides are completely free, open-source, and designed to eliminate desire through understanding—no willpower required.
        </p>
      </div>
    </section>

    <section class="catalog-section">
      <div class="container">
        <div class="book-grid">
{rendered_cards}
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-container">
      <p>
        Licensed under 
        <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener noreferrer">CC BY-SA 4.0</a>. 
        Open for all, forever.
      </p>
      <p class="footer-links">
        <a href="https://github.com/willfreee" target="_blank" rel="noopener noreferrer">GitHub</a></p>
    </div>
  </footer>

</body>
</html>
'''


def generate_sitemap_xml(books):
    """Generate dynamic sitemap.xml with updated timestamp for search engines."""
    today = date.today().isoformat()

    url_entries = [
        f'''  <url>
    <loc>{BASE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>'''
    ]

    for book in books:
        slug = html.escape(book["slug"])
        url_entries.append(
            f'''  <url>
    <loc>{BASE_URL}/{slug}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>'''
        )

    urls_rendered = "\n".join(url_entries)

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls_rendered}
</urlset>
'''


def main():
    print("Reading books.json...")
    books = load_books()

    print(f"Building pre-rendered index.html ({len(books)} books)...")
    index_html = generate_index_html(books)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(index_html)

    print("Building sitemap.xml...")
    sitemap_xml = generate_sitemap_xml(books)
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    print("Build complete! Static index.html & sitemap.xml updated successfully.")


if __name__ == "__main__":
    main()
