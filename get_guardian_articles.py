"""
Automatically download Guardian articles by decade and save as .txt files.
"""

import requests
import os
from tqdm import tqdm

API_KEY = "4e025d22-f2a2-4cb7-9259-21a7ec615632"
SEARCH_TERM = "depression"
DECADES = {
    "1990s": ("1990-01-01", "1999-12-31"),
    "2000s": ("2000-01-01", "2009-12-31"),
    "2010s": ("2010-01-01", "2019-12-31"),
    "2020s": ("2020-01-01", "2025-12-31"),
}
PAGE_SIZE = 50  # Max page size for Guardian API
SAVE_DIR = "data"
PAGES_PER_DECADE = 10 # Limit pages to avoid excessive requests

# ---- 2. LOOP THROUGH DECADES ----
for decade, (start, end) in DECADES.items():
    decade_dir = os.path.join(SAVE_DIR, decade)
    os.makedirs(decade_dir, exist_ok=True)

    print(f"\n📚 Fetching articles for {decade}...")

    for page in tqdm(range(1, PAGES_PER_DECADE + 1)):
        url = (
            "https://content.guardianapis.com/search"
            f"?q={SEARCH_TERM}"
            f"&from-date={start}"
            f"&to-date={end}"
            f"&page-size=10"
            f"&page={page}"
            f"&api-key={API_KEY}"
            f"&show-fields=bodyText"
        )

        response = requests.get(url)
        data = response.json()

        if "response" not in data or not data["response"]["results"]:
            break

        for article in data["response"]["results"]:
            title = article["webTitle"].replace("/", "-")[:50]  # truncate to safe length
            body = article["fields"].get("bodyText", "")

            # Skip empty articles
            if not body.strip():
                continue

            filename = os.path.join(decade_dir, f"{title}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(body)

print("\n✅ Done! All articles saved in decade folders.")