"""
This script automatically downloads Guardian articles by YEAR (1980-2025) 
and saves them as .txt files for tracking mental health language changes over time.
"""

import requests
import os
from tqdm import tqdm
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.environ.get("GUARDIAN_API_KEY")

# Broad mental health search terms to capture relevant articles
# We'll be analysing medicalised vs. human language within these articles
SEARCH_TERMS = [
    "mental health",
    "depression",
    "anxiety",
    "mental illness",
]

START_YEAR = 1980
END_YEAR = 2025
PAGE_SIZE = 10  # Articles per page
PAGES_PER_YEAR = 5  # Limit pages per year (5 pages × 10 = 50 articles/year)
SAVE_DIR = "data_by_year"

# Create main data directory
os.makedirs(SAVE_DIR, exist_ok=True)

# LOOP THROUGH SEARCH TERMS
for search_term in SEARCH_TERMS:
    print(f"\n{'='*60}")
    print(f"🔍 SEARCHING FOR: '{search_term}'")
    print(f"{'='*60}")
    
    # LOOP THROUGH YEARS 
    for year in range(START_YEAR, END_YEAR + 1):
        # Organize by term, then year
        term_slug = search_term.replace(" ", "_").    #Makes folder names cleaner
        year_dir = os.path.join(SAVE_DIR, term_slug, str(year))
        os.makedirs(year_dir, exist_ok=True)
        
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        
        print(f"\n📰 Fetching '{search_term}' articles for {year}...")
        
        article_count = 0
        
        for page in tqdm(range(1, PAGES_PER_YEAR + 1), desc=f"{year}"):
            url = (
                "https://content.guardianapis.com/search"
                f"?q={search_term}"
                f"&from-date={start_date}"
                f"&to-date={end_date}"
                f"&page-size={PAGE_SIZE}"
                f"&page={page}"
                f"&api-key={API_KEY}"
                f"&show-fields=bodyText,webPublicationDate"
            )
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                if "response" not in data or not data["response"]["results"]:
                    break
                
                for article in data["response"]["results"]:
                    title = article["webTitle"].replace("/", "-").replace("\\", "-")[:50]
                    body = article["fields"].get("bodyText", "")
                    pub_date = article["fields"].get("webPublicationDate", "")
                    
                    # Skip empty articles
                    if not body.strip():
                        continue
                    
                    # Create filename with date prefix for chronological sorting
                    date_prefix = pub_date[:10] if pub_date else f"{year}-00-00"
                    filename = os.path.join(year_dir, f"{date_prefix}_{title}.txt")
                    
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"Search Term: {search_term}\n")
                        f.write(f"Title: {article['webTitle']}\n")
                        f.write(f"Date: {pub_date}\n")
                        f.write(f"URL: {article.get('webUrl', '')}\n\n")
                        f.write(body)
                    
                    article_count += 1
                
                # Small delay between requests
                time.sleep(0.2)
                
            except Exception as e:
                print(f"\n⚠️  Error on year {year}, page {page}: {e}")
                continue
        
        print(f"   → Saved {article_count} articles for {year}")

print("\n✅ Done! All articles saved in year-based folders.")
print(f"📁 Check the '{SAVE_DIR}' directory")
