#!/usr/bin/env python3
"""
build.py — Static Site Generator for willfreee homepage.

Reads books.json, compiles index.html & sitemap.xml, and packages 
a complete, ready-to-deploy static website into the 'out/' directory.

Zero external dependencies (uses standard library only).
"""

import sys
import subprocess
from datetime import date, datetime
import argparse
import json
import html
import shutil
from datetime import date
from pathlib import Path

# Paths & Settings
BASE_DIR = Path(__file__).resolve().parent
BOOKS_FILE = BASE_DIR / "books.json"
OUT_DIR = BASE_DIR / "out"

BASE_URL = "https://willfreee.github.io"

# Đường dẫn thư mục static nguồn
STATIC_DIR = BASE_DIR / "static"


def load_books():
    """Load master catalog from books.json."""
    if not BOOKS_FILE.exists():
        raise FileNotFoundError(f"Missing required data file: {BOOKS_FILE}")
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        books = json.load(f)
    if not isinstance(books, list):
        raise ValueError("books.json must contain a JSON array of guide objects.")
    return books


def generate_index_html(books):
    """Generate pre-rendered static index.html with new 'willfreee from:' structure."""
    cards_html = []
    for book in books:
        slug = html.escape(book["slug"].strip("/"))
        dependency = html.escape(book["dependency"])
        tagline = html.escape(book["tagline"])

        card = f'''        <a href="./{slug}/" class="book-card">
          <article>
            <div class="card-kicker">will<span>freee</span> from:</div>
            <h2 class="book-title">{dependency}</h2>
            <p class="book-tagline">{tagline}</p>
            <div class="card-action">
              <span>Read guide</span>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </div>
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
  <meta name="description" content="Open-source psychological guidebooks based on understanding to help people effortlessly dismantle behavioral and psychological dependencies.">

  <!-- Anti-FOUC Theme Script: prevents white flash on dark theme -->
  <script>
    (function() {{
      try {{
        var saved = localStorage.getItem('willfreee-theme');
        var theme = saved || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', theme);
      }} catch (e) {{}}
    }})();
  </script>

  <!-- OpenGraph / Social Meta Tags -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/">
  <meta property="og:title" content="willfreee — Open Guides for Lasting Freedom">
  <meta property="og:description" content="Open-source psychological guidebooks based on understanding to help people effortlessly dismantle behavioral and psychological dependencies.">
  <meta property="og:image" content="{BASE_URL}/assets/logo.png">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="willfreee — Open Guides for Lasting Freedom">
  <meta name="twitter:description" content="Open-source psychological guidebooks based on understanding to help people effortlessly dismantle behavioral and psychological dependencies.">
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
        <h1 class="hero-title">open guides — lasting freedom</h1>
        <p class="hero-description">
          willfreee produces open-source guidebooks to help people dissolve behavioral dependencies.
          All guides are completely free, open-source, and designed to eliminate desire through understanding — no willpower required.
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
        <a href="https://github.com/willfreee" target="_blank" rel="noopener noreferrer">GitHub</a>
      </p>
    </div>
  </footer>

</body>
</html>
'''


def generate_sitemap_xml(books):
    """Generate dynamic sitemap.xml with today's ISO date."""
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
        slug = html.escape(book["slug"].strip("/"))
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


def clean_and_prepare_out():
    """Remove old out/ directory and recreate a clean one."""
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def copy_static_assets():
    """Copy all static files and folders from static/ into out/."""
    # 1. Copy toàn bộ tệp và thư mục con trong static/ vào thẳng out/
    if STATIC_DIR.exists() and STATIC_DIR.is_dir():
        shutil.copytree(STATIC_DIR, OUT_DIR, dirs_exist_ok=True)

    # 2. (Dự phòng) Nếu thư mục assets/ vẫn còn nằm ở ngoài gốc thay vì trong static/
    assets_src = BASE_DIR / "assets"
    if assets_src.exists() and assets_src.is_dir():
        shutil.copytree(assets_src, OUT_DIR / "assets", dirs_exist_ok=True)

