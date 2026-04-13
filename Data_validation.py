"""
Data validation script to assess corpus quality across years.
Checks article counts, token counts, and identifies years with insufficient data.
"""

import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import spacy

nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    """Tokenize and lemmatize text."""
    doc = nlp(text.lower())
    return [t.lemma_ for t in doc if t.is_alpha and not t.is_stop]

def analyze_year(year):
    #Get stats for a year across all search terms. 
    pattern = f"data_by_year/*/{year}/*.txt"
    files = glob.glob(pattern)
    
    article_count = len(files)
    total_tokens = 0
    
    for fname in files:
        with open(fname, encoding="utf-8") as f:
            tokens = preprocess(f.read())
            total_tokens += len(tokens)
    
    return {
        'year': year,
        'article_count': article_count,
        'total_tokens': total_tokens,
        'avg_tokens_per_article': total_tokens / article_count if article_count > 0 else 0
    }

# ===== ANALYSE ALL YEARS =====

print("Analyzing corpus quality by year...\n")

years = list(range(1980, 2026))
data = []

for year in years:
    stats = analyze_year(year)
    data.append(stats)
    
    if stats['article_count'] > 0:
        print(f"{year}: {stats['article_count']:>4} articles | {stats['total_tokens']:>8,} tokens | {stats['avg_tokens_per_article']:>6.0f} avg tokens/article")
    else:
        print(f"{year}: No data")

# ===== CREATE DATAFRAME =====

df = pd.DataFrame(data)
df.to_csv("corpus_quality_by_year.csv", index=False)
print("\n✅ Data saved to 'corpus_quality_by_year.csv'")

# ===== IDENTIFY PROBLEMATIC YEARS =====

print("\n" + "="*60)
print("DATA QUALITY ASSESSMENT")
print("="*60)

# Flag years with insufficient data
MIN_ARTICLES = 20  # Threshold for reliable analysis
MIN_TOKENS = 5000   # Threshold for reliable frequency counts

insufficient = df[(df['article_count'] < MIN_ARTICLES) | (df['total_tokens'] < MIN_TOKENS)]

if len(insufficient) > 0:
    print(f"\n⚠️  Years with insufficient data (< {MIN_ARTICLES} articles or < {MIN_TOKENS:,} tokens):")
    for _, row in insufficient.iterrows():
        print(f"   {int(row['year'])}: {int(row['article_count'])} articles, {int(row['total_tokens']):,} tokens")
    
    print(f"\n Consider excluding these years from analysis or starting from {insufficient['year'].max() + 1}")
else:
    print("All years have sufficient data for analysis.")

# ===== VISUALISATIONS =====

fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Articles per year
axes[0].bar(df['year'], df['article_count'], color='steelblue', alpha=0.7)
axes[0].axhline(y=MIN_ARTICLES, color='red', linestyle='--', linewidth=2, label=f'Min threshold ({MIN_ARTICLES})')
axes[0].set_xlabel('Year', fontsize=12)
axes[0].set_ylabel('Number of Articles', fontsize=12)
axes[0].set_title('Article Count by Year', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Tokens per year
axes[1].bar(df['year'], df['total_tokens'], color='darkorange', alpha=0.7)
axes[1].axhline(y=MIN_TOKENS, color='red', linestyle='--', linewidth=2, label=f'Min threshold ({MIN_TOKENS:,})')
axes[1].set_xlabel('Year', fontsize=12)
axes[1].set_ylabel('Total Tokens', fontsize=12)
axes[1].set_title('Token Count by Year', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("corpus_quality_validation.png", dpi=300)
print("\n✅ Visualization saved as 'corpus_quality_validation.png'")
plt.show()

# ===== SUMMARY STATS =====

print("\n" + "="*60)
print("CORPUS SUMMARY")
print("="*60)
print(f"Total years: {len(df)}")
print(f"Total articles: {df['article_count'].sum():,}")
print(f"Total tokens: {df['total_tokens'].sum():,}")
print(f"Average articles per year: {df['article_count'].mean():.1f}")
print(f"Average tokens per year: {df['total_tokens'].mean():,.0f}")
print(f"Years with data: {(df['article_count'] > 0).sum()}")
print(f"Years with sufficient data: {((df['article_count'] >= MIN_ARTICLES) & (df['total_tokens'] >= MIN_TOKENS)).sum()}")