"""
Analysis script to track medicalized vs. human/emotional language 
in mental health discourse over time (1980-2025).
UPDATED to 1998-2025 to focus on more recent trends and ensure data quality.
"""

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import glob
import spacy

nlp = spacy.load("en_core_web_sm")

# Removing case sensitivity, lemmatising and removing stop words.
def preprocess(text):
    doc = nlp(text.lower())
    return [t.lemma_ for t in doc if t.is_alpha and not t.is_stop]

def load_and_process(path_pattern):
    """Load all articles matching pattern and return token counts."""
    tokens = []
    for fname in glob.glob(path_pattern):
        with open(fname, encoding="utf-8") as f:
            tokens += preprocess(f.read())
    return Counter(tokens)

# ===== LEXICONS =====

# Medicalized/clinical language
medical_terms = [
    "disorder",
    "diagnosis", 
    "diagnose",
    "symptom",
    "treatment",
    "therapy",
    "medication",
    "clinical",
    "patient",
    "psychiatric",
    "pathology",
    "prescription",
    "syndrome",
    "dysfunction",
    "psychotherapy",
    "antidepressant",
    "pharmaceutical",
    "clinician",
]

# Human/emotional language
human_terms = [
    "sadness",
    "grief",
    "stress",
    "loneliness",
    "coping",
    "support",
    "friend",
    "community",
    "love",
    "feeling",
    "struggle",
    "hope",
    "pain",
    "healing",
    "connection",
    "suffering",
    "hurt",
    "comfort",
    "care",
    "empathy",
]

# ===== ANALYSIS BY YEAR =====

# Define year range
years = list(range(1998, 2026))
med_freqs, hum_freqs = [], []

print("Processing articles by year...")
for year in years:
    # Combine all search term folders for this year
    # e.g., "data_by_year/*/1980/*.txt"
    counts = load_and_process(f"data_by_year/*/{year}/*.txt")
    
    total = sum(counts.values())
    
    if total == 0:
        print(f" No data for {year}")
        med_freqs.append(0)
        hum_freqs.append(0)
        continue
    
    med_count = sum(counts[w] for w in medical_terms)
    hum_count = sum(counts[w] for w in human_terms)
    
    med_freqs.append(med_count / total)
    hum_freqs.append(hum_count / total)
    
    print(f"  {year}: {total:,} tokens | Med: {med_count} | Human: {hum_count}")

# ===== CREATE VISUALIZATION =====

plt.figure(figsize=(12, 6))
plt.plot(years, med_freqs, label="Medicalized Language", linewidth=2, marker='o', markersize=3)
plt.plot(years, hum_freqs, label="Human/Emotional Language", linewidth=2, marker='o', markersize=3)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Relative Frequency", fontsize=12)
plt.title("Medicalized vs. Human Language in Mental Health Media (1998-2025)", fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("mental_health_language_trends.png", dpi=300)
print("\n✅ Plot saved as 'mental_health_language_trends_1998-2025.png'")
plt.show()

# ===== SAVE DATA TO CSV =====

df = pd.DataFrame({
    'year': years,
    'medicalized_freq': med_freqs,
    'human_freq': hum_freqs
})
df.to_csv("language_frequencies_by_year.csv", index=False)
print("✅ Data saved as 'language_frequencies_by_year.csv'")