def run_git(args, cwd=None):
    """Chạy lệnh git và trả về stdout text."""
    res = subprocess.run(
        ["git"] + args,
        cwd=cwd or BASE_DIR,
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        raise RuntimeError(f"Git command failed: git {' '.join(args)}\n{res.stderr.strip()}")
    return res.stdout.strip()


def deploy_to_gh_pages(force=False):
    """Deploy nội dung thư mục out/ lên branch gh-pages của origin."""
    print("\n--- Bắt đầu quy trình Deploy GitHub Pages ---")

    # 1. Kiểm tra môi trường Git
    try:
        current_branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    except Exception:
        print("❌ Lỗi: Thư mục hiện tại không phải git repository.")
        sys.exit(1)

    if current_branch != "main":
        print(f"❌ Bạn đang ở branch '{current_branch}'. Vui lòng checkout về 'main' trước khi deploy.")
        sys.exit(1)

    # 2. Kiểm tra working tree sạch
    diff_status = subprocess.run(["git", "diff-index", "--quiet", "HEAD", "--"], cwd=BASE_DIR).returncode
    if diff_status != 0:
        print("❌ Working tree chưa sạch. Vui lòng commit hoặc stash toàn bộ thay đổi trước.")
        sys.exit(1)

    main_commit = run_git(["rev-parse", "HEAD"])
    marker_file = BASE_DIR / ".last_deploy_commit"

    # 3. Kiểm tra lần build trước (nếu không dùng --force)
    if not force and marker_file.exists():
        last_commit = marker_file.read_text(encoding="utf-8").strip()
        if last_commit == main_commit:
            print("ℹ️  Không có thay đổi mới trên main so với lần deploy trước. Bỏ qua.")
            print("💡 Dùng 'python3 build.py --deploy --force' nếu muốn ép buộc deploy lại.")
            return

    # 4. Lấy URL của remote origin
    try:
        remote_url = run_git(["remote", "get-url", "origin"])
    except Exception:
        print("❌ Không tìm thấy remote 'origin'.")
        sys.exit(1)

    # 5. Push trực tiếp từ out/ lên branch gh-pages (Không cần switch branch repo chính)
    print("🚀 Đang khởi tạo bản build để deploy...")
    run_git(["init"], cwd=OUT_DIR)
    run_git(["checkout", "-B", "gh-pages"], cwd=OUT_DIR)
    run_git(["add", "-A"], cwd=OUT_DIR)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Deploy from main @ {main_commit[:7]} ({now_str})"
    run_git(["commit", "-m", commit_msg], cwd=OUT_DIR)

    print(f"🚀 Đang force push lên {remote_url} (gh-pages)...")
    run_git(["push", "--force", remote_url, "gh-pages"], cwd=OUT_DIR)

    # 6. Ghi nhận commit vừa deploy
    marker_file.write_text(main_commit, encoding="utf-8")
    print("✨ Deploy hoàn tất")

def main():
    parser = argparse.ArgumentParser(description="willfreee Static Site Generator & Deployer")
    parser.add_argument("--deploy", action="store_true", help="Tự động build và push out/ lên gh-pages")
    parser.add_argument("--force", action="store_true", help="Bắt buộc deploy kể cả khi main chưa có commit mới")
    args = parser.parse_args()

    # --- TIẾN TRÌNH BUILD ---
    print("[1/4] Loading books.json...")
    books = load_books()
    print(f"      Found {len(books)} guides.")

    print("[2/4] Preparing output directory ('out/')...")
    clean_and_prepare_out()
    copy_static_assets()
    print("      Static assets copied successfully.")

    print("[3/4] Compiling index.html...")
    index_html = generate_index_html(books)
    with open(OUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    print("[4/4] Compiling sitemap.xml...")
    sitemap_xml = generate_sitemap_xml(books)
    with open(OUT_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    print("\n✓ Build succeeded! Static site is ready in 'out/'.")

    # --- TIẾN TRÌNH DEPLOY (Nếu có cờ --deploy) ---
    if args.deploy:
        deploy_to_gh_pages(force=args.force)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()